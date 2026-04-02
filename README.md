# Coin detector (web)

Mala **Django** aplikacija koja na slici pokreće tri pristupa detekciji kružnih objekata (morfološki *pipeline*, Hough krugovi, OpenCV *blob*) i prikazuje rezultate u pregledniku. U repozitoriju su i testne slike te `ground_truth/annotations.json` za usporedbu s anotacijama.

**Repozitorij:** [github.com/edina-kd/coin-detector](https://github.com/edina-kd/coin-detector) · **Licenca:** [MIT](LICENSE)

## Reprodukcija (lokalno)

Potreban je **Python 3.10+** i običan preglednik.

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

Otvori **http://127.0.0.1:8000/** , učitaj JPG/PNG i pokreni obradu.

**Napomena:** Ako si projekat prenio s Maca i folder `venv` već postoji, na Windowsu ga obriši i napravi novi (`python -m venv venv` kao gore). Alternativa na Windowsu: `run_dev_server_windows.bat` (nakon što je `venv` ispravno napravljen).

Za javni server postavi varijable okruženja `DJANGO_SECRET_KEY` i `DJANGO_DEBUG=False` (vidi [.env.example](.env.example)).
