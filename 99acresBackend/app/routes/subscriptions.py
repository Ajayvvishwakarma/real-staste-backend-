from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from enum import Enum

router = APIRouter()

# Subscription Models
class SubscriptionType(str, Enum):
    basic = "basic"
    standard = "standard"
    premium = "premium"
    enterprise = "enterprise"

class SubscriptionStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"
    cancelled = "cancelled"
    pending = "pending"

class BillingCycle(str, Enum):
    monthly = "monthly"
    quarterly = "quarterly"
    yearly = "yearly"

class SubscriptionPlan(BaseModel):
    id: int
    name: str
    type: SubscriptionType
    price: float
    billing_cycle: BillingCycle
    features: List[str]
    property_limit: int
    lead_limit: int
    email_limit: int
    support_level: str
    analytics_access: bool
    api_access: bool
    custom_branding: bool
    priority_listing: bool
    description: str
    is_popular: bool = False
    discount_percentage: Optional[float] = None

class UserSubscription(BaseModel):
    id: int
    user_id: int
    plan_id: int
    plan_name: str
    status: SubscriptionStatus
    start_date: datetime
    end_date: datetime
    auto_renew: bool
    payment_method: str
    total_amount: float
    discount_applied: Optional[float] = None
    properties_used: int
    leads_used: int
    emails_used: int
    created_at: datetime
    last_billing_date: Optional[datetime] = None
    next_billing_date: Optional[datetime] = None

class SubscriptionUsage(BaseModel):
    subscription_id: int
    properties_used: int
    properties_limit: int
    leads_used: int
    leads_limit: int
    emails_used: int
    emails_limit: int
    usage_percentage: float
    last_updated: datetime

# Sample subscription plans data
SUBSCRIPTION_PLANS = [
    SubscriptionPlan(
        id=1,
        name="Basic Starter",
        type=SubscriptionType.basic,
        price=999.0,
        billing_cycle=BillingCycle.monthly,
        features=[
            "Up to 5 property listings",
            "Basic lead management",
            "50 email campaigns per month",
            "Standard support",
            "Basic analytics",
            "Mobile app access"
        ],
        property_limit=5,
        lead_limit=25,
        email_limit=50,
        support_level="Standard",
        analytics_access=True,
        api_access=False,
        custom_branding=False,
        priority_listing=False,
        description="Perfect for individual agents starting their real estate journey",
        is_popular=False
    ),
    SubscriptionPlan(
        id=2,
        name="Professional",
        type=SubscriptionType.standard,
        price=2499.0,
        billing_cycle=BillingCycle.monthly,
        features=[
            "Up to 25 property listings",
            "Advanced lead management",
            "200 email campaigns per month",
            "Priority support",
            "Advanced analytics & reports",
            "API access",
            "Custom email templates",
            "Lead scoring system"
        ],
        property_limit=25,
        lead_limit=100,
        email_limit=200,
        support_level="Priority",
        analytics_access=True,
        api_access=True,
        custom_branding=False,
        priority_listing=True,
        description="Ideal for growing real estate professionals and small teams",
        is_popular=True
    ),
    SubscriptionPlan(
        id=3,
        name="Business Premium",
        type=SubscriptionType.premium,
        price=4999.0,
        billing_cycle=BillingCycle.monthly,
        features=[
            "Up to 100 property listings",
            "Complete CRM suite",
            "500 email campaigns per month",
            "24/7 premium support",
            "Advanced analytics & AI insights",
            "Full API access",
            "Custom branding",
            "Priority listing placement",
            "Multi-user team access",
            "Advanced lead automation"
        ],
        property_limit=100,
        lead_limit=500,
        email_limit=500,
        support_level="Premium 24/7",
        analytics_access=True,
        api_access=True,
        custom_branding=True,
        priority_listing=True,
        description="Comprehensive solution for established real estate businesses",
        is_popular=False
    ),
    SubscriptionPlan(
        id=4,
        name="Enterprise",
        type=SubscriptionType.enterprise,
        price=9999.0,
        billing_cycle=BillingCycle.monthly,
        features=[
            "Unlimited property listings",
            "Enterprise CRM & automation",
            "Unlimited email campaigns",
            "Dedicated account manager",
            "Custom analytics & reporting",
            "White-label API access",
            "Complete custom branding",
            "Featured listing placement",
            "Unlimited team members",
            "Custom integrations",
            "Advanced security features",
            "Training & onboarding"
        ],
        property_limit=999999,
        lead_limit=999999,
        email_limit=999999,
        support_level="Dedicated Manager",
        analytics_access=True,
        api_access=True,
        custom_branding=True,
        priority_listing=True,
        description="Ultimate solution for large real estate enterprises and franchises",
        is_popular=False
    )
]

