from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from enum import Enum
import math

router = APIRouter()

# Loan Models
class LoanType(str, Enum):
    home_loan = "home_loan"
    property_loan = "property_loan"
    construction_loan = "construction_loan"
    land_purchase_loan = "land_purchase_loan"
    home_improvement_loan = "home_improvement_loan"
    balance_transfer = "balance_transfer"

class LoanStatus(str, Enum):
    pending = "pending"
    under_review = "under_review"
    approved = "approved"
    rejected = "rejected"
    disbursed = "disbursed"
    closed = "closed"

class EmploymentType(str, Enum):
    salaried = "salaried"
    self_employed = "self_employed"
    business = "business"
    professional = "professional"

class LoanApplication(BaseModel):
    id: int
    applicant_name: str
    email: EmailStr
    phone: str
    loan_type: LoanType
    property_value: float
    loan_amount: float
    tenure_years: int
    interest_rate: float
    emi: float
    total_payable: float
    employment_type: EmploymentType
    monthly_income: float
    existing_emi: float
    credit_score: Optional[int] = None
    property_address: str
    co_applicant_name: Optional[str] = None
    co_applicant_income: Optional[float] = None
    status: LoanStatus
    applied_date: datetime
    approval_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    processing_fee: float
    documentation: List[str]
    bank_name: str
    loan_officer: Optional[str] = None
    remarks: Optional[str] = None

class LoanRequest(BaseModel):
    applicant_name: Optional[str] = "Guest User"
    email: Optional[str] = "guest@example.com"
    phone: Optional[str] = "+91-0000000000"
    loan_type: LoanType = LoanType.home_loan
    property_value: Optional[float] = None
    amount: float  # This matches your request field name
    tenure: int    # This matches your request field name
    interest_rate: float
    emi: float
    total_payable: float
    employment_type: EmploymentType = EmploymentType.salaried
    monthly_income: Optional[float] = 50000
    existing_emi: float = 0.0
    property_address: Optional[str] = "Not specified"
    co_applicant_name: Optional[str] = None
    co_applicant_income: Optional[float] = None

class EMICalculator(BaseModel):
    principal: float
    rate: float
    tenure_years: int

class EligibilityCheck(BaseModel):
    monthly_income: float
    existing_emi: float
    employment_type: EmploymentType
    credit_score: Optional[int] = None
    property_value: float
    loan_amount: float

class LoanComparison(BaseModel):
    amount: float
    tenure: int  # in years
    interest_rate: Optional[float] = None  # Optional, will calculate for all banks if not provided

class SimpleLoanRequest(BaseModel):
    amount: float
    tenure: int
    interest_rate: float
    emi: float
    total_payable: float
    applicant_name: Optional[str] = "Guest User"
    email: Optional[str] = "guest@example.com"
    phone: Optional[str] = "+91-0000000000"
    property_value: Optional[float] = None
    monthly_income: Optional[float] = 50000
    property_address: Optional[str] = "Not specified"

class LoanOption(BaseModel):
    bank_name: str
    loan_type: str
    interest_rate: float
    emi: float
    total_payable: float
    total_interest: float
    processing_fee: float
    processing_fee_percentage: float
    advantages: List[str]
    eligibility_criteria: dict

class ExpertConsultation(BaseModel):
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

