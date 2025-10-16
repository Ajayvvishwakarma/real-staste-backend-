from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from enum import Enum
from app.database.mongodb import mongodb

router = APIRouter()

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    INTERESTED = "interested"
    VIEWING_SCHEDULED = "viewing_scheduled"
    NEGOTIATING = "negotiating"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    FOLLOW_UP = "follow_up"

class LeadSource(str, Enum):
    WEBSITE = "website"
    SOCIAL_MEDIA = "social_media"
    REFERRAL = "referral"
    ADVERTISEMENT = "advertisement"
    COLD_CALL = "cold_call"
    WALK_IN = "walk_in"
    EMAIL_CAMPAIGN = "email_campaign"
    PROPERTY_PORTAL = "property_portal"

class PropertyInterest(str, Enum):
    BUY = "buy"
    SELL = "sell"
    RENT = "rent"
    INVEST = "invest"

class BudgetRange(str, Enum):
    UNDER_50L = "under_50l"
    RANGE_50L_1CR = "50l_1cr"
    RANGE_1CR_3CR = "1cr_3cr"
    RANGE_3CR_5CR = "3cr_5cr"
    RANGE_5CR_10CR = "5cr_10cr"
    ABOVE_10CR = "above_10cr"

class Lead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    status: LeadStatus
    source: LeadSource
    property_interest: PropertyInterest
    budget_range: BudgetRange
    preferred_location: str
    property_type: str
    message: Optional[str] = None
    assigned_agent: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_contacted: Optional[datetime] = None
    next_follow_up: Optional[datetime] = None
    priority: str  # high, medium, low
    tags: List[str]
    notes: List[Dict[str, Any]]
    property_views: List[int]  # Property IDs viewed
    scheduled_viewings: List[Dict[str, Any]]

class LeadStats(BaseModel):
    total_leads: int
    new_leads: int
    qualified_leads: int
    converted_leads: int
    conversion_rate: float
    leads_by_source: Dict[str, int]
    leads_by_status: Dict[str, int]
    average_response_time: str
    top_performing_agents: List[Dict[str, Any]]

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    property_interest: PropertyInterest
    budget_range: BudgetRange
    preferred_location: str
    property_type: str
    message: Optional[str] = None
    source: LeadSource = LeadSource.WEBSITE

# Replace leads_data with MongoDB operations
@router.post("/api/leads/", response_model=dict)
async def create_lead(lead: LeadCreate):
    """Create a new lead"""
    lead_data = lead.dict()
    lead_data["status"] = LeadStatus.NEW
    lead_data["created_at"] = datetime.utcnow()
    lead_data["updated_at"] = datetime.utcnow()
    result = await mongodb.database.leads.insert_one(lead_data)
    return {"message": "Lead created successfully", "id": str(result.inserted_id)}

@router.get("/api/leads", response_model=dict)
async def get_leads(limit: int = 10, status: Optional[LeadStatus] = None, source: Optional[LeadSource] = None):
    """Retrieve leads with optional filters"""
    query = {}
    if status:
        query["status"] = status
    if source:
        query["source"] = source

    leads = await mongodb.database.leads.find(query).to_list(limit)
    total_count = await mongodb.database.leads.count_documents(query)
    return {
        "message": "Leads retrieved successfully",
        "data": leads,
        "count": len(leads),
        "total_available": total_count
    }

@router.get("/dashboard", response_model=LeadStats)
async def get_leads_dashboard():
    """Get comprehensive leads dashboard statistics"""
    
    total_leads = len(leads_data)
    new_leads = len([lead for lead in leads_data if lead["status"] == LeadStatus.NEW])
    qualified_leads = len([lead for lead in leads_data if lead["status"] == LeadStatus.QUALIFIED])
    converted_leads = len([lead for lead in leads_data if lead["status"] == LeadStatus.CLOSED_WON])
    
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    
    # Leads by source
    leads_by_source = {}
    for lead in leads_data:
        source = lead["source"].value
        leads_by_source[source] = leads_by_source.get(source, 0) + 1
    
    # Leads by status
    leads_by_status = {}
    for lead in leads_data:
        status = lead["status"].value
        leads_by_status[status] = leads_by_status.get(status, 0) + 1
    
    # Calculate average response time (mock calculation)
    average_response_time = "2.5 hours"
    
    # Top performing agents
    agent_performance = {}
    for lead in leads_data:
        agent = lead.get("assigned_agent")
        if agent:
            if agent not in agent_performance:
                agent_performance[agent] = {"name": agent, "total_leads": 0, "converted": 0}
            agent_performance[agent]["total_leads"] += 1
            if lead["status"] == LeadStatus.CLOSED_WON:
                agent_performance[agent]["converted"] += 1
    
    # Calculate conversion rates and sort
    for agent_data in agent_performance.values():
        agent_data["conversion_rate"] = (agent_data["converted"] / agent_data["total_leads"] * 100) if agent_data["total_leads"] > 0 else 0
    
    top_performing_agents = sorted(agent_performance.values(), key=lambda x: x["conversion_rate"], reverse=True)[:5]
    
    return LeadStats(
        total_leads=total_leads,
        new_leads=new_leads,
        qualified_leads=qualified_leads,
        converted_leads=converted_leads,
        conversion_rate=round(conversion_rate, 2),
        leads_by_source=leads_by_source,
        leads_by_status=leads_by_status,
        average_response_time=average_response_time,
        top_performing_agents=top_performing_agents
    )

