from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from enum import Enum

router = APIRouter()

class StoryCategory(str, Enum):
    FIRST_TIME_BUYER = "first_time_buyer"
    INVESTMENT = "investment"
    LUXURY_PURCHASE = "luxury_purchase"
    QUICK_SALE = "quick_sale"
    RENTAL_SUCCESS = "rental_success"
    COMMERCIAL = "commercial"
    RELOCATION = "relocation"

class StoryStatus(str, Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    FEATURED = "featured"
    ARCHIVED = "archived"

class SuccessStory(BaseModel):
    id: int
    title: str
    client_name: str
    client_location: str
    property_type: str
    deal_value: float
    category: StoryCategory
    story_summary: str
    detailed_story: str
    challenges_faced: List[str]
    solutions_provided: List[str]
    agent_name: str
    agent_rating: float
    timeline_days: int
    status: StoryStatus
    featured: bool
    images: List[str]
    video_url: Optional[str] = None
    client_testimonial: str
    agent_comments: str
    created_at: datetime
    published_at: Optional[datetime] = None
    views: int
    likes: int
    tags: List[str]

class StoryStats(BaseModel):
    total_stories: int
    published_stories: int
    featured_stories: int
    total_deal_value: float
    average_timeline: float
    most_viewed_story: Dict[str, Any]
    top_performing_agents: List[Dict[str, Any]]

# Sample success stories data
success_stories_data = [
    {
        "id": 1,
        "title": "From Dream to Reality: Young Couple's First Home Journey",
        "client_name": "Raj & Priya Sharma",
        "client_location": "Gurgaon, Haryana",
        "property_type": "3BHK Apartment",
        "deal_value": 1850000.0,  # ₹18.5 Lakh
        "category": StoryCategory.FIRST_TIME_BUYER,
        "story_summary": "Young IT professionals successfully purchased their first home in Gurgaon with expert guidance on home loans and property selection.",
        "detailed_story": "Raj and Priya, both software engineers in their late 20s, had been dreaming of owning their first home. After years of saving and research, they approached our team with a budget of ₹20 lakhs. Our agent Neha Agarwal understood their requirements: a modern 3BHK apartment near IT hubs with good connectivity to Delhi. After showing them 15+ properties over 2 months, we found the perfect match in Sector 37C. The property offered excellent amenities, metro connectivity, and was within their budget. We also helped them secure a home loan at competitive rates and handled all documentation seamlessly.",
        "challenges_faced": [
            "Limited budget for desired location",
            "First-time home loan application complexity",
            "Understanding legal documentation",
            "Property title verification concerns",
            "Negotiating with multiple sellers"
        ],
        "solutions_provided": [
            "Identified emerging areas with growth potential",
            "Connected with pre-approved bank partners",
            "Provided legal documentation support",
            "Conducted thorough due diligence",
            "Expert negotiation saved ₹1.5 lakhs"
        ],
        "agent_name": "Neha Agarwal",
        "agent_rating": 4.9,
        "timeline_days": 67,
        "status": StoryStatus.FEATURED,
        "featured": True,
        "images": [
            "https://example.com/story1-property.jpg",
            "https://example.com/story1-clients.jpg",
            "https://example.com/story1-handover.jpg"
        ],
        "video_url": "https://example.com/story1-testimonial.mp4",
        "client_testimonial": "Neha was absolutely fantastic! She understood our needs perfectly and guided us through every step. As first-time buyers, we were overwhelmed, but she made the entire process smooth and stress-free. We saved money and got our dream home. Highly recommended!",
        "agent_comments": "Working with Raj and Priya was a pleasure. Their clear communication and trust in the process made it smooth. Seeing their joy during the handover was the best reward!",
        "created_at": datetime.now() - timedelta(days=30),
        "published_at": datetime.now() - timedelta(days=25),
        "views": 2850,
        "likes": 127,
        "tags": ["first_home", "young_professionals", "gurgaon", "success", "home_loan"]
    },
    {
        "id": 2,
        "title": "Smart Investment: ₹50 Lakh Property Generates 12% Returns",
        "client_name": "Mr. Vikram Malhotra",
        "client_location": "Mumbai, Maharashtra",
        "property_type": "2BHK Commercial Space",
        "deal_value": 5000000.0,  # ₹50 Lakh
        "category": StoryCategory.INVESTMENT,
        "story_summary": "Experienced investor diversified portfolio with a commercial property purchase that now generates consistent 12% annual returns.",
        "detailed_story": "Mr. Vikram Malhotra, a successful businessman, wanted to diversify his investment portfolio beyond stocks and mutual funds. He approached our Mumbai team with a budget of ₹50 lakhs for a commercial property investment. Our agent Rohit Mehta conducted extensive market research and identified a prime 2BHK commercial space in Andheri East, near the metro station and IT parks. The property was perfect for rental to corporate clients. Within 3 months of purchase, we helped him secure a multinational company as a tenant at ₹50,000 monthly rent, providing 12% annual returns plus capital appreciation potential.",
        "challenges_faced": [
            "Finding high-yield commercial properties",
            "Tenant verification and reliability",
            "Commercial property legal complexities",
            "Market timing for maximum returns",
            "Competition from other investors"
        ],
        "solutions_provided": [
            "Identified emerging commercial hubs",
            "Pre-verified tenant database access",
            "Comprehensive legal due diligence",
            "Market analysis for optimal timing",
            "Exclusive off-market property deals"
        ],
        "agent_name": "Rohit Mehta",
        "agent_rating": 4.8,
        "timeline_days": 45,
        "status": StoryStatus.PUBLISHED,
        "featured": True,
        "images": [
            "https://example.com/story2-commercial.jpg",
            "https://example.com/story2-location.jpg",
            "https://example.com/story2-returns.jpg"
        ],
        "video_url": None,
        "client_testimonial": "Rohit's market knowledge is exceptional. He found me a property that not only met my budget but exceeded my return expectations. The tenant he arranged is reliable, and I'm earning consistent monthly income. Great investment advice!",
        "agent_comments": "Mr. Malhotra's clear investment goals made it easier to find the right property. His trust in our market analysis led to this successful investment.",
        "created_at": datetime.now() - timedelta(days=45),
        "published_at": datetime.now() - timedelta(days=40),
        "views": 1920,
        "likes": 89,
        "tags": ["investment", "commercial", "mumbai", "high_returns", "portfolio_diversification"]
    },
    {
        "id": 3,
        "title": "Luxury Villa Dream Fulfilled: ₹3.5 Cr Goa Retreat",
        "client_name": "Dr. Anjali & Mr. Suresh Reddy",
        "client_location": "Bangalore to Goa",
        "property_type": "Luxury Villa",
        "deal_value": 35000000.0,  # ₹3.5 Cr
        "category": StoryCategory.LUXURY_PURCHASE,
        "story_summary": "Bangalore-based doctors fulfilled their dream of owning a luxury vacation villa in Goa with panoramic sea views and premium amenities.",
        "detailed_story": "Dr. Anjali and Mr. Suresh Reddy, successful medical professionals from Bangalore, had been planning to buy a luxury vacation home in Goa for years. They wanted a property that could serve as both a personal retreat and a potential rental investment. Our Goa specialist, Kavita Sharma, understood their vision of a villa with sea views, privacy, and luxury amenities. After an extensive search across North and South Goa, we found a stunning 4BHK villa in Candolim with panoramic Arabian Sea views, infinity pool, and beautifully landscaped gardens. The property also came with rental management services, making it a perfect investment too.",
        "challenges_faced": [
            "Finding authentic luxury properties in Goa",
            "Navigating interstate property purchase laws",
            "Verifying property titles in coastal areas",
            "Ensuring rental management quality",
            "Coordinating remote inspections from Bangalore"
        ],
        "solutions_provided": [
            "Exclusive access to luxury property network",
            "Legal expertise in Goa property laws",
            "Comprehensive title verification process",
            "Partnered with premium rental management",
            "Virtual tours and detailed video inspections"
        ],
        "agent_name": "Kavita Sharma",
        "agent_rating": 5.0,
        "timeline_days": 89,
        "status": StoryStatus.FEATURED,
        "featured": True,
        "images": [
            "https://example.com/story3-villa-exterior.jpg",
            "https://example.com/story3-sea-view.jpg",
            "https://example.com/story3-pool.jpg",
            "https://example.com/story3-interior.jpg"
        ],
        "video_url": "https://example.com/story3-villa-tour.mp4",
        "client_testimonial": "Kavita made our dream come true! The villa is absolutely stunning, exactly what we envisioned. Her attention to detail and understanding of luxury properties is remarkable. We now have our perfect Goa retreat!",
        "agent_comments": "Dr. Anjali and Mr. Suresh had a clear vision, and it was rewarding to find them the perfect property. Their trust throughout the process made this complex luxury transaction smooth.",
        "created_at": datetime.now() - timedelta(days=60),
        "published_at": datetime.now() - timedelta(days=50),
        "views": 3200,
        "likes": 156,
        "tags": ["luxury", "goa", "villa", "sea_view", "vacation_home", "investment"]
    },
    {
        "id": 4,
        "title": "Lightning Fast Sale: Property Sold in 15 Days",
        "client_name": "Mrs. Meera Gupta",
        "client_location": "Noida, Uttar Pradesh",
        "property_type": "2BHK Apartment",
        "deal_value": 1200000.0,  # ₹12 Lakh
        "category": StoryCategory.QUICK_SALE,
        "story_summary": "Urgent relocation requirement led to a record-breaking property sale in just 15 days at full market value.",
        "detailed_story": "Mrs. Meera Gupta needed to sell her 2BHK apartment in Noida urgently due to her husband's job transfer to Dubai. With only 20 days before their departure, she approached our team for a quick sale. Our agent Amit Kumar immediately activated our extensive buyer network and implemented a fast-track marketing strategy. Using professional photography, virtual tours, and targeted marketing to pre-qualified buyers, we generated 25+ inquiries in the first week. By day 10, we had 3 serious offers, and by day 15, the deal was closed at ₹12 lakhs - the full asking price. All paperwork was completed before their departure.",
        "challenges_faced": [
            "Extremely tight timeline for sale",
            "Achieving full market value in quick sale",
            "Buyer verification in compressed timeframe",
            "Coordinating documentation while packing",
            "Ensuring clean title transfer quickly"
        ],
        "solutions_provided": [
            "Activated premium buyer network immediately",
            "Professional staging and photography",
            "Pre-qualified buyer database access",
            "Dedicated documentation support team",
            "Express legal clearance services"
        ],
        "agent_name": "Amit Kumar",
        "agent_rating": 4.9,
        "timeline_days": 15,
        "status": StoryStatus.PUBLISHED,
        "featured": True,
        "images": [
            "https://example.com/story4-apartment.jpg",
            "https://example.com/story4-sale-board.jpg",
            "https://example.com/story4-handover.jpg"
        ],
        "video_url": None,
        "client_testimonial": "Amit was our savior! We thought we'd have to sell at a loss due to time pressure, but he got us the full price in just 15 days. His efficiency and network are incredible. Thank you for making our relocation stress-free!",
        "agent_comments": "Mrs. Gupta's trust in our fast-track process allowed us to work efficiently. The urgent timeline brought out the best in our team's coordination and buyer network.",
        "created_at": datetime.now() - timedelta(days=20),
        "published_at": datetime.now() - timedelta(days=15),
        "views": 1750,
        "likes": 93,
        "tags": ["quick_sale", "relocation", "noida", "full_price", "urgent", "efficiency"]
    },
    {
        "id": 5,
        "title": "Perfect Rental Match: 3BHK for IT Professional Family",
        "client_name": "Mr. Karan Singh",
        "client_location": "Pune, Maharashtra",
        "property_type": "3BHK Apartment",
        "deal_value": 35000.0,  # ₹35,000 monthly rent
        "category": StoryCategory.RENTAL_SUCCESS,
        "story_summary": "IT professional found the perfect family home rental in Pune with all desired amenities and excellent school proximity.",
        "detailed_story": "Mr. Karan Singh, a software architect, was relocating from Hyderabad to Pune for a new job. With two school-going children, he needed a 3BHK apartment near good schools, with family-friendly amenities, and within a ₹35,000 monthly budget. Our Pune team, led by Priya Patel, understood the family's priorities: safety, schools, parks, and community feel. After showing 8 properties over one weekend, we found the perfect match in Baner - a well-maintained apartment in a family-oriented society with a swimming pool, playground, and two renowned schools within 1km. The landlord was also a family person, making the relationship smooth.",
        "challenges_faced": [
            "Finding family-oriented rental properties",
            "School proximity requirements",
            "Landlord preference for families with children",
            "Relocation timeline pressure",
            "Ensuring safety and community feel"
        ],
        "solutions_provided": [
            "Specialized family rental database",
            "School proximity mapping and ratings",
            "Pre-screened family-friendly landlords",
            "Weekend intensive property tours",
            "Community safety and amenity verification"
        ],
        "agent_name": "Priya Patel",
        "agent_rating": 4.8,
        "timeline_days": 7,
        "status": StoryStatus.PUBLISHED,
        "featured": False,
        "images": [
            "https://example.com/story5-apartment.jpg",
            "https://example.com/story5-community.jpg",
            "https://example.com/story5-playground.jpg"
        ],
        "video_url": None,
        "client_testimonial": "Priya understood our family needs perfectly. The apartment she found is ideal - great schools nearby, safe community, and the kids love the playground. The entire process was smooth and quick!",
        "agent_comments": "Mr. Karan's clear family priorities made it easier to shortlist properties. Seeing the family settle happily in their new home was very satisfying.",
        "created_at": datetime.now() - timedelta(days=35),
        "published_at": datetime.now() - timedelta(days=30),
        "views": 980,
        "likes": 45,
        "tags": ["rental", "family", "pune", "schools", "relocation", "community"]
    },
    {
        "id": 6,
        "title": "Commercial Space Success: Restaurant Owner's Dream Location",
        "client_name": "Mr. Rajesh Khanna",
        "client_location": "Delhi, Delhi",
        "property_type": "Commercial Space",
        "deal_value": 8000000.0,  # ₹80 Lakh
        "category": StoryCategory.COMMERCIAL,
        "story_summary": "Restaurant entrepreneur found the perfect high-footfall location in Delhi's prime market area for his new fine dining venture.",
        "detailed_story": "Mr. Rajesh Khanna, an experienced restaurateur, was looking to open his third fine dining restaurant in Delhi. He needed a commercial space in a high-footfall area with parking, visibility, and the right ambiance for upscale dining. Our commercial specialist, Sunita Devi, conducted thorough market research and identified a premium ground floor space in Khan Market. The 2000 sq ft space had excellent street visibility, dedicated parking, and was surrounded by upscale shops and offices. The location's demographics perfectly matched his target customers. Within 6 months of purchase, his restaurant became one of Khan Market's most popular dining destinations.",
        "challenges_faced": [
            "Finding prime commercial locations",
            "High competition for premium spaces",
            "Ensuring proper licensing capabilities",
            "Parking and accessibility requirements",
            "Negotiating with commercial landlords"
        ],
        "solutions_provided": [
            "Exclusive commercial property network",
            "Market analysis and footfall studies",
            "Licensing and compliance verification",
            "Infrastructure and accessibility audit",
            "Expert commercial negotiation services"
        ],
        "agent_name": "Sunita Devi",
        "agent_rating": 4.9,
        "timeline_days": 52,
        "status": StoryStatus.PUBLISHED,
        "featured": False,
        "images": [
            "https://example.com/story6-commercial.jpg",
            "https://example.com/story6-location.jpg",
            "https://example.com/story6-restaurant.jpg"
        ],
        "video_url": None,
        "client_testimonial": "Sunita's understanding of commercial real estate is outstanding. She found me the perfect location that has contributed significantly to my restaurant's success. Her market knowledge is invaluable!",
        "agent_comments": "Mr. Rajesh's clear business vision and trust in market analysis made this successful. Seeing his restaurant thrive in the location we found is extremely rewarding.",
        "created_at": datetime.now() - timedelta(days=90),
        "published_at": datetime.now() - timedelta(days=80),
        "views": 1456,
        "likes": 78,
        "tags": ["commercial", "restaurant", "delhi", "prime_location", "business_success"]
    },
    {
        "id": 7,
        "title": "Corporate Relocation: Executive Housing in Record Time",
        "client_name": "Ms. Anita Sharma",
        "client_location": "Chennai to Bangalore",
        "property_type": "Furnished 2BHK",
        "deal_value": 45000.0,  # ₹45,000 monthly rent
        "category": StoryCategory.RELOCATION,
        "story_summary": "Senior executive's corporate relocation handled seamlessly with fully furnished premium accommodation near IT corridor.",
        "detailed_story": "Ms. Anita Sharma, a senior executive with a multinational company, was transferred from Chennai to Bangalore with just 10 days notice. She needed a fully furnished, premium 2BHK apartment near Electronic City, with modern amenities and corporate housing standards. Our Bangalore corporate housing specialist, Dr. Vikram Tech, immediately activated our executive housing network. Within 48 hours, we arranged virtual tours of 5 suitable properties. Ms. Sharma selected a premium furnished apartment in a corporate-friendly complex with gym, swimming pool, and 24/7 security. All documentation and setup were completed before her arrival, allowing her to focus on her new role immediately.",
        "challenges_faced": [
            "Extremely short notice for relocation",
            "Corporate housing quality standards",
            "Furnished apartment availability",
            "Electronic City proximity requirement",
            "Quick documentation and verification"
        ],
        "solutions_provided": [
            "Dedicated corporate housing network",
            "24/7 emergency relocation services",
            "Pre-verified furnished property database",
            "Location-specific property mapping",
            "Express documentation services"
        ],
        "agent_name": "Dr. Vikram Tech",
        "agent_rating": 5.0,
        "timeline_days": 3,
        "status": StoryStatus.PUBLISHED,
        "featured": False,
        "images": [
            "https://example.com/story7-furnished.jpg",
            "https://example.com/story7-amenities.jpg",
            "https://example.com/story7-location.jpg"
        ],
        "video_url": None,
        "client_testimonial": "Dr. Vikram's emergency service was incredible! In just 3 days, he arranged everything perfectly. The apartment exceeded my expectations, and I could start work without any housing stress. Exceptional service!",
        "agent_comments": "Ms. Anita's corporate relocation required precision and speed. Our emergency protocol and corporate network made this tight timeline achievable.",
        "created_at": datetime.now() - timedelta(days=15),
        "published_at": datetime.now() - timedelta(days=10),
        "views": 1250,
        "likes": 67,
        "tags": ["relocation", "corporate", "bangalore", "furnished", "emergency", "executive"]
    }
]

@router.get("/", response_model=List[SuccessStory])
async def get_success_stories(
    limit: Optional[int] = Query(10, description="Number of stories to return"),
    offset: Optional[int] = Query(0, description="Number of stories to skip"),
    category: Optional[StoryCategory] = Query(None, description="Filter by story category"),
    status: Optional[StoryStatus] = Query(None, description="Filter by status"),
    featured_only: Optional[bool] = Query(False, description="Show only featured stories"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    min_deal_value: Optional[float] = Query(None, description="Minimum deal value filter"),
    max_deal_value: Optional[float] = Query(None, description="Maximum deal value filter"),
    location: Optional[str] = Query(None, description="Filter by location")
):
    """Get success stories with comprehensive filtering"""
    
    filtered_stories = success_stories_data.copy()
    
    # Apply filters
    if category:
        filtered_stories = [story for story in filtered_stories if story["category"] == category]
    
    if status:
        filtered_stories = [story for story in filtered_stories if story["status"] == status]
    
    if featured_only:
        filtered_stories = [story for story in filtered_stories if story["featured"]]
    
    if agent_name:
        filtered_stories = [story for story in filtered_stories if agent_name.lower() in story["agent_name"].lower()]
    
    if min_deal_value is not None:
        filtered_stories = [story for story in filtered_stories if story["deal_value"] >= min_deal_value]
    
    if max_deal_value is not None:
        filtered_stories = [story for story in filtered_stories if story["deal_value"] <= max_deal_value]
    
    if location:
        filtered_stories = [story for story in filtered_stories if location.lower() in story["client_location"].lower()]
    
    # Apply pagination
    paginated_stories = filtered_stories[offset:offset + limit]
    
    return paginated_stories

@router.get("/dashboard", response_model=StoryStats)
async def get_stories_dashboard():
    """Get success stories dashboard statistics"""
    
    total_stories = len(success_stories_data)
    published_stories = len([story for story in success_stories_data if story["status"] in [StoryStatus.PUBLISHED, StoryStatus.FEATURED]])
    featured_stories = len([story for story in success_stories_data if story["featured"]])
    total_deal_value = sum(story["deal_value"] for story in success_stories_data)
    average_timeline = sum(story["timeline_days"] for story in success_stories_data) / total_stories if total_stories > 0 else 0
    
    # Find most viewed story
    most_viewed = max(success_stories_data, key=lambda x: x["views"]) if success_stories_data else None
    most_viewed_story = {
        "id": most_viewed["id"] if most_viewed else 0,
        "title": most_viewed["title"] if most_viewed else "",
        "views": most_viewed["views"] if most_viewed else 0,
        "client_name": most_viewed["client_name"] if most_viewed else ""
    }
    
    # Top performing agents
    agent_performance = {}
    for story in success_stories_data:
        agent = story["agent_name"]
        if agent not in agent_performance:
            agent_performance[agent] = {
                "name": agent,
                "stories_count": 0,
                "total_deal_value": 0,
                "average_rating": 0,
                "total_views": 0
            }
        agent_performance[agent]["stories_count"] += 1
        agent_performance[agent]["total_deal_value"] += story["deal_value"]
        agent_performance[agent]["average_rating"] += story["agent_rating"]
        agent_performance[agent]["total_views"] += story["views"]
    
    # Calculate averages and sort
    for agent_data in agent_performance.values():
        agent_data["average_rating"] = agent_data["average_rating"] / agent_data["stories_count"]
        agent_data["average_deal_value"] = agent_data["total_deal_value"] / agent_data["stories_count"]
    
    top_performing_agents = sorted(agent_performance.values(), key=lambda x: x["stories_count"], reverse=True)[:5]
    
    return StoryStats(
        total_stories=total_stories,
        published_stories=published_stories,
        featured_stories=featured_stories,
        total_deal_value=total_deal_value,
        average_timeline=round(average_timeline, 1),
        most_viewed_story=most_viewed_story,
        top_performing_agents=top_performing_agents
    )

@router.get("/featured")
async def get_featured_stories():
    """Get featured success stories"""
    
    featured_stories = [story for story in success_stories_data if story["featured"]]
    
    return {
        "count": len(featured_stories),
        "stories": featured_stories
    }

@router.get("/analytics")
async def get_stories_analytics():
    """Get detailed analytics for success stories"""
    
    # Category distribution
    category_distribution = {}
    for story in success_stories_data:
        category = story["category"].value
        category_distribution[category] = category_distribution.get(category, 0) + 1
    
    # Deal value ranges
    deal_ranges = {
        "under_10_lakh": len([s for s in success_stories_data if s["deal_value"] < 1000000]),
        "10_lakh_50_lakh": len([s for s in success_stories_data if 1000000 <= s["deal_value"] < 5000000]),
        "50_lakh_1_cr": len([s for s in success_stories_data if 5000000 <= s["deal_value"] < 10000000]),
        "1_cr_5_cr": len([s for s in success_stories_data if 10000000 <= s["deal_value"] < 50000000]),
        "above_5_cr": len([s for s in success_stories_data if s["deal_value"] >= 50000000])
    }
    
    # Timeline analysis
    timeline_ranges = {
        "under_7_days": len([s for s in success_stories_data if s["timeline_days"] < 7]),
        "7_30_days": len([s for s in success_stories_data if 7 <= s["timeline_days"] < 30]),
        "30_60_days": len([s for s in success_stories_data if 30 <= s["timeline_days"] < 60]),
        "60_90_days": len([s for s in success_stories_data if 60 <= s["timeline_days"] < 90]),
        "above_90_days": len([s for s in success_stories_data if s["timeline_days"] >= 90])
    }
    
    # Top performing stories
    top_stories = sorted(success_stories_data, key=lambda x: x["views"], reverse=True)[:3]
    top_performing_stories = [
        {
            "id": story["id"],
            "title": story["title"],
            "views": story["views"],
            "likes": story["likes"],
            "deal_value": story["deal_value"],
            "category": story["category"].value
        }
        for story in top_stories
    ]
    
    # Agent success metrics
    agent_metrics = {}
    for story in success_stories_data:
        agent = story["agent_name"]
        if agent not in agent_metrics:
            agent_metrics[agent] = {
                "stories": 0,
                "total_deal_value": 0,
                "avg_timeline": 0,
                "avg_rating": 0
            }
        agent_metrics[agent]["stories"] += 1
        agent_metrics[agent]["total_deal_value"] += story["deal_value"]
        agent_metrics[agent]["avg_timeline"] += story["timeline_days"]
        agent_metrics[agent]["avg_rating"] += story["agent_rating"]
    
    # Calculate averages
    for metrics in agent_metrics.values():
        count = metrics["stories"]
        metrics["avg_timeline"] = round(metrics["avg_timeline"] / count, 1)
        metrics["avg_rating"] = round(metrics["avg_rating"] / count, 2)
        metrics["avg_deal_value"] = round(metrics["total_deal_value"] / count, 0)
    
    return {
        "category_distribution": category_distribution,
        "deal_value_ranges": deal_ranges,
        "timeline_distribution": timeline_ranges,
        "top_performing_stories": top_performing_stories,
        "agent_performance_metrics": agent_metrics,
        "total_portfolio_value": sum(story["deal_value"] for story in success_stories_data),
        "average_client_satisfaction": round(sum(story["agent_rating"] for story in success_stories_data) / len(success_stories_data), 2),
        "success_rate_metrics": {
            "fastest_closure": min(story["timeline_days"] for story in success_stories_data),
            "highest_deal_value": max(story["deal_value"] for story in success_stories_data),
            "most_viewed": max(story["views"] for story in success_stories_data)
        }
    }

@router.get("/categories")
async def get_story_categories():
    """Get all story categories with counts"""
    
    categories = {}
    for story in success_stories_data:
        category = story["category"].value
        if category not in categories:
            categories[category] = {
                "name": category,
                "count": 0,
                "total_deal_value": 0,
                "average_timeline": 0,
                "stories": []
            }
        categories[category]["count"] += 1
        categories[category]["total_deal_value"] += story["deal_value"]
        categories[category]["average_timeline"] += story["timeline_days"]
        categories[category]["stories"].append({
            "id": story["id"],
            "title": story["title"],
            "client_name": story["client_name"]
        })
    
    # Calculate averages
    for cat_data in categories.values():
        if cat_data["count"] > 0:
            cat_data["average_timeline"] = round(cat_data["average_timeline"] / cat_data["count"], 1)
    
    return {
        "categories": categories,
        "total_categories": len(categories)
    }

@router.get("/search")
async def search_stories(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, description="Number of results to return")
):
    """Search success stories by title, client name, location, or content"""
    
    search_query = q.lower()
    matching_stories = []
    
    for story in success_stories_data:
        searchable_text = f"{story['title']} {story['client_name']} {story['client_location']} {story['story_summary']} {story['property_type']}".lower()
        
        if search_query in searchable_text:
            matching_stories.append(story)
    
    return {
        "query": q,
        "count": len(matching_stories),
        "stories": matching_stories[:limit]
    }

@router.get("/testimonials")
async def get_client_testimonials():
    """Get all client testimonials from success stories"""
    
    testimonials = []
    for story in success_stories_data:
        if story["status"] in [StoryStatus.PUBLISHED, StoryStatus.FEATURED]:
            testimonials.append({
                "id": story["id"],
                "client_name": story["client_name"],
                "client_location": story["client_location"],
                "testimonial": story["client_testimonial"],
                "agent_name": story["agent_name"],
                "agent_rating": story["agent_rating"],
                "deal_value": story["deal_value"],
                "property_type": story["property_type"],
                "category": story["category"].value,
                "created_at": story["created_at"]
            })
    
    return {
        "count": len(testimonials),
        "testimonials": sorted(testimonials, key=lambda x: x["agent_rating"], reverse=True)
    }

@router.get("/agent/{agent_name}")
async def get_stories_by_agent(agent_name: str):
    """Get success stories by specific agent"""
    
    agent_stories = [story for story in success_stories_data if agent_name.lower() in story["agent_name"].lower()]
    
    if not agent_stories:
        return {"message": f"No success stories found for agent {agent_name}", "stories": []}
    
    # Calculate agent performance
    total_deal_value = sum(story["deal_value"] for story in agent_stories)
    average_timeline = sum(story["timeline_days"] for story in agent_stories) / len(agent_stories)
    average_rating = sum(story["agent_rating"] for story in agent_stories) / len(agent_stories)
    total_views = sum(story["views"] for story in agent_stories)
    
    return {
        "agent_name": agent_name,
        "total_stories": len(agent_stories),
        "total_deal_value": total_deal_value,
        "average_timeline_days": round(average_timeline, 1),
        "average_rating": round(average_rating, 2),
        "total_views": total_views,
        "stories": agent_stories
    }

@router.get("/{story_id}", response_model=SuccessStory)
async def get_success_story(story_id: int):
    """Get specific success story by ID"""
    
    story = next((story for story in success_stories_data if story["id"] == story_id), None)
    
    if not story:
        raise HTTPException(status_code=404, detail="Success story not found")
    
    # Increment view count
    story["views"] += 1
    
    return story

@router.post("/{story_id}/like")
async def like_story(story_id: int):
    """Like a success story"""
    
    story = next((story for story in success_stories_data if story["id"] == story_id), None)
    
    if not story:
        raise HTTPException(status_code=404, detail="Success story not found")
    
    story["likes"] += 1
    
    return {
        "message": "Story liked successfully",
        "story_id": story_id,
        "total_likes": story["likes"]
    }