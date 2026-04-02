"""
Django Models for Coin Detector Application
"""

from django.db import models
from django.utils import timezone


class UploadedImage(models.Model):
    """Stores uploaded images"""
    
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    filename = models.CharField(max_length=255)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    file_size = models.IntegerField(default=0)  # bytes
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"


class DetectionResult(models.Model):
    """Stores detection results for each algorithm"""
    
    ALGORITHM_CHOICES = [
        ('circularity', 'Morphological approach (this work)'),
        ('hough', 'Hough Circle Transform'),
        ('blob', 'Blob Detection'),
    ]
    
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='results')
    algorithm = models.CharField(max_length=50, choices=ALGORITHM_CHOICES)
    coins_detected = models.IntegerField(default=0)
    processing_time = models.FloatField(default=0.0)  # milliseconds
    
    # Accuracy metrics (if ground truth available)
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)  # Harmonic mean of precision and recall
    mean_iou = models.FloatField(null=True, blank=True)  # Average IoU for matched detections
    true_positives = models.IntegerField(null=True, blank=True)
    false_positives = models.IntegerField(null=True, blank=True)
    false_negatives = models.IntegerField(null=True, blank=True)
    
    result_image = models.ImageField(upload_to='results/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['algorithm']
    
    def __str__(self):
        return f"{self.get_algorithm_display()} - {self.coins_detected} coins"


class DetectedCoin(models.Model):
    """Stores individual detected coin data"""
    
    result = models.ForeignKey(DetectionResult, on_delete=models.CASCADE, related_name='coins')
    center_x = models.FloatField()
    center_y = models.FloatField()
    radius = models.FloatField()
    
    # Optional metadata
    circularity = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Coin at ({self.center_x}, {self.center_y}), radius: {self.radius}"
