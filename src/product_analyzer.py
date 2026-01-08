"""
Product Analyzer Module
Manages Tunisian product database and provides alternatives
"""

import json
import logging
import os
from typing import Dict, List, Optional
import random

logger = logging.getLogger(__name__)


class ProductAnalyzer:
    """Analyze and suggest Tunisian product alternatives"""
    
    def __init__(self, data_path: str):
        # Handle relative paths by looking in parent directory
        if not os.path.isabs(data_path) and not os.path.exists(data_path):
            parent_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', os.path.basename(data_path))
            if os.path.exists(parent_data_path):
                data_path = parent_data_path
        
        self.data_path = data_path
        self.products: List[Dict] = []
        self.load_products()
    
    def load_products(self):
        """Load Tunisian products from JSON file"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.products = data.get("products", [])
                logger.info(f"Loaded {len(self.products)} Tunisian products")
        except FileNotFoundError:
            logger.warning(f"Products file not found at {self.data_path}")
            self.products = []
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in products file")
            self.products = []
    
    def get_alternatives(
        self,
        category: str = "general",
        exclude_brands: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Get alternative Tunisian products
        
        Args:
            category: Product category
            exclude_brands: Brand to exclude from results
            limit: Number of alternatives to return
            
        Returns:
            List of alternative products
        """
        alternatives = []
        
        # Filter by category if specified
        if category.lower() != "general":
            filtered = [
                p for p in self.products
                if p.get("category", "").lower() == category.lower()
            ]
        else:
            filtered = self.products
        
        # Exclude specified brand
        if exclude_brands:
            filtered = [
                p for p in filtered
                if p.get("brand", "").lower() != exclude_brands.lower()
            ]
        
        # Sort by rating (if available) and return top items
        filtered = sorted(
            filtered,
            key=lambda x: x.get("rating", 0),
            reverse=True
        )
        
        return filtered[:limit]
    
    def get_products(self, category: Optional[str] = None) -> List[Dict]:
        """Get all products or by category"""
        if category:
            return [
                p for p in self.products
                if p.get("category", "").lower() == category.lower()
            ]
        return self.products
    
    def get_categories(self) -> List[str]:
        """Get all available product categories"""
        categories = set()
        for product in self.products:
            category = product.get("category")
            if category:
                categories.add(category)
        return sorted(list(categories))
    
    def reload(self):
        """Reload products from file"""
        self.load_products()
