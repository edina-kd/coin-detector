"""
Ground Truth Management
Load and compare detection results with ground truth annotations
"""

import json
import os
import math
import numpy as np
from pathlib import Path


class GroundTruthManager:
    """
    Manages ground truth annotations and accuracy calculations
    """
    
    def __init__(self, annotations_path=None):
        """
        Initialize ground truth manager
        
        Args:
            annotations_path: Path to annotations.json file
        """
        if annotations_path is None:
            # Default path relative to project root
            base_dir = Path(__file__).resolve().parent.parent.parent
            annotations_path = base_dir / 'ground_truth' / 'annotations.json'
        
        self.annotations_path = annotations_path
        self.annotations = {}
        self.load_annotations()
    
    def load_annotations(self):
        """Load annotations from JSON file"""
        if os.path.exists(self.annotations_path):
            with open(self.annotations_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert list to dict keyed by filename
                for img_data in data.get('images', []):
                    self.annotations[img_data['filename']] = img_data
            print(f"DEBUG: Loaded {len(self.annotations)} ground truth annotations from {self.annotations_path}")
            print(f"DEBUG: Available filenames: {list(self.annotations.keys())}")
        else:
            print(f"Warning: Annotations file not found: {self.annotations_path}")
    
    def get_ground_truth(self, filename):
        """
        Get ground truth for a specific image
        
        Args:
            filename: Image filename
            
        Returns:
            dict: Ground truth data or None
        """
        return self.annotations.get(filename)
    
    def calculate_circle_iou(self, det_x, det_y, det_r, gt_x, gt_y, gt_r):
        """
        Calculate IoU (Intersection over Union) between two circles
        
        Args:
            det_x, det_y, det_r: Detected circle center and radius
            gt_x, gt_y, gt_r: Ground truth circle center and radius
            
        Returns:
            float: IoU score (0 to 1)
        """
        # Calculate distance between centers
        d = math.sqrt((det_x - gt_x) ** 2 + (det_y - gt_y) ** 2)
        
        # If circles don't overlap at all
        if d >= det_r + gt_r:
            return 0.0
        
        # If one circle is completely inside the other
        if d <= abs(det_r - gt_r):
            smaller_r = min(det_r, gt_r)
            larger_r = max(det_r, gt_r)
            intersection = math.pi * smaller_r ** 2
            union = math.pi * larger_r ** 2
            return intersection / union
        
        # Partial overlap - use geometric formula
        # Area of intersection of two circles
        r1, r2 = det_r, gt_r
        
        # Calculate intersection area using the formula for two intersecting circles
        # https://mathworld.wolfram.com/Circle-CircleIntersection.html
        part1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
        part2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
        part3 = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
        
        intersection = part1 + part2 - part3
        
        # Calculate union
        area1 = math.pi * r1 ** 2
        area2 = math.pi * r2 ** 2
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_accuracy(self, detected_coins, ground_truth_coins, iou_threshold=0.5):
        """
        Calculate detection accuracy metrics using IoU (Intersection over Union)
        
        Args:
            detected_coins: List of detected coins [{'center_x': x, 'center_y': y, 'radius': r}, ...]
            ground_truth_coins: List of ground truth coins
            iou_threshold: Minimum IoU to consider a match (0.5 default - standard in object detection)
            
        Returns:
            dict: {
                'tp': True Positives,
                'fp': False Positives,
                'fn': False Negatives,
                'precision': Precision score,
                'recall': Recall score,
                'accuracy': Accuracy percentage,
                'mean_iou': Average IoU for matched detections,
                'f1_score': F1 score (harmonic mean of precision and recall)
            }
        """
        if not ground_truth_coins:
            return {
                'tp': 0,
                'fp': len(detected_coins),
                'fn': 0,
                'precision': 0.0,
                'recall': 0.0,
                'accuracy': 0.0,
                'mean_iou': 0.0,
                'f1_score': 0.0
            }
        
        # Track which ground truth coins have been matched
        gt_matched = [False] * len(ground_truth_coins)
        tp = 0
        iou_scores = []
        
        # For each detection, find best matching ground truth by IoU
        for det in detected_coins:
            best_match_idx = None
            best_iou = 0.0
            
            for i, gt in enumerate(ground_truth_coins):
                if gt_matched[i]:
                    continue
                
                # Calculate IoU between detected circle and ground truth circle
                iou = self.calculate_circle_iou(
                    det['center_x'], det['center_y'], det['radius'],
                    gt['center_x'], gt['center_y'], gt['radius']
                )
                
                if iou > best_iou and iou >= iou_threshold:
                    best_iou = iou
                    best_match_idx = i
            
            if best_match_idx is not None:
                gt_matched[best_match_idx] = True
                tp += 1
                iou_scores.append(best_iou)
        
        # Calculate metrics
        fp = len(detected_coins) - tp  # Detected but not real
        fn = len(ground_truth_coins) - tp  # Missed real coins
        
        precision = tp / len(detected_coins) if len(detected_coins) > 0 else 0.0
        recall = tp / len(ground_truth_coins) if len(ground_truth_coins) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        accuracy = (tp / len(ground_truth_coins)) * 100 if len(ground_truth_coins) > 0 else 0.0
        mean_iou = np.mean(iou_scores) if iou_scores else 0.0
        
        return {
            'tp': tp,
            'fp': fp,
            'fn': fn,
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'accuracy': round(accuracy, 2),
            'mean_iou': round(float(mean_iou), 3),
            'f1_score': round(f1_score, 3)
        }

