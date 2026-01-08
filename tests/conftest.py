"""
ConsumeSafe Unit Tests Configuration
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing test data directory"""
    return project_root / "data"


@pytest.fixture
def sample_product():
    """Sample product for testing"""
    return {
        "product_name": "Test Coffee",
        "brand": "Test Brand",
        "category": "Beverages"
    }


@pytest.fixture
def sample_boycott_response():
    """Sample boycott response"""
    return {
        "is_boycotted": True,
        "reason": "Test reason",
        "confidence": 1.0
    }
