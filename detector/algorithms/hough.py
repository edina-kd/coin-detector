"""
Hough Circle Transform Algorithm
Classical computer vision approach for circle detection

Uses parameter space voting to detect circles
"""

import cv2
import numpy as np
import time


class HoughDetector:
    """
    Coin detection using Hough Circle Transform
    """
    
    def __init__(self, dp=1.2, minDist=50, param1=50, param2=50, 
                 minRadius=100, maxRadius=150):
        """
        Initialize Hough detector
        
        Args:
            dp: Inverse ratio of accumulator resolution (1.2 default)
            minDist: Minimum distance between circle centers (50 default - increased to avoid overlaps)
            param1: Canny edge threshold (50 default)
            param2: Accumulator threshold (50 default - increased to reduce false positives)
            minRadius: Minimum circle radius in pixels (20 default - increased to filter small noise)
            maxRadius: Maximum circle radius in pixels (150 default - increased for larger coins)
        """
        self.dp = dp
        self.minDist = minDist
        self.param1 = param1
        self.param2 = param2
        self.minRadius = minRadius
        self.maxRadius = maxRadius
        self.name = "Hough Circle Transform"
    
    def detect(self, image):
        """
        Detect coins using Hough Circle Transform
        
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
        
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Step 2: Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Step 3: Median blur for noise reduction
        median_blurred = cv2.medianBlur(blurred, 5)
        
        # Step 4: Hough Circle Transform
        circles = cv2.HoughCircles(
            median_blurred,
            method=cv2.HOUGH_GRADIENT,
            dp=self.dp,
            minDist=self.minDist,
            param1=self.param1,
            param2=self.param2,
            minRadius=self.minRadius,
            maxRadius=self.maxRadius
        )
        
        detected_coins = []
        
        if circles is not None:
            # Convert to integer coordinates
            circles = np.uint16(np.around(circles))
            
            for circle in circles[0, :]:
                x, y, radius = circle
                
                detected_coins.append({
                    'center_x': int(x),
                    'center_y': int(y),
                    'radius': int(radius)
                })
                
                # Draw circles on annotated image
                cv2.circle(annotated, (x, y), radius, (0, 255, 0), 2)
                cv2.circle(annotated, (x, y), 3, (0, 0, 255), -1)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return {
            'coins': detected_coins,
            'processing_time': processing_time,
            'annotated_image': annotated
        }

