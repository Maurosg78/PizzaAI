import pytest
from src.core.models.dough_formulator import DoughFormulator, DoughFormulation

@pytest.fixture
def formulator():
    return DoughFormulator()

@pytest.fixture
def sample_ingredients():
    return {
        "beetroot": 0.3,
        "cauliflower": 0.4,
        "chickpea": 0.3
    }

@pytest.fixture
def target_properties():
    return {
        "protein": 15.0,
        "fiber": 8.0,
        "fat": 5.0,
        "carbohydrates": 30.0
    }

def test_load_ingredients(formulator):
    """Test que verifica la carga de ingredientes"""
    assert len(formulator.ingredients_db) > 0
    assert "vegetables" in formulator.ingredients_db
    assert "legumes" in formulator.ingredients_db

def test_optimize_formulation(formulator, target_properties):
    """Test que verifica la optimización de formulación"""
    formulation = formulator.optimize_formulation(target_properties)
    assert isinstance(formulation, DoughFormulation)
    assert len(formulation.ingredients) > 0
    assert all(isinstance(amount, float) for amount in formulation.ingredients.values())

def test_evaluate_formulation(formulator, sample_ingredients):
    """Test que verifica la evaluación de formulación"""
    formulation = DoughFormulation(
        ingredients=sample_ingredients,
        target_properties={},
        nutritional_profile={},
        cost=0.0,
        sustainability_score=0.0
    )
    evaluation = formulator.evaluate_formulation(formulation)
    assert isinstance(evaluation, dict)
    assert "taste_score" in evaluation
    assert "texture_score" in evaluation
    assert "cost_score" in evaluation 