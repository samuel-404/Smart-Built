# SmartBuild: Intelligent PC Configuration Consultant

**Project Guide:** Ajish S.

**Team Members:** Irene, Naveen, Samuel, Vyshnav

---

## Project Overview

Personal computer configuration represents a significant challenge for consumers due to the overwhelming complexity of hardware compatibility, performance trade-offs, and budget constraints. The process demands specialized knowledge across multiple domains—CPU architectures, GPU specifications, power requirements, thermal management, and compatibility matrices—that most users do not possess. Consequently, many individuals either make suboptimal purchasing decisions, overspend on unnecessary components, or face system failures due to incompatible hardware selections. This knowledge gap disproportionately affects students, small businesses, and general consumers in emerging markets like India, where incorrect configurations can result in substantial financial losses and system downtime.

SmartBuild addresses this challenge through an **Intelligent PC Configuration Consultant**—an expert system that automates hardware selection using a hybrid inference engine combining two sophisticated algorithms. Rather than relegating users to manual component selection or generic recommendation lists, SmartBuild implements a two-phase decision process: first, a Constraint Satisfaction Problem (CSP) engine guarantees 100% hardware compatibility; second, a multi-objective genetic algorithm optimizes performance metrics against budget constraints. This intelligent automation democratizes access to expert-level PC configuration knowledge, enabling users to construct high-performance systems tailored to their specific use cases—whether gaming, content creation, professional workstation tasks, or educational pursuits—while maintaining strict adherence to their budgetary limitations and ensuring absolute hardware compatibility.

---

## Core Methodology: The Hybrid Inference Engine

### The Innovation: Two-Phase Decision Architecture

SmartBuild's core innovation lies in its hybrid inference engine, which decouples the **compatibility verification** problem from the **performance optimization** problem. This architectural separation ensures that every recommended configuration is guaranteed to be physically and electrically compatible before optimization occurs, eliminating the risk of incompatible system recommendations while maintaining sophisticated performance-cost balancing.

### Phase 1: The Gatekeeper—AC-3 Algorithm for Constraint Satisfaction

**Purpose:** Absolute Hardware Compatibility Verification

The first phase implements a **Constraint Satisfaction Problem (CSP)** engine utilizing the **AC-3 (Arc Consistency-3) Algorithm**, a foundational technique in constraint programming that guarantees domain consistency across variables.

**Technical Implementation:**

- **Variables:** Each PC component type (CPU, motherboard, GPU, RAM, power supply, case, cooler) represents a CSP variable with an associated domain consisting of all available market products.

- **Constraints:** Binary constraints model real-world hardware compatibility requirements:
  - **Socket Compatibility:** CPU socket type must match motherboard socket
  - **Power Requirements:** Total system power draw must not exceed power supply wattage (with appropriate margin)
  - **Thermal Management:** CPU cooler height and radiator dimensions must fit within case clearances
  - **Memory Compatibility:** RAM speed and type must be supported by the selected motherboard
  - **Form Factor Constraints:** Motherboard size must be compatible with case type
  - **BIOS/Firmware Support:** GPU and peripheral compatibility with chipset generation
  - **Physical Clearance:** GPU dimensions must fit case dimensions (length, height restrictions)

- **AC-3 Algorithm Process:**
  1. Initialize a queue with all variable pairs in the constraint graph
  2. For each arc (Vi, Vj), perform arc reduction:
     - Remove any value from Vi's domain that has no consistent value in Vj's domain
     - If the domain is reduced, add all neighboring arcs back to the queue
  3. Continue until the queue is empty or an inconsistency is detected
  4. Return the reduced domains representing feasible component options

**Output:** A filtered set of components where every pairwise combination is guaranteed to be compatible, eliminating invalid configurations at the source.

### Phase 2: The Optimizer—NSGA-II Genetic Algorithm for Multi-Objective Optimization

**Purpose:** Performance-Per-Rupee Optimization Across Multiple Dimensions

