from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .base_factory import BaseFactory
from .repository_factory import BaseRepository

class BaseService(ABC):
    """
    Abstract base service class defining business logic operations.
    """
    
    def __init__(self, repository: BaseRepository):
        self.repository = repository
    
    @abstractmethod
    def get_all(self, page: int = 1, limit: int = 10, **kwargs) -> List[Dict]:
        """Get all items with pagination."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Dict]:
        """Get item by ID."""
        pass
    
    @abstractmethod
    def create(self, data: Dict) -> Dict:
        """Create new item."""
        pass
    
    @abstractmethod
    def update(self, id: str, data: Dict) -> Dict:
        """Update item."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> Dict:
        """Delete item."""
        pass

class ProductService(BaseService):
    """
    Product service implementing business logic for product operations.
    """
    
    def get_all(self, page: int = 1, limit: int = 10, **kwargs) -> List[Dict]:
        """Get all products with pagination."""
        skip = (page - 1) * limit
        return self.repository.find_all(skip=skip, limit=limit)
    
    def get_by_id(self, id: str) -> Optional[Dict]:
        """Get product by ID."""
        return self.repository.find_by_id(id)
    
    def create(self, data: Dict) -> Dict:
        """Create new product."""
        result = self.repository.create(data)
        if result["success"]:
            return {
                "success": True,
                "message": "Product added successfully",
                "id": result["id"]
            }
        return {"success": False, "message": "Failed to create product"}
    
    def update(self, id: str, data: Dict) -> Dict:
        """Update product."""
        success = self.repository.update(id, data)
        if success:
            return {"success": True, "message": "Product updated successfully"}
        return {"success": False, "message": "Product not found or update failed"}
    
    def delete(self, id: str) -> Dict:
        """Delete product."""
        success = self.repository.delete(id)
        if success:
            return {"success": True, "message": "Product deleted successfully"}
        return {"success": False, "message": "Product not found"}
    
    def search_products(self, query: str) -> List[Dict]:
        """Search products by name."""
        if hasattr(self.repository, 'search_by_name'):
            return self.repository.search_by_name(query)
        # Fallback to generic search
        search_query = {"name": {"$regex": query, "$options": "i"}}
        return self.repository.search(search_query)
    
    def filter_products(self, filters: Dict) -> List[Dict]:
        """Filter products based on criteria."""
        if hasattr(self.repository, 'filter_products'):
            return self.repository.filter_products(filters)
        # Fallback implementation
        return self.repository.find_all(filters=filters)

class UserService(BaseService):
    """
    User service implementing business logic for user operations.
    """
    
    def get_all(self, page: int = 1, limit: int = 10, **kwargs) -> List[Dict]:
        """Get all users with pagination."""
        skip = (page - 1) * limit
        return self.repository.find_all(skip=skip, limit=limit)
    
    def get_by_id(self, id: str) -> Optional[Dict]:
        """Get user by ID."""
        return self.repository.find_by_id(id)
    
    def create(self, data: Dict) -> Dict:
        """Create new user."""
        result = self.repository.create(data)
        if result["success"]:
            return {
                "success": True,
                "message": "User created successfully",
                "id": result["id"]
            }
        return {"success": False, "message": "Failed to create user"}
    
    def update(self, id: str, data: Dict) -> Dict:
        """Update user."""
        success = self.repository.update(id, data)
        if success:
            return {"success": True, "message": "User updated successfully"}
        return {"success": False, "message": "User not found or update failed"}
    
    def delete(self, id: str) -> Dict:
        """Delete user."""
        success = self.repository.delete(id)
        if success:
            return {"success": True, "message": "User deleted successfully"}
        return {"success": False, "message": "User not found"}
    
    def find_by_email(self, email: str) -> Optional[Dict]:
        """Find user by email."""
        if hasattr(self.repository, 'find_by_email'):
            return self.repository.find_by_email(email)
        # Fallback to generic search
        users = self.repository.search({"email": email})
        return users[0] if users else None
    
    def count_admins(self) -> int:
        """Count admin users."""
        if hasattr(self.repository, 'count_admins'):
            return self.repository.count_admins()
        # Fallback implementation
        admins = self.repository.search({"role": "admin"})
        return len(admins)

