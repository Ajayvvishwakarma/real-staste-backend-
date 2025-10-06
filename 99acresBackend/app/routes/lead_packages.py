from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

router = APIRouter()

class PackageType(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class PackageStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMING_SOON = "coming_soon"

class LeadPackage(BaseModel):
    id: int
    name: str
    description: str
    package_type: PackageType
    price: float
    currency: str
    billing_cycle: str  # monthly, quarterly, yearly
    features: List[str]
    max_leads: int
    max_properties: int
    max_agents: int
    status: PackageStatus
    popular: bool
    discount_percentage: Optional[float] = None
    original_price: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class PackageStats(BaseModel):
    total_packages: int
    active_packages: int
    popular_packages: int
    total_revenue: float
    most_popular_package: Dict[str, Any]

# Sample lead packages data
lead_packages_data = [
    {
        "id": 1,
        "name": "Starter Package",
        "description": "Perfect for new real estate agents starting their journey",
        "package_type": PackageType.BASIC,
        "price": 2999.0,
        "currency": "INR",
        "billing_cycle": "monthly",
        "features": [
            "Up to 50 leads per month",
            "Basic property listings",
            "Email support",
            "Mobile app access",
            "Lead tracking dashboard",
            "Property search filters",
            "Client contact management"
        ],
        "max_leads": 50,
        "max_properties": 10,
        "max_agents": 1,
        "status": PackageStatus.ACTIVE,
        "popular": False,
        "discount_percentage": None,
        "original_price": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "name": "Professional Package",
        "description": "Ideal for established agents and small real estate teams",
        "package_type": PackageType.STANDARD,
        "price": 5999.0,
        "currency": "INR",
        "billing_cycle": "monthly",
        "features": [
            "Up to 200 leads per month",
            "Advanced property listings",
            "Priority email & phone support",
            "Mobile app access",
            "Advanced lead tracking & analytics",
            "Property comparison tools",
            "Client relationship management",
            "Automated follow-up emails",
            "Lead scoring system",
            "Market insights reports"
        ],
        "max_leads": 200,
        "max_properties": 50,
        "max_agents": 3,
        "status": PackageStatus.ACTIVE,
        "popular": True,
        "discount_percentage": 20.0,
        "original_price": 7499.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 3,
        "name": "Business Package",
        "description": "Comprehensive solution for growing real estate businesses",
        "package_type": PackageType.PREMIUM,
        "price": 12999.0,
        "currency": "INR",
        "billing_cycle": "monthly",
        "features": [
            "Up to 500 leads per month",
            "Premium property listings",
            "24/7 dedicated support",
            "Mobile & web app access",
            "Advanced analytics & reporting",
            "Property valuation tools",
            "Multi-agent team management",
            "Automated marketing campaigns",
            "Lead nurturing workflows",
            "API integrations",
            "Custom branding",
            "Virtual property tours",
            "Social media management"
        ],
        "max_leads": 500,
        "max_properties": 200,
        "max_agents": 10,
        "status": PackageStatus.ACTIVE,
        "popular": True,
        "discount_percentage": 15.0,
        "original_price": 15299.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 4,
        "name": "Enterprise Package",
        "description": "Complete enterprise solution for large real estate organizations",
        "package_type": PackageType.ENTERPRISE,
        "price": 25999.0,
        "currency": "INR",
        "billing_cycle": "monthly",
        "features": [
            "Unlimited leads",
            "Enterprise property listings",
            "Dedicated account manager",
            "All platform access",
            "Enterprise analytics & BI",
            "Custom property tools",
            "Unlimited agent accounts",
            "Advanced automation suite",
            "Custom lead workflows",
            "Full API access",
            "White-label solutions",
            "Enterprise integrations",
            "Custom reporting",
            "Training & onboarding",
            "SLA guarantee"
        ],
        "max_leads": -1,  # Unlimited
        "max_properties": -1,  # Unlimited
        "max_agents": -1,  # Unlimited
        "status": PackageStatus.ACTIVE,
        "popular": False,
        "discount_percentage": None,
        "original_price": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 5,
        "name": "Basic Annual Plan",
        "description": "Cost-effective yearly plan for budget-conscious agents",
        "package_type": PackageType.BASIC,
        "price": 29999.0,
        "currency": "INR",
        "billing_cycle": "yearly",
        "features": [
            "Up to 50 leads per month",
            "Basic property listings",
            "Email support",
            "Mobile app access",
            "Lead tracking dashboard",
            "Property search filters",
            "Client contact management",
            "Annual billing discount",
            "Free setup assistance"
        ],
        "max_leads": 50,
        "max_properties": 10,
        "max_agents": 1,
        "status": PackageStatus.ACTIVE,
        "popular": False,
        "discount_percentage": 17.0,
        "original_price": 35988.0,  # 12 * 2999
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 6,
        "name": "Premium Plus Package",
        "description": "Enhanced premium package with additional features",
        "package_type": PackageType.PREMIUM,
        "price": 18999.0,
        "currency": "INR",
        "billing_cycle": "monthly",
        "features": [
            "Up to 750 leads per month",
            "Premium+ property listings",
            "Priority 24/7 support",
            "All platform access",
            "Advanced AI analytics",
            "Predictive lead scoring",
            "Multi-location management",
            "Advanced automation",
            "Custom integrations",
            "Performance coaching",
            "Market trend analysis",
            "Competitor insights",
            "Lead quality optimization"
        ],
        "max_leads": 750,
        "max_properties": 300,
        "max_agents": 15,
        "status": PackageStatus.COMING_SOON,
        "popular": False,
        "discount_percentage": None,
        "original_price": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

@router.get("/", response_model=List[LeadPackage])
async def get_lead_packages(
    limit: Optional[int] = Query(10, description="Number of packages to return"),
    offset: Optional[int] = Query(0, description="Number of packages to skip"),
    package_type: Optional[PackageType] = Query(None, description="Filter by package type"),
    status: Optional[PackageStatus] = Query(None, description="Filter by status"),
    billing_cycle: Optional[str] = Query(None, description="Filter by billing cycle"),
    popular_only: Optional[bool] = Query(False, description="Show only popular packages"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter")
):
    """Get lead packages with filtering options"""
    
    filtered_packages = lead_packages_data.copy()
    
    # Apply filters
    if package_type:
        filtered_packages = [pkg for pkg in filtered_packages if pkg["package_type"] == package_type]
    
    if status:
        filtered_packages = [pkg for pkg in filtered_packages if pkg["status"] == status]
    
    if billing_cycle:
        filtered_packages = [pkg for pkg in filtered_packages if pkg["billing_cycle"] == billing_cycle]
    
    if popular_only:
        filtered_packages = [pkg for pkg in filtered_packages if pkg["popular"]]
    
    if min_price is not None:
        filtered_packages = [pkg for pkg in filtered_packages if pkg["price"] >= min_price]
    
    if max_price is not None:
        filtered_packages = [pkg for pkg in filtered_packages if pkg["price"] <= max_price]
    
    # Apply pagination
    paginated_packages = filtered_packages[offset:offset + limit]
    
    return paginated_packages

@router.get("/dashboard", response_model=PackageStats)
async def get_packages_dashboard():
    """Get lead packages dashboard statistics"""
    
    total_packages = len(lead_packages_data)
    active_packages = len([pkg for pkg in lead_packages_data if pkg["status"] == PackageStatus.ACTIVE])
    popular_packages = len([pkg for pkg in lead_packages_data if pkg["popular"]])
    
    # Calculate total revenue (mock calculation)
    total_revenue = sum(pkg["price"] for pkg in lead_packages_data if pkg["status"] == PackageStatus.ACTIVE)
    
    # Find most popular package
    popular_pkgs = [pkg for pkg in lead_packages_data if pkg["popular"]]
    most_popular = max(popular_pkgs, key=lambda x: x["price"]) if popular_pkgs else None
    
    most_popular_package = {
        "id": most_popular["id"] if most_popular else 0,
        "name": most_popular["name"] if most_popular else "",
        "price": most_popular["price"] if most_popular else 0,
        "package_type": most_popular["package_type"].value if most_popular else ""
    }
    
    return PackageStats(
        total_packages=total_packages,
        active_packages=active_packages,
        popular_packages=popular_packages,
        total_revenue=total_revenue,
        most_popular_package=most_popular_package
    )

@router.get("/popular")
async def get_popular_packages():
    """Get popular lead packages"""
    
    popular_packages = [pkg for pkg in lead_packages_data if pkg["popular"]]
    
    return {
        "count": len(popular_packages),
        "packages": popular_packages
    }

@router.get("/pricing")
async def get_pricing_comparison():
    """Get pricing comparison for all packages"""
    
    pricing_data = []
    for pkg in lead_packages_data:
        if pkg["status"] == PackageStatus.ACTIVE:
            pricing_info = {
                "id": pkg["id"],
                "name": pkg["name"],
                "package_type": pkg["package_type"].value,
                "price": pkg["price"],
                "original_price": pkg.get("original_price"),
                "discount_percentage": pkg.get("discount_percentage"),
                "billing_cycle": pkg["billing_cycle"],
                "max_leads": pkg["max_leads"],
                "max_properties": pkg["max_properties"],
                "max_agents": pkg["max_agents"],
                "popular": pkg["popular"],
                "key_features": pkg["features"][:5]  # Top 5 features
            }
            pricing_data.append(pricing_info)
    
    return {
        "pricing_plans": pricing_data,
        "currency": "INR",
        "tax_info": "All prices are exclusive of GST (18%)",
        "billing_options": ["monthly", "quarterly", "yearly"],
        "payment_methods": ["Credit Card", "Debit Card", "Net Banking", "UPI", "Wallet"]
    }

@router.get("/features-comparison")
async def get_features_comparison():
    """Get detailed features comparison across packages"""
    
    all_features = set()
    for pkg in lead_packages_data:
        all_features.update(pkg["features"])
    
    comparison_data = []
    for pkg in lead_packages_data:
        if pkg["status"] == PackageStatus.ACTIVE:
            pkg_features = {feature: feature in pkg["features"] for feature in all_features}
            comparison_data.append({
                "id": pkg["id"],
                "name": pkg["name"],
                "package_type": pkg["package_type"].value,
                "price": pkg["price"],
                "features": pkg_features,
                "limits": {
                    "leads": pkg["max_leads"],
                    "properties": pkg["max_properties"],
                    "agents": pkg["max_agents"]
                }
            })
    
    return {
        "packages": comparison_data,
        "all_features": sorted(list(all_features))
    }

@router.get("/analytics")
async def get_packages_analytics():
    """Get analytics for lead packages"""
    
    # Package type distribution
    type_distribution = {}
    for pkg in lead_packages_data:
        pkg_type = pkg["package_type"].value
        type_distribution[pkg_type] = type_distribution.get(pkg_type, 0) + 1
    
    # Status distribution
    status_distribution = {}
    for pkg in lead_packages_data:
        status = pkg["status"].value
        status_distribution[status] = status_distribution.get(status, 0) + 1
    
    # Billing cycle distribution
    billing_distribution = {}
    for pkg in lead_packages_data:
        billing = pkg["billing_cycle"]
        billing_distribution[billing] = billing_distribution.get(billing, 0) + 1
    
    # Price ranges
    active_packages = [pkg for pkg in lead_packages_data if pkg["status"] == PackageStatus.ACTIVE]
    prices = [pkg["price"] for pkg in active_packages]
    
    price_analysis = {
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "average_price": sum(prices) / len(prices) if prices else 0,
        "median_price": sorted(prices)[len(prices)//2] if prices else 0
    }
    
    return {
        "package_type_distribution": type_distribution,
        "status_distribution": status_distribution,
        "billing_cycle_distribution": billing_distribution,
        "price_analysis": price_analysis,
        "total_packages": len(lead_packages_data),
        "revenue_potential": sum(pkg["price"] for pkg in active_packages),
        "popular_packages_ratio": len([pkg for pkg in lead_packages_data if pkg["popular"]]) / len(lead_packages_data) * 100
    }

@router.get("/search")
async def search_packages(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, description="Number of results to return")
):
    """Search packages by name, description, or features"""
    
    search_query = q.lower()
    matching_packages = []
    
    for pkg in lead_packages_data:
        searchable_text = f"{pkg['name']} {pkg['description']} {' '.join(pkg['features'])}".lower()
        
        if search_query in searchable_text:
            matching_packages.append(pkg)
    
    return {
        "query": q,
        "count": len(matching_packages),
        "packages": matching_packages[:limit]
    }

@router.get("/recommendations")
async def get_package_recommendations(
    leads_needed: Optional[int] = Query(None, description="Number of leads needed per month"),
    team_size: Optional[int] = Query(None, description="Team size (number of agents)"),
    budget: Optional[float] = Query(None, description="Monthly budget")
):
    """Get package recommendations based on requirements"""
    
    active_packages = [pkg for pkg in lead_packages_data if pkg["status"] == PackageStatus.ACTIVE]
    recommendations = []
    
    for pkg in active_packages:
        score = 0
        reasons = []
        
        # Check leads requirement
        if leads_needed:
            if pkg["max_leads"] == -1 or pkg["max_leads"] >= leads_needed:
                score += 3
                reasons.append("Meets lead requirements")
            elif pkg["max_leads"] >= leads_needed * 0.8:
                score += 2
                reasons.append("Close to lead requirements")
        
        # Check team size
        if team_size:
            if pkg["max_agents"] == -1 or pkg["max_agents"] >= team_size:
                score += 3
                reasons.append("Supports team size")
            elif pkg["max_agents"] >= team_size * 0.5:
                score += 1
                reasons.append("Partially supports team size")
        
        # Check budget
        if budget:
            if pkg["price"] <= budget:
                score += 3
                reasons.append("Within budget")
            elif pkg["price"] <= budget * 1.2:
                score += 1
                reasons.append("Slightly over budget")
        
        # Bonus for popular packages
        if pkg["popular"]:
            score += 1
            reasons.append("Popular choice")
        
        if score > 0:
            recommendations.append({
                "package": pkg,
                "score": score,
                "match_percentage": min(100, (score / 10) * 100),
                "reasons": reasons
            })
    
    # Sort by score
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "recommendations": recommendations[:3],  # Top 3 recommendations
        "search_criteria": {
            "leads_needed": leads_needed,
            "team_size": team_size,
            "budget": budget
        }
    }

@router.get("/{package_id}", response_model=LeadPackage)
async def get_package(package_id: int):
    """Get specific package by ID"""
    
    package = next((pkg for pkg in lead_packages_data if pkg["id"] == package_id), None)
    
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    return package

@router.get("/type/{package_type}")
async def get_packages_by_type(package_type: PackageType):
    """Get packages by type"""
    
    type_packages = [pkg for pkg in lead_packages_data if pkg["package_type"] == package_type]
    
    return {
        "package_type": package_type.value,
        "count": len(type_packages),
        "packages": type_packages
    }

@router.get("/billing/{billing_cycle}")
async def get_packages_by_billing(billing_cycle: str):
    """Get packages by billing cycle"""
    
    billing_packages = [pkg for pkg in lead_packages_data if pkg["billing_cycle"] == billing_cycle]
    
    return {
        "billing_cycle": billing_cycle,
        "count": len(billing_packages),
        "packages": billing_packages,
        "total_value": sum(pkg["price"] for pkg in billing_packages)
    }