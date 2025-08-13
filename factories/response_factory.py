from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .base_factory import BaseFactory
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class BaseResponseFormatter(ABC):
    """
    Abstract base class for response formatting strategies.
    """
    
    @abstractmethod
    def success_response(self, data: Any, message: str = "Success", status_code: int = 200) -> Dict:
        """Format successful response."""
        pass
    
    @abstractmethod
    def error_response(self, message: str, status_code: int = 400, details: Any = None) -> Dict:
        """Format error response."""
        pass
    
    @abstractmethod
    def paginated_response(self, data: List, page: int, limit: int, total: int = None) -> Dict:
        """Format paginated response."""
        pass

class StandardResponseFormatter(BaseResponseFormatter):
    """
    Standard JSON response formatter.
    """
    
    def success_response(self, data: Any, message: str = "Success", status_code: int = 200) -> Dict:
        """Format successful response with standard structure."""
        return {
            "success": True,
            "message": message,
            "data": data,
            "status_code": status_code
        }
    
    def error_response(self, message: str, status_code: int = 400, details: Any = None) -> Dict:
        """Format error response with standard structure."""
        response = {
            "success": False,
            "message": message,
            "status_code": status_code
        }
        if details:
            response["details"] = details
        return response
    
    def paginated_response(self, data: List, page: int, limit: int, total: int = None) -> Dict:
        """Format paginated response with metadata."""
        response = {
            "success": True,
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "count": len(data)
            }
        }
        if total is not None:
            response["pagination"]["total"] = total
            response["pagination"]["pages"] = (total + limit - 1) // limit
        return response

class APIResponseFormatter(BaseResponseFormatter):
    """
    API-specific response formatter with additional metadata.
    """
    
    def success_response(self, data: Any, message: str = "Success", status_code: int = 200) -> Dict:
        """Format API success response."""
        return {
            "status": "success",
            "message": message,
            "result": data,
            "code": status_code,
            "timestamp": self._get_timestamp()
        }
    
    def error_response(self, message: str, status_code: int = 400, details: Any = None) -> Dict:
        """Format API error response."""
        response = {
            "status": "error",
            "message": message,
            "code": status_code,
            "timestamp": self._get_timestamp()
        }
        if details:
            response["error_details"] = details
        return response
    
    def paginated_response(self, data: List, page: int, limit: int, total: int = None) -> Dict:
        """Format API paginated response."""
        response = {
            "status": "success",
            "result": {
                "items": data,
                "pagination": {
                    "current_page": page,
                    "per_page": limit,
                    "count": len(data)
                }
            },
            "timestamp": self._get_timestamp()
        }
        if total is not None:
            response["result"]["pagination"]["total_items"] = total
            response["result"]["pagination"]["total_pages"] = (total + limit - 1) // limit
        return response
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime, UTC
        return datetime.now(UTC).isoformat()

class ResponseService:
    """
    Service for handling API responses with different formatters.
    """
    
    def __init__(self, formatter: BaseResponseFormatter):
        self.formatter = formatter
    
    def success(self, data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
        """Return successful JSON response."""
        response_data = self.formatter.success_response(data, message, status_code)
        return JSONResponse(content=response_data, status_code=status_code)
    
    def error(self, message: str, status_code: int = 400, details: Any = None) -> HTTPException:
        """Return HTTP exception with formatted error."""
        error_data = self.formatter.error_response(message, status_code, details)
        raise HTTPException(status_code=status_code, detail=error_data)
    
    def paginated(self, data: List, page: int, limit: int, total: int = None, status_code: int = 200) -> JSONResponse:
        """Return paginated JSON response."""
        response_data = self.formatter.paginated_response(data, page, limit, total)
        return JSONResponse(content=response_data, status_code=status_code)
    
    def not_found(self, resource: str = "Resource") -> HTTPException:
        """Return 404 not found error."""
        return self.error(f"{resource} not found", 404)
    
    def unauthorized(self, message: str = "Unauthorized access") -> HTTPException:
        """Return 401 unauthorized error."""
        return self.error(message, 401)
    
    def forbidden(self, message: str = "Access forbidden") -> HTTPException:
        """Return 403 forbidden error."""
        return self.error(message, 403)
    
    def validation_error(self, details: Any) -> HTTPException:
        """Return 422 validation error."""
        return self.error("Validation failed", 422, details)
    
    def server_error(self, message: str = "Internal server error") -> HTTPException:
        """Return 500 server error."""
        return self.error(message, 500)

class ResponseFactory(BaseFactory):
    """
    Factory for creating response formatters and services.
    """
    
    def __init__(self):
        self._formatters = {
            "standard": StandardResponseFormatter,
            "api": APIResponseFormatter,
        }
        self._services = {
            "response": ResponseService,
        }
    
    def create_formatter(self, formatter_type: str, *args, **kwargs) -> BaseResponseFormatter:
        """
        Create a response formatter.
        
        Args:
            formatter_type: Type of formatter to create
            
        Returns:
            Response formatter instance
            
        Raises:
            ValueError: If formatter type not supported
        """
        if formatter_type not in self._formatters:
            raise ValueError(f"Formatter type '{formatter_type}' not supported. Available: {list(self._formatters.keys())}")
        
        formatter_class = self._formatters[formatter_type]
        return formatter_class(*args, **kwargs)
    
    def create_service(self, formatter: BaseResponseFormatter) -> ResponseService:
        """
        Create a response service.
        
        Args:
            formatter: Response formatter to use
            
        Returns:
            Response service instance
        """
        return ResponseService(formatter)
    
    def create(self, factory_type: str, *args, **kwargs) -> Any:
        """
        Create response-related objects.
        
        Args:
            factory_type: Type of object to create ('formatter' or 'service')
            
        Returns:
            Created object instance
        """
        if factory_type == "formatter":
            formatter_type = args[0] if args else kwargs.get("formatter_type")
            return self.create_formatter(formatter_type, *args[1:], **{k: v for k, v in kwargs.items() if k != "formatter_type"})
        elif factory_type == "service":
            return self.create_service(*args, **kwargs)
        else:
            raise ValueError(f"Factory type '{factory_type}' not supported. Available: ['formatter', 'service']")
    
    def get_available_types(self) -> list:
        """Get list of available factory types."""
        return ["formatter", "service"]
    
    def get_available_formatters(self) -> list:
        """Get list of available response formatters."""
        return list(self._formatters.keys())
