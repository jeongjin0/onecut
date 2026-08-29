from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from onecut.config import load_settings
from onecut.engine import run_cut
from onecut.models import RunReceipt
from onecut.agent import DEFAULT_PROMPT, PLAN_PROMPT

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "web"))
app = FastAPI(title="Onecut", version="0.1.0")


def latest(settings) -> RunReceipt | None:
    path = settings.receipts_dir / "latest.json"
    if not path.exists():
        return None
    return RunReceipt.model_validate_json(path.read_text())


@app.get("/healthz")
def healthz() -> dict:
    settings = load_settings()
    return {
        "ok": True,
        "mode": settings.onecut_mode,
        "runner": settings.onecut_runner,
        "model": settings.onecut_model,
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    settings = load_settings()
    return TEMPLATES.TemplateResponse(
        request,
        "index.html",
        {
            "receipt": latest(settings),
            "runner": settings.onecut_runner,
            "model": settings.onecut_model,
        },
    )


@app.post("/run")
def run(fixture: str = Form("scattered"), prompt: str = Form("")):
    settings = load_settings()
    if fixture == "protected":
        name = "protected.json"
        asked = prompt or DEFAULT_PROMPT
    elif fixture == "plan":
        name = "scattered.json"
        asked = PLAN_PROMPT
    else:
        name = "scattered.json"
        asked = prompt or DEFAULT_PROMPT
    settings = settings.model_copy(update={"onecut_fixture_path": Path("fixtures") / name})
    run_cut(settings, prompt=asked)
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/latest")
def api_latest() -> JSONResponse:
    settings = load_settings()
    receipt = latest(settings)
    return JSONResponse({"receipt": None if receipt is None else receipt.model_dump(mode="json")})
