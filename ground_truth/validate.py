#!/usr/bin/env python3
"""
Validate Ground Truth Annotations
Visualize annotations to verify they are correct.

Usage:
    python validate.py
"""

import cv2
import json
from pathlib import Path


def validate_annotations():
    """Display annotated images to verify correctness"""
    script_dir = Path(__file__).parent
    images_dir = script_dir.parent / "images"
    annotations_path = script_dir / "annotations.json"

    # Load annotations
    if not annotations_path.exists():
        print(f"Error: No annotations file found: {annotations_path}")
        print("Run annotate.py first!")
        return

    with open(annotations_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 60)
    print("Ground Truth Validation")
    print("=" * 60)
    print(f"Total images: {len(data['images'])}")
    print("Press any key to cycle through images, ESC to quit")
    print()

    for img_data in data["images"]:
        filename = img_data["filename"]
        img_path = images_dir / filename

        if not img_path.exists():
            print(f"Warning: Image not found: {img_path}")
            continue

        # Load image
        image = cv2.imread(str(img_path))
        display = image.copy()

        # Draw all annotated coins
        for coin in img_data["coins"]:
            center = (coin["center_x"], coin["center_y"])
            radius = coin["radius"]
            coin_id = coin["id"]

            # Draw circle
            cv2.circle(display, center, radius, (0, 255, 0), 2)
            # Draw center
            cv2.circle(display, center, 3, (0, 0, 255), -1)
            # Draw ID label
            cv2.putText(
                display,
                str(coin_id),
                (center[0] - 10, center[1] - radius - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
            )

        # Display info
        info = f"{filename} - {img_data['total_coins']} coin(s)"
        print(f"✓ {info}")

        # Show image
        cv2.namedWindow(info, cv2.WINDOW_NORMAL)
        cv2.imshow(info, display)

        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if key == 27:  # ESC
            print("\nValidation stopped.")
            return

    print()
    print("=" * 60)
    print("✓ Validation complete - all images reviewed")
    print("=" * 60)


if __name__ == "__main__":
    validate_annotations()