# Sample loan applications data
LOAN_APPLICATIONS = [
    {
        "id": 1,
        "applicant_name": "Rajesh Kumar",
        "email": "rajesh.kumar@gmail.com",
        "phone": "+91-9876543210",
        "loan_type": LoanType.home_loan,
        "property_value": 8500000.0,
        "loan_amount": 6800000.0,
        "tenure_years": 20,
        "interest_rate": 8.5,
        "emi": 58736.0,
        "total_payable": 14096640.0,
        "employment_type": EmploymentType.salaried,
        "monthly_income": 125000.0,
        "existing_emi": 15000.0,
        "credit_score": 785,
        "property_address": "Sector 45, Gurgaon, Haryana",
        "co_applicant_name": "Priya Kumar",
        "co_applicant_income": 85000.0,
        "status": LoanStatus.approved,
        "applied_date": datetime(2024, 8, 15),
        "approval_date": datetime(2024, 9, 2),
        "disbursement_date": datetime(2024, 9, 15),
        "processing_fee": 68000.0,
        "documentation": ["Income Proof", "Property Papers", "Identity Proof", "Bank Statements"],
        "bank_name": "HDFC Bank",
        "loan_officer": "Amit Sharma",
        "remarks": "Excellent credit profile, quick approval"
    },
    {
        "id": 2,
        "applicant_name": "Neha Agarwal",
        "email": "neha.agarwal@outlook.com",
        "phone": "+91-9876543211",
        "loan_type": LoanType.property_loan,
        "property_value": 12000000.0,
        "loan_amount": 9600000.0,
        "tenure_years": 15,
        "interest_rate": 9.2,
        "emi": 97847.0,
        "total_payable": 17612460.0,
        "employment_type": EmploymentType.self_employed,
        "monthly_income": 250000.0,
        "existing_emi": 0.0,
        "credit_score": 750,
        "property_address": "Koramangala, Bangalore, Karnataka",
        "co_applicant_name": None,
        "co_applicant_income": None,
        "status": LoanStatus.under_review,
        "applied_date": datetime(2024, 9, 20),
        "approval_date": None,
        "disbursement_date": None,
        "processing_fee": 96000.0,
        "documentation": ["Business Proof", "ITR Documents", "Property Valuation", "Bank Statements"],
        "bank_name": "ICICI Bank",
        "loan_officer": "Sunita Devi",
        "remarks": "Under technical evaluation"
    },
    {
        "id": 3,
        "applicant_name": "Vikram Malhotra",
        "email": "vikram.malhotra@company.com",
        "phone": "+91-9876543212",
        "loan_type": LoanType.construction_loan,
        "property_value": 15000000.0,
        "loan_amount": 10500000.0,
        "tenure_years": 25,
        "interest_rate": 8.8,
        "emi": 85234.0,
        "total_payable": 25570200.0,
        "employment_type": EmploymentType.business,
        "monthly_income": 300000.0,
        "existing_emi": 25000.0,
        "credit_score": 720,
        "property_address": "Sector 50, Noida, Uttar Pradesh",
        "co_applicant_name": "Kavita Malhotra",
        "co_applicant_income": 150000.0,
        "status": LoanStatus.pending,
        "applied_date": datetime(2024, 10, 1),
        "approval_date": None,
        "disbursement_date": None,
        "processing_fee": 105000.0,
        "documentation": ["Construction Plan", "Approved Blueprint", "Income Proof", "Land Documents"],
        "bank_name": "SBI",
        "loan_officer": "Rajesh Gupta",
        "remarks": "Documentation under verification"
    }
]

# Bank interest rates data
BANK_RATES = [
    {"bank": "HDFC Bank", "home_loan": 8.50, "property_loan": 9.00, "construction_loan": 9.25},
    {"bank": "ICICI Bank", "home_loan": 8.65, "property_loan": 9.15, "construction_loan": 9.40},
    {"bank": "SBI", "home_loan": 8.40, "property_loan": 8.90, "construction_loan": 9.10},
    {"bank": "Axis Bank", "home_loan": 8.75, "property_loan": 9.25, "construction_loan": 9.50},
    {"bank": "Kotak Bank", "home_loan": 8.55, "property_loan": 9.05, "construction_loan": 9.30},
    {"bank": "PNB", "home_loan": 8.30, "property_loan": 8.80, "construction_loan": 9.00}
]

# Expert consultation requests storage
EXPERT_CONSULTATIONS = []

