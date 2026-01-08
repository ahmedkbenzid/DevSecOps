"""
ConsumeSafe - Boycott Product Checker Application
Detects if a product is on a boycott list and suggests Tunisian alternatives.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
from typing import List, Optional
import os
from pathlib import Path

from boycott_checker import BoycottChecker
from product_analyzer import ProductAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ConsumeSafe API",
    description="Boycott checker and Tunisian product alternatives",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Security
security = HTTPBearer()

# Initialize checkers
boycott_checker = BoycottChecker(
    data_path=os.getenv("BOYCOTT_DATA_PATH", "data/boycott_list.json")
)
product_analyzer = ProductAnalyzer(
    data_path=os.getenv("PRODUCTS_DATA_PATH", "data/tunisian_products.json")
)


class ProductCheckRequest(BaseModel):
    """Request model for product check"""
    product_name: str
    brand: Optional[str] = None
    category: Optional[str] = None


class BoycottStatus(BaseModel):
    """Response model for boycott status"""
    is_boycotted: bool
    reason: Optional[str] = None
    highlight: bool
    confidence: float


class AlternativeProduct(BaseModel):
    """Alternative Tunisian product"""
    name: str
    brand: str
    category: str
    origin: str
    description: Optional[str] = None


class CheckResponse(BaseModel):
    """Full check response"""
    product_name: str
    boycott_status: BoycottStatus
    alternatives: List[AlternativeProduct]


@app.get("/")
async def root():
    """Serve the frontend"""
    from fastapi.responses import FileResponse
    frontend_index = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_index.exists():
        return FileResponse(frontend_index)
    return {"message": "ConsumeSafe API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ConsumeSafe API"}


@app.post("/check", response_model=CheckResponse)
async def check_product(request: ProductCheckRequest):
    """
    Check if a product is on boycott list and get Tunisian alternatives
    """
    try:
        logger.info(f"Checking product: {request.product_name}")
        
        # Check boycott status
        boycott_info = boycott_checker.check(
            product_name=request.product_name,
            brand=request.brand
        )
        
        # Get alternatives
        alternatives = product_analyzer.get_alternatives(
            category=request.category or "general",
            exclude_brands=request.brand if request.brand else None
        )
        
        response = CheckResponse(
            product_name=request.product_name,
            boycott_status=BoycottStatus(
                is_boycotted=boycott_info["is_boycotted"],
                reason=boycott_info.get("reason"),
                highlight=boycott_info["is_boycotted"],
                confidence=boycott_info.get("confidence", 1.0)
            ),
            alternatives=[
                AlternativeProduct(**alt) for alt in alternatives[:5]
            ]
        )
        
        logger.info(f"Check completed for {request.product_name}")
        return response
        
    except Exception as e:
        logger.error(f"Error checking product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/boycott-list")
async def get_boycott_list():
    """Get all boycott list items"""
    try:
        items = boycott_checker.get_all_items()
        return {"count": len(items), "items": items}
    except Exception as e:
        logger.error(f"Error fetching boycott list: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tunisian-products")
async def get_tunisian_products(category: Optional[str] = None):
    """Get all Tunisian products or by category"""
    try:
        products = product_analyzer.get_products(category=category)
        return {"count": len(products), "products": products}
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories")
async def get_categories():
    """Get all available product categories"""
    try:
        categories = product_analyzer.get_categories()
        return {"count": len(categories), "categories": categories}
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "info")
    )
