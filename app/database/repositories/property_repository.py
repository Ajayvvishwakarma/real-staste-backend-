from typing import Optional, List
from bson import ObjectId
from datetime import datetime
from app.database.sqlite_models import Property
from app.database.enums import PropertyType, ListingType, PropertyStatus


class PropertyRepository:
    
    @staticmethod
    async def create_property(property_data: dict, owner_id: str) -> Property:
        """Create a new property"""
        # Map schema fields to model fields
        model_data = {
            'title': property_data.get('title'),
            'description': property_data.get('description') or '',
            'property_type': property_data.get('property_type'),
            'listing_type': property_data.get('listing_type'),
            
            # Location fields
            'address': property_data.get('area') or '',  # Map 'area' from schema to 'address' in model
            'city': property_data.get('city'),
            'state': property_data.get('state'),
            'pincode': property_data.get('pincode') or '',
            
            # Property details
            'bedrooms': property_data.get('bedrooms'),
            'bathrooms': property_data.get('bathrooms'),
            'area_sqft': property_data.get('carpet_area'),  # Use carpet_area as primary area
            'floor_number': property_data.get('floor_number'),
            'total_floors': property_data.get('total_floors'),
            
            # Pricing
            'price': property_data.get('price'),
            
            # Features and amenities
            'amenities': property_data.get('amenities', []),
            'features': property_data.get('features', []),
            
            # Status and management
            'status': PropertyStatus.PENDING,
            'is_featured': False,
            'views': 0,
            
            # Required fields
            'created_by': owner_id,  # Set created_by as required by model
            'images': [],
            'documents': [],
        }
        
        # Remove None values
        model_data = {k: v for k, v in model_data.items() if v is not None}
        
        property_obj = Property(**model_data)
        await property_obj.insert()
        return property_obj
    
    @staticmethod
    async def get_property_by_id(property_id: str) -> Optional[Property]:
        """Get property by ID"""
        try:
            return await Property.get(ObjectId(property_id))
        except:
            return None
    
    @staticmethod
    async def update_property(property_id: str, update_data: dict) -> Optional[Property]:
        """Update property"""
        try:
            property_obj = await Property.get(ObjectId(property_id))
            if property_obj:
                update_data['updated_at'] = datetime.utcnow()
                for key, value in update_data.items():
                    setattr(property_obj, key, value)
                await property_obj.save()
                return property_obj
        except:
            pass
        return None
    
    @staticmethod
    async def delete_property(property_id: str) -> bool:
        """Delete property"""
        try:
            property_obj = await Property.get(ObjectId(property_id))
            if property_obj:
                await property_obj.delete()
                return True
        except:
            pass
        return False
    
    @staticmethod
    async def get_properties(
        skip: int = 0,
        limit: int = 20,
        city: Optional[str] = None,
        state: Optional[str] = None,
        property_type: Optional[PropertyType] = None,
        listing_type: Optional[ListingType] = None,
        status: Optional[PropertyStatus] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        bedrooms: Optional[int] = None,
        is_featured: Optional[bool] = None,
        owner_id: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Property]:
        """Get properties with filters"""
        query = {}
        
        if city:
            query['city'] = {"$regex": city, "$options": "i"}
        if state:
            query['state'] = {"$regex": state, "$options": "i"}
        if property_type:
            query['property_type'] = property_type
        if listing_type:
            query['listing_type'] = listing_type
        if status:
            query['status'] = status
        if min_price is not None:
            query['price'] = {"$gte": min_price}
        if max_price is not None:
            if 'price' in query:
                query['price']['$lte'] = max_price
            else:
                query['price'] = {"$lte": max_price}
        if bedrooms is not None:
            query['bedrooms'] = bedrooms
        if is_featured is not None:
            query['is_featured'] = is_featured
        if owner_id:
            query['owner_id'] = ObjectId(owner_id)
        
        properties = Property.find(query)
        
        if search:
            properties = properties.find({
                "$or": [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                    {"area": {"$regex": search, "$options": "i"}}
                ]
            })
        
        return await properties.skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def count_properties(
        city: Optional[str] = None,
        state: Optional[str] = None,
        property_type: Optional[PropertyType] = None,
        listing_type: Optional[ListingType] = None,
        status: Optional[PropertyStatus] = None,
        owner_id: Optional[str] = None
    ) -> int:
        """Count properties with filters"""
        query = {}
        
        if city:
            query['city'] = {"$regex": city, "$options": "i"}
        if state:
            query['state'] = {"$regex": state, "$options": "i"}
        if property_type:
            query['property_type'] = property_type
        if listing_type:
            query['listing_type'] = listing_type
        if status:
            query['status'] = status
        if owner_id:
            query['owner_id'] = ObjectId(owner_id)
        
        return await Property.find(query).count()
    
    @staticmethod
    async def increment_views(property_id: str) -> None:
        """Increment property views count"""
        try:
            property_obj = await Property.get(ObjectId(property_id))
            if property_obj:
                property_obj.views_count += 1
                await property_obj.save()
        except:
            pass
    
    @staticmethod
    async def get_property_stats() -> dict:
        """Get property statistics"""
        total_properties = await Property.find().count()
        pending_properties = await Property.find(Property.status == PropertyStatus.PENDING).count()
        approved_properties = await Property.find(Property.status == PropertyStatus.ACTIVE).count()
        featured_properties = await Property.find(Property.is_featured == True).count()
        
        # Properties by type
        types_count = {}
        for prop_type in PropertyType:
            count = await Property.find(Property.property_type == prop_type).count()
            types_count[prop_type.value] = count
        
        # Properties by city (top 10)
        pipeline = [
            {"$group": {"_id": "$city", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        cities_count = {}
        async for doc in Property.aggregate(pipeline):
            cities_count[doc["_id"]] = doc["count"]
        
        # Recent listings (last 30 days)
        from datetime import timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_listings = await Property.find(
            Property.created_at >= thirty_days_ago
        ).count()
        
        return {
            "total_properties": total_properties,
            "pending_properties": pending_properties,
            "approved_properties": approved_properties,
            "featured_properties": featured_properties,
            "properties_by_type": types_count,
            "properties_by_city": cities_count,
            "recent_listings": recent_listings
        }