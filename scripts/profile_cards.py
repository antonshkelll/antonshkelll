"""Генерирует SVG для профиля GitHub: шапку и карточки проектов в светлой и тёмной теме.

Запуск из корня репозитория: python scripts/profile_cards.py
Карточка Subly нарисована вручную и скриптом не перезаписывается."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

THEMES = {
    "light": dict(bg="#ffffff", card="#f5f5f7", ink="#1d1d1f", muted="#6e6e73"),
    "dark": dict(bg="#0d1117", card="#1c1c1e", ink="#f5f5f7", muted="#a1a1a6"),
}
ACCENT = {
    "blue": ("#0071e3", "#2997ff"), "green": ("#248a3d", "#30d158"), "red": ("#d70015", "#ff453a"),
    "purple": ("#8944ab", "#bf5af2"), "orange": ("#bf4800", "#ff9f0a"), "teal": ("#0b7285", "#64d2ff"),
}


def header(theme: str) -> str:
    t = THEMES[theme]
    blue = ACCENT["blue"][0 if theme == "light" else 1]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 330" width="1280" height="330" role="img" aria-label="Антон Шкель">
  <rect width="1280" height="330" fill="{t['bg']}"/>
  <text x="64" y="92" font-family="{FONT}" font-size="24" font-weight="600" fill="{blue}">Продуктовая аналитика · Данные · Финтех</text>
  <text x="60" y="186" font-family="{FONT}" font-size="88" font-weight="700" letter-spacing="-2" fill="{t['ink']}">Антон Шкель.</text>
  <text x="64" y="244" font-family="{FONT}" font-size="30" fill="{t['muted']}">Делаю продукты и считаю, что с ними происходит.</text>
  <text x="64" y="284" font-family="{FONT}" font-size="30" fill="{t['muted']}">Москва, Финансовый университет.</text>
</svg>"""