@router.get("/analytics")
async def get_leads_analytics():
    """Get detailed analytics for lead management"""
    
    # Lead conversion funnel
    funnel_data = {
        "new": len([l for l in leads_data if l["status"] == LeadStatus.NEW]),
        "contacted": len([l for l in leads_data if l["status"] == LeadStatus.CONTACTED]),
        "qualified": len([l for l in leads_data if l["status"] == LeadStatus.QUALIFIED]),
        "interested": len([l for l in leads_data if l["status"] == LeadStatus.INTERESTED]),
        "viewing_scheduled": len([l for l in leads_data if l["status"] == LeadStatus.VIEWING_SCHEDULED]),
        "negotiating": len([l for l in leads_data if l["status"] == LeadStatus.NEGOTIATING]),
        "closed_won": len([l for l in leads_data if l["status"] == LeadStatus.CLOSED_WON]),
        "closed_lost": len([l for l in leads_data if l["status"] == LeadStatus.CLOSED_LOST])
    }
    
    # Budget range distribution
    budget_distribution = {}
    for lead in leads_data:
        budget = lead["budget_range"].value
        budget_distribution[budget] = budget_distribution.get(budget, 0) + 1
    
    # Property interest distribution
    interest_distribution = {}
    for lead in leads_data:
        interest = lead["property_interest"].value
        interest_distribution[interest] = interest_distribution.get(interest, 0) + 1
    
    # Lead quality by source
    source_quality = {}
    for lead in leads_data:
        source = lead["source"].value
        if source not in source_quality:
            source_quality[source] = {"total": 0, "qualified": 0, "converted": 0}
        source_quality[source]["total"] += 1
        if lead["status"] in [LeadStatus.QUALIFIED, LeadStatus.INTERESTED, LeadStatus.NEGOTIATING, LeadStatus.CLOSED_WON]:
            source_quality[source]["qualified"] += 1
        if lead["status"] == LeadStatus.CLOSED_WON:
            source_quality[source]["converted"] += 1
    
    # Calculate conversion rates for each source
    for source_data in source_quality.values():
        source_data["qualification_rate"] = (source_data["qualified"] / source_data["total"] * 100) if source_data["total"] > 0 else 0
        source_data["conversion_rate"] = (source_data["converted"] / source_data["total"] * 100) if source_data["total"] > 0 else 0
    
    # Hot leads (high priority + interested status)
    hot_leads = [
        {
            "id": lead["id"],
            "name": lead["name"],
            "status": lead["status"].value,
            "budget_range": lead["budget_range"].value,
            "assigned_agent": lead.get("assigned_agent"),
            "next_follow_up": lead.get("next_follow_up")
        }
        for lead in leads_data 
        if lead["priority"] == "high" and lead["status"] in [LeadStatus.QUALIFIED, LeadStatus.INTERESTED, LeadStatus.NEGOTIATING]
    ]
    
    return {
        "conversion_funnel": funnel_data,
        "budget_distribution": budget_distribution,
        "property_interest_distribution": interest_distribution,
        "source_quality_analysis": source_quality,
        "hot_leads": hot_leads,
        "total_leads_value": len(leads_data),
        "monthly_growth_rate": "+15.2%",  # Mock data
        "lead_response_metrics": {
            "average_first_response": "2.5 hours",
            "average_qualification_time": "1.2 days",
            "average_conversion_time": "18.5 days"
        }
    }

@router.get("/priority/{priority_level}")
async def get_leads_by_priority(priority_level: str):
    """Get leads by priority level (high, medium, low)"""
    
    priority_leads = [lead for lead in leads_data if lead["priority"] == priority_level.lower()]
    
    if not priority_leads:
        return {"message": f"No {priority_level} priority leads found", "leads": []}
    
    return {
        "priority": priority_level,
        "count": len(priority_leads),
        "leads": priority_leads
    }

@router.get("/status/{status}")
async def get_leads_by_status(status: LeadStatus):
    """Get leads by status"""
    
    status_leads = [lead for lead in leads_data if lead["status"] == status]
    
    return {
        "status": status.value,
        "count": len(status_leads),
        "leads": status_leads
    }

