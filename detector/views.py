"""
Django Views for Coin Detector Application
"""

import os
import cv2
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.conf import settings
from pathlib import Path

from .models import UploadedImage, DetectionResult, DetectedCoin
from .algorithms.circularity import CircularityDetector
from .algorithms.hough import HoughDetector
from .algorithms.blob import BlobDetector
from .utils.ground_truth import GroundTruthManager
from .utils.preprocessing import load_image, resize_image, validate_image


def index(request):
    """Main page with upload form and results"""
    
    if request.method == 'POST':
        # Handle file upload (multiple files)
        uploaded_files = request.FILES.getlist('images')
        if not uploaded_files:
            messages.error(request, 'Please select at least one image to upload.')
            return redirect('index')
        
        # Limit to 6 files
        if len(uploaded_files) > 6:
            messages.error(request, 'Maximum 6 images allowed.')
            return redirect('index')
        
        # Validate each file
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        for uploaded_file in uploaded_files:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_ext not in allowed_extensions:
                messages.error(request, f'Invalid file format for "{uploaded_file.name}". Please upload JPG or PNG images.')
                return redirect('index')
            
            if uploaded_file.size > 10 * 1024 * 1024:
                messages.error(request, f'File "{uploaded_file.name}" is too large. Maximum size: 10MB.')
                return redirect('index')
        
        # Get selected algorithms
        selected_algorithms = request.POST.getlist('algorithms')
        if not selected_algorithms:
            selected_algorithms = ['circularity', 'hough', 'blob']  # Default: all
        
        # Extract algorithm parameters from request
        params = {}
        if 'circ_threshold' in request.POST:
            params['circ_threshold'] = request.POST.get('circ_threshold')
        for key in ['hough_minDist', 'hough_param2', 'hough_minRadius', 'hough_maxRadius']:
            if key in request.POST:
                params[key] = request.POST.get(key)
        for key in ['blob_minArea', 'blob_maxArea', 'blob_minCircularity', 
                   'blob_minConvexity', 'blob_minInertia']:
            if key in request.POST:
                params[key] = request.POST.get(key)
        
        # Process all images
        all_results = []
        uploaded_images = []
        
        try:
            for uploaded_file in uploaded_files:
                # Save uploaded image
                uploaded_image = UploadedImage(
                    filename=uploaded_file.name,
                    file_size=uploaded_file.size
                )
                uploaded_image.image.save(uploaded_file.name, uploaded_file)
                uploaded_images.append(uploaded_image)
                
                # Load image to get dimensions
                img_path = uploaded_image.image.path
                img = cv2.imread(img_path)
                
                if img is None:
                    messages.warning(request, f'Could not process image file: {uploaded_file.name}')
                    continue
                
                # Validate dimensions
                is_valid, error_msg = validate_image(img)
                if not is_valid:
                    messages.warning(request, f'{uploaded_file.name}: {error_msg}')
                    continue
                
                uploaded_image.height, uploaded_image.width = img.shape[:2]
                uploaded_image.save()
                
                # Process with selected algorithms
                results = process_image(uploaded_image, selected_algorithms, params)
                
                all_results.append({
                    'image': uploaded_image,
                    'results': results
                })
            
            if not all_results:
                messages.error(request, 'No images could be processed successfully.')
                return redirect('index')
            
            # Render results page with all results
            return render(request, 'detector/results.html', {
                'batch_results': all_results,
                'selected_algorithms': selected_algorithms,
                'is_batch': len(all_results) > 1
            })
            
        except Exception as e:
            messages.error(request, f'Error processing images: {str(e)}')
            for img in uploaded_images:
                try:
                    img.delete()
                except:
                    pass
            return redirect('index')
    
    # GET request - show upload form
    return render(request, 'detector/index.html')


