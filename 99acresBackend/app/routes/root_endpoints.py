from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.routes.loans import EXPERT_CONSULTATIONS, ExpertConsultation
from app.routes.properties_simple import SAMPLE_PROPERTIES, PropertySearchRequest
from datetime import datetime

router = APIRouter()

# Re-export the models for direct access
class RootExpertConsultation(BaseModel):
    savings: float
    emi: float
    loan_tenure: int
    loan_amount: float
    total_budget: float
    name: Optional[str] = "Guest User"
    phone: Optional[str] = None
    email: Optional[str] = None
    preferred_time: Optional[str] = "Any time"
    message: Optional[str] = None

class RootPropertySearch(BaseModel):
    savings: float
    emi: float
    loan_tenure: int
    loan_amount: float
    total_budget: float
    property_type: Optional[str] = None
    location: Optional[str] = None
    bedrooms: Optional[int] = None

@router.post("/talk-to-expert")
@router.post("/talk-to-expert/")
async def talk_to_expert_root(consultation_data: RootExpertConsultation):
    """Submit request to talk to a loan expert (Root level endpoint)"""
    try:
        # Generate new consultation ID
        consultation_id = len(EXPERT_CONSULTATIONS) + 1
        
        # Calculate loan-to-value ratio
        ltv_ratio = (consultation_data.loan_amount / consultation_data.total_budget) * 100
        
        # Determine priority based on loan amount
        if consultation_data.loan_amount > 5000000:  # 50L+
            priority = "High"
            response_time = "Within 2 hours"
        elif consultation_data.loan_amount > 2000000:  # 20L+
            priority = "Medium"
            response_time = "Within 4 hours"
        else:
            priority = "Standard"
            response_time = "Within 24 hours"
        
        # Create consultation record
        consultation_record = {
            "id": consultation_id,
            "name": consultation_data.name,
            "phone": consultation_data.phone,
            "email": consultation_data.email,
            "financial_details": {
                "savings": consultation_data.savings,
                "emi_capacity": consultation_data.emi,
                "loan_tenure": consultation_data.loan_tenure,
                "loan_amount": consultation_data.loan_amount,
                "total_budget": consultation_data.total_budget,
                "ltv_ratio": round(ltv_ratio, 2)
            },
            "preferred_time": consultation_data.preferred_time,
            "message": consultation_data.message,
            "priority": priority,
            "status": "Pending",
            "submitted_at": datetime.now(),
            "assigned_expert": None,
            "scheduled_call_time": None
        }
        
        # Add to consultations list
        EXPERT_CONSULTATIONS.append(consultation_record)
        
        # Determine expert recommendation
        if ltv_ratio > 80:
            expert_recommendation = "High LTV - recommend discussing alternative financing options"
        elif consultation_data.emi > consultation_data.savings * 0.5:
            expert_recommendation = "EMI-to-savings ratio is high - need detailed financial planning"
        else:
            expert_recommendation = "Good financial profile - standard loan processing"
        
        return {
            "success": True,
            "message": "Expert consultation request submitted successfully",
            "consultation_id": consultation_id,
            "priority": priority,
            "expected_response_time": response_time,
            "financial_summary": {
                "loan_amount": consultation_data.loan_amount,
                "down_payment": consultation_data.savings,
                "total_budget": consultation_data.total_budget,
                "ltv_ratio": f"{round(ltv_ratio, 1)}%",
                "monthly_emi": consultation_data.emi,
                "loan_tenure": f"{consultation_data.loan_tenure} years"
            },
            "next_steps": [
                "Expert will review your financial profile",
                "Call will be scheduled within response time",
                "Detailed loan options will be discussed",
                "Personalized recommendations will be provided"
            ],
            "expert_recommendation": expert_recommendation,
            "contact_info": {
                "helpline": "+91-1800-EXPERT-99",
                "email": "experts@99acres.com",
                "whatsapp": "+91-98765-EXPERT"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing expert consultation request: {str(e)}")

@router.post("/find-properties")
@router.post("/find-properties/")
async def find_properties_root(search_request: RootPropertySearch):
    """Find properties based on budget and loan criteria (Root level endpoint)"""
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