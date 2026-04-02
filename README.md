# Coin detector (web)

Small **Django** app that runs three circle-detection approaches on an uploaded image (morphological pipeline, Hough circles, OpenCV blob) and shows results in the browser. The repo includes sample images and `ground_truth/annotations.json` for comparison with manual annotations.

**Repository:** [github.com/edina-kd/coin-detector](https://github.com/edina-kd/coin-detector) · **License:** [MIT](LICENSE)

## Run locally

You need **Python 3.10+** and a web browser.

```bash
git clone https://github.com/edina-kd/coin-detector.git
cd coin-detector
python -m venv venv
```

**Windows (PowerShell):** `.\venv\Scripts\activate`  
**macOS / Linux:** `source venv/bin/activate`

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000/**, upload JPG/PNG images, and run detection.

On Windows you can start the server with **`run_dev_server_windows.bat`** after the virtual environment is set up (same `venv` folder as above).

For a public deployment, set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=False` in the environment (see [.env.example](.env.example)).
