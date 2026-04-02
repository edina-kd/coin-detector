# Coin Detector - Comparative Analysis of Circle Detection Methods

A Django web application that demonstrates and compares three computer vision algorithms for automated coin detection and counting.

## 🎯 Project Overview

This educational tool compares three different circle detection methods:
- **Morphological Circularity Detection** (Multi-step pipeline based on Kadrić Durmiš)
- **Hough Circle Transform** (Classical parameter space approach)
- **Blob Detection** (Feature-based approach)

**Purpose**: Educational demonstration of digital image processing techniques for university-level teaching and academic publication.

## Open source

The application is released under the **MIT License** (see [`LICENSE`](LICENSE)) so readers can reproduce experiments, adapt the code, and use it in teaching. If you refer to this work in a publication, you can cite the repository URL once it is published on GitHub.

**Security note for deployment:** set a unique `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=False` in the server environment for any public or shared host (see [`.env.example`](.env.example)). The default settings are intended for local development only.

### First-time push to GitHub

1. On [GitHub](https://github.com/new), create a **new empty** repository (without adding a README there, if you already have one here).
2. In the project folder:

```bash
git init
git add -A
git status   # check that venv/, media/, .env are not listed
git commit -m "Initial commit: coin detector Django app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Replace `YOUR_USERNAME/YOUR_REPO` with your account and repository name. On Windows, use **Git for Windows** or GitHub Desktop if you prefer a GUI.

## 🚀 Features

- ✅ Upload single or multiple coin images (JPG/PNG, max 10MB each, up to 6 images)
- ✅ **Batch processing** - analyze multiple images at once
- ✅ Process with multiple detection algorithms simultaneously
- ✅ **Interactive parameter tuning** - adjust algorithm parameters via UI sliders
- ✅ View annotated results with detected coins highlighted
- ✅ Compare algorithm performance (coins detected, processing time, accuracy)
- ✅ Visual charts for performance comparison
- ✅ Ground truth validation with IoU metrics for test images
- ✅ Responsive Bootstrap 5 UI with drag & drop support

## 📋 Requirements

- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- Modern web browser (Chrome, Firefox, Edge, Safari)

## 🔧 Installation

### 1. Clone or Download the Project

```bash
cd detekcija
```

### 2. Create Virtual Environment

**Ako ste kopirali projekat s Mac-a:** postojeća mapa `venv` ne radi na Windowsu (unutra je Linux/mac struktura i putanje ka Homebrew Pythonu). Obrišite ili preimenujte tu mapu, pa napravite novo okruženje na Windowsu:

```powershell
# PowerShell u korijenu projekta
Remove-Item -Recurse -Force .\venv   # ili preimenujte staru mapu
py -3.11 -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\python manage.py migrate
```

Na macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Brzi start na Windowsu nakon instalacije: dvoklik na `run_dev_server_windows.bat` (ili `.\venv\Scripts\python manage.py runserver`).

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter SSL certificate issues on macOS:

```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

### 6. Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

## 📁 Project Structure

```
detekcija/
├── manage.py
├── requirements.txt
├── README.md
├── LICENSE
├── PAPER_Spoznaja_2025.md   # Article draft / manuscript (Markdown)
├── .env.example             # Environment variables template (optional)
├── coin_detector/           # Django project settings
├── detector/                # Main application
│   ├── algorithms/          # Detection algorithms
│   │   ├── circularity.py
│   │   ├── hough.py
│   │   └── blob.py
│   ├── utils/               # Utility functions
│   │   ├── ground_truth.py
│   │   ├── preprocessing.py
│   │   └── visualization.py
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   └── templates/           # HTML templates
├── static/                  # Static files (CSS, JS)
├── media/                   # Uploaded & result images
├── images/                  # Test images
│   ├── 2KM.jpg
│   ├── 4i05KM.jpg
│   ├── 5i05KM.jpg
│   ├── 7KM.jpg
│   └── 7i05KM.jpg
└── ground_truth/            # Ground truth annotations
    ├── annotate.py          # Annotation tool
    ├── validate.py          # Validation tool
    └── annotations.json     # Manual annotations (23 coins)
```

## 🎓 How to Use

1. **Upload Image**: Drag & drop or click to upload a coin image
2. **Select Algorithms**: Choose which detection methods to run (default: all three)
3. **Analyze**: Click "Analyze Image" to process
4. **View Results**: See side-by-side comparison with metrics
5. **Compare**: Review performance charts

## 🔬 Detection Algorithms

### 1. Morphological Circularity Detection
Python translation of the original C++/Qt algorithm by Kadrić Durmiš, E. "Brojač kovanica"
- Faithful implementation matching the original pennydetector.cpp line-by-line
- Pipeline: Blur (3×3) → HSV background removal → Otsu threshold → Dilate (5×5, 4x) → Erode (3×3, 1x) → Canny (100, 200) → External contours → Circularity filter
- Circularity formula: `C = (4π × Area) / (Perimeter²)`
- Threshold: C ≥ 0.85 (empirically determined from original implementation)

**Tunable Parameters:**
- `circularity_threshold` (0.5-1.0): Minimum circularity score, higher = stricter

### 2. Hough Circle Transform
Classical parameter space voting method
- Rotation invariant
- Well-established approach

**Tunable Parameters:**
- `minDist` (10-100): Minimum distance between circle centers
- `param2` (10-100): Accumulator threshold (higher = fewer false positives)
- `minRadius` (5-50): Minimum circle radius in pixels
- `maxRadius` (50-300): Maximum circle radius in pixels

### 3. Blob Detection
Feature-based using SimpleBlobDetector
- Filters by area, circularity, convexity, inertia

**Tunable Parameters:**
- `minArea` (100-1000): Minimum blob area in pixels²
- `maxArea` (5000-100000): Maximum blob area in pixels²
- `minCircularity` (0.5-1.0): Minimum circularity score
- `minConvexity` (0.5-1.0): Minimum convexity score
- `minInertia` (0.1-1.0): Minimum inertia ratio

## 📊 Metrics

The application calculates:

**Basic Metrics:**
- **Coins Detected**: Number of coins found
- **Processing Time**: Execution time in milliseconds

**Accuracy Metrics** (when ground truth available):
- **Accuracy**: Percentage correct (TP / Total Ground Truth)
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1-Score**: Harmonic mean of precision and recall
- **Mean IoU**: Average Intersection over Union for matched detections

**IoU (Intersection over Union)** measures how well detected circles overlap with ground truth:
- IoU = Area of Overlap / Area of Union
- Standard threshold: IoU ≥ 0.5 for positive match
- Mean IoU provides quality metric beyond simple counting

## 🧪 Testing with Sample Images

The project includes 5 test images with ground truth annotations (23 total coins):
- `2KM.jpg` - 1 coin
- `4i05KM.jpg` - 4 coins
- `5i05KM.jpg` - 5 coins
- `7KM.jpg` - 6 coins
- `7i05KM.jpg` - 7 coins

These images will show accuracy metrics when processed.

## 📝 Ground Truth Annotations

The `ground_truth/` directory contains tools for creating and validating annotations:

```bash
# Annotate images (if needed)
cd ground_truth
python annotate.py

# Validate annotations
python validate.py
```

## 🛠️ Technology Stack

**Backend:**
- Django 4.2.7
- OpenCV 4.8+
- NumPy, Pillow, Matplotlib

**Frontend:**
- Bootstrap 5.3
- Chart.js
- Vanilla JavaScript

**Database:**
- SQLite3 (development)

## 📖 Academic Purpose

This project is developed for a professional paper (stručni članak) for the journal **Spoznaja** - Filozofski fakultet Univerziteta u Zenici.

**Focus**: Practical comparison of circle detection methods for educational purposes.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8080
```

### Migration Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## 📄 License

[MIT License](LICENSE) — free use with attribution; suitable for academic and educational reuse.

## 👤 Author

Developed as part of academic research on computer vision algorithms.

## 🙏 Acknowledgments

- **Kadrić Durmiš, E.** - Original "Brojač kovanica" (Penny Counter) C++/Qt implementation
  - Source files: pennydetector.cpp, backgroundremover.cpp, controller.cpp
  - Our morphological circularity algorithm is a faithful Python translation of this work
- **OpenCV community** - Computer vision library (used in both C++ original and our Python version)
- **Django framework** - Web application framework
- **Bootstrap team** - UI components

---

For the research manuscript in Markdown, see [PAPER_Spoznaja_2025.md](PAPER_Spoznaja_2025.md).

**Status**: ✅ Implementation Complete | Ready for Testing | October 2025
