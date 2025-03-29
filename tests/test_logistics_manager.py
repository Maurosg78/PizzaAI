import pytest
from src.features.logistics.logistics_manager import LogisticsManager, StorageRequirements, DistributionChannel

@pytest.fixture
def manager():
    return LogisticsManager()

@pytest.fixture
def sample_storage_requirements():
    return {
        "temperature": -18.0,
        "humidity": 85.0,
        "shelf_life_days": 90,
        "packaging_type": "vacuum_sealed"
    }

@pytest.fixture
def sample_distribution_channel():
    return {
        "name": "local_delivery",
        "cost_per_unit": 5.0,
        "delivery_time_days": 1,
        "min_order_quantity": 10,
        "max_distance_km": 50
    }

def test_load_storage_requirements(manager):
    """Test que verifica la carga de requisitos de almacenamiento"""
    requirements = manager._load_storage_requirements()
    assert isinstance(requirements, dict)
    assert "frozen" in requirements
    assert "refrigerated" in requirements
    assert "room_temperature" in requirements

def test_load_distribution_channels(manager):
    """Test que verifica la carga de canales de distribución"""
    channels = manager._load_distribution_channels()
    assert isinstance(channels, dict)
    assert "local_delivery" in channels
    assert "regional_shipping" in channels
    assert "national_shipping" in channels

def test_optimize_distribution(manager, sample_distribution_channel):
    """Test que verifica la optimización de distribución"""
    channel = DistributionChannel(**sample_distribution_channel)
    optimization = manager.optimize_distribution(channel)
    assert isinstance(optimization, dict)
    assert "cost_efficiency" in optimization
    assert "delivery_efficiency" in optimization

def test_calculate_shipping_costs(manager, sample_distribution_channel):
    """Test que verifica el cálculo de costos de envío"""
    channel = DistributionChannel(**sample_distribution_channel)
    costs = manager.calculate_shipping_costs(channel, distance_km=30)
    assert isinstance(costs, dict)
    assert "base_cost" in costs
    assert "distance_cost" in costs
    assert "total_cost" in costs

def test_estimate_delivery_time(manager, sample_distribution_channel):
    """Test que verifica la estimación del tiempo de entrega"""
    channel = DistributionChannel(**sample_distribution_channel)
    delivery_time = manager.estimate_delivery_time(channel, distance_km=30)
    assert isinstance(delivery_time, float)
    assert delivery_time > 0 