# Sample user subscriptions data
USER_SUBSCRIPTIONS = [
    UserSubscription(
        id=1,
        user_id=1,
        plan_id=2,
        plan_name="Professional",
        status=SubscriptionStatus.active,
        start_date=datetime(2024, 9, 1),
        end_date=datetime(2024, 12, 1),
        auto_renew=True,
        payment_method="Credit Card",
        total_amount=2499.0,
        discount_applied=None,
        properties_used=18,
        leads_used=75,
        emails_used=156,
        created_at=datetime(2024, 8, 28),
        last_billing_date=datetime(2024, 9, 1),
        next_billing_date=datetime(2024, 12, 1)
    ),
    UserSubscription(
        id=2,
        user_id=2,
        plan_id=3,
        plan_name="Business Premium",
        status=SubscriptionStatus.active,
        start_date=datetime(2024, 8, 15),
        end_date=datetime(2025, 2, 15),
        auto_renew=True,
        payment_method="Bank Transfer",
        total_amount=24995.0,
        discount_applied=2500.0,
        properties_used=67,
        leads_used=298,
        emails_used=387,
        created_at=datetime(2024, 8, 10),
        last_billing_date=datetime(2024, 8, 15),
        next_billing_date=datetime(2025, 2, 15)
    ),
    UserSubscription(
        id=3,
        user_id=3,
        plan_id=1,
        plan_name="Basic Starter",
        status=SubscriptionStatus.expired,
        start_date=datetime(2024, 6, 1),
        end_date=datetime(2024, 9, 1),
        auto_renew=False,
        payment_method="Credit Card",
        total_amount=999.0,
        discount_applied=None,
        properties_used=5,
        leads_used=25,
        emails_used=42,
        created_at=datetime(2024, 5, 28),
        last_billing_date=datetime(2024, 6, 1),
        next_billing_date=None
    ),
    UserSubscription(
        id=4,
        user_id=4,
        plan_id=4,
        plan_name="Enterprise",
        status=SubscriptionStatus.active,
        start_date=datetime(2024, 7, 1),
        end_date=datetime(2025, 7, 1),
        auto_renew=True,
        payment_method="Enterprise Contract",
        total_amount=99990.0,
        discount_applied=19998.0,
        properties_used=435,
        leads_used=1256,
        emails_used=2847,
        created_at=datetime(2024, 6, 15),
        last_billing_date=datetime(2024, 7, 1),
        next_billing_date=datetime(2025, 7, 1)
    ),
    UserSubscription(
        id=5,
        user_id=5,
        plan_id=2,
        plan_name="Professional",
        status=SubscriptionStatus.cancelled,
        start_date=datetime(2024, 5, 1),
        end_date=datetime(2024, 8, 1),
        auto_renew=False,
        payment_method="Credit Card",
        total_amount=2499.0,
        discount_applied=None,
        properties_used=12,
        leads_used=45,
        emails_used=89,
        created_at=datetime(2024, 4, 25),
        last_billing_date=datetime(2024, 5, 1),
        next_billing_date=None
    )
]

@router.get("/plans", response_model=List[SubscriptionPlan])
async def get_subscription_plans(
    type: Optional[SubscriptionType] = Query(None, description="Filter by subscription type"),
    billing_cycle: Optional[BillingCycle] = Query(None, description="Filter by billing cycle"),
    popular_only: Optional[bool] = Query(False, description="Show only popular plans")
):
    """Get all available subscription plans with optional filtering"""
    plans = SUBSCRIPTION_PLANS.copy()
    
    if type:
        plans = [plan for plan in plans if plan.type == type]
    
    if billing_cycle:
        plans = [plan for plan in plans if plan.billing_cycle == billing_cycle]
    
    if popular_only:
        plans = [plan for plan in plans if plan.is_popular]
    
    return plans

