from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class PremiumProperty(BaseModel):
    id: int
    title: str
    description: str
    price: float
    location: str
    property_type: str
    bedrooms: int
    bathrooms: int
    area: float
    amenities: List[str]
    images: List[str]
    agent: Dict[str, Any]
    featured: bool
    created_at: datetime
    views: int
    status: str
    premium_features: Dict[str, Any]
    exclusive_features: Dict[str, Any]
    luxury_amenities: List[str]
    concierge_services: List[str]
    investment_details: Dict[str, Any]

class PremiumStats(BaseModel):
    total_properties: int
    total_views: int
    average_price: float
    most_viewed_property: Dict[str, Any]
    luxury_properties_count: int
    exclusive_deals_count: int
    investment_grade_count: int

# Premium listings data - Ultra-luxury properties with exclusive features
premium_properties = [
    {
        "id": 1,
        "title": "Royal Heritage Palace - Ultimate Luxury",
        "description": "Ultra-luxury heritage palace with royal amenities, private helipad, and exclusive concierge services. Investment-grade property with guaranteed returns.",
        "price": 50000000.0,  # ₹50 Cr
        "location": "Lutyens' Delhi, New Delhi",
        "property_type": "Heritage Palace",
        "bedrooms": 12,
        "bathrooms": 15,
        "area": 25000.0,
        "amenities": [
            "Private Helipad", "Royal Ballroom", "Wine Cellar", "Private Theater",
            "Indoor Pool", "Spa & Wellness Center", "Private Gardens", "Staff Quarters",
            "Security Command Center", "Private Elevator", "Panic Room", "Art Gallery"
        ],
        "images": [
            "https://example.com/premium1-1.jpg",
            "https://example.com/premium1-2.jpg",
            "https://example.com/premium1-3.jpg",
            "https://example.com/premium1-4.jpg"
        ],
        "agent": {
            "name": "Rajesh Khanna",
            "phone": "+91 98765 43210",
            "email": "rajesh@premiumrealty.com",
            "company": "Premium Realty Group",
            "rating": 5.0,
            "experience": "25+ years",
            "specialization": "Ultra-luxury Heritage Properties",
            "certification": "Certified Luxury Home Marketing Specialist (CLHMS)"
        },
        "featured": True,
        "created_at": datetime.now(),
        "views": 5230,
        "status": "available",
        "premium_features": {
            "vr_tour": True,
            "drone_photography": True,
            "professional_video": True,
            "floor_plans": True,
            "3d_walkthrough": True,
            "virtual_staging": True,
            "aerial_views": True,
            "neighborhood_insights": True,
            "market_analysis": True,
            "investment_calculator": True,
            "mortgage_calculator": True,
            "social_media_promotion": True,
            "premium_placement": True,
            "featured_listing": True,
            "priority_support": True
        },
        "exclusive_features": {
            "private_showing": True,
            "helicopter_tour": True,
            "personal_butler": True,
            "interior_designer_consultation": True,
            "legal_assistance": True,
            "property_management": True,
            "concierge_services": True,
            "vip_access": True,
            "exclusive_events": True,
            "lifestyle_consultation": True
        },
        "luxury_amenities": [
            "Royal Heritage Architecture", "Hand-carved Marble Interiors", "Crystal Chandeliers",
            "Italian Marble Flooring", "Gold-plated Fixtures", "Imported Furniture",
            "Smart Home Automation", "Climate Control", "Sound-proof Rooms",
            "Bulletproof Glass", "Private Parking (50 cars)", "Servant Quarters"
        ],
        "concierge_services": [
            "24/7 Personal Butler", "Private Chef Service", "Housekeeping Staff",
            "Personal Security Team", "Chauffeur Service", "Event Management",
            "Travel Arrangements", "Shopping Assistance", "Medical Services",
            "Pet Care Services"
        ],
        "investment_details": {
            "appreciation_rate": "15% per annum",
            "rental_yield": "8% per annum",
            "investment_grade": "AAA+",
            "guaranteed_returns": True,
            "buyback_guarantee": True,
            "tax_benefits": True,
            "capital_gains_exemption": True,
            "property_insurance": "Comprehensive Coverage"
        }
    },
    {
        "id": 2,
        "title": "Skyscraper Penthouse with Private Sky Lounge",
        "description": "Ultra-exclusive penthouse at 80th floor with 360-degree city views, private sky lounge, and helicopter landing facility.",
        "price": 35000000.0,  # ₹35 Cr
        "location": "Worli, Mumbai",
        "property_type": "Sky Penthouse",
        "bedrooms": 8,
        "bathrooms": 10,
        "area": 15000.0,
        "amenities": [
            "Private Sky Lounge", "Helicopter Landing", "Infinity Pool", "Private Cinema",
            "Wine Cellar", "Gym & Spa", "Game Room", "Library", "Home Office",
            "Guest Suites", "Staff Quarters", "Panic Room"
        ],
        "images": [
            "https://example.com/premium2-1.jpg",
            "https://example.com/premium2-2.jpg",
            "https://example.com/premium2-3.jpg"
        ],
        "agent": {
            "name": "Priya Sharma",
            "phone": "+91 99888 77666",
            "email": "priya@luxuryskyhomes.com",
            "company": "Luxury Sky Homes",
            "rating": 4.9,
            "experience": "20+ years",
            "specialization": "Luxury Penthouses & Sky Homes",
            "certification": "International Real Estate Specialist"
        },
        "featured": True,
        "created_at": datetime.now(),
        "views": 4150,
        "status": "available",
        "premium_features": {
            "vr_tour": True,
            "drone_photography": True,
            "professional_video": True,
            "floor_plans": True,
            "3d_walkthrough": True,
            "virtual_staging": True,
            "aerial_views": True,
            "neighborhood_insights": True,
            "market_analysis": True,
            "investment_calculator": True,
            "mortgage_calculator": True,
            "social_media_promotion": True,
            "premium_placement": True,
            "featured_listing": True,
            "priority_support": True
        },
        "exclusive_features": {
            "private_showing": True,
            "helicopter_tour": True,
            "personal_butler": True,
            "interior_designer_consultation": True,
            "legal_assistance": True,
            "property_management": True,
            "concierge_services": True,
            "vip_access": True,
            "exclusive_events": True,
            "lifestyle_consultation": True
        },
        "luxury_amenities": [
            "360-Degree City Views", "Floor-to-Ceiling Windows", "Italian Designer Kitchen",
            "Smart Home System", "Private Elevator", "Climate Control",
            "High-Speed Internet", "Security System", "Intercom System"
        ],
        "concierge_services": [
            "24/7 Concierge", "Housekeeping", "Maintenance", "Security",
            "Valet Parking", "Pet Services", "Dry Cleaning", "Grocery Shopping"
        ],
        "investment_details": {
            "appreciation_rate": "12% per annum",
            "rental_yield": "6% per annum",
            "investment_grade": "AAA",
            "guaranteed_returns": True,
            "buyback_guarantee": False,
            "tax_benefits": True,
            "capital_gains_exemption": False,
            "property_insurance": "Full Coverage"
        }
    },
    {
        "id": 3,
        "title": "Private Island Resort Villa",
        "description": "Exclusive private island villa with pristine beaches, yacht access, and complete privacy for the ultimate luxury experience.",
        "price": 75000000.0,  # ₹75 Cr
        "location": "Lakshadweep Islands",
        "property_type": "Island Resort Villa",
        "bedrooms": 15,
        "bathrooms": 18,
        "area": 45000.0,
        "amenities": [
            "Private Beach", "Yacht Dock", "Seaplane Landing", "Resort Facilities",
            "Water Sports Center", "Spa Resort", "Multiple Pools", "Tennis Court",
            "Golf Course", "Marina", "Helipad", "Conference Center"
        ],
        "images": [
            "https://example.com/premium3-1.jpg",
            "https://example.com/premium3-2.jpg",
            "https://example.com/premium3-3.jpg"
        ],
        "agent": {
            "name": "Captain Arjun Singh",
            "phone": "+91 97654 32109",
            "email": "arjun@islandluxury.com",
            "company": "Island Luxury Estates",
            "rating": 5.0,
            "experience": "30+ years",
            "specialization": "Island Properties & Resort Estates",
            "certification": "International Luxury Property Specialist"
        },
        "featured": True,
        "created_at": datetime.now(),
        "views": 8750,
        "status": "available",
        "premium_features": {
            "vr_tour": True,
            "drone_photography": True,
            "professional_video": True,
            "floor_plans": True,
            "3d_walkthrough": True,
            "virtual_staging": True,
            "aerial_views": True,
            "neighborhood_insights": True,
            "market_analysis": True,
            "investment_calculator": True,
            "mortgage_calculator": True,
            "social_media_promotion": True,
            "premium_placement": True,
            "featured_listing": True,
            "priority_support": True
        },
        "exclusive_features": {
            "private_showing": True,
            "helicopter_tour": True,
            "personal_butler": True,
            "interior_designer_consultation": True,
            "legal_assistance": True,
            "property_management": True,
            "concierge_services": True,
            "vip_access": True,
            "exclusive_events": True,
            "lifestyle_consultation": True
        },
        "luxury_amenities": [
            "Private Island Ownership", "Pristine Beaches", "Crystal Clear Waters",
            "Tropical Gardens", "Luxury Accommodation", "World-class Dining",
            "Water Sports Equipment", "Spa & Wellness", "Entertainment Center"
        ],
        "concierge_services": [
            "Island Management Team", "Personal Chef", "Yacht Crew",
            "Housekeeping Staff", "Security Personnel", "Activity Coordinators",
            "Spa Therapists", "Tour Guides", "Transportation Services"
        ],
        "investment_details": {
            "appreciation_rate": "20% per annum",
            "rental_yield": "10% per annum",
            "investment_grade": "AAA++",
            "guaranteed_returns": True,
            "buyback_guarantee": True,
            "tax_benefits": True,
            "capital_gains_exemption": True,
            "property_insurance": "Comprehensive Island Coverage"
        }
    },
    {
        "id": 4,
        "title": "Maharaja's Palace with Royal Court",
        "description": "Authentic Maharaja's palace with royal court, throne room, and extensive palace grounds. A piece of Indian royalty for exclusive ownership.",
        "price": 45000000.0,  # ₹45 Cr
        "location": "Udaipur, Rajasthan",
        "property_type": "Royal Palace",
        "bedrooms": 20,
        "bathrooms": 25,
        "area": 35000.0,
        "amenities": [
            "Royal Throne Room", "Palace Courts", "Royal Gardens", "Palace Museum",
            "Royal Kitchen", "Guard Towers", "Palace Gates", "Royal Stables",
            "Palace Temple", "Royal Library", "Treasury Room", "Palace Armory"
        ],
        "images": [
            "https://example.com/premium4-1.jpg",
            "https://example.com/premium4-2.jpg",
            "https://example.com/premium4-3.jpg"
        ],
        "agent": {
            "name": "Maharani Sunita Devi",
            "phone": "+91 96543 21087",
            "email": "sunita@royalpalaces.com",
            "company": "Royal Palace Estates",
            "rating": 5.0,
            "experience": "35+ years",
            "specialization": "Royal Heritage Properties",
            "certification": "Heritage Property Conservation Expert"
        },
        "featured": True,
        "created_at": datetime.now(),
        "views": 6890,
        "status": "available",
        "premium_features": {
            "vr_tour": True,
            "drone_photography": True,
            "professional_video": True,
            "floor_plans": True,
            "3d_walkthrough": True,
            "virtual_staging": True,
            "aerial_views": True,
            "neighborhood_insights": True,
            "market_analysis": True,
            "investment_calculator": True,
            "mortgage_calculator": True,
            "social_media_promotion": True,
            "premium_placement": True,
            "featured_listing": True,
            "priority_support": True
        },
        "exclusive_features": {
            "private_showing": True,
            "helicopter_tour": True,
            "personal_butler": True,
            "interior_designer_consultation": True,
            "legal_assistance": True,
            "property_management": True,
            "concierge_services": True,
            "vip_access": True,
            "exclusive_events": True,
            "lifestyle_consultation": True
        },
        "luxury_amenities": [
            "Royal Architecture", "Authentic Palace Interiors", "Historical Artifacts",
            "Royal Gardens", "Palace Courtyards", "Heritage Conservation",
            "Traditional Rajasthani Decor", "Royal Furniture", "Palace Security"
        ],
        "concierge_services": [
            "Palace Management", "Heritage Guides", "Cultural Events",
            "Royal Dining Service", "Traditional Entertainment", "Palace Tours",
            "Security Services", "Maintenance Team", "Guest Services"
        ],
        "investment_details": {
            "appreciation_rate": "18% per annum",
            "rental_yield": "7% per annum",
            "investment_grade": "AAA+",
            "guaranteed_returns": True,
            "buyback_guarantee": True,
            "tax_benefits": True,
            "capital_gains_exemption": True,
            "property_insurance": "Heritage Property Coverage"
        }
    },
    {
        "id": 5,
        "title": "Tech Billionaire's Smart Mansion",
        "description": "Ultra-modern smart mansion with AI integration, robotics, and futuristic technology. Perfect for tech enthusiasts seeking the ultimate smart home experience.",
        "price": 40000000.0,  # ₹40 Cr
        "location": "Whitefield, Bangalore",
        "property_type": "Smart Mansion",
        "bedrooms": 10,
        "bathrooms": 12,
        "area": 20000.0,
        "amenities": [
            "AI Integration", "Smart Home Automation", "Robotic Services", "Tech Lab",
            "Home Theater", "Gaming Center", "Fitness Center", "Pool Area",
            "Smart Kitchen", "Home Office", "Conference Room", "Server Room"
        ],
        "images": [
            "https://example.com/premium5-1.jpg",
            "https://example.com/premium5-2.jpg",
            "https://example.com/premium5-3.jpg"
        ],
        "agent": {
            "name": "Dr. Vikram Tech",
            "phone": "+91 95432 10876",
            "email": "vikram@smartluxury.com",
            "company": "Smart Luxury Homes",
            "rating": 4.8,
            "experience": "15+ years",
            "specialization": "Smart Technology Homes",
            "certification": "Smart Home Technology Expert"
        },
        "featured": True,
        "created_at": datetime.now(),
        "views": 5540,
        "status": "available",
        "premium_features": {
            "vr_tour": True,
            "drone_photography": True,
            "professional_video": True,
            "floor_plans": True,
            "3d_walkthrough": True,
            "virtual_staging": True,
            "aerial_views": True,
            "neighborhood_insights": True,
            "market_analysis": True,
            "investment_calculator": True,
            "mortgage_calculator": True,
            "social_media_promotion": True,
            "premium_placement": True,
            "featured_listing": True,
            "priority_support": True
        },
        "exclusive_features": {
            "private_showing": True,
            "helicopter_tour": True,
            "personal_butler": True,
            "interior_designer_consultation": True,
            "legal_assistance": True,
            "property_management": True,
            "concierge_services": True,
            "vip_access": True,
            "exclusive_events": True,
            "lifestyle_consultation": True
        },
        "luxury_amenities": [
            "AI-Powered Home System", "Voice Control", "Automated Climate",
            "Smart Security", "Robotic Cleaning", "Smart Lighting",
            "Tech Integration", "High-Speed Connectivity", "Smart Appliances"
        ],
        "concierge_services": [
            "Tech Support Team", "AI Maintenance", "Home Automation",
            "Security Monitoring", "Smart Device Management", "Tech Upgrades",
            "Digital Assistance", "Remote Support", "Innovation Updates"
        ],
        "investment_details": {
            "appreciation_rate": "16% per annum",
            "rental_yield": "8% per annum",
            "investment_grade": "AAA",
            "guaranteed_returns": True,
            "buyback_guarantee": False,
            "tax_benefits": True,
            "capital_gains_exemption": False,
            "property_insurance": "Technology Coverage"
        }
    },
    {
        "id": 6,
        "title": "Himalayan Retreat Castle",
        "description": "Majestic castle nestled in the Himalayas with panoramic mountain views, private ski slopes, and luxury mountain resort amenities.",
        "price": 60000000.0,  # ₹60 Cr
        "location": "Manali, Himachal Pradesh",
        "property_type": "Mountain Castle",
        "bedrooms": 18,
        "bathrooms": 22,
        "area": 30000.0,
        "amenities": [
            "Mountain Views", "Private Ski Slopes", "Castle Architecture", "Great Hall",
            "Tower Suites", "Castle Grounds", "Wine Cellar", "Library Tower",
            "Mountain Spa", "Heated Pools", "Helipad", "Adventure Center"
        ],
        "images": [
            "https://example.com/premium6-1.jpg",
            "https://example.com/premium6-2.jpg",
            "https://example.com/premium6-3.jpg"
        ],
        "agent": {
            "name": "Himalaya Singh",
            "phone": "+91 94321 08765",
            "email": "himalaya@mountaincastles.com",
            "company": "Mountain Castle Estates",
            "rating": 5.0,
            "experience": "28+ years",
            "specialization": "Mountain & Adventure Properties",
            "certification": "Mountain Property Expert"
        },
        "featured": True,
        "created_at": datetime.now(),
        "views": 7320,
        "status": "available",
        "premium_features": {
            "vr_tour": True,
            "drone_photography": True,
            "professional_video": True,
            "floor_plans": True,
            "3d_walkthrough": True,
            "virtual_staging": True,
            "aerial_views": True,
            "neighborhood_insights": True,
            "market_analysis": True,
            "investment_calculator": True,
            "mortgage_calculator": True,
            "social_media_promotion": True,
            "premium_placement": True,
            "featured_listing": True,
            "priority_support": True
        },
        "exclusive_features": {
            "private_showing": True,
            "helicopter_tour": True,
            "personal_butler": True,
            "interior_designer_consultation": True,
            "legal_assistance": True,
            "property_management": True,
            "concierge_services": True,
            "vip_access": True,
            "exclusive_events": True,
            "lifestyle_consultation": True
        },
        "luxury_amenities": [
            "Panoramic Mountain Views", "Castle Architecture", "Stone Fireplaces",
            "Medieval Decor", "Mountain Air", "Ski-in Ski-out Access",
            "Adventure Sports", "Hiking Trails", "Mountain Dining"
        ],
        "concierge_services": [
            "Castle Management", "Adventure Guides", "Ski Instructors",
            "Mountain Safety", "Outdoor Activities", "Weather Monitoring",
            "Equipment Rental", "Transportation", "Emergency Services"
        ],
        "investment_details": {
            "appreciation_rate": "14% per annum",
            "rental_yield": "9% per annum",
            "investment_grade": "AAA+",
            "guaranteed_returns": True,
            "buyback_guarantee": True,
            "tax_benefits": True,
            "capital_gains_exemption": True,
            "property_insurance": "Mountain Property Coverage"
        }
    }
]

