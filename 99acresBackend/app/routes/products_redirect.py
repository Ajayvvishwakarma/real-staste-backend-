from fastapi import APIRouter

router = APIRouter()

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_products_redirect():
    """Redirect products to properties"""
    return {
        "success": True,
        "message": "Products endpoint - please use /api/properties instead",
        "redirect_to": "/api/properties",
        "note": "This is a real estate API, properties are available at /api/properties"
    }