"""
Visualization Utilities
Functions for drawing and annotating detection results
"""

import cv2
import numpy as np


def draw_coins(image, coins, color=(0, 255, 0), thickness=2):
    """
    Draw detected coins on image
    
    Args:
        image: Input image (will be copied)
        coins: List of detected coins [{'center_x': x, 'center_y': y, 'radius': r}, ...]
        color: Circle color in BGR (green default)
        thickness: Line thickness (2 default)
        
    Returns:
        numpy.ndarray: Annotated image
    """
    annotated = image.copy()
    
    for coin in coins:
        center = (coin['center_x'], coin['center_y'])
        radius = coin['radius']
        
        # Draw circle
        cv2.circle(annotated, center, radius, color, thickness)
        # Draw center point
        cv2.circle(annotated, center, 3, (0, 0, 255), -1)
    
    return annotated


def add_text_overlay(image, text, position=(10, 30), 
                     font_scale=0.7, color=(255, 255, 255), thickness=2):
    """
    Add text overlay to image
    
    Args:
        image: Input image
        text: Text to display
        position: Text position (x, y)
        font_scale: Font size
        color: Text color in BGR
        thickness: Text thickness
        
    Returns:
        numpy.ndarray: Image with text overlay
    """
    annotated = image.copy()
    
    # Add background rectangle for better readability
    (text_width, text_height), _ = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
    )
    
    cv2.rectangle(
        annotated, 
        (position[0] - 5, position[1] - text_height - 5),
        (position[0] + text_width + 5, position[1] + 5),
        (0, 0, 0),
        -1
    )
    
    # Add text
    cv2.putText(
        annotated,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness
    )
    
    return annotated


def create_comparison_image(images_with_labels, max_width=400):
    """
    Create side-by-side comparison of multiple images
    
    Args:
        images_with_labels: List of tuples [(image, label), ...]
        max_width: Maximum width for each image
        
    Returns:
        numpy.ndarray: Combined comparison image
    """
    if not images_with_labels:
        return None
    
    # Resize all images to same height
    resized_images = []
    max_height = 0
    
    for img, label in images_with_labels:
        h, w = img.shape[:2]
        scale = min(max_width / w, 1.0)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        resized = cv2.resize(img, (new_w, new_h))
        # Add label
        labeled = add_text_overlay(resized, label, position=(10, 30))
        resized_images.append(labeled)
        max_height = max(max_height, new_h)
    
    # Make all images same height
    padded_images = []
    for img in resized_images:
        h, w = img.shape[:2]
        if h < max_height:
            # Add padding at bottom
            padding = np.zeros((max_height - h, w, 3), dtype=np.uint8)
            padded = np.vstack([img, padding])
            padded_images.append(padded)
        else:
            padded_images.append(img)
    
    # Concatenate horizontally
    comparison = np.hstack(padded_images)
    
    return comparison


def save_image(image, output_path):
    """
    Save image to file
    
    Args:
        image: Image to save
        output_path: Output file path
        
    Returns:
        bool: True if successful
    """
    try:
        cv2.imwrite(str(output_path), image)
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

