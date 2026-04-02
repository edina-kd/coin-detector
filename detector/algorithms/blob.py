"""
Blob Detection Algorithm
Feature-based approach using SimpleBlobDetector

Detects blobs (circular regions) based on multiple criteria:
- Area, Circularity, Convexity, Inertia
"""

import cv2
import numpy as np
import time


class BlobDetector:
    """
    Coin detection using Blob Detection
    """
    
    def __init__(self, minArea=300, maxArea=50000, minCircularity=0.7, 
                 minConvexity=0.8, minInertiaRatio=0.4):
        """
        Initialize blob detector
        
        Args:
            minArea: Minimum blob area (300 default - lowered to catch smaller coins)
            maxArea: Maximum blob area (50000 default - increased for larger coins)
            minCircularity: Minimum circularity (0.7 default - relaxed)
            minConvexity: Minimum convexity (0.8 default - relaxed)
            minInertiaRatio: Minimum inertia ratio (0.4 default - relaxed)
        """
        self.minArea = minArea
        self.maxArea = maxArea
        self.minCircularity = minCircularity
        self.minConvexity = minConvexity
        self.minInertiaRatio = minInertiaRatio
        self.name = "Blob Detection"
        
        # Set up blob detector parameters
        params = cv2.SimpleBlobDetector_Params()
        
        # Change thresholds (important for blob detection)
        params.minThreshold = 10
        params.maxThreshold = 200
        params.thresholdStep = 10
        
        # Filter by Area
        params.filterByArea = True
        params.minArea = self.minArea
        params.maxArea = self.maxArea
        
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = self.minCircularity
        
        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = self.minConvexity
        
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = self.minInertiaRatio
        
        # Filter by color (look for dark blobs after inversion)
        params.filterByColor = True
        params.blobColor = 0  # 0 for dark blobs, 255 for bright blobs
        
        # Create detector
        self.detector = cv2.SimpleBlobDetector_create(params)
    
    def detect(self, image):
        """
        Detect coins using blob detection
        
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
        
        # Step 2: Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Step 3: Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(blurred)
        
        # Step 4: Invert image (SimpleBlobDetector looks for dark blobs)
        inverted = cv2.bitwise_not(enhanced)
        
        # Step 5: Detect blobs
        keypoints = self.detector.detect(inverted)
        
        detected_coins = []
        
        for kp in keypoints:
            x, y = kp.pt
            radius = int(kp.size / 2)  # size is diameter
            
            detected_coins.append({
                'center_x': int(x),
                'center_y': int(y),
                'radius': radius
            })
            
            # Draw circles on annotated image
            cv2.circle(annotated, (int(x), int(y)), radius, (0, 255, 0), 2)
            cv2.circle(annotated, (int(x), int(y)), 3, (0, 0, 255), -1)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return {
            'coins': detected_coins,
            'processing_time': processing_time,
            'annotated_image': annotated
        }