@router.get("/", response_model=List[PremiumProperty])
async def get_premium_listings(
    limit: Optional[int] = Query(10, description="Number of properties to return"),
    offset: Optional[int] = Query(0, description="Number of properties to skip"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    location: Optional[str] = Query(None, description="Location filter"),
    property_type: Optional[str] = Query(None, description="Property type filter"),
    bedrooms: Optional[int] = Query(None, description="Minimum bedrooms filter"),
    featured_only: Optional[bool] = Query(False, description="Show only featured properties")
):
    """Get premium property listings with advanced filtering"""
    
    filtered_properties = premium_properties.copy()
    
    # Apply filters
    if min_price is not None:
        filtered_properties = [p for p in filtered_properties if p["price"] >= min_price]
    
    if max_price is not None:
        filtered_properties = [p for p in filtered_properties if p["price"] <= max_price]
    
    if location:
        filtered_properties = [p for p in filtered_properties if location.lower() in p["location"].lower()]
    
    if property_type:
        filtered_properties = [p for p in filtered_properties if property_type.lower() in p["property_type"].lower()]
    
    if bedrooms is not None:
        filtered_properties = [p for p in filtered_properties if p["bedrooms"] >= bedrooms]
    
    if featured_only:
        filtered_properties = [p for p in filtered_properties if p["featured"]]
    
    # Apply pagination
    total_properties = len(filtered_properties)
    paginated_properties = filtered_properties[offset:offset + limit]
    
    return paginated_properties

@router.get("/dashboard", response_model=PremiumStats)
async def get_premium_dashboard():
    """Get premium listings dashboard with comprehensive statistics"""
    
    total_properties = len(premium_properties)
    total_views = sum(prop["views"] for prop in premium_properties)
    average_price = sum(prop["price"] for prop in premium_properties) / total_properties if total_properties > 0 else 0
    
    # Find most viewed property
    most_viewed = max(premium_properties, key=lambda x: x["views"]) if premium_properties else None
    most_viewed_property = {
        "id": most_viewed["id"] if most_viewed else 0,
        "title": most_viewed["title"] if most_viewed else "",
        "views": most_viewed["views"] if most_viewed else 0,
        "price": most_viewed["price"] if most_viewed else 0
    }
    
    # Count luxury properties (>30 Cr)
    luxury_properties_count = len([p for p in premium_properties if p["price"] > 30000000])
    
    # Count exclusive deals (properties with exclusive features)
    exclusive_deals_count = len([p for p in premium_properties if p.get("exclusive_features", {}).get("private_showing", False)])
    
    # Count investment grade properties
    investment_grade_count = len([p for p in premium_properties if p.get("investment_details", {}).get("investment_grade", "").startswith("AAA")])
    
    return PremiumStats(
        total_properties=total_properties,
        total_views=total_views,
        average_price=average_price,
        most_viewed_property=most_viewed_property,
        luxury_properties_count=luxury_properties_count,
        exclusive_deals_count=exclusive_deals_count,
        investment_grade_count=investment_grade_count
    )

@router.get("/analytics")
async def get_premium_analytics():
    """Get detailed analytics for premium listings"""
    
    # Price distribution
    price_ranges = {
        "30-40_cr": len([p for p in premium_properties if 30000000 <= p["price"] < 40000000]),
        "40-50_cr": len([p for p in premium_properties if 40000000 <= p["price"] < 50000000]),
        "50-60_cr": len([p for p in premium_properties if 50000000 <= p["price"] < 60000000]),
        "60_cr_plus": len([p for p in premium_properties if p["price"] >= 60000000])
    }
    
    # Property type distribution
    property_types = {}
    for prop in premium_properties:
        prop_type = prop["property_type"]
        property_types[prop_type] = property_types.get(prop_type, 0) + 1
    
    # Location distribution
    locations = {}
    for prop in premium_properties:
        location = prop["location"].split(",")[-1].strip()  # Get city/state
        locations[location] = locations.get(location, 0) + 1
    
    # Investment grade distribution
    investment_grades = {}
    for prop in premium_properties:
        grade = prop.get("investment_details", {}).get("investment_grade", "Not Rated")
        investment_grades[grade] = investment_grades.get(grade, 0) + 1
    
    # Top performing properties
    top_properties = sorted(premium_properties, key=lambda x: x["views"], reverse=True)[:3]
    top_performers = [
        {
            "id": prop["id"],
            "title": prop["title"],
            "views": prop["views"],
            "price": prop["price"],
            "location": prop["location"]
        }
        for prop in top_properties
    ]
    
    return {
        "price_distribution": price_ranges,
        "property_type_distribution": property_types,
        "location_distribution": locations,
        "investment_grade_distribution": investment_grades,
        "top_performing_properties": top_performers,
        "total_portfolio_value": sum(prop["price"] for prop in premium_properties),
        "average_views_per_property": sum(prop["views"] for prop in premium_properties) / len(premium_properties),
        "featured_properties_percentage": (len([p for p in premium_properties if p["featured"]]) / len(premium_properties)) * 100
    }

@router.get("/featured")
async def get_featured_premium():
    """Get featured premium properties"""
    featured_properties = [prop for prop in premium_properties if prop["featured"]]
    return {
        "count": len(featured_properties),
        "properties": featured_properties
    }

@router.get("/luxury")
async def get_luxury_premium():
    """Get ultra-luxury premium properties (>₹50 Cr)"""
    luxury_properties = [prop for prop in premium_properties if prop["price"] > 50000000]
    return {
        "count": len(luxury_properties),
        "properties": luxury_properties,
        "average_price": sum(prop["price"] for prop in luxury_properties) / len(luxury_properties) if luxury_properties else 0
    }

@router.get("/investment-grade")
async def get_investment_grade_premium():
    """Get investment-grade premium properties"""
    investment_properties = [
        prop for prop in premium_properties 
        if prop.get("investment_details", {}).get("investment_grade", "").startswith("AAA")
    ]
    return {
        "count": len(investment_properties),
        "properties": investment_properties,
        "total_investment_value": sum(prop["price"] for prop in investment_properties)
    }

@router.get("/exclusive-features")
async def get_exclusive_features():
    """Get properties with exclusive features"""
    exclusive_properties = [
        prop for prop in premium_properties 
        if prop.get("exclusive_features", {}).get("private_showing", False)
    ]
    return {
        "count": len(exclusive_properties),
        "properties": exclusive_properties,
        "available_exclusive_services": [
            "Private Helicopter Tours",
            "Personal Butler Service",
            "Interior Designer Consultation",
            "Legal Assistance",
            "Property Management",
            "Concierge Services",
            "VIP Access",
            "Exclusive Events",
            "Lifestyle Consultation"
        ]
    }

@router.get("/search")
async def search_premium_properties(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, description="Number of results to return")
):
    """Search premium properties by title, description, location, or amenities"""
    
    search_query = q.lower()
    matching_properties = []
    
    for prop in premium_properties:
        # Search in title, description, location, amenities
        searchable_text = f"{prop['title']} {prop['description']} {prop['location']} {' '.join(prop['amenities'])}".lower()
        
        if search_query in searchable_text:
            matching_properties.append(prop)
    
    return {
        "query": q,
        "count": len(matching_properties),
        "properties": matching_properties[:limit]
    }

