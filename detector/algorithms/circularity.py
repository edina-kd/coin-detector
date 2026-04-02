"""
Morphological coin-detection pipeline (this work).

OpenCV pipeline: blur, HSV background mask, Otsu threshold, dilation/erosion,
Canny edges, external contours, circularity filter
C = (4π × Area) / (Perimeter²), default threshold ≥ 0.85.
"""

import cv2
import numpy as np
import time


class CircularityDetector:
    """Morphological approach to coin-shaped objects: pipeline + circularity filter."""
    
    def __init__(self, circularity_threshold=0.85):
        """
        Initialize morphological circularity detector
        
        Args:
            circularity_threshold: Minimum circularity score (0.85 default)
                                 Empirically determined threshold for coin-like circles
        """
        self.circularity_threshold = circularity_threshold
        self.name = "Morphological approach (this work)"
    
    def calculate_circularity(self, contour):
        """
        Calculate circularity score for a contour
        
        Args:
            contour: OpenCV contour
            
        Returns:
            float: Circularity score (0 to 1)
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return 0
        
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        return circularity
    
    def detect(self, image):
        """
        Detect coins using morphological circularity-based algorithm
        
        This method implements the complete pipeline:
        1. Blur (noise reduction)
        2. HSV conversion and background removal
        3. Otsu's thresholding (adaptive binarization)
        4. Morphological operations (dilate → erode)
        5. Canny edge detection
        6. Contour extraction (external contours only)
        7. Circularity filtering (threshold = 0.85)
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            dict: {
                'coins': list of detected coins (x, y, radius),
                'processing_time': time in milliseconds,
                'annotated_image': image with circles drawn
            }
        """
        start_time = time.time()
        
        # Make a copy for annotation
        annotated = image.copy()
        
        # Step 1: Blur (3x3 kernel for noise reduction)
        # Using cv2.blur as in original implementation
        blurred = cv2.blur(image, (3, 3))
        
        # Step 2: Convert BGR to HSV
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # Step 3: Background removal (returns binary mask)
        # This removes the background, keeping only objects with saturation > 70
        mask = cv2.inRange(hsv, (0, 60, 0), (255, 255, 255))
        
        # Step 4: Otsu's thresholding ON THE MASK (not on original grayscale)
        # This further refines the binary mask
        _, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # Step 5: Morphological operations
        # Dilation
        kernel_dilate = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(thresh, kernel_dilate, iterations=4)
        
        # Erosion
        kernel_erode = np.ones((3, 3), np.uint8)
        eroded = cv2.erode(dilated, kernel_erode, iterations=1)
        
        # Step 6: Canny edge detection (thresholds: 100, 200 as in original)
        edges = cv2.Canny(eroded, 100, 200)
        
        # Step 7: Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Step 8: Filter by circularity
        detected_coins = []
        
        for contour in contours:
            # Calculate circularity
            circularity = self.calculate_circularity(contour)
            
            # Filter by circularity threshold
            if circularity >= self.circularity_threshold:
                # Get enclosing circle
                (x, y), radius = cv2.minEnclosingCircle(contour)
                
                # Filter by size (avoid noise)
                if radius > 15 and radius < 200:
                    detected_coins.append({
                        'center_x': int(x),
                        'center_y': int(y),
                        'radius': int(radius),
                        'circularity': float(circularity)
                    })
                    
                    # Draw on annotated image
                    cv2.circle(annotated, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                    cv2.circle(annotated, (int(x), int(y)), 3, (0, 0, 255), -1)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return {
            'coins': detected_coins,
            'processing_time': processing_time,
            'annotated_image': annotated
        }