def calculate_emi(principal: float, annual_rate: float, tenure_years: int) -> dict:
    """Calculate EMI and other loan details"""
    monthly_rate = (annual_rate / 100) / 12
    tenure_months = tenure_years * 12
    
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * (monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    
    total_payable = emi * tenure_months
    total_interest = total_payable - principal
    
    return {
        "emi": round(emi, 2),
        "total_payable": round(total_payable, 2),
        "total_interest": round(total_interest, 2),
        "principal": principal,
        "tenure_months": tenure_months,
        "interest_rate": annual_rate
    }

def check_eligibility(income: float, existing_emi: float, employment_type: str, credit_score: int = None) -> dict:
    """Check loan eligibility based on income and other factors"""
    # Calculate available income for EMI (50% rule)
    available_income = income * 0.5 - existing_emi
    
    # Base eligibility multiplier
    if employment_type == "salaried":
        multiplier = 60  # 60x monthly income
    elif employment_type == "self_employed":
        multiplier = 55  # 55x monthly income
    else:
        multiplier = 50  # 50x monthly income
    
    # Credit score bonus
    if credit_score:
        if credit_score >= 750:
            multiplier += 10
        elif credit_score >= 700:
            multiplier += 5
        elif credit_score < 650:
            multiplier -= 10
    
    max_loan_amount = available_income * multiplier
    
    return {
        "eligible": available_income > 0 and max_loan_amount > 500000,
        "max_loan_amount": round(max_loan_amount, 2),
        "max_emi": round(available_income, 2),
        "available_income": round(available_income, 2),
        "employment_factor": multiplier,
        "credit_score_impact": credit_score
    }

@router.post("", response_model=dict)
@router.post("/", response_model=dict)
async def apply_loan(loan_request: LoanRequest):
    """Submit a new loan application"""
    try:
        # Generate new application ID
        new_id = max([app["id"] for app in LOAN_APPLICATIONS]) + 1 if LOAN_APPLICATIONS else 1
        
        # Calculate processing fee (1% of loan amount)
        processing_fee = loan_request.amount * 0.01
        
        # Set default property value if not provided
        property_value = loan_request.property_value or (loan_request.amount * 1.33)  # Assume 75% LTV
        
        # Determine initial status based on loan amount
        if loan_request.amount > 10000000:  # 1 Cr+
            status = LoanStatus.under_review
        else:
            status = LoanStatus.pending
        
        # Create loan application
        new_application = {
            "id": new_id,
            "applicant_name": loan_request.applicant_name,
            "email": loan_request.email,
            "phone": loan_request.phone,
            "loan_type": loan_request.loan_type,
            "property_value": property_value,
            "loan_amount": loan_request.amount,
            "tenure_years": loan_request.tenure,
            "interest_rate": loan_request.interest_rate,
            "emi": loan_request.emi,
            "total_payable": loan_request.total_payable,
            "employment_type": loan_request.employment_type,
            "monthly_income": loan_request.monthly_income,
            "existing_emi": loan_request.existing_emi,
            "credit_score": None,
            "property_address": loan_request.property_address,
            "co_applicant_name": loan_request.co_applicant_name,
            "co_applicant_income": loan_request.co_applicant_income,
            "status": status,
            "applied_date": datetime.now(),
            "approval_date": None,
            "disbursement_date": None,
            "processing_fee": processing_fee,
            "documentation": ["Application Form", "Income Proof Required", "Property Documents Required"],
            "bank_name": "To be assigned",
            "loan_officer": None,
            "remarks": "Application submitted successfully"
        }
        
        # Add to applications list
        LOAN_APPLICATIONS.append(new_application)
        
        return {
            "success": True,
            "message": "Loan application submitted successfully",
            "application_id": new_id,
            "status": status,
            "processing_fee": processing_fee,
            "next_steps": [
                "Upload required documents",
                "Credit score verification",
                "Property valuation",
                "Bank processing"
            ],
            "estimated_processing_time": "7-14 business days",
            "contact_info": {
                "helpline": "+91-1800-123-LOAN",
                "email": "loans@99acres.com"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing loan application: {str(e)}")

@router.get("/applications", response_model=List[dict])
async def get_loan_applications(
    status: Optional[LoanStatus] = Query(None, description="Filter by application status"),
    loan_type: Optional[LoanType] = Query(None, description="Filter by loan type"),
    limit: int = Query(10, ge=1, le=100, description="Number of applications to return")
):
    """Get loan applications with optional filtering"""
    applications = LOAN_APPLICATIONS.copy()
    
    if status:
        applications = [app for app in applications if app["status"] == status]
    
    if loan_type:
        applications = [app for app in applications if app["loan_type"] == loan_type]
    
    # Convert to response format
    response_data = []
    for app in applications[:limit]:
        response_data.append({
            "id": app["id"],
            "applicant_name": app["applicant_name"],
            "email": app["email"],
            "phone": app["phone"],
            "loan_type": app["loan_type"],
            "loan_amount": app["loan_amount"],
            "emi": app["emi"],
            "tenure_years": app["tenure_years"],
            "interest_rate": app["interest_rate"],
            "status": app["status"],
            "applied_date": app["applied_date"],
            "bank_name": app["bank_name"],
            "loan_officer": app["loan_officer"]
        })
    
    return response_data

@router.get("/applications/{application_id}", response_model=dict)
async def get_loan_application(application_id: int):
    """Get specific loan application details"""
    application = next((app for app in LOAN_APPLICATIONS if app["id"] == application_id), None)
    
    if not application:
        raise HTTPException(status_code=404, detail="Loan application not found")
    
    return {
        "success": True,
        "data": application
    }

@router.post("/apply-simple")
@router.post("/apply-simple/")
async def apply_loan_simple(loan_data: SimpleLoanRequest):
    """Submit a simple loan application with minimal data"""
    try:
        # Generate new application ID
        new_id = max([app["id"] for app in LOAN_APPLICATIONS]) + 1 if LOAN_APPLICATIONS else 1
        
        # Set default property value if not provided
        property_value = loan_data.property_value or (loan_data.amount * 1.33)  # Assume 75% LTV
        
        # Create simplified loan application
        new_application = {
            "id": new_id,
            "applicant_name": loan_data.applicant_name,
            "email": loan_data.email,
            "phone": loan_data.phone,
            "loan_type": LoanType.home_loan,
            "property_value": property_value,
            "loan_amount": loan_data.amount,
            "tenure_years": loan_data.tenure,
            "interest_rate": loan_data.interest_rate,
            "emi": loan_data.emi,
            "total_payable": loan_data.total_payable,
            "employment_type": EmploymentType.salaried,
            "monthly_income": loan_data.monthly_income,
            "existing_emi": 0.0,
            "credit_score": None,
            "property_address": loan_data.property_address,
            "co_applicant_name": None,
            "co_applicant_income": None,
            "status": LoanStatus.pending,
            "applied_date": datetime.now(),
            "approval_date": None,
            "disbursement_date": None,
            "processing_fee": loan_data.amount * 0.005,  # 0.5% processing fee
            "documentation": ["Basic documents pending"],
            "bank_name": "To be assigned",
            "loan_officer": None,
            "remarks": "Quick application submitted"
        }
        
        # Add to applications list
        LOAN_APPLICATIONS.append(new_application)
        
        return {
            "success": True,
            "message": "Loan application submitted successfully",
            "application_id": new_id,
            "status": "pending",
            "loan_details": {
                "amount": loan_data.amount,
                "tenure": loan_data.tenure,
                "emi": loan_data.emi,
                "total_payable": loan_data.total_payable,
                "interest_rate": loan_data.interest_rate
            },
            "next_steps": [
                "Document verification pending",
                "Complete profile details",
                "Credit assessment",
                "Final approval"
            ],
            "estimated_processing_time": "3-7 business days",
            "contact_info": {
                "helpline": "+91-1800-123-LOAN",
                "email": "loans@99acres.com"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing simple loan application: {str(e)}")

@router.post("/calculate-emi", response_model=dict)
async def calculate_loan_emi(emi_data: EMICalculator):
    """Calculate EMI for given loan parameters"""
    calculation = calculate_emi(emi_data.principal, emi_data.rate, emi_data.tenure_years)
    
    return {
        "success": True,
        "calculation": calculation,
        "amortization_summary": {
            "monthly_emi": calculation["emi"],
            "total_amount": calculation["total_payable"],
            "total_interest": calculation["total_interest"],
            "principal_amount": calculation["principal"],
            "interest_rate": calculation["interest_rate"],
            "tenure": f"{emi_data.tenure_years} years ({calculation['tenure_months']} months)"
        }
    }

@router.post("/check-eligibility", response_model=dict)
async def check_loan_eligibility(eligibility_data: EligibilityCheck):
    """Check loan eligibility based on income and other factors"""
    eligibility = check_eligibility(
        eligibility_data.monthly_income,
        eligibility_data.existing_emi,
        eligibility_data.employment_type,
        eligibility_data.credit_score
    )
    
    # Calculate LTV ratio
    ltv_ratio = (eligibility_data.loan_amount / eligibility_data.property_value) * 100
    max_ltv = 80.0  # Maximum 80% LTV
    
    return {
        "success": True,
        "eligibility": eligibility,
        "ltv_analysis": {
            "requested_ltv": round(ltv_ratio, 2),
            "max_allowed_ltv": max_ltv,
            "ltv_compliant": ltv_ratio <= max_ltv,
            "max_loan_on_property": round(eligibility_data.property_value * 0.8, 2)
        },
        "recommendation": {
            "eligible": eligibility["eligible"] and ltv_ratio <= max_ltv,
            "recommended_loan_amount": min(eligibility["max_loan_amount"], eligibility_data.property_value * 0.8),
            "recommended_emi": min(eligibility["max_emi"], eligibility["max_emi"]),
            "suggestions": [
                "Maintain good credit score for better rates",
                "Consider co-applicant to increase eligibility",
                "Reduce existing EMIs if possible"
            ]
        }
    }

@router.get("/bank-rates", response_model=dict)
async def get_bank_interest_rates():
    """Get current interest rates from different banks"""
    return {
        "success": True,
        "message": "Current bank interest rates",
        "rates": BANK_RATES,
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "note": "Rates are indicative and subject to change. Final rates depend on credit profile."
    }

@router.post("/compare")
@router.post("/compare/")
async def compare_loan_options(comparison_data: LoanComparison):
    """Compare loan options across different banks"""
    try:
        loan_options = []
        
        # Use the provided interest rate or default to home loan rates
        loan_type = "home_loan"  # Default to home loan
        
        for bank_data in BANK_RATES:
            bank_name = bank_data["bank"]
            
            # Use provided interest rate or bank's rate for the loan type
            interest_rate = comparison_data.interest_rate if comparison_data.interest_rate else bank_data[loan_type]
            
            # EMI Calculation
            monthly_rate = interest_rate / (12 * 100)
            tenure_months = comparison_data.tenure * 12
            
            if monthly_rate > 0:
                emi = (comparison_data.amount * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
            else:
                emi = comparison_data.amount / tenure_months
            
            # Total calculations
            total_payment = emi * tenure_months
            total_interest = total_payment - comparison_data.amount
            
            # Processing fee calculation (standard 0.5% with max 50,000)
            processing_fee = min(0.005 * comparison_data.amount, 50000)
            
            # Create loan option
            loan_option = LoanOption(
                bank_name=bank_name,
                loan_type="Home Loan",
                interest_rate=interest_rate,
                emi=round(emi, 2),
                total_payable=round(total_payment, 2),
                total_interest=round(total_interest, 2),
                processing_fee=round(processing_fee, 2),
                processing_fee_percentage=0.5,
                advantages=["Digital process", "Quick approval", "Competitive rates"],
                eligibility_criteria={
                    "min_income": 50000,
                    "min_credit_score": 650,
                    "max_age": 65,
                    "employment_type": ["Salaried", "Self-employed"]
                }
            )
            
            loan_options.append(loan_option)
        
        # Sort by EMI (lowest first)
        loan_options.sort(key=lambda x: x.emi)
        
        # Find best options
        best_emi = min(loan_options, key=lambda x: x.emi)
        best_total_cost = min(loan_options, key=lambda x: x.total_payable)
        best_processing_fee = min(loan_options, key=lambda x: x.processing_fee)
        
        return {
            "success": True,
            "message": "Loan comparison completed successfully",
            "comparison_summary": {
                "loan_amount": comparison_data.amount,
                "tenure_years": comparison_data.tenure,
                "requested_rate": comparison_data.interest_rate,
                "total_banks_compared": len(loan_options)
            },
            "loan_options": [option.dict() for option in loan_options],
            "recommendations": {
                "best_emi": {
                    "bank": best_emi.bank_name,
                    "emi": best_emi.emi,
                    "savings_vs_highest": round(max(loan_options, key=lambda x: x.emi).emi - best_emi.emi, 2)
                },
                "best_total_cost": {
                    "bank": best_total_cost.bank_name,
                    "total_payment": best_total_cost.total_payable,
                    "savings_vs_highest": round(max(loan_options, key=lambda x: x.total_payable).total_payable - best_total_cost.total_payable, 2)
                },
                "best_processing_fee": {
                    "bank": best_processing_fee.bank_name,
                    "processing_fee": best_processing_fee.processing_fee,
                    "savings_vs_highest": round(max(loan_options, key=lambda x: x.processing_fee).processing_fee - best_processing_fee.processing_fee, 2)
                }
            },
            "market_analysis": {
                "average_emi": round(sum(option.emi for option in loan_options) / len(loan_options), 2),
                "emi_range": {
                    "min": min(option.emi for option in loan_options),
                    "max": max(option.emi for option in loan_options)
                },
                "interest_rate_range": {
                    "min": min(option.interest_rate for option in loan_options),
                    "max": max(option.interest_rate for option in loan_options)
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing loan options: {str(e)}")

@router.get("/analytics", response_model=dict)
async def get_loan_analytics():
    """Get loan application analytics and statistics"""
    total_applications = len(LOAN_APPLICATIONS)
    
    if total_applications == 0:
        return {
            "success": True,
            "analytics": {
                "total_applications": 0,
                "status_distribution": {},
                "loan_type_distribution": {},
                "average_loan_amount": 0,
                "total_loan_amount": 0
            }
        }
    
    # Status distribution
    status_counts = {}
    for app in LOAN_APPLICATIONS:
        status = app["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Loan type distribution
    type_counts = {}
    for app in LOAN_APPLICATIONS:
        loan_type = app["loan_type"]
        type_counts[loan_type] = type_counts.get(loan_type, 0) + 1
    
    # Financial metrics
    total_loan_amount = sum(app["loan_amount"] for app in LOAN_APPLICATIONS)
    average_loan_amount = total_loan_amount / total_applications
    average_tenure = sum(app["tenure_years"] for app in LOAN_APPLICATIONS) / total_applications
    average_interest_rate = sum(app["interest_rate"] for app in LOAN_APPLICATIONS) / total_applications
    
    # Approval rate
    approved_count = status_counts.get(LoanStatus.approved, 0)
    approval_rate = (approved_count / total_applications) * 100
    
    return {
        "success": True,
        "analytics": {
            "total_applications": total_applications,
            "status_distribution": status_counts,
            "loan_type_distribution": type_counts,
            "financial_metrics": {
                "total_loan_amount": round(total_loan_amount, 2),
                "average_loan_amount": round(average_loan_amount, 2),
                "average_tenure_years": round(average_tenure, 1),
                "average_interest_rate": round(average_interest_rate, 2)
            },
            "performance_metrics": {
                "approval_rate": round(approval_rate, 2),
                "pending_applications": status_counts.get(LoanStatus.pending, 0),
                "under_review_applications": status_counts.get(LoanStatus.under_review, 0)
            }
        }
    }

@router.put("/applications/{application_id}/status", response_model=dict)
async def update_application_status(application_id: int, new_status: LoanStatus, remarks: Optional[str] = None):
    """Update loan application status (Admin function)"""
    application = next((app for app in LOAN_APPLICATIONS if app["id"] == application_id), None)
    
    if not application:
        raise HTTPException(status_code=404, detail="Loan application not found")
    
    old_status = application["status"]
    application["status"] = new_status
    
    # Update relevant dates
    if new_status == LoanStatus.approved:
        application["approval_date"] = datetime.now()
    elif new_status == LoanStatus.disbursed:
        application["disbursement_date"] = datetime.now()
    
    if remarks:
        application["remarks"] = remarks
    
    return {
        "success": True,
        "message": f"Application status updated from {old_status} to {new_status}",
        "application_id": application_id,
        "old_status": old_status,
        "new_status": new_status,
        "updated_at": datetime.now().isoformat()
    }

@router.post("/talk-to-expert")
@router.post("/talk-to-expert/")
async def talk_to_expert(consultation_data: ExpertConsultation):
    """Submit request to talk to a loan expert"""
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

@router.get("/consultations", response_model=dict)
async def get_expert_consultations():
    """Get all expert consultation requests (Admin function)"""
    return {
        "success": True,
        "total_consultations": len(EXPERT_CONSULTATIONS),
        "consultations": EXPERT_CONSULTATIONS,
        "summary": {
            "pending": len([c for c in EXPERT_CONSULTATIONS if c["status"] == "Pending"]),
            "high_priority": len([c for c in EXPERT_CONSULTATIONS if c["priority"] == "High"]),
            "average_loan_amount": sum(c["financial_details"]["loan_amount"] for c in EXPERT_CONSULTATIONS) / len(EXPERT_CONSULTATIONS) if EXPERT_CONSULTATIONS else 0
        }
    }