@router.get("/agent/{agent_name}")
async def get_leads_by_agent(agent_name: str):
    """Get leads assigned to a specific agent"""
    
    agent_leads = [lead for lead in leads_data if lead.get("assigned_agent") == agent_name]
    
    if not agent_leads:
        return {"message": f"No leads found for agent {agent_name}", "leads": []}
    
    # Calculate agent performance
    total_leads = len(agent_leads)
    converted = len([lead for lead in agent_leads if lead["status"] == LeadStatus.CLOSED_WON])
    conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0
    
    return {
        "agent_name": agent_name,
        "total_leads": total_leads,
        "converted_leads": converted,
        "conversion_rate": round(conversion_rate, 2),
        "leads": agent_leads
    }

@router.get("/follow-up")
async def get_follow_up_leads():
    """Get leads that need follow-up today"""
    
    today = datetime.now().date()
    follow_up_leads = [
        lead for lead in leads_data 
        if lead.get("next_follow_up") and lead["next_follow_up"].date() <= today
    ]
    
    return {
        "count": len(follow_up_leads),
        "leads": follow_up_leads,
        "message": f"{len(follow_up_leads)} leads need follow-up today"
    }

@router.get("/hot-leads")
async def get_hot_leads():
    """Get hot leads (high priority + active status)"""
    
    hot_leads = [
        lead for lead in leads_data 
        if lead["priority"] == "high" and lead["status"] in [
            LeadStatus.QUALIFIED, LeadStatus.INTERESTED, LeadStatus.NEGOTIATING, LeadStatus.VIEWING_SCHEDULED
        ]
    ]
    
    return {
        "count": len(hot_leads),
        "leads": hot_leads,
        "total_potential_value": "Estimated high-value opportunities"
    }

@router.get("/search")
async def search_leads(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, description="Number of results to return")
):
    """Search leads by name, email, phone, or location"""
    
    search_query = q.lower()
    matching_leads = []
    
    for lead in leads_data:
        searchable_text = f"{lead['name']} {lead['email']} {lead['phone']} {lead['preferred_location']}".lower()
        
        if search_query in searchable_text:
            matching_leads.append(lead)
    
    return {
        "query": q,
        "count": len(matching_leads),
        "leads": matching_leads[:limit]
    }

@router.post("/", response_model=Lead)
async def create_lead(lead_data: LeadCreate):
    """Create a new lead"""
    
    # Generate new ID
    new_id = max([lead["id"] for lead in leads_data], default=0) + 1
    
    # Create new lead
    new_lead = {
        "id": new_id,
        "name": lead_data.name,
        "email": lead_data.email,
        "phone": lead_data.phone,
        "status": LeadStatus.NEW,
        "source": lead_data.source,
        "property_interest": lead_data.property_interest,
        "budget_range": lead_data.budget_range,
        "preferred_location": lead_data.preferred_location,
        "property_type": lead_data.property_type,
        "message": lead_data.message,
        "assigned_agent": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "last_contacted": None,
        "next_follow_up": datetime.now() + timedelta(hours=4),  # Follow up in 4 hours
        "priority": "medium",
        "tags": ["new_lead"],
        "notes": [],
        "property_views": [],
        "scheduled_viewings": []
    }
    
    # Add to leads data
    leads_data.append(new_lead)
    
    return new_lead

@router.get("/{lead_id}", response_model=Lead)
async def get_lead(lead_id: int):
    """Get specific lead by ID"""
    
    lead = next((lead for lead in leads_data if lead["id"] == lead_id), None)
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return lead

@router.put("/{lead_id}/status")
async def update_lead_status(lead_id: int, new_status: LeadStatus):
    """Update lead status"""
    
    lead = next((lead for lead in leads_data if lead["id"] == lead_id), None)
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    old_status = lead["status"]
    lead["status"] = new_status
    lead["updated_at"] = datetime.now()
    
    return {
        "message": f"Lead status updated from {old_status.value} to {new_status.value}",
        "lead_id": lead_id,
        "old_status": old_status.value,
        "new_status": new_status.value
    }

@router.put("/{lead_id}/assign")
async def assign_lead_to_agent(lead_id: int, agent_name: str):
    """Assign lead to an agent"""
    
    lead = next((lead for lead in leads_data if lead["id"] == lead_id), None)
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    old_agent = lead.get("assigned_agent")
    lead["assigned_agent"] = agent_name
    lead["updated_at"] = datetime.now()
    
    return {
        "message": f"Lead assigned to {agent_name}",
        "lead_id": lead_id,
        "old_agent": old_agent,
        "new_agent": agent_name
    }

@router.post("/{lead_id}/notes")
async def add_lead_note(lead_id: int, note_text: str, created_by: str):
    """Add a note to a lead"""
    
    lead = next((lead for lead in leads_data if lead["id"] == lead_id), None)
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Generate new note ID
    existing_note_ids = [note["id"] for note in lead["notes"]]
    new_note_id = max(existing_note_ids, default=0) + 1
    
    new_note = {
        "id": new_note_id,
        "note": note_text,
        "created_by": created_by,
        "created_at": datetime.now()
    }
    
    lead["notes"].append(new_note)
    lead["updated_at"] = datetime.now()
    
    return {
        "message": "Note added successfully",
        "note": new_note
    }