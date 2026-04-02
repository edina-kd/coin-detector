"""
Image Preprocessing Utilities
Common preprocessing functions for coin detection
"""

import cv2
import numpy as np


def load_image(image_path):
    """
    Load image from file path
    
    Args:
        image_path: Path to image file
        
    Returns:
        numpy.ndarray: Loaded image in BGR format
    """
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return image


def resize_image(image, max_width=1200, max_height=1600):
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: Input image
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        numpy.ndarray: Resized image
    """
    height, width = image.shape[:2]
    
    # Calculate scaling factor
    scale = min(max_width / width, max_height / height, 1.0)
    
    if scale < 1.0:
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized
    
    return image


def validate_image(image, min_width=500, min_height=500, max_width=5000, max_height=5000):
    """
    Validate image dimensions
    
    Args:
        image: Input image
        min_width: Minimum width
        min_height: Minimum height
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        tuple: (is_valid, error_message)
    """
    height, width = image.shape[:2]
    
    if width < min_width or height < min_height:
        return False, f"Image too small. Minimum dimensions: {min_width}×{min_height}px"
    
    if width > max_width or height > max_height:
        return False, f"Image too large. Maximum dimensions: {max_width}×{max_height}px"
    
    return True, None


def enhance_image(image):
    """
    Enhance image quality for better detection
    
    Args:
        image: Input image
        
    Returns:
        numpy.ndarray: Enhanced image
    """
    # Apply bilateral filter (edge-preserving smoothing)
    enhanced = cv2.bilateralFilter(image, 9, 75, 75)
    return enhanced

