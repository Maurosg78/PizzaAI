import pytest
from src.features.nutrition.nutrition_analyzer import NutritionAnalyzer, NutritionalProfile

@pytest.fixture
def analyzer():
    return NutritionAnalyzer()

@pytest.fixture
def sample_nutritional_profile():
    return {
        "protein": 15.0,
        "fiber": 8.0,
        "fat": 5.0,
        "carbohydrates": 30.0,
        "calories": 250.0,
        "glycemic_index": 45.0
    }

def test_load_nutrient_references(analyzer):
    """Test que verifica la carga de referencias nutricionales"""
    references = analyzer._load_nutrient_references()
    assert isinstance(references, dict)
    assert "pizza" in references
    assert "bread" in references

def test_analyze_nutritional_profile(analyzer, sample_nutritional_profile):
    """Test que verifica el análisis del perfil nutricional"""
    profile = NutritionalProfile(**sample_nutritional_profile)
    analysis = analyzer.analyze_nutritional_profile(profile)
    assert isinstance(analysis, dict)
    assert "protein_score" in analysis
    assert "fiber_score" in analysis
    assert "fat_score" in analysis

def test_calculate_glycemic_index(analyzer, sample_nutritional_profile):
    """Test que verifica el cálculo del índice glucémico"""
    profile = NutritionalProfile(**sample_nutritional_profile)
    glycemic_index = analyzer.calculate_glycemic_index(profile)
    assert isinstance(glycemic_index, float)
    assert 0 <= glycemic_index <= 100

def test_optimize_for_nutrition(analyzer, sample_nutritional_profile):
    """Test que verifica la optimización nutricional"""
    profile = NutritionalProfile(**sample_nutritional_profile)
    optimized = analyzer.optimize_for_nutrition(profile)
    assert isinstance(optimized, dict)
    assert "protein" in optimized
    assert "fiber" in optimized
    assert "fat" in optimized 