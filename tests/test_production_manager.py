import pytest
from src.features.production.production_manager import ProductionManager, ProductionEquipment, ProductionProcess

@pytest.fixture
def manager():
    return ProductionManager()

@pytest.fixture
def sample_equipment():
    return {
        "name": "Mixer Pro",
        "capacity": 50.0,
        "cost": 5000.0,
        "energy_consumption": 2.5,
        "maintenance_frequency": 30
    }

@pytest.fixture
def sample_process():
    return {
        "steps": ["mezclar", "amasar", "fermentar", "hornear"],
        "temperature_requirements": {
            "mezclar": 25.0,
            "amasar": 28.0,
            "fermentar": 30.0,
            "hornear": 220.0
        },
        "time_requirements": {
            "mezclar": 10,
            "amasar": 15,
            "fermentar": 120,
            "hornear": 20
        },
        "equipment": ["Mixer Pro", "Amasadora", "Fermentadora", "Horno"]
    }

def test_load_equipment(manager):
    """Test que verifica la carga de equipamiento"""
    equipment = manager._load_equipment()
    assert isinstance(equipment, dict)
    assert "mixer" in equipment
    assert "kneader" in equipment
    assert "proofer" in equipment

def test_load_process_templates(manager):
    """Test que verifica la carga de plantillas de proceso"""
    templates = manager._load_process_templates()
    assert isinstance(templates, dict)
    assert "pizza" in templates
    assert "bread" in templates

def test_optimize_production(manager, sample_process):
    """Test que verifica la optimización de producción"""
    process = ProductionProcess(**sample_process)
    optimization = manager.optimize_production(process)
    assert isinstance(optimization, dict)
    assert "efficiency_score" in optimization
    assert "cost_optimization" in optimization

def test_calculate_production_costs(manager, sample_process):
    """Test que verifica el cálculo de costos de producción"""
    process = ProductionProcess(**sample_process)
    costs = manager.calculate_production_costs(process)
    assert isinstance(costs, dict)
    assert "equipment_costs" in costs
    assert "energy_costs" in costs
    assert "labor_costs" in costs 