"""Карточка «Сегодня на рынке» для профиля: берёт свежие данные из ru-market-pulse и рисует SVG.

Запускается по расписанию из .github/workflows/pulse.yml. Только стандартная библиотека.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

SOURCE = "https://raw.githubusercontent.com/antonshkelll/ru-market-pulse/main/docs/data.json"
OUT = Path(__file__).resolve().parents[1] / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
THEMES = {
    "light": dict(bg="#ffffff", card="#f5f5f7", ink="#1d1d1f", muted="#6e6e73", up="#248a3d", down="#d70015", line="#0071e3"),
    "dark": dict(bg="#0d1117", card="#1c1c1e", ink="#f5f5f7", muted="#a1a1a6", up="#30d158", down="#ff453a", line="#2997ff"),
}
SHOW = {"IMOEX": "Индекс МосБиржи", "RGBI": "Гособлигации", "CNYRUB": "Юань", "SBER": "Сбербанк"}


def pct(x: float | None) -> str:
    if x is None:
        return "—"
    return f"{x:+.1%}".replace(".", ",").replace("-", "−")


def value(x: float, unit: str) -> str:
    s = f"{x:,.2f}" if x < 1000 else f"{x:,.0f}"
    return s.replace(",", " ").replace(".", ",") + (f" {unit}" if unit and unit != "п." else "")


def sparkline(points: list[float], x0: int, y0: int, w: int, h: int) -> str:
    lo, hi = min(points), max(points)
    span = (hi - lo) or 1
    step = w / (len(points) - 1)
    coords = " ".join(f"{x0 + i * step:.1f},{y0 + h - (p - lo) / span * h:.1f}" for i, p in enumerate(points))
    return coords


def render(data: dict, theme: str) -> str:
    t = THEMES[theme]
    kpi = {k["key"]: k for k in data["kpi"]}
    tiles = []
    for i, key in enumerate(k for k in SHOW if k in kpi):
        k = kpi[key]
        x = 44 + i * 230
        color = t["up"] if (k["d1"] or 0) > 0 else t["down"] if (k["d1"] or 0) < 0 else t["muted"]
        tiles.append(
            f'<text x="{x}" y="132" font-family="{FONT}" font-size="17" fill="{t["muted"]}">{escape(SHOW[key])}</text>'
            f'<text x="{x}" y="170" font-family="{FONT}" font-size="32" font-weight="700" fill="{t["ink"]}">{escape(value(k["last"], k["unit"]))}</text>'
            f'<text x="{x}" y="198" font-family="{FONT}" font-size="17" fill="{color}">{pct(k["d1"])} за день</text>')
    closes = data["series"].get("IMOEX", {}).get("close", [])[-90:]
    line = ""
    if len(closes) > 2:
        line = (f'<polyline points="{sparkline(closes, 44, 236, 872, 64)}" fill="none" stroke="{t["line"]}" '
                f'stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'
                f'<text x="44" y="330" font-family="{FONT}" font-size="15" fill="{t["muted"]}">Индекс МосБиржи за последние 90 торговых дней</text>')
    trade_date = max((k["date"] for k in data["kpi"]), key=lambda d: datetime.strptime(d, "%d.%m.%Y"))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 360" width="960" height="360" role="img" aria-label="Сегодня на рынке">
  <rect width="960" height="360" fill="{t['bg']}"/>
  <rect x="8" y="8" width="944" height="344" rx="30" fill="{t['card']}"/>
  <text x="44" y="66" font-family="{FONT}" font-size="30" font-weight="700" letter-spacing="-0.5" fill="{t['ink']}">Сегодня на рынке</text>
  <text x="916" y="66" text-anchor="end" font-family="{FONT}" font-size="17" fill="{t['muted']}">торги {escape(trade_date)} · обновляется автоматически</text>
  {''.join(tiles)}
  {line}
</svg>"""


def main() -> int:
    try:
        with urllib.request.urlopen(SOURCE, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"Не удалось получить данные: {e}", file=sys.stderr)
        return 0                      # старая карточка остаётся, профиль не ломается
    if not data.get("kpi"):
        print("В данных нет показателей", file=sys.stderr)
        return 0
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"market-{theme}.svg").write_text(render(data, theme), encoding="utf-8")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
