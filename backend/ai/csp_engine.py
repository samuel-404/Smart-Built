"""
CSP Engine - AC-3 Algorithm Implementation for PC Component Compatibility
SmartBuild: Intelligent PC Configuration Consultant
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from collections import deque
from dataclasses import dataclass, field
import copy
import logging

logger = logging.getLogger(__name__)


@dataclass
class Variable:
    """Represents a CSP variable (component type) with its domain"""
    name: str
    domain: List[Dict[str, Any]]
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return self.name == other.name


@dataclass
class Constraint:
    """Represents a binary constraint between two variables"""
    var1: str
    var2: str
    check_function: callable
    description: str


class CSPEngine:
    """
    Constraint Satisfaction Problem Engine using AC-3 Algorithm
    Implements arc consistency for PC component compatibility checking
    """
    
    def __init__(self, components_data: Dict[str, Any]):
        self.components = components_data
        self.variables: Dict[str, Variable] = {}
        self.constraints: List[Constraint] = []
        self.constraint_graph: Dict[str, List[str]] = {}
        
        self._setup_constraints()
    
    # Chipset → supported CPU architectures
    CHIPSET_COMPAT = {
        'A320': ['Zen','Zen+','Zen2'], 'B450': ['Zen','Zen+','Zen2','Zen3'],
        'A520': ['Zen2','Zen3'], 'B550': ['Zen2','Zen3'], 'X570': ['Zen2','Zen3'],
        'B650': ['Zen4','Zen5'], 'B650E': ['Zen4','Zen5'],
        'X670': ['Zen4','Zen5'], 'X670E': ['Zen4','Zen5'],
        'B850': ['Zen4','Zen5'], 'X870': ['Zen4','Zen5'], 'X870E': ['Zen4','Zen5'],
        'B460': ['CometLake','RocketLake'], 'B560': ['CometLake','RocketLake'],
        'Z490': ['CometLake','RocketLake'], 'Z590': ['CometLake','RocketLake'],
        'B660': ['AlderLake','RaptorLake','RaptorLakeR'],
        'B760': ['AlderLake','RaptorLake','RaptorLakeR'],
        'H770': ['AlderLake','RaptorLake','RaptorLakeR'],
        'Z690': ['AlderLake','RaptorLake','RaptorLakeR'],
        'Z790': ['AlderLake','RaptorLake','RaptorLakeR'],
    }
    # CPU name pattern → architecture
    CPU_ARCH = {
        'Ryzen 3 3200G':'Zen+','Ryzen 5 3400G':'Zen+','Athlon 3000G':'Zen',
        'Ryzen 5 3600':'Zen2','Ryzen 7 3700X':'Zen2','Ryzen 9 3900X':'Zen2',
        'Ryzen 5 4600G':'Zen3','Ryzen 5 5500':'Zen3','Ryzen 5 5600':'Zen3',
        'Ryzen 5 5600G':'Zen3','Ryzen 5 5600X':'Zen3','Ryzen 7 5700G':'Zen3',
        'Ryzen 7 5800X':'Zen3','Ryzen 9 5900X':'Zen3','Ryzen 9 5950X':'Zen3',
        'Ryzen 5 7600':'Zen4','Ryzen 7 7700':'Zen4','Ryzen 7 7700X':'Zen4',
        'Ryzen 7 7800X3D':'Zen4','Ryzen 9 7950X':'Zen4','Ryzen 9 7950X3D':'Zen4',
        'Ryzen 5 8600G':'Zen4','Ryzen 7 8700G':'Zen4',
        'Ryzen 5 9600X':'Zen5','Ryzen 7 9700X':'Zen5','Ryzen 7 9800X3D':'Zen5',
        'Ryzen 9 9900X':'Zen5','Ryzen 9 9950X':'Zen5','Ryzen 9 9950X3D':'Zen5',
        'i5-10400F':'CometLake','i7-10700K':'CometLake',
        'i5-11400F':'RocketLake',
        'i3-12100F':'AlderLake','i3-12100':'AlderLake',
        'i5-12400F':'AlderLake','i5-12400':'AlderLake',
        'i3-13100':'RaptorLake','i5-13400F':'RaptorLake','i5-13400':'RaptorLake',
        'i7-13700KF':'RaptorLake','i9-13900K':'RaptorLake',
        'i5-14400F':'RaptorLakeR','i5-14600K':'RaptorLakeR',
        'i7-14700K':'RaptorLakeR','i7-14700KF':'RaptorLakeR',
        'i9-14900K':'RaptorLakeR','i9-14900KS':'RaptorLakeR',
        'Core Ultra 9 285K':'ArrowLake',
    }

    def _check_cpu_mb(self, cpu, mb):
        """Check socket + chipset generation compatibility."""
        if cpu.get('socket') != mb.get('socket'):
            return False
        # Use chipset field if present, else parse from name
        chipset = mb.get('chipset', '')
        if not chipset:
            for cs in sorted(self.CHIPSET_COMPAT.keys(), key=len, reverse=True):
                if cs in mb.get('name', ''):
                    chipset = cs
                    break
        if not chipset:
            return True  # Unknown chipset → allow (socket matched)
        cpu_name = cpu.get('name', '')
        arch = None
        for pattern, a in self.CPU_ARCH.items():
            if pattern in cpu_name:
                arch = a
                break
        if not arch:
            return True  # Unknown arch → allow (socket matched)
        return arch in self.CHIPSET_COMPAT.get(chipset, [])

    def _setup_constraints(self):
        """Define all compatibility constraints between components"""
        
        self.add_constraint(
            'cpu', 'motherboard',
            lambda cpu, mb: self._check_cpu_mb(cpu, mb),
            "CPU must be compatible with motherboard socket AND chipset"
        )
        
        self.add_constraint(
            'cpu', 'ram',
            lambda cpu, ram: ram.get('type', 'DDR4') in cpu.get('supported_ram', ['DDR4', 'DDR5']),
            "RAM type must be supported by CPU"
        )
        
        self.add_constraint(
            'motherboard', 'ram',
            lambda mb, ram: ram.get('type', 'DDR4') in mb.get('supported_ram', ['DDR4']),
            "RAM type must be supported by motherboard"
        )
        
        self.add_constraint(
            'cpu', 'psu',
            lambda cpu, psu: True,
            "PSU wattage check (partial)"
        )
        
        self.add_constraint(
            'gpu', 'psu',
            lambda gpu, psu: True,
            "PSU wattage check (partial)"
        )
    
    def add_constraint(self, var1: str, var2: str, check_fn: callable, description: str):
        """Add a binary constraint between two variables"""
        constraint = Constraint(var1, var2, check_fn, description)
        self.constraints.append(constraint)
        
        if var1 not in self.constraint_graph:
            self.constraint_graph[var1] = []
        if var2 not in self.constraint_graph:
            self.constraint_graph[var2] = []
        
        if var2 not in self.constraint_graph[var1]:
            self.constraint_graph[var1].append(var2)
        if var1 not in self.constraint_graph[var2]:
            self.constraint_graph[var2].append(var1)
    
    def initialize_domains(self, budget: int, usage_type: str) -> Dict[str, Variable]:
        """Initialize variable domains based on budget and usage requirements"""
        domains = {}
        
        budget_allocations = self._get_budget_allocation(budget, usage_type)
        
        cpu_budget = budget_allocations.get('cpu', budget * 0.25)
        cpu_domain = [
            cpu for cpu in self.components['cpus']
            if cpu['price'] <= cpu_budget * 2.5
        ]
        domains['cpu'] = Variable('cpu', cpu_domain if cpu_domain else self.components['cpus'][:2])
        
        gpu_budget = budget_allocations.get('gpu', budget * 0.35)
        gpu_domain = [
            gpu for gpu in self.components['gpus']
            if gpu['price'] <= gpu_budget * 2.5
        ]
        domains['gpu'] = Variable('gpu', gpu_domain if gpu_domain else self.components['gpus'][:2])
        
        mb_budget = budget_allocations.get('motherboard', budget * 0.12)
        mb_domain = [
            mb for mb in self.components['motherboards']
            if mb['price'] <= mb_budget * 2.5
        ]
        domains['motherboard'] = Variable('motherboard', mb_domain if mb_domain else self.components['motherboards'][:2])
        
        ram_budget = budget_allocations.get('ram', budget * 0.08)
        ram_domain = [
            ram for ram in self.components['ram']
            if ram['price'] <= ram_budget * 2.5
        ]
        domains['ram'] = Variable('ram', ram_domain if ram_domain else self.components['ram'][:2])
        
        psu_budget = budget_allocations.get('psu', budget * 0.08)
        psu_domain = [
            psu for psu in self.components['psus']
            if psu['price'] <= psu_budget * 2.5
        ]
        domains['psu'] = Variable('psu', psu_domain if psu_domain else self.components['psus'][:2])
        
        case_budget = budget_allocations.get('case', budget * 0.07)
        case_domain = [
            case for case in self.components['cases']
            if case['price'] <= case_budget * 2.5
        ]
        domains['case'] = Variable('case', case_domain if case_domain else self.components['cases'][:2])
        
        storage_budget = budget_allocations.get('storage', budget * 0.08)
        storage_domain = [
            storage for storage in self.components['storage']
            if storage['price'] <= storage_budget * 2.5
        ]
        domains['storage'] = Variable('storage', storage_domain if storage_domain else self.components['storage'][:2])
        
        self.variables = domains
        return domains
    
    def _get_budget_allocation(self, budget: int, usage_type: str) -> Dict[str, float]:
        """Get budget allocation percentages based on usage type"""
        allocations = {
            'gaming': {
                'cpu': budget * 0.20,
                'gpu': budget * 0.38,
                'motherboard': budget * 0.12,
                'ram': budget * 0.08,
                'psu': budget * 0.08,
                'case': budget * 0.07,
                'storage': budget * 0.07
            },
            'content_creation': {
                'cpu': budget * 0.28,
                'gpu': budget * 0.25,
                'motherboard': budget * 0.12,
                'ram': budget * 0.15,
                'psu': budget * 0.07,
                'case': budget * 0.06,
                'storage': budget * 0.07
            },
            'student': {
                'cpu': budget * 0.25,
                'gpu': budget * 0.20,
                'motherboard': budget * 0.15,
                'ram': budget * 0.12,
                'psu': budget * 0.10,
                'case': budget * 0.08,
                'storage': budget * 0.10
            },
            'workstation': {
                'cpu': budget * 0.30,
                'gpu': budget * 0.22,
                'motherboard': budget * 0.12,
                'ram': budget * 0.18,
                'psu': budget * 0.07,
                'case': budget * 0.05,
                'storage': budget * 0.06
            }
        }
        return allocations.get(usage_type, allocations['gaming'])
    
    def ac3(self) -> bool:
        """
        AC-3 Algorithm Implementation
        Returns True if arc consistency is achieved, False if domain wipeout
        """
        queue = deque()
        
        for constraint in self.constraints:
            queue.append((constraint.var1, constraint.var2, constraint))
            queue.append((constraint.var2, constraint.var1, constraint))
        
        iterations = 0
        max_iterations = 10000
        
        while queue and iterations < max_iterations:
            iterations += 1
            xi, xj, constraint = queue.popleft()
            
            if self._revise(xi, xj, constraint):
                if len(self.variables[xi].domain) == 0:
                    return False
                
                for xk in self.constraint_graph.get(xi, []):
                    if xk != xj:
                        for c in self.constraints:
                            if (c.var1 == xk and c.var2 == xi) or (c.var1 == xi and c.var2 == xk):
                                queue.append((xk, xi, c))
        
        return True
    
    def _revise(self, xi: str, xj: str, constraint: Constraint) -> bool:
        """
        Revise the domain of xi with respect to xj
        Returns True if domain was reduced
        """
        revised = False
        domain_i = self.variables[xi].domain.copy()
        
        for val_i in domain_i:
            has_support = False
            
            for val_j in self.variables[xj].domain:
                if self._satisfies_constraint(xi, val_i, xj, val_j, constraint):
                    has_support = True
                    break
            
            if not has_support:
                self.variables[xi].domain.remove(val_i)
                revised = True
        
        return revised
    
    def _satisfies_constraint(self, var1: str, val1: Dict, var2: str, val2: Dict, constraint: Constraint) -> bool:
        """Check if a pair of values satisfies the given constraint"""
        try:
            if constraint.var1 == var1:
                return constraint.check_function(val1, val2)
            else:
                return constraint.check_function(val2, val1)
        except (KeyError, TypeError, AttributeError) as e:
            # When data is incomplete, ALLOW the combination rather than rejecting it.
            # The genetic optimizer's _is_valid_build will do final validation.
            logger.debug(f"Constraint check error ({constraint.description}): {e} - allowing combo")
            return True
    
    def check_psu_compatibility(self, cpu: Dict, gpu: Dict, psu: Dict) -> bool:
        """Special check for PSU wattage with 20% headroom"""
        total_tdp = cpu.get('tdp', 0) + gpu.get('tdp', 0)
        required_wattage = total_tdp * 1.2
        required_wattage += 100
        
        return psu.get('wattage', 0) >= required_wattage
    
    def get_compatible_components(self, budget: int, usage_type: str) -> Dict[str, List[Dict]]:
        """
        Main entry point: Get all compatible components after AC-3 filtering
        """
        self.initialize_domains(budget, usage_type)
        
        original_domains = {
            name: copy.deepcopy(var.domain) 
            for name, var in self.variables.items()
        }
        
        success = self.ac3()
        
        if not success:
            return {
                name: original_domains[name]
                for name in self.variables.keys()
            }
        
        result = {}
        for name, variable in self.variables.items():
            result[name] = variable.domain
        
        return result
    
    def validate_build(self, build: Dict[str, Dict]) -> Tuple[bool, List[str]]:
        """
        Validate a complete build configuration
        Returns (is_valid, list_of_issues)
        """
        issues = []
        
        if build.get('cpu') and build.get('motherboard'):
            if build['cpu']['socket'] != build['motherboard']['socket']:
                issues.append(
                    f"Socket mismatch: CPU ({build['cpu']['socket']}) != "
                    f"Motherboard ({build['motherboard']['socket']})"
                )
        
        if build.get('ram') and build.get('motherboard'):
            ram_type = build['ram'].get('type', 'DDR4')
            if ram_type not in build['motherboard'].get('supported_ram', ['DDR4', 'DDR5']):
                issues.append(
                    f"RAM type {ram_type} not supported by motherboard"
                )
        
        if build.get('ram') and build.get('cpu'):
            ram_type = build['ram'].get('type', 'DDR4')
            if ram_type not in build['cpu'].get('supported_ram', ['DDR4', 'DDR5']):
                issues.append(
                    f"RAM type {ram_type} not supported by CPU"
                )
        
        if build.get('gpu') and build.get('case'):
            gpu_len = build['gpu'].get('length_mm', 0)
            case_clearance = build['case'].get('gpu_clearance_mm', 999)
            if gpu_len > case_clearance:
                issues.append(
                    f"GPU too long ({gpu_len}mm) for case "
                    f"({case_clearance}mm clearance)"
                )
        
        if build.get('motherboard') and build.get('case'):
            mb_ff = build['motherboard'].get('form_factor', 'ATX')
            case_ff = build['case'].get('form_factor', ['ATX', 'Micro-ATX', 'Mini-ITX'])
            if mb_ff not in case_ff:
                issues.append(
                    f"Motherboard form factor ({mb_ff}) "
                    f"doesn't fit case"
                )
        
        if build.get('cpu') and build.get('gpu') and build.get('psu'):
            if not self.check_psu_compatibility(build['cpu'], build['gpu'], build['psu']):
                total_tdp = build['cpu']['tdp'] + build['gpu']['tdp']
                required = int(total_tdp * 1.2 + 100)
                issues.append(
                    f"PSU wattage ({build['psu']['wattage']}W) insufficient. "
                    f"Recommended: {required}W minimum"
                )
        
        return len(issues) == 0, issues


class CompatibilityChecker:
    """Utility class for quick compatibility checks"""
    
    @staticmethod
    def check_socket_match(cpu: Dict, motherboard: Dict) -> bool:
        return cpu.get('socket') == motherboard.get('socket')
    
    @staticmethod
    def check_ram_compatibility(ram: Dict, motherboard: Dict, cpu: Dict) -> bool:
        ram_type = ram.get('type')
        mb_supports = ram_type in motherboard.get('supported_ram', [])
        cpu_supports = ram_type in cpu.get('supported_ram', [])
        return mb_supports and cpu_supports
    
    @staticmethod
    def check_gpu_clearance(gpu: Dict, case: Dict) -> bool:
        return gpu.get('length_mm', 0) <= case.get('gpu_clearance_mm', 0)
    
    @staticmethod
    def check_psu_headroom(cpu: Dict, gpu: Dict, psu: Dict, headroom: float = 0.2) -> bool:
        total_tdp = cpu.get('tdp', 0) + gpu.get('tdp', 0) + 100
        required = total_tdp * (1 + headroom)
        return psu.get('wattage', 0) >= required