def process_image(uploaded_image, selected_algorithms, params=None):
    """
    Process image with selected detection algorithms
    
    Args:
        uploaded_image: UploadedImage instance
        selected_algorithms: List of algorithm names
        params: Dictionary of algorithm parameters from request
        
    Returns:
        list: Detection results
    """
    if params is None:
        params = {}
    
    # Load image
    img_path = uploaded_image.image.path
    image = cv2.imread(img_path)
    
    # Initialize ground truth manager
    gt_manager = GroundTruthManager()
    ground_truth = gt_manager.get_ground_truth(uploaded_image.filename)
    
    # Debug: Print ground truth status
    print(f"DEBUG: Looking for ground truth for filename: {uploaded_image.filename}")
    print(f"DEBUG: Ground truth found: {ground_truth is not None}")
    if ground_truth:
        print(f"DEBUG: Ground truth has {len(ground_truth.get('coins', []))} coins")
    
    # Initialize detectors with custom parameters
    detectors = {}
    if 'circularity' in selected_algorithms:
        circ_threshold = float(params.get('circ_threshold', 0.85))
        detectors['circularity'] = CircularityDetector(circularity_threshold=circ_threshold)
        print(f"DEBUG: Circularity detector - threshold={circ_threshold}")
    
    if 'hough' in selected_algorithms:
        hough_params = {
            'minDist': int(params.get('hough_minDist', 50)),
            'param2': int(params.get('hough_param2', 50)),
            'minRadius': int(params.get('hough_minRadius', 20)),
            'maxRadius': int(params.get('hough_maxRadius', 150))
        }
        detectors['hough'] = HoughDetector(**hough_params)
        print(f"DEBUG: Hough detector - {hough_params}")
    
    if 'blob' in selected_algorithms:
        blob_params = {
            'minArea': int(params.get('blob_minArea', 300)),
            'maxArea': int(params.get('blob_maxArea', 50000)),
            'minCircularity': float(params.get('blob_minCircularity', 0.7)),
            'minConvexity': float(params.get('blob_minConvexity', 0.8)),
            'minInertiaRatio': float(params.get('blob_minInertia', 0.4))
        }
        detectors['blob'] = BlobDetector(**blob_params)
        print(f"DEBUG: Blob detector - {blob_params}")
    
    results = []
    
    for algo_name, detector in detectors.items():
        # Run detection
        detection_result = detector.detect(image)
        
        # Save result to database
        result = DetectionResult(
            image=uploaded_image,
            algorithm=algo_name,
            coins_detected=len(detection_result['coins']),
            processing_time=detection_result['processing_time']
        )
        
        # Calculate accuracy if ground truth available
        if ground_truth:
            print(f"DEBUG: Calculating accuracy for {algo_name}")
            print(f"DEBUG: Detected {len(detection_result['coins'])} coins")
            print(f"DEBUG: Ground truth has {len(ground_truth.get('coins', []))} coins")
            
            accuracy_metrics = gt_manager.calculate_accuracy(
                detection_result['coins'],
                ground_truth.get('coins', [])
            )
            
            print(f"DEBUG: Accuracy metrics: {accuracy_metrics}")
            
            result.accuracy = accuracy_metrics['accuracy']
            result.precision = accuracy_metrics['precision']
            result.recall = accuracy_metrics['recall']
            result.f1_score = accuracy_metrics['f1_score']
            result.mean_iou = accuracy_metrics['mean_iou']
            result.true_positives = accuracy_metrics['tp']
            result.false_positives = accuracy_metrics['fp']
            result.false_negatives = accuracy_metrics['fn']
        
        result.save()
        
        # Save annotated image
        annotated_img = detection_result['annotated_image']
        _, buffer = cv2.imencode('.jpg', annotated_img)
        result.result_image.save(
            f"{algo_name}_{uploaded_image.filename}",
            ContentFile(buffer.tobytes()),
            save=True
        )
        
        # Save detected coins
        for coin_data in detection_result['coins']:
            DetectedCoin.objects.create(
                result=result,
                center_x=coin_data['center_x'],
                center_y=coin_data['center_y'],
                radius=coin_data['radius'],
                circularity=coin_data.get('circularity')
            )
        
        # Add to results list
        result_dict = {
            'algorithm': result.get_algorithm_display(),
            'algo_name': algo_name,
            'coins_detected': result.coins_detected,
            'processing_time': round(result.processing_time, 2),
            'accuracy': result.accuracy,
            'precision': result.precision,
            'recall': result.recall,
            'f1_score': result.f1_score,
            'mean_iou': result.mean_iou,
            'tp': result.true_positives,
            'fp': result.false_positives,
            'fn': result.false_negatives,
            'result_image_url': result.result_image.url if result.result_image else None
        }
        print(f"DEBUG: Result dict for {algo_name}: accuracy={result_dict['accuracy']}, precision={result_dict['precision']}, recall={result_dict['recall']}, f1={result_dict['f1_score']}, mean_iou={result_dict['mean_iou']}")
        results.append(result_dict)
    
    return results


def about(request):
    """About page with project information"""
    return render(request, 'detector/about.html')
