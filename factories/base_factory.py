from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar

T = TypeVar('T')

class BaseFactory(ABC):
    """
    Abstract base factory class that defines the interface for all factories.
    Implements the Factory Method pattern.
    """
    
    @abstractmethod
    def create(self, factory_type: str, *args, **kwargs) -> Any:
        """
        Abstract method to create objects based on type.
        
        Args:
            factory_type: String identifier for the type of object to create
            *args: Positional arguments for object creation
            **kwargs: Keyword arguments for object creation
            
        Returns:
            Created object instance
        """
        pass
    
    @abstractmethod
    def get_available_types(self) -> list:
        """
        Get list of available types this factory can create.
        
        Returns:
            List of available type identifiers
        """
        pass

class FactoryRegistry:
    """
    Registry to manage multiple factories and provide a centralized access point.
    Implements the Abstract Factory pattern.
    """
    
    _factories: Dict[str, BaseFactory] = {}
    
    @classmethod
    def register_factory(cls, name: str, factory: BaseFactory) -> None:
        """
        Register a factory with a given name.
        
        Args:
            name: Factory identifier
            factory: Factory instance to register
        """
        cls._factories[name] = factory
    
    @classmethod
    def get_factory(cls, name: str) -> BaseFactory:
        """
        Get a registered factory by name.
        
        Args:
            name: Factory identifier
            
        Returns:
            Factory instance
            
        Raises:
            ValueError: If factory not found
        """
        if name not in cls._factories:
            raise ValueError(f"Factory '{name}' not registered. Available: {list(cls._factories.keys())}")
        return cls._factories[name]
    
    @classmethod
    def list_factories(cls) -> list:
        """
        Get list of all registered factory names.
        
        Returns:
            List of factory names
        """
        return list(cls._factories.keys())
