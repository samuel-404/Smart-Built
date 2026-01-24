"""
NSGA-II Genetic Algorithm Implementation for PC Build Optimization
SmartBuild: Intelligent PC Configuration Consultant
"""

import random
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class Individual:
    """Represents a single PC build configuration"""
    genes: Dict[str, Dict[str, Any]]
    objectives: List[float] = field(default_factory=list)
    rank: int = 0
    crowding_distance: float = 0.0
    domination_count: int = 0
    dominated_solutions: List = field(default_factory=list)
    
    def __hash__(self):
        return hash(tuple(self.genes[k]['id'] for k in sorted(self.genes.keys()) if k in self.genes))
    
    def get_total_cost(self) -> int:
        return sum(comp.get('price', 0) for comp in self.genes.values())
    
    def get_total_performance(self, weights: Dict[str, float]) -> float:
        total = 0
        for comp_type, component in self.genes.items():
            weight = weights.get(comp_type, 0.1)
            score = component.get('performance_score', 50)
            total += weight * score
        return total


class NSGA2Optimizer:
    """
    Non-dominated Sorting Genetic Algorithm II (NSGA-II) Implementation
    Optimizes for: (1) Maximum Performance, (2) Minimum Cost Divergence
    """
    
    def __init__(
        self,
        compatible_components: Dict[str, List[Dict]],
        target_budget: int,
        usage_type: str,
        usage_profiles: Dict[str, Any],
        population_size: int = 50,
        generations: int = 100,
        crossover_rate: float = 0.9,
        mutation_rate: float = 0.1
    ):
        self.components = compatible_components
        self.target_budget = target_budget
        self.usage_type = usage_type
        self.usage_profiles = usage_profiles
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        
        self.weights = self._get_usage_weights()
        self.generation_stats = []
    
    def _get_usage_weights(self) -> Dict[str, float]:
        """Get component importance weights based on usage type"""
        profile = self.usage_profiles.get(self.usage_type, {})
        return profile.get('weights', {
            'gpu': 0.30,
            'cpu': 0.25,
            'ram': 0.15,
            'storage': 0.10,
            'motherboard': 0.10,
            'psu': 0.05,
            'case': 0.05
        })
    
    def initialize_population(self) -> List[Individual]:
        """Create initial population of random valid builds"""
        population = []
        attempts = 0
        max_attempts = self.population_size * 10
        
        while len(population) < self.population_size and attempts < max_attempts:
            attempts += 1
            individual = self._create_random_individual()
            
            if individual and self._is_valid_build(individual):
                population.append(individual)
        
        while len(population) < self.population_size:
            individual = self._create_random_individual(relaxed=True)
            if individual:
                population.append(individual)
        
        return population
    
    def _create_random_individual(self, relaxed: bool = False) -> Optional[Individual]:
        """Create a random build configuration"""
        genes = {}
        
        for comp_type in ['cpu', 'motherboard', 'gpu', 'ram', 'psu', 'case', 'storage']:
            if comp_type in self.components and self.components[comp_type]:
                candidates = self.components[comp_type]
                
                if not relaxed:
                    budget_fraction = self._get_budget_fraction(comp_type)
                    max_price = self.target_budget * budget_fraction * 1.5
                    filtered = [c for c in candidates if c['price'] <= max_price]
                    candidates = filtered if filtered else candidates
                
                genes[comp_type] = random.choice(candidates)
        
        return Individual(genes=genes) if genes else None
    
    def _get_budget_fraction(self, comp_type: str) -> float:
        """Get the fraction of budget typically allocated to a component type"""
        fractions = {
            'cpu': 0.20,
            'gpu': 0.35,
            'motherboard': 0.12,
            'ram': 0.10,
            'psu': 0.08,
            'case': 0.08,
            'storage': 0.07
        }
        return fractions.get(comp_type, 0.10)
    
    def _is_valid_build(self, individual: Individual) -> bool:
        """Check if a build is valid (compatible components)"""
        genes = individual.genes
        
        if 'cpu' in genes and 'motherboard' in genes:
            if genes['cpu']['socket'] != genes['motherboard']['socket']:
                return False
        
        if 'ram' in genes and 'motherboard' in genes:
            if genes['ram']['type'] not in genes['motherboard']['supported_ram']:
                return False
        
        if 'ram' in genes and 'cpu' in genes:
            if genes['ram']['type'] not in genes['cpu']['supported_ram']:
                return False
        
        if 'gpu' in genes and 'case' in genes:
            if genes['gpu']['length_mm'] > genes['case']['gpu_clearance_mm']:
                return False
        
        if 'motherboard' in genes and 'case' in genes:
            if genes['motherboard']['form_factor'] not in genes['case']['form_factor']:
                return False
        
        if 'cpu' in genes and 'gpu' in genes and 'psu' in genes:
            total_tdp = genes['cpu']['tdp'] + genes['gpu']['tdp'] + 100
            required = total_tdp * 1.2
            if genes['psu']['wattage'] < required:
                return False
        
        return True
    
    def evaluate_objectives(self, individual: Individual) -> List[float]:
        """
        Calculate objective values for an individual
        Objective 1: Maximize Performance Score (weighted by usage)
        Objective 2: Minimize Cost Divergence from Target Budget
        """
        performance = individual.get_total_performance(self.weights)
        
        total_cost = individual.get_total_cost()
        cost_divergence = abs(total_cost - self.target_budget) / self.target_budget
        
        if total_cost > self.target_budget * 1.1:
            over_budget_penalty = (total_cost - self.target_budget) / self.target_budget
            cost_divergence += over_budget_penalty * 2
        
        individual.objectives = [performance, -cost_divergence]
        return individual.objectives
    
    def dominates(self, p: Individual, q: Individual) -> bool:
        """Check if individual p dominates individual q"""
        dominated = False
        for i in range(len(p.objectives)):
            if p.objectives[i] < q.objectives[i]:
                return False
            elif p.objectives[i] > q.objectives[i]:
                dominated = True
        return dominated
    
    def fast_non_dominated_sort(self, population: List[Individual]) -> List[List[Individual]]:
        """NSGA-II Fast Non-dominated Sorting"""
        fronts = [[]]
        
        for p in population:
            p.dominated_solutions = []
            p.domination_count = 0
            
            for q in population:
                if self.dominates(p, q):
                    p.dominated_solutions.append(q)
                elif self.dominates(q, p):
                    p.domination_count += 1
            
            if p.domination_count == 0:
                p.rank = 0
                fronts[0].append(p)
        
        i = 0
        # --- THE FIX IS IN THIS LINE BELOW ---
        while i < len(fronts) and fronts[i]:
            next_front = []
            for p in fronts[i]:
                for q in p.dominated_solutions:
                    q.domination_count -= 1
                    if q.domination_count == 0:
                        q.rank = i + 1
                        next_front.append(q)
            i += 1
            if next_front:
                fronts.append(next_front)
        
        return fronts[:-1] if len(fronts) > 0 and fronts[-1] == [] else fronts
    
    def calculate_crowding_distance(self, front: List[Individual]) -> None:
        """Calculate crowding distance for individuals in a front"""
        if len(front) <= 2:
            for ind in front:
                ind.crowding_distance = float('inf')
            return
        
        for ind in front:
            ind.crowding_distance = 0
        
        num_objectives = len(front[0].objectives)
        
        for m in range(num_objectives):
            front.sort(key=lambda x: x.objectives[m])
            
            front[0].crowding_distance = float('inf')
            front[-1].crowding_distance = float('inf')
            
            obj_min = front[0].objectives[m]
            obj_max = front[-1].objectives[m]
            obj_range = obj_max - obj_min if obj_max != obj_min else 1
            
            for i in range(1, len(front) - 1):
                distance = (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / obj_range
                front[i].crowding_distance += distance
    
    def tournament_selection(self, population: List[Individual]) -> Individual:
        """Binary tournament selection based on rank and crowding distance"""
        candidates = random.sample(population, min(2, len(population)))
        
        if len(candidates) == 1:
            return candidates[0]
        
        p, q = candidates
        
        if p.rank < q.rank:
            return p
        elif q.rank < p.rank:
            return q
        elif p.crowding_distance > q.crowding_distance:
            return p
        else:
            return q
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Uniform crossover of two parent builds"""
        if random.random() > self.crossover_rate:
            return deepcopy(parent1), deepcopy(parent2)
        
        child1_genes = {}
        child2_genes = {}
        
        for comp_type in parent1.genes.keys():
            if random.random() < 0.5:
                child1_genes[comp_type] = deepcopy(parent1.genes[comp_type])
                child2_genes[comp_type] = deepcopy(parent2.genes[comp_type])
            else:
                child1_genes[comp_type] = deepcopy(parent2.genes[comp_type])
                child2_genes[comp_type] = deepcopy(parent1.genes[comp_type])
        
        return Individual(genes=child1_genes), Individual(genes=child2_genes)
    
    def mutate(self, individual: Individual) -> Individual:
        """Mutate an individual by randomly changing components"""
        mutated = deepcopy(individual)
        
        for comp_type in mutated.genes.keys():
            if random.random() < self.mutation_rate:
                if comp_type in self.components and self.components[comp_type]:
                    mutated.genes[comp_type] = random.choice(self.components[comp_type])
        
        return mutated
    
    def repair(self, individual: Individual) -> Individual:
        """Repair an invalid individual to make it valid"""
        repaired = deepcopy(individual)
        genes = repaired.genes
        max_attempts = 50
        
        for _ in range(max_attempts):
            if self._is_valid_build(repaired):
                return repaired
            
            if 'cpu' in genes and 'motherboard' in genes:
                if genes['cpu']['socket'] != genes['motherboard']['socket']:
                    compatible_mbs = [
                        mb for mb in self.components.get('motherboard', [])
                        if mb['socket'] == genes['cpu']['socket']
                    ]
                    if compatible_mbs:
                        genes['motherboard'] = random.choice(compatible_mbs)
            
            if 'ram' in genes and 'motherboard' in genes:
                if genes['ram']['type'] not in genes['motherboard']['supported_ram']:
                    compatible_rams = [
                        ram for ram in self.components.get('ram', [])
                        if ram['type'] in genes['motherboard']['supported_ram']
                    ]
                    if compatible_rams:
                        genes['ram'] = random.choice(compatible_rams)
            
            if 'gpu' in genes and 'case' in genes:
                if genes['gpu']['length_mm'] > genes['case']['gpu_clearance_mm']:
                    compatible_cases = [
                        case for case in self.components.get('case', [])
                        if case['gpu_clearance_mm'] >= genes['gpu']['length_mm']
                    ]
                    if compatible_cases:
                        genes['case'] = random.choice(compatible_cases)
            
            if 'cpu' in genes and 'gpu' in genes and 'psu' in genes:
                total_tdp = genes['cpu']['tdp'] + genes['gpu']['tdp'] + 100
                required = total_tdp * 1.2
                if genes['psu']['wattage'] < required:
                    compatible_psus = [
                        psu for psu in self.components.get('psu', [])
                        if psu['wattage'] >= required
                    ]
                    if compatible_psus:
                        genes['psu'] = random.choice(compatible_psus)
        
        return repaired
    
    def create_offspring(self, population: List[Individual]) -> List[Individual]:
        """Create offspring population through selection, crossover, and mutation"""
        offspring = []
        
        while len(offspring) < self.population_size:
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            
            child1, child2 = self.crossover(parent1, parent2)
            
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            
            if not self._is_valid_build(child1):
                child1 = self.repair(child1)
            if not self._is_valid_build(child2):
                child2 = self.repair(child2)
            
            offspring.append(child1)
            if len(offspring) < self.population_size:
                offspring.append(child2)
        
        return offspring
    
    def select_next_generation(self, combined: List[Individual]) -> List[Individual]:
        """Select individuals for next generation based on NSGA-II"""
        fronts = self.fast_non_dominated_sort(combined)
        
        next_generation = []
        front_index = 0
        
        while len(next_generation) + len(fronts[front_index]) <= self.population_size:
            self.calculate_crowding_distance(fronts[front_index])
            next_generation.extend(fronts[front_index])
            front_index += 1
            if front_index >= len(fronts):
                break
        
        if len(next_generation) < self.population_size and front_index < len(fronts):
            self.calculate_crowding_distance(fronts[front_index])
            fronts[front_index].sort(key=lambda x: x.crowding_distance, reverse=True)
            
            remaining = self.population_size - len(next_generation)
            next_generation.extend(fronts[front_index][:remaining])
        
        return next_generation
    
    def optimize(self) -> List[Individual]:
        """Run the NSGA-II optimization algorithm"""
        population = self.initialize_population()
        
        for individual in population:
            self.evaluate_objectives(individual)
        
        for generation in range(self.generations):
            offspring = self.create_offspring(population)
            
            for individual in offspring:
                self.evaluate_objectives(individual)
            
            combined = population + offspring
            
            population = self.select_next_generation(combined)
            
            best_performance = max(ind.objectives[0] for ind in population)
            best_cost_fit = max(ind.objectives[1] for ind in population)
            avg_cost = sum(ind.get_total_cost() for ind in population) / len(population)
            
            self.generation_stats.append({
                'generation': generation,
                'best_performance': best_performance,
                'best_cost_fit': best_cost_fit,
                'avg_cost': avg_cost
            })
        
        return population
    
    def get_pareto_front(self, population: List[Individual]) -> List[Individual]:
        """Extract the Pareto-optimal front from the final population"""
        fronts = self.fast_non_dominated_sort(population)
        return fronts[0] if fronts else []
    
    def get_best_builds(self, num_builds: int = 3) -> List[Dict[str, Any]]:
        """
        Run optimization and return the best builds
        Returns builds with different trade-offs (performance vs budget)
        """
        final_population = self.optimize()
        pareto_front = self.get_pareto_front(final_population)
        
        if not pareto_front:
            return []
        
        builds = []
        
        pareto_front.sort(key=lambda x: x.objectives[0], reverse=True)
        if pareto_front:
            best_perf = self._format_build(pareto_front[0], "Best Performance")
            builds.append(best_perf)
        
        pareto_front.sort(key=lambda x: x.objectives[0] + x.objectives[1], reverse=True)
        if pareto_front and len(builds) < num_builds:
            best_value = self._format_build(pareto_front[0], "Best Value")
            if best_value['total_cost'] != builds[0]['total_cost']:
                builds.append(best_value)
        
        pareto_front.sort(key=lambda x: x.objectives[1], reverse=True)
        if pareto_front and len(builds) < num_builds:
            budget_friendly = self._format_build(pareto_front[0], "Budget Friendly")
            if budget_friendly['total_cost'] not in [b['total_cost'] for b in builds]:
                builds.append(budget_friendly)
        
        while len(builds) < num_builds and len(pareto_front) > len(builds):
            idx = len(builds)
            if idx < len(pareto_front):
                build = self._format_build(pareto_front[idx], f"Alternative {idx}")
                if build['total_cost'] not in [b['total_cost'] for b in builds]:
                    builds.append(build)
                else:
                    break
            else:
                break
        
        return builds[:num_builds]
    
    def _format_build(self, individual: Individual, label: str) -> Dict[str, Any]:
        """Format an individual as a build recommendation"""
        components = {}
        
        for comp_type, component in individual.genes.items():
            components[comp_type] = {
                'id': component.get('id'),
                'name': component.get('name'),
                'brand': component.get('brand'),
                'price': component.get('price'),
                'performance_score': component.get('performance_score'),
                **{k: v for k, v in component.items() 
                   if k not in ['id', 'name', 'brand', 'price', 'performance_score']}
            }
        
        total_cost = individual.get_total_cost()
        performance_score = individual.get_total_performance(self.weights)
        
        return {
            'label': label,
            'components': components,
            'total_cost': total_cost,
            'performance_score': round(performance_score, 2),
            'budget_utilization': round((total_cost / self.target_budget) * 100, 1),
            'within_budget': total_cost <= self.target_budget * 1.05
        }
