"""
Flask API Server for SmartBuild
Connects the frontend UI to the AI inference engine
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import logging
import httpx
from typing import Dict, Any

from dotenv import load_dotenv
load_dotenv()

from ai.csp_engine import CSPEngine
from ai.genetic_optimizer import NSGA2Optimizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Supabase Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase_headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Cache for data to avoid hitting Supabase on every request
_DATA_CACHE = None

def fetch_supabase_data(table_name: str):
    """Fetch all rows from a Supabase table using REST API"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Supabase credentials missing! Check environment variables.")
        return []
        
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=*"
    try:
        response = httpx.get(url, headers=supabase_headers, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching from Supabase '{table_name}': {e}")
        return []

def get_data() -> Dict[str, Any]:
    """Get component data from Supabase, with basic memory caching"""
    global _DATA_CACHE
    if _DATA_CACHE is not None:
        return _DATA_CACHE
        
    logger.info("Fetching fresh data from Supabase DB...")
    
    components_raw = fetch_supabase_data("components")
    usage_profiles_raw = fetch_supabase_data("usage_profiles")
    budget_tiers_raw = fetch_supabase_data("budget_tiers")
    
    # Reconstruct the expected nested structure for the algorithm
    structured_components = {
        "cpus": [], "gpus": [], "motherboards": [], 
        "ram": [], "storage": [], "psus": [], "cases": []
    }
    
    for item in components_raw:
        comp_type = item.get("type", "")
        # The frontend/algorithm expects a flat dict of specs mixed with core columns
        flat_item = item.get("specs", {})
        flat_item.update({
            "id": item.get("id"),
            "name": item.get("name"),
            "brand": item.get("brand"),
            "price": item.get("price"),
            "performance_score": item.get("performance_score")
        })
        if comp_type in structured_components:
            structured_components[comp_type].append(flat_item)
            
    # Reconstruct dictionary layouts
    usage_profiles = {p["id"]: p for p in usage_profiles_raw}
    budget_tiers = {b["id"]: b for b in budget_tiers_raw}
    
    # Fallback defaults if Supabase tables are empty or not seeded
    if not usage_profiles:
        logger.warning("Usage profiles empty from Supabase, using defaults")
        usage_profiles = {
            "gaming": {
                "id": "gaming",
                "name": "Gaming",
                "min_requirements": {"gpu_score": 50, "cpu_score": 40},
                "weights": {"gpu": 0.35, "cpu": 0.25, "ram": 0.12, "storage": 0.08, "motherboard": 0.10, "psu": 0.05, "case": 0.05}
            },
            "content_creation": {
                "id": "content_creation",
                "name": "Content Creation",
                "min_requirements": {"cpu_score": 60, "ram_score": 50},
                "weights": {"gpu": 0.25, "cpu": 0.30, "ram": 0.18, "storage": 0.10, "motherboard": 0.08, "psu": 0.05, "case": 0.04}
            },
            "student": {
                "id": "student",
                "name": "Student",
                "min_requirements": {"cpu_score": 30},
                "weights": {"gpu": 0.15, "cpu": 0.25, "ram": 0.18, "storage": 0.15, "motherboard": 0.12, "psu": 0.08, "case": 0.07}
            },
            "workstation": {
                "id": "workstation",
                "name": "Workstation",
                "min_requirements": {"cpu_score": 70, "ram_score": 60},
                "weights": {"gpu": 0.20, "cpu": 0.35, "ram": 0.20, "storage": 0.08, "motherboard": 0.08, "psu": 0.05, "case": 0.04}
            }
        }
    
    if not budget_tiers:
        logger.warning("Budget tiers empty from Supabase, using defaults")
        budget_tiers = {
            "budget": {"id": "budget", "name": "Budget", "min": 30000, "max": 50000, "description": "Essential builds for everyday tasks and light gaming"},
            "mid_range": {"id": "mid_range", "name": "Mid-Range", "min": 50000, "max": 100000, "description": "Balanced performance for gaming and productivity"},
            "high_end": {"id": "high_end", "name": "High-End", "min": 100000, "max": 200000, "description": "Premium builds for enthusiast gaming and heavy workloads"},
            "enthusiast": {"id": "enthusiast", "name": "Enthusiast", "min": 200000, "max": 500000, "description": "Top-tier builds with the best components available"}
        }
    
    _DATA_CACHE = {
        "components": structured_components,
        "usage_profiles": usage_profiles,
        "budget_tiers": budget_tiers
    }
    return _DATA_CACHE


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "SmartBuild AI Engine",
        "version": "1.0.0"
    })


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the data cache to force re-fetch from Supabase"""
    global _DATA_CACHE
    _DATA_CACHE = None
    logger.info("Data cache cleared")
    return jsonify({
        "success": True,
        "message": "Cache cleared. Next request will fetch fresh data from Supabase."
    })


@app.route('/api/usage-types', methods=['GET'])
def get_usage_types():
    """Get available usage types/profiles"""
    usage_profiles = get_data().get('usage_profiles', {})
    
    profiles = []
    for key, profile in usage_profiles.items():
        profiles.append({
            "id": key,
            "name": profile.get('name', key),
            "description": _get_usage_description(key),
            "icon": _get_usage_icon(key),
            "min_requirements": profile.get('min_requirements', {})
        })
    
    return jsonify({
        "success": True,
        "usage_types": profiles
    })


def _get_usage_description(usage_type: str) -> str:
    """Get description for usage type"""
    descriptions = {
        "gaming": "High FPS gaming at 1080p/1440p with ray tracing support",
        "content_creation": "Video editing, 3D rendering, and creative workflows",
        "student": "Coding, office work, light gaming, and everyday tasks",
        "workstation": "Professional CAD, simulation, and heavy computational work"
    }
    return descriptions.get(usage_type, "General purpose computing")


def _get_usage_icon(usage_type: str) -> str:
    """Get icon identifier for usage type"""
    icons = {
        "gaming": "gamepad",
        "content_creation": "video",
        "student": "book",
        "workstation": "briefcase"
    }
    return icons.get(usage_type, "computer")


@app.route('/api/budget-tiers', methods=['GET'])
def get_budget_tiers():
    """Get budget tier information"""
    budget_tiers = get_data().get('budget_tiers', {})
    
    tiers = []
    for key, tier in budget_tiers.items():
        tiers.append({
            "id": key,
            "name": tier.get('name', key),
            "min": tier.get('min', 0),
            "max": tier.get('max', 0),
            "description": tier.get('description', '')
        })
    
    tiers.sort(key=lambda x: x['min'])
    
    return jsonify({
        "success": True,
        "budget_tiers": tiers,
        "currency": "INR",
        "symbol": "₹"
    })


@app.route('/api/components', methods=['GET'])
def get_all_components():
    """Get all available components"""
    components = get_data().get('components', {})
    
    summary = {}
    for comp_type, items in components.items():
        summary[comp_type] = {
            "count": len(items),
            "price_range": {
                "min": min(item['price'] for item in items) if items else 0,
                "max": max(item['price'] for item in items) if items else 0
            }
        }
    
    return jsonify({
        "success": True,
        "components": components,
        "summary": summary
    })


@app.route('/api/components/<component_type>', methods=['GET'])
def get_components_by_type(component_type: str):
    """Get components of a specific type"""
    components = get_data().get('components', {})
    
    type_mapping = {
        'cpu': 'cpus',
        'gpu': 'gpus',
        'motherboard': 'motherboards',
        'ram': 'ram',
        'psu': 'psus',
        'case': 'cases',
        'storage': 'storage'
    }
    
    lookup_type = type_mapping.get(component_type, component_type)
    
    if lookup_type not in components:
        return jsonify({
            "success": False,
            "error": f"Unknown component type: {component_type}"
        }), 404
    
    return jsonify({
        "success": True,
        "component_type": component_type,
        "components": components[lookup_type]
    })


@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """
    Main endpoint: Get PC build recommendations
    Accepts budget and usage type, returns optimized builds
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        budget = data.get('budget')
        usage_type = data.get('usage_type', 'gaming')
        num_builds = data.get('num_builds', 1)  # Default to 1 build
        cpu_brand = data.get('cpu_brand', None)  # Optional: 'Intel' or 'AMD'
        
        if not budget:
            return jsonify({
                "success": False,
                "error": "Budget is required"
            }), 400
        
        try:
            budget = int(budget)
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Budget must be a valid number"
            }), 400
        
        if budget < 30000:
            return jsonify({
                "success": False,
                "error": "Minimum budget is ₹30,000"
            }), 400
        
        if budget > 500000:
            return jsonify({
                "success": False,
                "error": "Maximum budget is ₹5,00,000"
            }), 400
        
        valid_usage_types = list(get_data().get('usage_profiles', {}).keys())
        if usage_type not in valid_usage_types:
            return jsonify({
                "success": False,
                "error": f"Invalid usage type. Valid types: {valid_usage_types}"
            }), 400
        
        # Validate cpu_brand if provided
        if cpu_brand and cpu_brand not in ('Intel', 'AMD'):
            return jsonify({
                "success": False,
                "error": f"Invalid CPU brand. Valid brands: Intel, AMD"
            }), 400
        
        logger.info(f"Generating recommendations: Budget=₹{budget:,}, Usage={usage_type}, CPU Brand={cpu_brand or 'Any'}")
        
        csp_engine = CSPEngine(get_data()['components'])
        compatible_components = csp_engine.get_compatible_components(budget, usage_type)
        
        # Filter by CPU brand preference if specified
        if cpu_brand and 'cpu' in compatible_components:
            brand_cpus = [
                cpu for cpu in compatible_components['cpu']
                if cpu.get('brand', '') == cpu_brand
            ]
            logger.info(f"Brand filter ({cpu_brand}): {len(compatible_components['cpu'])} CPUs -> {len(brand_cpus)}")
            if brand_cpus:
                compatible_components['cpu'] = brand_cpus
                
                # Also filter motherboards to only compatible sockets
                brand_sockets = set(cpu.get('socket', '') for cpu in brand_cpus)
                if 'motherboard' in compatible_components and brand_sockets:
                    brand_boards = [
                        mb for mb in compatible_components['motherboard']
                        if mb.get('socket', '') in brand_sockets
                    ]
                    if brand_boards:
                        logger.info(f"Socket filter: {len(compatible_components['motherboard'])} boards -> {len(brand_boards)}")
                        compatible_components['motherboard'] = brand_boards
        
        # HARD FILTER: For budget builds (< 45k), ONLY allow APUs (integrated graphics)
        # Remove ALL GPUs and non-APU CPUs for budget builds
        if budget < 45000:
            logger.info("Budget build detected - filtering for APU-only builds")
            
            # Keep ONLY CPUs with integrated graphics
            if 'cpu' in compatible_components:
                apu_only = [
                    cpu for cpu in compatible_components['cpu']
                    if cpu.get('integrated_graphics', False) == True
                ]
                logger.info(f"APU filter: {len(compatible_components['cpu'])} CPUs -> {len(apu_only)} APUs")
                compatible_components['cpu'] = apu_only
            
            # Remove ALL GPUs for budget builds (APU handles graphics)
            if 'gpu' in compatible_components:
                logger.info(f"Removing {len(compatible_components['gpu'])} GPUs for APU build")
                compatible_components['gpu'] = []
        
        csp_summary = {k: len(v) for k, v in compatible_components.items()}
        logger.info(f"CSP filtered components: {csp_summary}")
        
        optimizer = NSGA2Optimizer(
            compatible_components=compatible_components,
            target_budget=budget,
            usage_type=usage_type,
            usage_profiles=get_data()['usage_profiles'],
            population_size=40,
            generations=60
        )
        
        builds = optimizer.get_best_builds(num_builds)
        
        if not builds:
            return jsonify({
                "success": False,
                "error": "Could not generate valid builds for the given constraints"
            }), 400
        
        stats = optimizer.generation_stats[-5:] if optimizer.generation_stats else []
        
        response = {
            "success": True,
            "request": {
                "budget": budget,
                "usage_type": usage_type,
                "usage_name": get_data()['usage_profiles'][usage_type]['name']
            },
            "recommendations": builds,
            "optimization_info": {
                "csp_filtered_counts": csp_summary,
                "generations_run": len(optimizer.generation_stats),
                "final_stats": stats
            }
        }
        
        logger.info(f"Generated {len(builds)} build recommendations")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/alternatives', methods=['POST'])
