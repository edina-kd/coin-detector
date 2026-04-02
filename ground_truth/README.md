# Ground Truth Annotations

This directory contains tools and data for creating ground truth annotations of coin images.

## Files

- `annotate.py` - Interactive annotation tool
- `validate.py` - Visualization tool to verify annotations
- `annotations.json` - Ground truth data (generated)

## Installation

**Recommended: Use virtual environment**

```bash
# 1. Create and activate venv (from project root)
cd /path/to/detekcija
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install --trusted-host pypi.org --trusted-host pypi.python.org opencv-python numpy
```

Or install globally:

```bash
pip3 install opencv-python numpy
```

## Quick Start

### 1. Create Annotations

```bash
cd ground_truth
python annotate.py
```

**Instructions:**
- **Left click twice per coin:**
  - 1st click = coin center (red dot)
  - 2nd click = coin edge (green circle drawn)
- **Right click:** Undo last coin
- **Press 's':** Save and continue to next image
- **Press 'q':** Quit without saving

**Time required:** ~1-2 minutes per image

### 2. Validate Annotations

```bash
python validate.py
```

View annotated images to verify correctness. Press any key to cycle through, ESC to quit.

## Output Format

`annotations.json` structure:

```json
{
  "images": [
    {
      "filename": "2KM.jpg",
      "width": 1200,
      "height": 1600,
      "total_coins": 1,
      "coins": [
        {
          "id": 1,
          "center_x": 324,
          "center_y": 512,
          "radius": 45
        }
      ]
    }
  ]
}
```

## Coordinate System

- **Origin:** Top-left corner (0, 0)
- **X-axis:** Left to right
- **Y-axis:** Top to bottom
- **Units:** Pixels

This follows OpenCV's standard coordinate system.

## Usage in Django App

The Django application will:
1. Load `annotations.json` on startup
2. Compare detected coins against ground truth
3. Calculate accuracy metrics (precision, recall)
4. Display results on results page

## Notes

- Annotations are for the 5 test images in `../images/`
- Store approximate radii - exact pixel precision not critical
- If you need to re-annotate, just run `annotate.py` again

