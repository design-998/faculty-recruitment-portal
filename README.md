# Faculty Recruitment Portal

A Flask dashboard for faculty recruitment listings at Indian IITs and NITs. It serves the checked-in `data.json` snapshot and includes institute-specific scrapers for refreshing available details.

**Live website:** <https://faculty-recruitment-portal.onrender.com>

The free hosting instance may take about a minute to wake after inactivity. If the first page load is delayed, wait a little and refresh.

## Requirements

- Python 3.10 or later
- Internet access when refreshing listings

## Run locally

From this directory, create and activate a virtual environment. Install all project dependencies from the included requirements file:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the dashboard with Waitress, a production-ready server that also works on Windows:

```powershell
waitress-serve --host=127.0.0.1 --port=5000 app:app
```

Open <http://127.0.0.1:5000> in a browser. The portal includes an overview, searchable opportunities, institute directory and institute detail pages, and an explanation of how listings are collected.

The project does not require dependencies to be installed one by one: `python -m pip install -r requirements.txt` installs them together. Python itself and pip are still required.

## Publish on GitHub

1. Install Git for Windows if `git --version` is not recognized.
2. Create an empty repository on GitHub. Do not initialize it with a README or other files.
3. In PowerShell, switch to this project folder and run the following, replacing the URL with your repository's URL:

   ```powershell
   cd "C:\Users\Panav\Faculty recruitment Portal\Faculty recruitment Portal"
   git init
   git add .
   git commit -m "Prepare faculty recruitment portal"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   git push -u origin main
   ```

The `.gitignore` excludes the local virtual environment, Python caches, zip files, and `Downloads` directory. Check the files staged by `git add` before pushing; do not upload unrelated files, credentials, or personal data.

## Put the website online

GitHub Pages only hosts static files; it cannot run this Flask/Python application. This project includes a `render.yaml` deployment configuration for Render:

1. Push the project to GitHub using the steps above.
2. Sign in to Render and choose **New → Blueprint**.
3. Connect the GitHub repository and deploy the `faculty-recruitment-portal` web service described by `render.yaml`.
4. Share the public `*.onrender.com` URL Render gives you with your professor.

The web service installs `requirements.txt` during deployment and serves the Flask app with Waitress. Render's free web service may sleep when idle and take a little time to wake up. This deployment serves the checked-in recruitment snapshot; it does not run the 2:00 AM scheduler. Render's free filesystem is ephemeral, so scraper updates written to local JSON files are not durable across restarts/redeploys. For a permanent online daily-refresh service, a persistent database/storage and separately hosted scheduled job would need to be configured.

## Refresh recruitment data

Run the scraper from this directory:

```powershell
python scraper.py
```

The scraper updates successful records in `data.json` and writes `sync_metadata.json` after at least one successful update. If every institute refresh fails, the existing recruitment data and last-successful-refresh timestamp are preserved. Scraper results are best-effort; always verify deadlines and application instructions with the official institute.

## Schedule the daily refresh

To attempt a refresh every day at 2:00 AM in the computer's local time zone, start the scheduler and keep it running:

```powershell
python scheduler.py
```

The scheduler is a separate process from the web app. It does not run if the computer is off, asleep, or the scheduler process has been stopped. To have it start automatically after Windows restarts, configure `scheduler.py` in Windows Task Scheduler with the project virtual environment's Python executable and the project directory as the working directory.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Project files

- `app.py` — Flask application and dashboard route.
- `data.json` — recruitment listing snapshot.
- `scraper.py` — refresh command and institute-to-scraper mapping.
- `scheduler.py` — long-running daily 2:00 AM refresh scheduler.
- `scrapers/` — institute-specific page parsers.
- `templates/` and `static/css/style.css` — multi-page portal UI.
