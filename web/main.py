from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from application import Application
from controllers import JournalManager

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

core_app = Application()
core_app.initialize()
container = core_app._container

# Последние параметры слайдеров для предпросмотра
LAST_PARAMS = {"difficulty": 50, "enemies": 10, "reward": 100}


def compute_preview(difficulty: int, enemies: int, reward: int):
    """
    Простейшая псевдо-модель, чтобы значения на экране менялись от слайдеров.
    Это визуальный расчет, не заменяет внутренний прогноз ядра.
    """
    diff = max(0, min(100, difficulty))
    enem = max(0, min(200, enemies))
    rew = max(50, min(200, reward))

    expected_players = max(100, int(900 - diff * 3 + rew * 2 - enem * 2))
    completion = max(5, min(98, int(72 + (rew - 100) * 0.2 - (diff - 50) * 0.35 - (enem - 10) * 0.25)))
    avg_time = max(5, int(30 + (diff - 50) * 0.25 + (enem - 10) * 0.5 - (rew - 100) * 0.05))

    if expected_players < 700:
        server_load = "Небольшая"
    elif expected_players < 1000:
        server_load = "Умеренная"
    else:
        server_load = "Высокая"

    return {
        "expected_players": expected_players,
        "completion": completion,
        "avg_time": avg_time,
        "server_load": server_load,
    }


def build_recs(base_text: str | None):
    """Единый список рекомендаций, чтобы кнопки работали одинаково."""
    first = base_text or "Нет активного прогноза"
    return [
        {
            "key": "lower_diff",
            "title": first,
            "effect": "Рекомендации, сгенерированные системой на основе анализа данных.",
        },
        {
            "key": "more_reward",
            "title": "Увеличить награды на 20%",
            "effect": "+15% активности игроков (пример возможной оптимизации)",
        },
        {
            "key": "add_checkpoint",
            "title": "Добавить контрольную точку",
            "effect": "Снизить количество повторных попыток прохождения уровня.",
        },
    ]


@app.get("/", response_class=HTMLResponse)
async def splash(request: Request):
    return templates.TemplateResponse("splash.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str | None = None):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error},
    )


VALID_USERS = {
    "designer": "pass",
    "developer": "pass2",
}


@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if username in VALID_USERS and VALID_USERS[username] == password:
        return RedirectResponse(url="/menu", status_code=303)

    return RedirectResponse(
        url="/login?error=Неверный+логин+или+пароль",
        status_code=303,
    )


@app.get("/menu", response_class=HTMLResponse)
async def menu(request: Request):
    return templates.TemplateResponse(
        "menu.html",
        {"request": request, "username": "Вася Пупкин"},
    )


@app.get("/monitoring", response_class=HTMLResponse)
async def monitoring_scenarios(request: Request):
    scenarios = [
        {"name": "Обучающий уровень", "players": 1250, "completion": 87, "problems": 2},
        {"name": "Первый босс", "players": 980, "completion": 62, "problems": 5},
        {"name": "Сбор ресурсов", "players": 1500, "completion": 94, "problems": 1},
        {"name": "Командная миссия", "players": 450, "completion": 45, "problems": 8},
    ]
    return templates.TemplateResponse(
        "monitoring.html",
        {
            "request": request,
            "tab": "scenarios",
            "scenarios": scenarios,
        },
    )


@app.get("/monitoring/problems", response_class=HTMLResponse)
async def monitoring_problems(request: Request):
    problems = [
        {
            "title": "Первый босс",
            "tag": "Высокая сложность",
            "description": "Только 62% игроков проходят уровень",
        },
        {
            "title": "Командная миссия",
            "tag": "Низкий процент завершения",
            "description": "Узкое место: требуется балансировка наград",
        },
        {
            "title": "Первый босс",
            "tag": "Долгое время прохождения",
            "description": "Среднее время: 45 минут (ожидалось 30)",
        },
    ]
    return templates.TemplateResponse(
        "monitoring.html",
        {
            "request": request,
            "tab": "problems",
            "problems": problems,
        },
    )


@app.get("/level-testing", response_class=HTMLResponse)
async def level_edit(request: Request):
    return templates.TemplateResponse(
        "level_testing.html",
        {
            "request": request,
            "tab": "edit",
            "params": LAST_PARAMS,
        },
    )


@app.get("/level-testing/forecast", response_class=HTMLResponse)
async def level_forecast_get(request: Request):
    forecast_repo = container.resolve("repo:forecast")
    report_repo = container.resolve("repo:report")
    journal: JournalManager = container.resolve(JournalManager)

    forecasts = forecast_repo.get_all()
    reports = report_repo.get_all()
    last_forecast = forecasts[-1] if forecasts else None
    last_report = reports[-1] if reports else None

    preview = compute_preview(
        LAST_PARAMS["difficulty"], LAST_PARAMS["enemies"], LAST_PARAMS["reward"]
    )

    return templates.TemplateResponse(
        "level_testing.html",
        {
            "request": request,
            "tab": "forecast",
            "forecast_obj": last_forecast,
            "report": last_report,
            "log": journal.view_history(),
            "params": LAST_PARAMS,
            "preview": preview,
        },
    )