Following compatibility verification, the second phase applies the **NSGA-II (Non-dominated Sorting Genetic Algorithm II)**, a multi-objective evolutionary algorithm designed to balance competing objectives without predetermined weightings.

**Technical Implementation:**

- **Optimization Objectives:**
  - **Maximize Performance:** Gaming FPS, rendering speed, computational throughput (use-case dependent)
  - **Maximize Cost-Efficiency:** Performance-per-rupee ratio across CPU, GPU, and memory components
  - **Minimize Total Cost:** System price within the user's budget tier
  - **Minimize Power Consumption:** Operational cost and thermal output (secondary objective)

- **NSGA-II Algorithm Process:**
  1. **Population Initialization:** Generate random valid PC configurations (Pareto-feasible solutions) from the CSP-filtered component domain
  2. **Selection:** Binary tournament selection based on non-dominated rank and crowding distance
  3. **Crossover:** Uniform crossover between parent configurations at component boundaries
  4. **Mutation:** Random component swaps maintaining compatibility constraints
  5. **Environmental Selection:** Combine parent and offspring populations, apply non-dominated sorting, and retain solutions on the Pareto frontier
  6. **Termination:** After N generations, return the final Pareto-optimal front

- **Pareto Optimality:** The algorithm identifies configurations where improving one objective (e.g., performance) necessarily worsens another (e.g., cost). Users select their preferred trade-off point rather than receiving a single recommendation, increasing decision autonomy while leveraging AI guidance.

**Output:** A ranked set of Pareto-optimal PC configurations, each representing a distinct performance-cost trade-off. Users can select based on their preferences without facing artificial limitations.

---

## Technology Stack

### Frontend Architecture
- **Framework:** React.js (v18.2.0) with functional components and hooks
- **Styling:** Tailwind CSS (v3.4.0) for responsive, utility-first design; PostCSS with Autoprefixer for cross-browser compatibility
- **Animation & Interaction:** Framer Motion (v10.16.16) for smooth, physics-based component transitions and micro-interactions
- **Build System:** Vite (v5.0.8) for rapid development iteration and optimized production builds
- **Bundler Output:** ES modules for modern JavaScript environments

**Key UI Components:**
- SmartWizard: Interactive multi-step configuration wizard guiding users through usage-type and budget-tier selection
- Component Explorer: Visual representation of available components with filtering and comparison tools
- Configuration Builder: Real-time system assembly interface with live compatibility checking
- Results Dashboard: Visualization of Pareto-optimal configurations with performance metrics and cost breakdowns

### Backend Infrastructure
- **Runtime:** Python 3.x with Flask (v2.x) microframework
- **CORS Support:** Flask-CORS extension enabling cross-origin requests from frontend
- **Computation:** NumPy for efficient numerical operations in genetic algorithms and constraint solving
- **Environment Management:** Python-dotenv for secure configuration and credential management

**REST API Endpoints:**
- `/api/health` - Service health and version information
- `/api/usage-types` - Available user profiles (Gaming, Content Creation, Student, Workstation)
- `/api/budget-tiers` - Budget categories with ₹ pricing in Indian Rupees
- `/api/components` - Full hardware component database with metadata
- `/api/components/<type>` - Filtered components by category (CPU, GPU, RAM, etc.)
- `/api/optimize` - Primary endpoint accepting user preferences and returning Pareto-optimal configurations

### Data Layer
- **Format:** JSON-based component database with real-time Indian market pricing
- **Structure:** Hierarchical organization by component type with specifications and pricing metadata
- **Pricing Currency:** Indian Rupee (₹) reflecting local market conditions and consumer purchasing power
- **Data Source:** Aggregated from Indian retailers (MDComputers, Amazon.in, local market data) reflecting real availability and pricing
- **Update Mechanism:** Scheduled data refresh for market price synchronization

