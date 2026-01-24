"""
Flask API Server for SmartBuild
Connects the frontend UI to the AI inference engine
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import logging
from typing import Dict, Any

from ai.csp_engine import CSPEngine
from ai.genetic_optimizer import NSGA2Optimizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'seed_data.json')

def load_data() -> Dict[str, Any]:
    """Load component data from JSON file"""
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Data file not found: {DATA_PATH}")
        return {"components": {}, "usage_profiles": {}, "budget_tiers": {}}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing data file: {e}")
        return {"components": {}, "usage_profiles": {}, "budget_tiers": {}}

DATA = load_data()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "SmartBuild AI Engine",
        "version": "1.0.0"
    })


@app.route('/api/usage-types', methods=['GET'])
def get_usage_types():
    """Get available usage types/profiles"""
    usage_profiles = DATA.get('usage_profiles', {})
    
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
    budget_tiers = DATA.get('budget_tiers', {})
    
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
    components = DATA.get('components', {})
    
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
    components = DATA.get('components', {})
    
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
        num_builds = data.get('num_builds', 3)
        
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
        
        valid_usage_types = list(DATA.get('usage_profiles', {}).keys())
        if usage_type not in valid_usage_types:
            return jsonify({
                "success": False,
                "error": f"Invalid usage type. Valid types: {valid_usage_types}"
            }), 400
        
        logger.info(f"Generating recommendations: Budget=₹{budget:,}, Usage={usage_type}")
        
        csp_engine = CSPEngine(DATA['components'])
        compatible_components = csp_engine.get_compatible_components(budget, usage_type)
        
        csp_summary = {k: len(v) for k, v in compatible_components.items()}
        logger.info(f"CSP filtered components: {csp_summary}")
        
        optimizer = NSGA2Optimizer(
            compatible_components=compatible_components,
            target_budget=budget,
            usage_type=usage_type,
            usage_profiles=DATA['usage_profiles'],
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
                "usage_name": DATA['usage_profiles'][usage_type]['name']
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
        
        csp_engine = CSPEngine(DATA['components'])
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