def get_alternatives():
    """
    Get compatible alternative components for a specific type.
    Accepts the current build and a component_type, returns compatible swaps.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        component_type = data.get('component_type')
        current_build = data.get('current_build', {})
        
        if not component_type:
            return jsonify({"success": False, "error": "component_type is required"}), 400
        
        # Map component type to data key
        type_to_data = {
            'cpu': 'cpus', 'gpu': 'gpus', 'motherboard': 'motherboards',
            'ram': 'ram', 'psu': 'psus', 'case': 'cases', 'storage': 'storage'
        }
        
        data_key = type_to_data.get(component_type)
        if not data_key:
            return jsonify({"success": False, "error": f"Invalid component type: {component_type}"}), 400
        
        all_components = get_data().get('components', {}).get(data_key, [])
        current_component_id = None
        if component_type in current_build and current_build[component_type]:
            current_component_id = current_build[component_type].get('id')
        
        # Filter for compatibility with the rest of the build
        compatible = []
        for candidate in all_components:
            # Skip the currently selected component
            if candidate.get('id') == current_component_id:
                continue
            
            # Build a test configuration with the candidate swapped in
            test_build = {k: v for k, v in current_build.items() if v}
            test_build[component_type] = candidate
            
            # Run CSP validation
            csp_engine = CSPEngine(get_data()['components'])
            is_valid, issues = csp_engine.validate_build(test_build)
            
            if is_valid:
                compatible.append({
                    'id': candidate.get('id'),
                    'name': candidate.get('name'),
                    'brand': candidate.get('brand'),
                    'price': candidate.get('price'),
                    'performance_score': candidate.get('performance_score'),
                    **{k: v for k, v in candidate.items()
                       if k not in ['id', 'name', 'brand', 'price', 'performance_score']}
                })
        
        # Sort by price
        compatible.sort(key=lambda x: x.get('price', 0))
        
        logger.info(f"Alternatives for {component_type}: {len(compatible)} compatible out of {len(all_components)}")
        
        return jsonify({
            "success": True,
            "component_type": component_type,
            "alternatives": compatible,
            "total_available": len(all_components)
        })
    
    except Exception as e:
        logger.error(f"Error fetching alternatives: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/api/validate-build', methods=['POST'])
def validate_build():
    """Validate a custom build configuration"""
    try:
        data = request.get_json()
        
        if not data or 'build' not in data:
            return jsonify({
                "success": False,
                "error": "Build configuration required"
            }), 400
        
        build = data['build']
        
        csp_engine = CSPEngine(get_data()['components'])
        is_valid, issues = csp_engine.validate_build(build)
        
        total_cost = sum(
            comp.get('price', 0) 
            for comp in build.values() 
            if isinstance(comp, dict)
        )
        
        total_tdp = sum(
            comp.get('tdp', 0) 
            for comp in build.values() 
            if isinstance(comp, dict)
        )
        
        return jsonify({
            "success": True,
            "is_valid": is_valid,
            "issues": issues,
            "totals": {
                "cost": total_cost,
                "tdp": total_tdp,
                "recommended_psu": int(total_tdp * 1.2 + 100)
            }
        })
    
    except Exception as e:
        logger.error(f"Error validating build: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Validation error: {str(e)}"
        }), 500


@app.route('/api/prices/update-live', methods=['POST'])
def update_live_price():
    """
    Endpoint for fetching and updating the live price of a specific component.
    Expects JSON: { "component_id": "cpu_001" }
    """
    try:
        data = request.get_json()
        component_id = data.get('component_id')
        
        if not component_id:
            return jsonify({"success": False, "error": "component_id required"}), 400
            
        # 1. "Scrape" or "Fetch" real-time pricing here.
        # For demonstration purposes, we will simulate a real-time price fluctuation API
        # In production this would use Beautiful Soup or a specific Vendor API (e.g. Amazon PA-API)
        import random
        # Simulate connecting to an external server and fetching a newer price calculation.
        simulated_live_price = float(random.randint(5000, 80000))
        
        # 2. Update the specific row in Supabase via REST API
        if not SUPABASE_URL or not SUPABASE_KEY:
             return jsonify({"success": False, "error": "Supabase Connection Missing"}), 500
        
        url = f"{SUPABASE_URL}/rest/v1/components?id=eq.{component_id}"
        payload = {"price": simulated_live_price}
        
        update_response = httpx.patch(url, headers=supabase_headers, json=payload, timeout=10.0)
        update_response.raise_for_status()

        # Invalidate the memory cache so the UI sees the new price
        global _DATA_CACHE
        _DATA_CACHE = None
        
        return jsonify({
            "success": True,
            "message": f"Successfully updated component {component_id} pricing.",
            "new_price": simulated_live_price
        })

    except httpx.HTTPError as he:
        logger.error(f"Live Price update Supabase Error: {he}")
        return jsonify({"success": False, "error": f"Database mutation failed: {he}"}), 500
    except Exception as e:
        logger.error(f"Error fetching live prices: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500



@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    logger.info(f"Starting SmartBuild API Server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