**Component Database Schema:**
```json
{
  "components": {
    "cpus": [{ "id", "model", "socket", "cores", "frequency", "tdp", "price_inr" }],
    "gpus": [{ "id", "model", "vram", "power", "dimensions", "price_inr" }],
    "motherboards": [{ "id", "model", "socket", "formfactor", "price_inr" }],
    "ram": [{ "id", "capacity", "speed", "type", "price_inr" }],
    "psus": [{ "id", "wattage", "efficiency", "modular", "price_inr" }],
    "cases": [{ "id", "formfactor", "max_gpu_length", "max_cooler_height", "price_inr" }]
  },
  "usage_profiles": {
    "gaming": { "target_fps": 60, "resolution": "1440p", "priority": "performance" },
    "content_creation": { "target_metric": "render_time", "priority": "cpu_power" },
    "student": { "budget_conscious": true, "priority": "value" },
    "workstation": { "priority": "reliability", "ecc_memory": true }
  }
}
```

---

## Future Scope

### Advanced Frontend Visualization
- **3D Component Visualizer:** WebGL-based interactive visualization of internal PC case layout showing thermal airflow simulation and component placement
- **Augmented Reality (AR) Internal Case View:** Mobile AR application enabling users to visualize component arrangement and cooling performance in their physical environment before purchase
- **Real-time Thermal Simulation:** Predictive temperature modeling with component stress testing recommendations

### Market Integration & Live Data
- **Retailer API Integration:** Direct connections to Indian e-commerce platforms (Amazon.in, Flipkart, MDComputers) for:
  - Real-time pricing synchronization
  - Live stock availability checking
  - Automated purchase link generation
- **Price History Analytics:** Historical pricing trends enabling users to identify optimal purchase windows
- **Review Aggregation:** Automated sentiment analysis from product reviews to flag reliability issues

### Machine Learning-Driven Personalization
- **Natural Language Processing (NLP):** Multi-language support (English, Hindi, Tamil, Telugu, Kannada) allowing users to describe their needs in conversational language:
  - "I want to play Cyberpunk at high settings"
  - "मुझे एडिटिंग के लिए एक सस्ता लेकिन तेज़ कंप्यूटर चाहिए"
- **Usage Pattern Learning:** Collaborative filtering based on similar user profiles and purchasing patterns
- **Predictive Recommendations:** ML models trained on successful builds to identify emerging component combinations
- **Sentiment-based Customization:** Emotional tone analysis to adjust recommendation strategies (risk-averse vs. aggressive buyers)

### Advanced Algorithm Enhancements
- **Supply Chain Optimization:** Algorithm variant considering component availability and shipping timelines
- **Sustainability Metrics:** Energy efficiency scoring and carbon footprint calculation per configuration
- **Future-Proofing Analysis:** Upgrade path recommendations and component longevity predictions
- **Thermal-Acoustic Optimization:** Balanced recommendations considering noise levels and heat dissipation

---

## Conclusion

SmartBuild represents a paradigm shift in personal computer configuration through **intelligent automation of expert-level decision-making**. By combining formal constraint satisfaction methods with evolutionary optimization techniques, we have created a system that transcends simple recommendation engines to guarantee both correctness and optimality. 

In democratizing access to high-performance computing configuration expertise, SmartBuild addresses a significant gap in the Indian consumer technology market, where knowledge asymmetry disproportionately affects students, small businesses, and general users. The hybrid CSP-GA architecture ensures that recommendations are not merely plausible but scientifically optimized within the Pareto frontier of feasible solutions.

Looking forward, the integration of NLP, AR visualization, and real-time market data will elevate SmartBuild toward a complete intelligent commerce ecosystem. This project demonstrates how algorithmic rigor, domain expertise, and user-centric design converge to solve authentic real-world problems while advancing the practical application of constraint programming and evolutionary computation in consumer technology decision support systems.

---

**Project Status:** Active Development  
**Last Updated:** January 27, 2026  
**Submission Ready:** Yes