@app.post("/level-testing/forecast", response_class=HTMLResponse)
async def level_forecast_post(
    request: Request,
    difficulty: int = Form(50),
    enemies: int = Form(10),
    reward: int = Form(100),
):
    """
    Кнопка "Рассчитать прогноз":
    запускаем сценарий тестирования уровня из Application,
    затем показываем последний прогноз, отчёт и журнал.
    """
    LAST_PARAMS["difficulty"] = difficulty
    LAST_PARAMS["enemies"] = enemies
    LAST_PARAMS["reward"] = reward

    core_app.start()

    forecast_repo = container.resolve("repo:forecast")
    report_repo = container.resolve("repo:report")
    journal: JournalManager = container.resolve(JournalManager)

    forecasts = forecast_repo.get_all()
    reports = report_repo.get_all()
    last_forecast = forecasts[-1] if forecasts else None
    last_report = reports[-1] if reports else None

    preview = compute_preview(difficulty, enemies, reward)

    return templates.TemplateResponse(
        "level_testing.html",
        {
            "request": request,
            "tab": "forecast",
            "forecast_obj": last_forecast,
            "report": last_report,
            "log": journal.view_history(),
            "params": LAST_PARAMS,
            "preview": preview,
        },
    )


@app.get("/level-testing/recommendations", response_class=HTMLResponse)
async def level_recommendations(request: Request):
    """
    Вкладка "Рекомендации":
    используем последнее поле recommendations из прогноза +
    чуть-чуть статических вариантов.
    """
    forecast_repo = container.resolve("repo:forecast")
    forecasts = forecast_repo.get_all()
    last_forecast = forecasts[-1] if forecasts else None

    base_text = last_forecast.recommendations if last_forecast else "Нет активного прогноза"

    recs = build_recs(base_text)
    return templates.TemplateResponse(
        "level_testing.html",
        {
            "request": request,
            "tab": "recs",
            "recs": recs,
            "params": LAST_PARAMS,
        },
    )


@app.post("/level-testing/recommendations", response_class=HTMLResponse)
async def apply_recommendation(
    request: Request,
    action: str = Form(...),
):
    forecast_repo = container.resolve("repo:forecast")
    forecasts = forecast_repo.get_all()
    last_forecast = forecasts[-1] if forecasts else None
    base_text = last_forecast.recommendations if last_forecast else "Нет активного прогноза"

    if action == "lower_diff":
        LAST_PARAMS["difficulty"] = max(0, LAST_PARAMS["difficulty"] - 10)
        msg = "Сложность снижена на 10%."
    elif action == "more_reward":
        LAST_PARAMS["reward"] = min(200, LAST_PARAMS["reward"] + 20)
        msg = "Награды увеличены на 20%."
    elif action == "add_checkpoint":
        LAST_PARAMS["enemies"] = max(0, LAST_PARAMS["enemies"] - 2)
        msg = "Добавлена контрольная точка — меньше повторных попыток."
    else:
        msg = "Рекомендация применена."

    recs = build_recs(base_text)
    preview = compute_preview(
        LAST_PARAMS["difficulty"], LAST_PARAMS["enemies"], LAST_PARAMS["reward"]
    )

    return templates.TemplateResponse(
        "level_testing.html",
        {
            "request": request,
            "tab": "recs",
            "recs": recs,
            "params": LAST_PARAMS,
            "preview": preview,
            "message": msg,
        },
    )


@app.get("/reports", response_class=HTMLResponse)
async def reports_setup(request: Request):
    metrics = [
        "Количество игроков",
        "Процент прохождения",
        "Среднее время прохождения",
        "Доход от уровня",
        "Вовлечённость игроков",
        "Удержание игроков",
    ]
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "stage": "setup",
            "metrics": metrics,
            "params": LAST_PARAMS,
        },
    )


@app.post("/reports/generate", response_class=HTMLResponse)
async def reports_generate(request: Request):
    """
    Генерация отчёта:
    используем реальные прогнозы из репозитория, но без сложной математики.
    Берём последний прогноз и делаем из него основные числа.
    """
    forecast_repo = container.resolve("repo:forecast")
    forecasts = forecast_repo.get_all()
    last_forecast = forecasts[-1] if forecasts else None

    preview = compute_preview(
        LAST_PARAMS["difficulty"], LAST_PARAMS["enemies"], LAST_PARAMS["reward"]
    )

    if last_forecast:
        passability_pct = round(last_forecast.passability_score * 100)
        difficulty_pct = round(getattr(last_forecast, "difficulty", 0.0) * 100)
    else:
        passability_pct = preview["completion"]
        difficulty_pct = LAST_PARAMS["difficulty"]

    revenue_val = max(
        50_000,
        int(
            200_000
            + (LAST_PARAMS["reward"] - 100) * 1500
            - LAST_PARAMS["difficulty"] * 500
            - (LAST_PARAMS["enemies"] - 10) * 800
        ),
    )
    players_val = max(500, preview["expected_players"])

    report = {
        "players": f"{players_val:,}".replace(",", " "),
        "players_delta": "+15%" if players_val >= 900 else "+5%",
        "completion": f"{passability_pct}%",
        "completion_delta": "+5%" if passability_pct > 0 else "0%",
        "avg_time": f"{preview['avg_time']} мин",
        "avg_time_delta": "-8%" if preview["avg_time"] <= 35 else "-2%",
        "revenue": f"₽{revenue_val:,}".replace(",", " "),
        "revenue_delta": "+22%" if revenue_val >= 220_000 else "+8%",
        "difficulty": f"{difficulty_pct}%",
        "server_load": preview["server_load"],
    }
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "stage": "result",
            "report": report,
            "params": LAST_PARAMS,
        },
    )


@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return templates.TemplateResponse(
        "exit.html",
        {"request": request},
    )
