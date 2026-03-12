# SmartCurriculum - Input Validators
# Validation utilities for user input

import re
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 255:
        return False, "Email too long (max 255 characters)"
    
    return True, None


def validate_password(password: str, min_length: int = 6) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Args:
        password: Password string to validate
        min_length: Minimum required length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    
    if len(password) > 128:
        return False, "Password too long (max 128 characters)"
    
    return True, None


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate user name.
    
    Args:
        name: Name string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Name is required"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if len(name) > 255:
        return False, "Name too long (max 255 characters)"
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, None


def validate_semester(semester: int) -> Tuple[bool, Optional[str]]:
    """
    Validate semester number.
    
    Args:
        semester: Semester number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if semester is None:
        return False, "Semester is required"
    
    try:
        semester = int(semester)
    except (ValueError, TypeError):
        return False, "Semester must be a number"
    
    if semester < 1 or semester > 12:
        return False, "Semester must be between 1 and 12"
    
    return True, None


def validate_skill_level(level: str) -> Tuple[bool, Optional[str]]:
    """
    Validate skill level.
    
    Args:
        level: Skill level string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
    
    if not level:
        return True, None  # Optional field
    
    if level.lower() not in valid_levels:
        return False, f"Skill level must be one of: {', '.join(valid_levels)}"
    
    return True, None


def validate_career_goal(goal: str) -> Tuple[bool, Optional[str]]:
    """
    Validate career goal.
    
    Args:
        goal: Career goal string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_goals = ['placement', 'higher_studies', 'startup', 'research']
    
    if not goal:
        return True, None  # Optional field
    
    if goal.lower() not in valid_goals:
        return False, f"Career goal must be one of: {', '.join(valid_goals)}"
    
    return True, None


def validate_learning_pace(pace: str) -> Tuple[bool, Optional[str]]:
    """
    Validate learning pace.
    
    Args:
        pace: Learning pace string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_paces = ['slow', 'moderate', 'fast']
    
    if not pace:
        return True, None  # Optional field
    
    if pace.lower() not in valid_paces:
        return False, f"Learning pace must be one of: {', '.join(valid_paces)}"
    
    return True, None


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize text input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = text.strip()
    
    # Limit length
    sanitized = sanitized[:max_length]
    
    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')
    
    return sanitized


def validate_json_list(data, field_name: str = "list") -> Tuple[bool, Optional[str]]:
    """
    Validate that data is a valid list.
    
    Args:
        data: Data to validate
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if data is None:
        return True, None  # Optional
    
    if not isinstance(data, list):
        return False, f"{field_name} must be a list"
    
    # Validate each item is a string
    for item in data:
        if not isinstance(item, str):
            return False, f"All items in {field_name} must be strings"
    
    return True, None