@router.get("/plans/compare")
async def compare_subscription_plans():
    """Compare all subscription plans with detailed feature matrix"""
    comparison_matrix = []
    
    for plan in SUBSCRIPTION_PLANS:
        comparison_matrix.append({
            "plan_id": plan.id,
            "name": plan.name,
            "type": plan.type,
            "price": plan.price,
            "billing_cycle": plan.billing_cycle,
            "property_limit": plan.property_limit,
            "lead_limit": plan.lead_limit,
            "email_limit": plan.email_limit,
            "support_level": plan.support_level,
            "analytics_access": plan.analytics_access,
            "api_access": plan.api_access,
            "custom_branding": plan.custom_branding,
            "priority_listing": plan.priority_listing,
            "is_popular": plan.is_popular,
            "features_count": len(plan.features),
            "price_per_property": round(plan.price / plan.property_limit, 2) if plan.property_limit > 0 else 0,
            "price_per_lead": round(plan.price / plan.lead_limit, 2) if plan.lead_limit > 0 else 0
        })
    
    return {
        "plans_comparison": comparison_matrix,
        "comparison_summary": {
            "cheapest_plan": min(SUBSCRIPTION_PLANS, key=lambda x: x.price).name,
            "most_expensive_plan": max(SUBSCRIPTION_PLANS, key=lambda x: x.price).name,
            "best_value_plan": min(SUBSCRIPTION_PLANS, key=lambda x: x.price / max(x.property_limit, 1)).name,
            "most_features_plan": max(SUBSCRIPTION_PLANS, key=lambda x: len(x.features)).name
        }
    }

