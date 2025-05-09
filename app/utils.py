from flask import current_app

def validate_rating(rating):
    """
    Validate rating value
    
    Args:
        rating: Rating value to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        return False, "Rating must be a number"
        
    if not 1 <= rating <= 5:
        return False, "Rating must be between 1 and 5"
        
    return True, None

def validate_pagination_params(page, per_page):
    """
    Validate pagination parameters
    
    Args:
        page: Page number
        per_page: Items per page
        
    Returns:
        tuple: (page, per_page, error_message)
    """
    if page < 1:
        return None, None, "Page must be greater than 0"
        
    if per_page < 1:
        return None, None, "Items per page must be greater than 0"
        
    # Limit per_page to prevent excessive data loading
    per_page = min(per_page, current_app.config['MAX_PER_PAGE'])
    
    return page, per_page, None