@router.get("/{property_id}", response_model=PremiumProperty)
async def get_premium_property(property_id: int):
    """Get specific premium property by ID"""
    
    property_data = next((prop for prop in premium_properties if prop["id"] == property_id), None)
    
    if not property_data:
        raise HTTPException(status_code=404, detail="Premium property not found")
    
    # Increment view count
    property_data["views"] += 1
    
    return property_data

@router.get("/agent/{agent_name}")
async def get_properties_by_agent(agent_name: str):
    """Get premium properties by agent name"""
    
    agent_properties = [
        prop for prop in premium_properties 
        if agent_name.lower() in prop["agent"]["name"].lower()
    ]
    
    if not agent_properties:
        raise HTTPException(status_code=404, detail="No properties found for this agent")
    
    return {
        "agent_name": agent_name,
        "properties_count": len(agent_properties),
        "properties": agent_properties,
        "total_portfolio_value": sum(prop["price"] for prop in agent_properties)
    }

@router.get("/location/{city}")
async def get_properties_by_city(city: str):
    """Get premium properties by city"""
    
    city_properties = [
        prop for prop in premium_properties 
        if city.lower() in prop["location"].lower()
    ]
    
    if not city_properties:
        raise HTTPException(status_code=404, detail="No premium properties found in this city")
    
    return {
        "city": city,
        "properties_count": len(city_properties),
        "properties": city_properties,
        "average_price": sum(prop["price"] for prop in city_properties) / len(city_properties)
    }