@router.get("/plans/{plan_id}", response_model=SubscriptionPlan)
async def get_subscription_plan(plan_id: int):
    """Get details of a specific subscription plan"""
    plan = next((plan for plan in SUBSCRIPTION_PLANS if plan.id == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    return plan

@router.get("", response_model=List[UserSubscription])
@router.get("/", response_model=List[UserSubscription])
async def get_user_subscriptions(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    status: Optional[SubscriptionStatus] = Query(None, description="Filter by subscription status"),
    plan_type: Optional[SubscriptionType] = Query(None, description="Filter by plan type")
):
    """Get user subscriptions with optional filtering"""
    subscriptions = USER_SUBSCRIPTIONS.copy()
    
    if user_id:
        subscriptions = [sub for sub in subscriptions if sub.user_id == user_id]
    
    if status:
        subscriptions = [sub for sub in subscriptions if sub.status == status]
    
    if plan_type:
        plan_ids = [plan.id for plan in SUBSCRIPTION_PLANS if plan.type == plan_type]
        subscriptions = [sub for sub in subscriptions if sub.plan_id in plan_ids]
    
    return subscriptions

@router.get("/{subscription_id}", response_model=UserSubscription)
async def get_subscription(subscription_id: int):
    """Get details of a specific subscription"""
    subscription = next((sub for sub in USER_SUBSCRIPTIONS if sub.id == subscription_id), None)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.get("/{subscription_id}/usage", response_model=SubscriptionUsage)
async def get_subscription_usage(subscription_id: int):
    """Get usage statistics for a specific subscription"""
    subscription = next((sub for sub in USER_SUBSCRIPTIONS if sub.id == subscription_id), None)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    plan = next((plan for plan in SUBSCRIPTION_PLANS if plan.id == subscription.plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    
    # Calculate usage percentage based on highest utilization
    property_usage = (subscription.properties_used / plan.property_limit) * 100 if plan.property_limit > 0 else 0
    lead_usage = (subscription.leads_used / plan.lead_limit) * 100 if plan.lead_limit > 0 else 0
    email_usage = (subscription.emails_used / plan.email_limit) * 100 if plan.email_limit > 0 else 0
    
    usage_percentage = max(property_usage, lead_usage, email_usage)
    
    return SubscriptionUsage(
        subscription_id=subscription_id,
        properties_used=subscription.properties_used,
        properties_limit=plan.property_limit,
        leads_used=subscription.leads_used,
        leads_limit=plan.lead_limit,
        emails_used=subscription.emails_used,
        emails_limit=plan.email_limit,
        usage_percentage=round(usage_percentage, 2),
        last_updated=datetime.now()
    )

@router.get("/analytics/overview")
async def get_subscription_analytics():
    """Get comprehensive subscription analytics"""
    total_subscriptions = len(USER_SUBSCRIPTIONS)
    active_subscriptions = len([sub for sub in USER_SUBSCRIPTIONS if sub.status == SubscriptionStatus.active])
    expired_subscriptions = len([sub for sub in USER_SUBSCRIPTIONS if sub.status == SubscriptionStatus.expired])
    cancelled_subscriptions = len([sub for sub in USER_SUBSCRIPTIONS if sub.status == SubscriptionStatus.cancelled])
    
    # Revenue calculations
    total_revenue = sum(sub.total_amount for sub in USER_SUBSCRIPTIONS if sub.status == SubscriptionStatus.active)
    
    # Plan distribution
    plan_distribution = {}
    for subscription in USER_SUBSCRIPTIONS:
        if subscription.status == SubscriptionStatus.active:
            plan_name = subscription.plan_name
            plan_distribution[plan_name] = plan_distribution.get(plan_name, 0) + 1
    
    # Usage statistics
    avg_properties_used = sum(sub.properties_used for sub in USER_SUBSCRIPTIONS) / len(USER_SUBSCRIPTIONS)
    avg_leads_used = sum(sub.leads_used for sub in USER_SUBSCRIPTIONS) / len(USER_SUBSCRIPTIONS)
    avg_emails_used = sum(sub.emails_used for sub in USER_SUBSCRIPTIONS) / len(USER_SUBSCRIPTIONS)
    
    # Renewal rate
    auto_renew_count = len([sub for sub in USER_SUBSCRIPTIONS if sub.auto_renew and sub.status == SubscriptionStatus.active])
    renewal_rate = (auto_renew_count / active_subscriptions * 100) if active_subscriptions > 0 else 0
    
    return {
        "total_subscriptions": total_subscriptions,
        "active_subscriptions": active_subscriptions,
        "expired_subscriptions": expired_subscriptions,
        "cancelled_subscriptions": cancelled_subscriptions,
        "total_active_revenue": total_revenue,
        "plan_distribution": plan_distribution,
        "average_usage": {
            "properties": round(avg_properties_used, 1),
            "leads": round(avg_leads_used, 1),
            "emails": round(avg_emails_used, 1)
        },
        "renewal_rate_percentage": round(renewal_rate, 2),
        "churn_rate_percentage": round((cancelled_subscriptions / total_subscriptions * 100), 2) if total_subscriptions > 0 else 0
    }

@router.get("/user/{user_id}/recommendations")
async def get_subscription_recommendations(user_id: int):
    """Get personalized subscription recommendations for a user"""
    user_subscription = next((sub for sub in USER_SUBSCRIPTIONS if sub.user_id == user_id), None)
    
    if not user_subscription:
        # New user recommendations
        return {
            "user_type": "new_user",
            "recommended_plan": "Professional",
            "reason": "Most popular plan with balanced features for growing businesses",
            "alternative_plans": ["Basic Starter", "Business Premium"],
            "recommendations": [
                "Start with Professional plan for comprehensive features",
                "Upgrade to Business Premium if you need custom branding",
                "Consider Basic Starter if you're just starting out"
            ]
        }
    
    current_plan = next((plan for plan in SUBSCRIPTION_PLANS if plan.id == user_subscription.plan_id), None)
    
    # Calculate usage ratios
    property_usage_ratio = user_subscription.properties_used / current_plan.property_limit if current_plan.property_limit > 0 else 0
    lead_usage_ratio = user_subscription.leads_used / current_plan.lead_limit if current_plan.lead_limit > 0 else 0
    email_usage_ratio = user_subscription.emails_used / current_plan.email_limit if current_plan.email_limit > 0 else 0
    
    max_usage = max(property_usage_ratio, lead_usage_ratio, email_usage_ratio)
    
    recommendations = []
    
    if max_usage > 0.8:  # High usage - recommend upgrade
        higher_plans = [plan for plan in SUBSCRIPTION_PLANS if plan.price > current_plan.price]
        if higher_plans:
            recommended_plan = min(higher_plans, key=lambda x: x.price)
            recommendations.append({
                "type": "upgrade",
                "recommended_plan": recommended_plan.name,
                "reason": f"You're using {round(max_usage * 100)}% of your current plan limits",
                "benefits": ["Avoid overage charges", "More features", "Better support"]
            })
    
    elif max_usage < 0.3:  # Low usage - recommend downgrade
        lower_plans = [plan for plan in SUBSCRIPTION_PLANS if plan.price < current_plan.price]
        if lower_plans:
            recommended_plan = max(lower_plans, key=lambda x: x.price)
            recommendations.append({
                "type": "downgrade",
                "recommended_plan": recommended_plan.name,
                "reason": f"You're only using {round(max_usage * 100)}% of your current plan",
                "benefits": ["Reduce costs", "Right-sized features", "Better value"]
            })
    
    else:  # Good usage - stay current
        recommendations.append({
            "type": "maintain",
            "recommended_plan": current_plan.name,
            "reason": f"Your usage at {round(max_usage * 100)}% is optimal for your current plan",
            "benefits": ["Cost-effective", "Adequate features", "Room for growth"]
        })
    
    return {
        "user_id": user_id,
        "current_plan": current_plan.name,
        "usage_summary": {
            "properties": f"{user_subscription.properties_used}/{current_plan.property_limit}",
            "leads": f"{user_subscription.leads_used}/{current_plan.lead_limit}",
            "emails": f"{user_subscription.emails_used}/{current_plan.email_limit}",
            "max_usage_percentage": round(max_usage * 100, 1)
        },
        "recommendations": recommendations
    }