class OrderService(BaseService):
    """
    Order service implementing business logic for order operations.
    """
    
    def get_all(self, page: int = 1, limit: int = 10, **kwargs) -> List[Dict]:
        """Get all orders with pagination."""
        skip = (page - 1) * limit
        filters = kwargs.get('filters', {})
        return self.repository.find_all(skip=skip, limit=limit, filters=filters)
    
    def get_by_id(self, id: str) -> Optional[Dict]:
        """Get order by ID."""
        return self.repository.find_by_id(id)
    
    def create(self, data: Dict) -> Dict:
        """Create new order."""
        result = self.repository.create(data)
        if result["success"]:
            return {
                "success": True,
                "message": "Order created successfully",
                "id": result["id"]
            }
        return {"success": False, "message": "Failed to create order"}
    
    def update(self, id: str, data: Dict) -> Dict:
        """Update order."""
        success = self.repository.update(id, data)
        if success:
            return {"success": True, "message": "Order updated successfully"}
        return {"success": False, "message": "Order not found or update failed"}
    
    def delete(self, id: str) -> Dict:
        """Delete order."""
        success = self.repository.delete(id)
        if success:
            return {"success": True, "message": "Order deleted successfully"}
        return {"success": False, "message": "Order not found"}
    
    def get_user_orders(self, user_id: str) -> List[Dict]:
        """Get orders for a specific user."""
        return self.repository.search({"user_id": user_id})

class CartService(BaseService):
    """
    Cart service implementing business logic for cart operations.
    """
    
    def get_all(self, page: int = 1, limit: int = 10, **kwargs) -> List[Dict]:
        """Get all carts with pagination."""
        skip = (page - 1) * limit
        return self.repository.find_all(skip=skip, limit=limit)
    
    def get_by_id(self, id: str) -> Optional[Dict]:
        """Get cart by ID."""
        return self.repository.find_by_id(id)
    
    def create(self, data: Dict) -> Dict:
        """Create new cart."""
        result = self.repository.create(data)
        if result["success"]:
            return {
                "success": True,
                "message": "Cart created successfully",
                "id": result["id"]
            }
        return {"success": False, "message": "Failed to create cart"}
    
    def update(self, id: str, data: Dict) -> Dict:
        """Update cart."""
        success = self.repository.update(id, data)
        if success:
            return {"success": True, "message": "Cart updated successfully"}
        return {"success": False, "message": "Cart not found or update failed"}
    
    def delete(self, id: str) -> Dict:
        """Delete cart."""
        success = self.repository.delete(id)
        if success:
            return {"success": True, "message": "Cart deleted successfully"}
        return {"success": False, "message": "Cart not found"}
    
    def get_user_cart(self, user_id: str) -> Optional[Dict]:
        """Get cart for a specific user."""
        carts = self.repository.search({"user_id": user_id})
        return carts[0] if carts else None

class ServiceFactory(BaseFactory):
    """
    Factory for creating service instances.
    """
    
    def __init__(self):
        self._services = {
            "product": ProductService,
            "user": UserService,
            "order": OrderService,
            "cart": CartService,
        }
    
    def create(self, service_type: str, repository: BaseRepository, *args, **kwargs) -> BaseService:
        """
        Create a service instance.
        
        Args:
            service_type: Type of service to create
            repository: Repository instance for the service
            
        Returns:
            Service instance
            
        Raises:
            ValueError: If service type not supported
        """
        if service_type not in self._services:
            raise ValueError(f"Service type '{service_type}' not supported. Available: {list(self._services.keys())}")
        
        service_class = self._services[service_type]
        return service_class(repository, *args, **kwargs)
    
    def get_available_types(self) -> list:
        """Get list of available service types."""
        return list(self._services.keys())
