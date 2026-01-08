"""
Unit tests for ConsumeSafe application
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app, boycott_checker, product_analyzer


client = TestClient(app)


class TestHealthCheck:
    """Health check tests"""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestBoycottChecker:
    """Boycott checker tests"""
    
    def test_check_boycotted_product(self):
        response = client.post(
            "/check",
            json={"product_name": "coffee", "brand": "Nescafé"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["boycott_status"]["is_boycotted"] == True
        assert data["boycott_status"]["highlight"] == True
    
    def test_check_non_boycotted_product(self):
        response = client.post(
            "/check",
            json={"product_name": "Local Tunisian Dates"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["boycott_status"]["is_boycotted"] == False
    
    def test_get_boycott_list(self):
        response = client.get("/boycott-list")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "items" in data


class TestProductAnalyzer:
    """Product analyzer tests"""
    
    def test_get_tunisian_products(self):
        response = client.get("/tunisian-products")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] > 0
        assert "products" in data
    
    def test_get_products_by_category(self):
        response = client.get("/tunisian-products?category=Beverages")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 0
        if data["count"] > 0:
            for product in data["products"]:
                assert product["category"] == "Beverages"
    
    def test_get_categories(self):
        response = client.get("/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert "count" in data
        assert isinstance(data["categories"], list)
    
    def test_check_with_alternatives(self):
        response = client.post(
            "/check",
            json={
                "product_name": "coffee",
                "category": "Beverages"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "alternatives" in data
        assert len(data["alternatives"]) > 0


class TestProductCheckRequest:
    """Product check request validation"""
    
    def test_missing_product_name(self):
        response = client.post("/check", json={})
        assert response.status_code == 422
    
    def test_valid_request_with_optional_fields(self):
        response = client.post(
            "/check",
            json={
                "product_name": "Test Product",
                "brand": "Test Brand",
                "category": "Food"
            }
        )
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