def card(theme: str, c: dict) -> str:
    t = THEMES[theme]
    accent = ACCENT[c["color"]][0 if theme == "light" else 1]
    desc = "".join(f'<text x="44" y="{168 + i * 32}" font-family="{FONT}" font-size="23" fill="{t["muted"]}">{escape(line)}</text>'
                   for i, line in enumerate(c["desc"]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 380" width="640" height="380" role="img" aria-label="{escape(c['title'])}">
  <rect width="640" height="380" fill="{t['bg']}"/>
  <rect x="8" y="8" width="624" height="364" rx="30" fill="{t['card']}"/>
  <text x="44" y="70" font-family="{FONT}" font-size="20" font-weight="600" fill="{accent}">{escape(c['eyebrow'])}</text>
  <text x="42" y="122" font-family="{FONT}" font-size="44" font-weight="700" letter-spacing="-1" fill="{t['ink']}">{escape(c['title'])}</text>
  {desc}
  <text x="42" y="312" font-family="{FONT}" font-size="58" font-weight="700" letter-spacing="-1.5" fill="{accent}">{escape(c['metric'])}</text>
  <text x="44" y="344" font-family="{FONT}" font-size="19" fill="{t['muted']}">{escape(c['caption'])}</text>
</svg>"""


CARDS = [
    dict(slug="splitlab", color="blue", eyebrow="Продуктовая аналитика", title="SplitLab",
         desc=["Оплата частями после 283-ФЗ: метрики,", "юнит-экономика, DiD и A/B-тест с CUPED"],
         metric="+15,1%", caption="конверсии в покупку частями в A/B-тесте"),
    dict(slug="uplift", color="green", eyebrow="Causal ML · реальные данные", title="Uplift",
         desc=["Кому отправлять предложение, а кому нет:", "эксперимент, Qini-кривые, IPW-политики"],
         metric="64 000", caption="клиентов в реальном рандомизированном тесте"),
    dict(slug="drophunter", color="red", eyebrow="Антифрод", title="DropHunter",
         desc=["Поиск дропперов в P2P-переводах:", "SQL-признаки, бустинг, порог по деньгам"],
         metric="0,81", caption="PR-AUC против 0,36 у правил"),
    dict(slug="txgpt", color="purple", eyebrow="Языковые модели", title="TxGPT",
         desc=["GPT с нуля на PyTorch: свой BPE, attention,", "предобучение, сравнение с бейзлайном"],
         metric="2 млн", caption="параметров, обучение на обычном процессоре"),
    dict(slug="finpilot", color="orange", eyebrow="AI-агенты · MCP", title="finpilot",
         desc=["Банковская выписка для Claude и Cursor:", "подписки, необычные списания, прогноз"],
         metric="7", caption="инструментов для AI-ассистента, данные локально"),
    dict(slug="pulse", color="teal", eyebrow="Данные · автоматизация", title="Пульс рынка",
         desc=["Дашборд по данным Московской биржи,", "который обновляется сам"],
         metric="каждую ночь", caption="новые торги через GitHub Actions"),
]


def wide(theme: str, w: dict) -> str:
    """Широкая карточка 1280×380: текст слева, мини-витрина продукта справа."""
    t = THEMES[theme]
    accent = ACCENT[w["color"]][0 if theme == "light" else 1]
    panel = "#ffffff" if theme == "light" else "#2c2c2e"
    stroke = "#e3e3e8" if theme == "light" else "#3a3a3c"
    desc = "".join(f'<text x="48" y="{180 + i * 32}" font-family="{FONT}" font-size="24" fill="{t["muted"]}">{escape(line)}</text>'
                   for i, line in enumerate(w["desc"]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 380" width="1280" height="380" role="img" aria-label="{escape(w['title'])}">
  <rect width="1280" height="380" fill="{t['bg']}"/>
  <rect x="8" y="8" width="1264" height="364" rx="30" fill="{t['card']}"/>
  <text x="48" y="74" font-family="{FONT}" font-size="20" font-weight="600" fill="{accent}">{escape(w['eyebrow'])}</text>
  <text x="46" y="134" font-family="{FONT}" font-size="50" font-weight="700" letter-spacing="-1.5" fill="{t['ink']}">{escape(w['title'])}</text>
  {desc}
  <text x="48" y="282" font-family="{FONT}" font-size="20" font-weight="600" fill="{t['ink']}">{escape(w['stack'])}</text>
  <text x="48" y="320" font-family="{FONT}" font-size="18" fill="{t['muted']}">{escape(w['caption'])}</text>
  <rect x="872" y="40" width="344" height="314" rx="26" fill="{panel}" stroke="{stroke}"/>
  {w['panel'](theme, t, accent)}
</svg>"""


def sbp_panel(theme, t, accent):
    """Мини-график: сколько продавец платит с чека 1 700 ₽."""
    rows = [("Карта 2% + НДС", 41.48, ACCENT["red"][0 if theme == "light" else 1]),
            ("СБП 0,7%", 11.90, accent),
            ("Цифровой рубль 2027", 5.10, ACCENT["green"][0 if theme == "light" else 1])]
    out = [f'<text x="900" y="84" font-family="{FONT}" font-size="15" fill="{t["muted"]}">Продавец платит с чека 1 700 ₽</text>']
    for i, (label, value, color) in enumerate(rows):
        y = 118 + i * 76
        width = 288 * value / 41.48
        out.append(f'<text x="900" y="{y}" font-family="{FONT}" font-size="15" font-weight="600" fill="{t["ink"]}">{escape(label)}</text>')
        out.append(f'<rect x="900" y="{y + 10}" width="{width:.0f}" height="26" rx="8" fill="{color}"/>')
        money = f"{value:.2f} ₽".replace(".", ",")
        if width > 220:   # длинная полоса — подпись внутри, белым
            out.append(f'<text x="{900 + width - 12:.0f}" y="{y + 29}" text-anchor="end" font-family="{FONT}" font-size="16" font-weight="700" fill="#ffffff">{money}</text>')
        else:
            out.append(f'<text x="{900 + width + 10:.0f}" y="{y + 29}" font-family="{FONT}" font-size="16" font-weight="700" fill="{t["ink"]}">{money}</text>')
    out.append(f'<text x="900" y="338" font-family="{FONT}" font-size="13" fill="{t["muted"]}">расчёт по тарифам на 20.10.2026</text>')
    return "\n  ".join(out)


def nab_panel(theme, t, accent):
    """Мини-экран «Мои обращения»."""
    rows = [("Вопрос", "Ответ получен · ★ 5", ACCENT["green"]), ("Поломка", "В работе", ACCENT["orange"]),
            ("Инициатива", "Принята", ACCENT["blue"]), ("Анонс", "Записались · напомним", ACCENT["purple"])]
    out = [f'<text x="900" y="84" font-family="{FONT}" font-size="15" fill="{t["muted"]}">Мои обращения</text>']
    row_bg = "#f5f5f7" if theme == "light" else "#3a3a3c"
    for i, (kind, status, pair) in enumerate(rows):
        y = 100 + i * 60
        color = pair[0 if theme == "light" else 1]
        out.append(f'<rect x="888" y="{y}" width="312" height="50" rx="12" fill="{row_bg}"/>')
        out.append(f'<rect x="900" y="{y + 13}" width="24" height="24" rx="7" fill="{color}"/>')
        out.append(f'<text x="936" y="{y + 31}" font-family="{FONT}" font-size="16" font-weight="600" fill="{t["ink"]}">{escape(kind)}</text>')
        out.append(f'<text x="1188" y="{y + 31}" text-anchor="end" font-family="{FONT}" font-size="14" fill="{t["muted"]}">{escape(status)}</text>')
    return "\n  ".join(out)


WIDE = [
    dict(slug="sbp", color="teal", eyebrow="Исследование · финтех · данные Банка России", title="Экономика быстрого платежа",
         desc=["Сколько стоит продавцу платёж картой, через СБП", "и в цифровых рублях — и куда движется рынок."],
         stack="Python · данные ЦБ · юнит-экономика · GitHub Pages",
         caption="Исследование на 29 страниц, 60 слайдов и веб-калькулятор для бизнеса", panel=sbp_panel),
    dict(slug="nab", color="purple", eyebrow="Живой продукт · Telegram · версия 3", title="Спроси ССт НАБ",
         desc=["Бот и Mini App студсовета: обращения со статусами,", "анонсы, опросы, админка и метрики без слежки."],
         stack="Python · aiogram 3 · aiohttp · SQLite · Telegram Mini App",
         caption="164 автопроверки · SLA по обращениям · отчёт в Excel каждый месяц", panel=nab_panel),
]

for theme in THEMES:
    (OUT / f"header-{theme}.svg").write_text(header(theme), encoding="utf-8", newline="\n")
    for c in CARDS:
        (OUT / f"{c['slug']}-{theme}.svg").write_text(card(theme, c), encoding="utf-8", newline="\n")
    for w in WIDE:
        (OUT / f"{w['slug']}-{theme}.svg").write_text(wide(theme, w), encoding="utf-8", newline="\n")
print(sorted(p.name for p in OUT.iterdir()))
