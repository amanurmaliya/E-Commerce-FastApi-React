from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from bson import ObjectId
from pymongo.collection import Collection
from .base_factory import BaseFactory

class BaseRepository(ABC):
    """
    Abstract base repository class defining common database operations.
    """
    
    def __init__(self, collection: Collection):
        self.collection = collection
    
    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 10, filters: Dict = None) -> List[Dict]:
        """Find all documents with pagination and optional filters."""
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Dict]:
        """Find a document by ID."""
        pass
    
    @abstractmethod
    def create(self, data: Dict) -> Dict:
        """Create a new document."""
        pass
    
    @abstractmethod
    def update(self, id: str, data: Dict) -> bool:
        """Update a document by ID."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete a document by ID."""
        pass
    
    @abstractmethod
    def search(self, query: Dict) -> List[Dict]:
        """Search documents based on query."""
        pass

class MongoRepository(BaseRepository):
    """
    MongoDB implementation of the repository pattern.
    """
    
    def find_all(self, skip: int = 0, limit: int = 10, filters: Dict = None) -> List[Dict]:
        """Find all documents with pagination and optional filters."""
        query = filters or {}
        documents = list(self.collection.find(query).skip(skip).limit(limit))
        return self._transform_documents(documents)
    
    def find_by_id(self, id: str) -> Optional[Dict]:
        """Find a document by ID."""
        try:
            document = self.collection.find_one({"_id": ObjectId(id)})
            if document:
                return self._transform_document(document)
            return None
        except Exception:
            return None
    
    def create(self, data: Dict) -> Dict:
        """Create a new document."""
        result = self.collection.insert_one(data)
        return {
            "success": result.acknowledged,
            "id": str(result.inserted_id)
        }
    
    def update(self, id: str, data: Dict) -> bool:
        """Update a document by ID."""
        try:
            # Filter out None values
            update_data = {k: v for k, v in data.items() if v is not None}
            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            return result.matched_count > 0
        except Exception:
            return False
    
    def delete(self, id: str) -> bool:
        """Delete a document by ID."""
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    def search(self, query: Dict) -> List[Dict]:
        """Search documents based on query."""
        documents = list(self.collection.find(query))
        return self._transform_documents(documents)
    
    def _transform_document(self, document: Dict) -> Dict:
        """Transform MongoDB document by converting _id to id."""
        if document and "_id" in document:
            document["id"] = str(document["_id"])
            del document["_id"]
        return document
    
    def _transform_documents(self, documents: List[Dict]) -> List[Dict]:
        """Transform multiple MongoDB documents."""
        return [self._transform_document(doc) for doc in documents]

class ProductRepository(MongoRepository):
    """
    Product-specific repository with custom methods.
    """
    
    def search_by_name(self, query: str) -> List[Dict]:
        """Search products by name using regex."""
        search_query = {"name": {"$regex": query, "$options": "i"}}
        return self.search(search_query)
    
    def filter_products(self, filters: Dict) -> List[Dict]:
        """Filter products based on multiple criteria."""
        query = {}
        
        if filters.get("category"):
            query["category"] = filters["category"]
            
        if filters.get("min_price") is not None or filters.get("max_price") is not None:
            query["price"] = {}
            if filters.get("min_price") is not None:
                query["price"]["$gte"] = filters["min_price"]
            if filters.get("max_price") is not None:
                query["price"]["$lte"] = filters["max_price"]
                
        if filters.get("min_rating") is not None:
            query["rating"] = {"$gte": filters["min_rating"]}
            
        return self.search(query)

class UserRepository(MongoRepository):
    """
    User-specific repository with custom methods.
    """
    
    def find_by_email(self, email: str) -> Optional[Dict]:
        """Find user by email."""
        document = self.collection.find_one({"email": email})
        if document:
            return self._transform_document(document)
        return None
    
    def count_admins(self) -> int:
        """Count number of admin users."""
        return self.collection.count_documents({"role": "admin"})

class RepositoryFactory(BaseFactory):
    """
    Factory for creating repository instances.
    """
    
    def __init__(self):
        self._repositories = {
            "mongo": MongoRepository,
            "product": ProductRepository,
            "user": UserRepository,
        }
    
    def create(self, repo_type: str, collection: Collection, *args, **kwargs) -> BaseRepository:
        """
        Create a repository instance.
        
        Args:
            repo_type: Type of repository to create
            collection: MongoDB collection instance
            
        Returns:
            Repository instance
            
        Raises:
            ValueError: If repository type not supported
        """
        if repo_type not in self._repositories:
            raise ValueError(f"Repository type '{repo_type}' not supported. Available: {list(self._repositories.keys())}")
        
        repository_class = self._repositories[repo_type]
        return repository_class(collection, *args, **kwargs)
    
    def get_available_types(self) -> list:
        """Get list of available repository types."""
        return list(self._repositories.keys())
