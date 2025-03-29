import pytest
from src.core.services.usda_service import usda_service, NutrientInfo

@pytest.mark.asyncio
async def test_search_foods():
    """Prueba la búsqueda de alimentos"""
    results = await usda_service.search_foods("quinoa", page_size=5)
    assert len(results) > 0
    assert all("fdcId" in food for food in results)
    assert all("description" in food for food in results)

@pytest.mark.asyncio
async def test_get_food_details():
    """Prueba la obtención de detalles de un alimento"""
    # Primero buscamos un alimento
    results = await usda_service.search_foods("quinoa", page_size=1)
    assert len(results) > 0
    
    # Obtenemos los detalles del primer resultado
    fdc_id = results[0]["fdcId"]
    details = await usda_service.get_food_details(fdc_id)
    assert details is not None
    assert "foodNutrients" in details
    assert "servingSize" in details

@pytest.mark.asyncio
async def test_get_nutrient_info():
    """Prueba la obtención de información nutricional"""
    # Primero buscamos un alimento
    results = await usda_service.search_foods("quinoa", page_size=1)
    assert len(results) > 0
    
    # Obtenemos la información nutricional
    fdc_id = results[0]["fdcId"]
    nutrients = await usda_service.get_nutrient_info(fdc_id)
    assert len(nutrients) > 0
    assert all(isinstance(nutrient, NutrientInfo) for nutrient in nutrients)
    assert all(nutrient.value >= 0 for nutrient in nutrients) 