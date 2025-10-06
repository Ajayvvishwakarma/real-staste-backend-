from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()

class PropertySearchRequest(BaseModel):
    savings: float
    emi: float
    loan_tenure: int
    loan_amount: float
    total_budget: float
    property_type: Optional[str] = None
    location: Optional[str] = None
    bedrooms: Optional[int] = None

# Sample property data for testing
SAMPLE_PROPERTIES = [
    {
        "id": 1,
        "title": "Luxury 3BHK Apartment",
        "description": "Spacious 3BHK apartment with modern amenities",
        "property_type": "apartment",
        "price": 15000000,
        "area": 1200,
        "bedrooms": 3,
        "bathrooms": 2,
        "address": "Sector 62, Noida",
        "city": "Noida",
        "state": "Uttar Pradesh",
        "pincode": "201301",
        "status": "available",
        "is_featured": True
    },
    {
        "id": 2,
        "title": "2BHK Builder Floor",
        "description": "Well-ventilated 2BHK builder floor",
        "property_type": "house",
        "price": 8500000,
        "area": 900,
        "bedrooms": 2,
        "bathrooms": 2,
        "address": "Lajpat Nagar, Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "pincode": "110024",
        "status": "available",
        "is_featured": False
    },
    {
        "id": 3,
        "title": "Commercial Office Space",
        "description": "Modern office space in business district",
        "property_type": "commercial",
        "price": 25000000,
        "area": 2000,
        "bedrooms": 0,
        "bathrooms": 4,
        "address": "Cyber City, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "pincode": "122002",
        "status": "available",
        "is_featured": True
    },
    {
        "id": 4,
        "title": "Budget 2BHK Apartment",
        "description": "Affordable 2BHK apartment in developing area",
        "property_type": "apartment",
        "price": 3500000,
        "area": 800,
        "bedrooms": 2,
        "bathrooms": 2,
        "address": "Sector 120, Noida",
        "city": "Noida",
        "state": "Uttar Pradesh",
        "pincode": "201307",
        "status": "available",
        "is_featured": False
    },
    {
        "id": 5,
        "title": "Compact 1BHK Flat",
        "description": "Well-designed 1BHK flat for first-time buyers",
        "property_type": "apartment",
        "price": 2800000,
        "area": 600,
        "bedrooms": 1,
        "bathrooms": 1,
        "address": "Indirapuram, Ghaziabad",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "pincode": "201014",
        "status": "available",
        "is_featured": False
    },
    {
        "id": 6,
        "title": "Spacious 3BHK in Suburbs",
        "description": "Large 3BHK apartment in peaceful suburb",
        "property_type": "apartment",
        "price": 4200000,
        "area": 1100,
        "bedrooms": 3,
        "bathrooms": 2,
        "address": "Raj Nagar Extension, Ghaziabad",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "pincode": "201017",
        "status": "available",
        "is_featured": True
    },
    {
        "id": 7,
        "title": "Modern 2BHK Ready to Move",
        "description": "Ready to move 2BHK with modern amenities",
        "property_type": "apartment",
        "price": 3800000,
        "area": 900,
        "bedrooms": 2,
        "bathrooms": 2,
        "address": "Greater Noida West",
        "city": "Greater Noida",
        "state": "Uttar Pradesh",
        "pincode": "201310",
        "status": "available",
        "is_featured": True
    }
]

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_properties(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    city: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Get all properties with filtering - SQLite integration pending"""
    
    # Simple filtering on sample data
    filtered_properties = SAMPLE_PROPERTIES.copy()
    
    if city:
        filtered_properties = [p for p in filtered_properties if city.lower() in p["city"].lower()]
    
    if property_type:
        filtered_properties = [p for p in filtered_properties if p["property_type"] == property_type]
    
    if min_price:
        filtered_properties = [p for p in filtered_properties if p["price"] >= min_price]
        
    if max_price:
        filtered_properties = [p for p in filtered_properties if p["price"] <= max_price]
    
    # Apply pagination
    total = len(filtered_properties)
    properties = filtered_properties[skip:skip + limit]
    
    return {
        "success": True,
        "message": "Properties retrieved successfully - SQLite integration in progress",
        "data": properties,
        "pagination": {
            "total": total,
            "count": len(properties),
            "skip": skip,
            "limit": limit
        }
    }

@router.get("/{property_id}", response_model=dict)
async def get_property(property_id: int):
    """Get single property by ID - SQLite integration pending"""
    
    property_data = next((p for p in SAMPLE_PROPERTIES if p["id"] == property_id), None)
    
    if not property_data:
        raise HTTPException(
            status_code=404, 
            detail=f"Property with ID {property_id} not found"
        )
    
    return {
        "success": True,
        "message": "Property retrieved successfully",
        "data": property_data
    }

@router.get("/featured/list", response_model=dict)
async def get_featured_properties():
    """Get featured properties - SQLite integration pending"""
    
    featured = [p for p in SAMPLE_PROPERTIES if p.get("is_featured", False)]
    
    return {
        "success": True,
        "message": "Featured properties retrieved successfully",
        "data": featured,
        "count": len(featured)
    }

@router.post("/", response_model=dict)
async def create_property():
    """Create new property - SQLite integration pending"""
    return {
        "success": False,
        "message": "Property creation - SQLite integration in progress"
    }

@router.put("/{property_id}", response_model=dict)
async def update_property(property_id: int):
    """Update property - SQLite integration pending"""
    return {
        "success": False,
        "message": f"Property {property_id} update - SQLite integration in progress"
    }

@router.post("/find-properties")
@router.post("/find-properties/")
async def find_properties(search_request: PropertySearchRequest):
    """Find properties based on budget and loan criteria"""
    try:
        # Filter properties based on total budget
        budget_range_min = search_request.total_budget * 0.8  # Allow 20% below budget
        budget_range_max = search_request.total_budget * 1.1  # Allow 10% above budget
        
        filtered_properties = []
        
        for property in SAMPLE_PROPERTIES:
            # Check if property price is within budget range
            if budget_range_min <= property["price"] <= budget_range_max:
                # Calculate financing details for this property
                down_payment_needed = property["price"] - search_request.loan_amount
                down_payment_percentage = (down_payment_needed / property["price"]) * 100
                
                # Calculate affordability score (higher is better)
                affordability_score = 100
                if down_payment_needed > search_request.savings:
                    affordability_score -= 30  # Insufficient down payment
                if property["price"] > search_request.total_budget:
                    affordability_score -= 20  # Over budget
                
                # Add financing details to property
                property_with_finance = property.copy()
                property_with_finance["financing_details"] = {
                    "property_price": property["price"],
                    "loan_amount": search_request.loan_amount,
                    "down_payment_needed": round(down_payment_needed),
                    "down_payment_percentage": round(down_payment_percentage, 1),
                    "monthly_emi": search_request.emi,
                    "loan_tenure": search_request.loan_tenure,
                    "affordability_score": affordability_score,
                    "is_affordable": down_payment_needed <= search_request.savings
                }
                
                filtered_properties.append(property_with_finance)
        
        # Sort by affordability score (best matches first)
        filtered_properties.sort(key=lambda x: x["financing_details"]["affordability_score"], reverse=True)
        
        # Calculate summary statistics
        total_properties = len(filtered_properties)
        affordable_count = len([p for p in filtered_properties if p["financing_details"]["is_affordable"]])
        
        if total_properties == 0:
            return {
                "success": True,
                "message": "No properties found within your budget range",
                "search_criteria": {
                    "total_budget": search_request.total_budget,
                    "loan_amount": search_request.loan_amount,
                    "savings": search_request.savings,
                    "monthly_emi": search_request.emi
                },
                "properties": [],
                "summary": {
                    "total_found": 0,
                    "affordable_count": 0,
                    "budget_range": f"₹{budget_range_min:,.0f} - ₹{budget_range_max:,.0f}"
                },
                "suggestions": [
                    "Consider increasing your budget",
                    "Look for properties in different locations",
                    "Consider a higher loan amount if eligible",
                    "Explore properties with lower prices"
                ]
            }
        
        return {
            "success": True,
            "message": f"Found {total_properties} properties matching your criteria",
            "search_criteria": {
                "total_budget": search_request.total_budget,
                "loan_amount": search_request.loan_amount,
                "savings": search_request.savings,
                "monthly_emi": search_request.emi,
                "loan_tenure": search_request.loan_tenure
            },
            "properties": filtered_properties,
            "summary": {
                "total_found": total_properties,
                "affordable_count": affordable_count,
                "budget_range": f"₹{budget_range_min:,.0f} - ₹{budget_range_max:,.0f}",
                "average_price": round(sum(p["price"] for p in filtered_properties) / total_properties),
                "price_range": {
                    "min": min(p["price"] for p in filtered_properties),
                    "max": max(p["price"] for p in filtered_properties)
                }
            },
            "financing_summary": {
                "average_down_payment": round(sum(p["financing_details"]["down_payment_needed"] for p in filtered_properties) / total_properties),
                "properties_within_savings": affordable_count,
                "recommended_property": filtered_properties[0]["title"] if filtered_properties else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding properties: {str(e)}")