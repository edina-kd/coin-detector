#!/usr/bin/env python3
"""
Simple Ground Truth Annotation Tool
Click coins to annotate them for accuracy testing.

Usage:
    python annotate.py

Instructions:
    - Left click: 1st click = center, 2nd click = edge (sets radius)
    - Right click: Undo last coin
    - Press 's' to save and continue to next image
    - Press 'q' to quit without saving
"""

import cv2
import json
import numpy as np
from pathlib import Path


class CoinAnnotator:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(str(image_path))
        if self.image is None:
            raise ValueError(f"Cannot load image: {image_path}")

        self.display_image = self.image.copy()
        self.coins = []
        self.current_center = None

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # First click: set center
            if self.current_center is None:
                self.current_center = (x, y)
                # Draw red dot at center
                cv2.circle(self.display_image, (x, y), 3, (0, 0, 255), -1)
                print(f"  Center set at ({x}, {y}). Click on coin edge to set radius.")

            # Second click: calculate radius and save coin
            else:
                radius = int(
                    np.sqrt(
                        (x - self.current_center[0]) ** 2
                        + (y - self.current_center[1]) ** 2
                    )
                )

                coin = {
                    "id": len(self.coins) + 1,
                    "center_x": self.current_center[0],
                    "center_y": self.current_center[1],
                    "radius": radius,
                }
                self.coins.append(coin)

                # Draw green circle for saved coin
                cv2.circle(
                    self.display_image, self.current_center, radius, (0, 255, 0), 2
                )
                cv2.circle(self.display_image, self.current_center, 3, (0, 255, 0), -1)

                print(
                    f"  ✓ Coin {coin['id']}: center ({coin['center_x']}, {coin['center_y']}), radius {radius}"
                )
                self.current_center = None

        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click: undo last coin
            if self.coins:
                removed = self.coins.pop()
                print(f"  ✗ Removed coin {removed['id']}")
                # Redraw all coins
                self.display_image = self.image.copy()
                for coin in self.coins:
                    cv2.circle(
                        self.display_image,
                        (coin["center_x"], coin["center_y"]),
                        coin["radius"],
                        (0, 255, 0),
                        2,
                    )
                    cv2.circle(
                        self.display_image,
                        (coin["center_x"], coin["center_y"]),
                        3,
                        (0, 255, 0),
                        -1,
                    )

    def annotate(self):
        """Interactive annotation window"""
        window_name = f"Annotate: {self.image_path.name}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, self.mouse_callback)

        print(f"\nAnnotating: {self.image_path.name}")
        print(
            "  Left click: 1st=center, 2nd=edge | Right click: undo | 's'=save | 'q'=quit"
        )

        while True:
            cv2.imshow(window_name, self.display_image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                cv2.destroyAllWindows()
                return self.coins
            elif key == ord("q"):
                cv2.destroyAllWindows()
                return None


def annotate_all_images():
    """Main annotation loop"""
    # Setup paths
    script_dir = Path(__file__).parent
    images_dir = script_dir.parent / "images"
    output_path = script_dir / "annotations.json"

    if not images_dir.exists():
        print(f"Error: Images directory not found: {images_dir}")
        return

    # Find all JPG images
    image_files = sorted(images_dir.glob("*.jpg")) + sorted(images_dir.glob("*.JPG"))

    if not image_files:
        print(f"Error: No .jpg images found in {images_dir}")
        return

    print("=" * 60)
    print("Ground Truth Annotation Tool")
    print("=" * 60)
    print(f"Found {len(image_files)} images to annotate")
    print()

    annotations = {"images": []}

    for img_path in image_files:
        try:
            annotator = CoinAnnotator(img_path)
            coins = annotator.annotate()

            if coins is None:
                print("\n❌ Annotation cancelled by user.")
                return

            # Get image dimensions
            img = cv2.imread(str(img_path))
            height, width = img.shape[:2]

            annotations["images"].append(
                {
                    "filename": img_path.name,
                    "width": width,
                    "height": height,
                    "total_coins": len(coins),
                    "coins": coins,
                }
            )

            print(f"  ✓ Saved {len(coins)} coin(s)")

        except Exception as e:
            print(f"\n❌ Error processing {img_path.name}: {e}")
            return

    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 60)
    print(f"✓ All annotations saved to: {output_path}")
    print(f"✓ Total images: {len(annotations['images'])}")
    print(f"✓ Total coins: {sum(img['total_coins'] for img in annotations['images'])}")
    print("=" * 60)


if __name__ == "__main__":
    annotate_all_images()
