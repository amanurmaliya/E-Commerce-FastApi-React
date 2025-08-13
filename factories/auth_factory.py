from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from .base_factory import BaseFactory
import jwt
import os
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext

class BaseAuthStrategy(ABC):
    """
    Abstract base class for authentication strategies.
    """
    
    @abstractmethod
    def authenticate(self, credentials: Dict) -> Optional[Dict]:
        """Authenticate user with given credentials."""
        pass
    
    @abstractmethod
    def generate_token(self, user_data: Dict) -> str:
        """Generate authentication token."""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode authentication token."""
        pass
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash password for storage."""
        pass
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        pass

class JWTAuthStrategy(BaseAuthStrategy):
    """
    JWT-based authentication strategy.
    """
    
    def __init__(self, secret_key: str = None, algorithm: str = "HS256"):
        self.secret_key = secret_key or os.getenv("JWT_SECRET", "secret123")
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def authenticate(self, credentials: Dict) -> Optional[Dict]:
        """
        Authenticate user with email/password credentials.
        Note: This method should be used with a user service/repository.
        """
        # This is a placeholder - actual authentication should involve
        # checking credentials against database via service layer
        return None
    
    def generate_token(self, user_data: Dict, expires_minutes: int = 60) -> str:
        """Generate JWT token for user."""
        to_encode = user_data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=expires_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against bcrypt hash."""
        return self.pwd_context.verify(plain_password, hashed_password)

class OAuth2AuthStrategy(BaseAuthStrategy):
    """
    OAuth2-based authentication strategy (placeholder for future implementation).
    """
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def authenticate(self, credentials: Dict) -> Optional[Dict]:
        """Authenticate using OAuth2 flow."""
        # Placeholder for OAuth2 implementation
        raise NotImplementedError("OAuth2 authentication not implemented yet")
    
    def generate_token(self, user_data: Dict) -> str:
        """Generate OAuth2 token."""
        # Placeholder for OAuth2 token generation
        raise NotImplementedError("OAuth2 token generation not implemented yet")
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify OAuth2 token."""
        # Placeholder for OAuth2 token verification
        raise NotImplementedError("OAuth2 token verification not implemented yet")
    
    def hash_password(self, password: str) -> str:
        """OAuth2 doesn't typically hash passwords locally."""
        raise NotImplementedError("Password hashing not applicable for OAuth2")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """OAuth2 doesn't typically verify passwords locally."""
        raise NotImplementedError("Password verification not applicable for OAuth2")

class AuthService:
    """
    Authentication service that uses different auth strategies.
    """
    
    def __init__(self, auth_strategy: BaseAuthStrategy, user_service=None):
        self.auth_strategy = auth_strategy
        self.user_service = user_service
    
    def login(self, email: str, password: str) -> Optional[Dict]:
        """
        Login user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dict with access token if successful, None otherwise
        """
        if not self.user_service:
            return None
        
        # Find user by email
        user = self.user_service.find_by_email(email)
        if not user:
            return None
        
        # Verify password
        if not self.auth_strategy.verify_password(password, user.get("password", "")):
            return None
        
        # Generate token
        token_data = {
            "user_id": user["id"],
            "email": user["email"],
            "role": user.get("role", "user")
        }
        token = self.auth_strategy.generate_token(token_data)
        
        return {"access_token": token, "token_type": "bearer"}
    
    def register(self, user_data: Dict) -> Dict:
        """
        Register new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            Dict with registration result
        """
        if not self.user_service:
            return {"success": False, "message": "User service not available"}
        
        # Check if user already exists
        existing_user = self.user_service.find_by_email(user_data.get("email", ""))
        if existing_user:
            return {"success": False, "message": "Email already exists"}
        
        # Hash password
        user_data["password"] = self.auth_strategy.hash_password(user_data["password"])
        user_data["role"] = user_data.get("role", "user")
        
        # Create user
        result = self.user_service.create(user_data)
        if result["success"]:
            return {
                "success": True,
                "message": "User registered successfully",
                "user": {
                    "id": result["id"],
                    "email": user_data["email"],
                    "name": user_data.get("name", ""),
                    "role": user_data["role"]
                }
            }
        
        return {"success": False, "message": "Registration failed"}
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify authentication token."""
        return self.auth_strategy.verify_token(token)
    
    def get_current_user(self, token: str) -> Optional[Dict]:
        """
        Get current user from token.
        
        Args:
            token: Authentication token
            
        Returns:
            User data if token is valid, None otherwise
        """
        payload = self.verify_token(token)
        if not payload:
            return None
        
        if self.user_service:
            return self.user_service.get_by_id(payload.get("user_id"))
        
        return payload

class AuthFactory(BaseFactory):
    """
    Factory for creating authentication-related objects.
    """
    
    def __init__(self):
        self._auth_strategies = {
            "jwt": JWTAuthStrategy,
            "oauth2": OAuth2AuthStrategy,
        }
        self._services = {
            "auth": AuthService,
        }
    
    def create_auth_strategy(self, strategy_type: str, *args, **kwargs) -> BaseAuthStrategy:
        """
        Create an authentication strategy.
        
        Args:
            strategy_type: Type of auth strategy to create
            
        Returns:
            Auth strategy instance
            
        Raises:
            ValueError: If strategy type not supported
        """
        if strategy_type not in self._auth_strategies:
            raise ValueError(f"Auth strategy '{strategy_type}' not supported. Available: {list(self._auth_strategies.keys())}")
        
        strategy_class = self._auth_strategies[strategy_type]
        return strategy_class(*args, **kwargs)
    
    def create_auth_service(self, auth_strategy: BaseAuthStrategy, user_service=None) -> AuthService:
        """
        Create an authentication service.
        
        Args:
            auth_strategy: Authentication strategy to use
            user_service: User service for database operations
            
        Returns:
            Auth service instance
        """
        return AuthService(auth_strategy, user_service)
    
    def create(self, factory_type: str, *args, **kwargs) -> Any:
        """
        Create auth-related objects.
        
        Args:
            factory_type: Type of object to create ('strategy' or 'service')
            
        Returns:
            Created object instance
        """
        if factory_type == "strategy":
            strategy_type = args[0] if args else kwargs.get("strategy_type")
            return self.create_auth_strategy(strategy_type, *args[1:], **{k: v for k, v in kwargs.items() if k != "strategy_type"})
        elif factory_type == "service":
            return self.create_auth_service(*args, **kwargs)
        else:
            raise ValueError(f"Factory type '{factory_type}' not supported. Available: ['strategy', 'service']")
    
    def get_available_types(self) -> list:
        """Get list of available factory types."""
        return ["strategy", "service"]
    
    def get_available_strategies(self) -> list:
        """Get list of available auth strategies."""
        return list(self._auth_strategies.keys())
