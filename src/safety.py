# src/safety.py

def is_safe_request(text: str) -> bool:
    """
    Checks if the input text contains unsafe or blocked keywords.
    """
    if not text:
        return False
        
    lowered = text.lower()
    # Basic blocked terms list as per exam requirements [cite: 750]
    blocked = ["weapon", "bomb", "explicit", "porn", "hate", "self-harm", "suicide"]
    
    # Return False if any blocked word is found
    return not any(b in lowered for b in blocked)