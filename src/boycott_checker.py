"""
Boycott Checker Module
Loads and checks products against boycott list
"""

import json
import logging
import os
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BoycottChecker:
    """Check if products are on boycott list"""
    
    def __init__(self, data_path: str):
        # Handle relative paths by looking in parent directory
        if not os.path.isabs(data_path) and not os.path.exists(data_path):
            parent_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', os.path.basename(data_path))
            if os.path.exists(parent_data_path):
                data_path = parent_data_path
        
        self.data_path = data_path
        self.boycott_list: List[Dict] = []
        self.load_boycott_list()
    
    def load_boycott_list(self):
        """Load boycott list from JSON file"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.boycott_list = data.get("items", [])
                logger.info(f"Loaded {len(self.boycott_list)} boycott items")
        except FileNotFoundError:
            logger.warning(f"Boycott list file not found at {self.data_path}")
            self.boycott_list = []
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in boycott list file")
            self.boycott_list = []
    
    def check(self, product_name: str, brand: Optional[str] = None) -> Dict:
        """
        Check if product is on boycott list
        
        Args:
            product_name: Name of the product
            brand: Brand name (optional)
            
        Returns:
            Dict with is_boycotted, reason, and confidence
        """
        product_lower = product_name.lower()
        brand_lower = brand.lower() if brand else ""
        
        for item in self.boycott_list:
            # Check product name match
            if product_lower in item.get("products", []):
                return {
                    "is_boycotted": True,
                    "reason": item.get("reason", "On boycott list"),
                    "confidence": 1.0,
                    "date_added": item.get("date_added")
                }
            
            # Check brand match
            if brand_lower and brand_lower in item.get("brands", []):
                return {
                    "is_boycotted": True,
                    "reason": item.get("reason", "Brand is on boycott list"),
                    "confidence": 0.95,
                    "date_added": item.get("date_added")
                }
            
            # Partial match (lower confidence)
            if product_lower in item.get("keywords", []):
                return {
                    "is_boycotted": True,
                    "reason": item.get("reason", "Related to boycott"),
                    "confidence": 0.7,
                    "date_added": item.get("date_added")
                }
        
        return {
            "is_boycotted": False,
            "reason": None,
            "confidence": 1.0
        }
    
    def get_all_items(self) -> List[Dict]:
        """Get all boycott list items"""
        return self.boycott_list
    
    def get_active_boycotts(self) -> List[Dict]:
        """Get only active boycotts"""
        return [
            item for item in self.boycott_list
            if item.get("is_active", True)
        ]
    
    def reload(self):
        """Reload boycott list from file"""
        self.load_boycott_list()
