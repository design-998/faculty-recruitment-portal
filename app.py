import json
import re
from pathlib import Path

from flask import Flask, abort, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data.json"
METADATA_PATH = BASE_DIR / "sync_metadata.json"

app = Flask(__name__)


def load_json(path, default):
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default


def load_recruitments():
    recruitments = load_json(DATA_PATH, [])
    if not isinstance(recruitments, list):
        raise ValueError(f"{DATA_PATH} must contain a JSON array")
    return recruitments


def institute_slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


app.jinja_env.filters["institute_slug"] = institute_slug


def make_institute_directory(recruitments):
    institutes = {}
    for job in recruitments:
        name = job.get("institute", "Unknown institute")
        institute = institutes.setdefault(
            name,
            {
                "name": name,
                "slug": institute_slug(name),
                "category": "IIT" if name.upper().startswith("IIT ") else "NIT",
                "jobs": [],
                "open_count": 0,
            },
        )
        institute["jobs"].append(job)
        if str(job.get("status", "")).strip().lower() == "open":
            institute["open_count"] += 1
    return sorted(institutes.values(), key=lambda item: item["name"].casefold())


def get_dashboard_context():
    recruitments = load_recruitments()
    open_count = sum(
        str(job.get("status", "")).strip().lower() == "open"
        for job in recruitments
    )
    closed_count = sum(
        str(job.get("status", "")).strip().lower() == "closed"
        for job in recruitments
    )
    return {
        "total_institutes": len(recruitments),
        "open_count": open_count,
        "closed_count": closed_count,
        "last_updated": load_json(METADATA_PATH, {}).get(
            "last_updated", "Not yet synced"
        ),
    }


@app.route("/")
def home():
    recruitments = load_recruitments()
    context = get_dashboard_context()
    context["featured_recruitments"] = [
        job
        for job in recruitments
        if str(job.get("status", "")).strip().lower() == "open"
    ][:6]
    context["institutes"] = make_institute_directory(recruitments)
    return render_template("index.html", **context)


@app.route("/opportunities")
def opportunities():
    recruitments = load_recruitments()
    query = request.args.get("q", "").strip()
    status = request.args.get("status", "all").strip().lower()
    if status not in {"all", "open", "closed"}:
        status = "all"

    filtered = []
    for job in recruitments:
        job_status = str(job.get("status", "")).strip().lower()
        searchable = " ".join(
            str(job.get(field, ""))
            for field in ("institute", "post", "eligibility", "deadline")
        )
        if status != "all" and job_status != status:
            continue
        if query and query.casefold() not in searchable.casefold():
            continue
        filtered.append(job)
    filtered.sort(key=lambda job: job.get("institute", "").casefold())

    return render_template(
        "opportunities.html",
        recruitments=filtered,
        query=query,
        status=status,
        result_count=len(filtered),
        **get_dashboard_context(),
    )


@app.route("/institutes")
def institutes():
    directory = make_institute_directory(load_recruitments())
    return render_template(
        "institutes.html",
        institutes=directory,
        iit_count=sum(item["category"] == "IIT" for item in directory),
        nit_count=sum(item["category"] == "NIT" for item in directory),
        **get_dashboard_context(),
    )


@app.route("/institutes/<institute_slug>")
def institute_detail(institute_slug):
    directory = make_institute_directory(load_recruitments())
    institute = next(
        (item for item in directory if item["slug"] == institute_slug),
        None,
    )
    if institute is None:
        abort(404)
    return render_template("institute_detail.html", institute=institute)


@app.route("/about")
def about():
    return render_template("about.html", **get_dashboard_context())


if __name__ == "__main__":
    app.run(debug=False)
