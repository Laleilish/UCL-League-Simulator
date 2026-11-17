"""Reusable HTML cards and formatting helpers (all text is escaped)."""

from __future__ import annotations

from datetime import date, datetime
from html import escape
from pathlib import Path

import streamlit as st

TEMPLATE_DIR = Path(__file__).parent / "templates"

MONTHS_ID = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des",
}


def pct(value: float, digits: int = 1) -> str:
    """Format a percentage with Indonesian decimal comma."""
    return f"{value:.{digits}f}%".replace(".", ",")


def number(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def int_id(value: int | float) -> str:
    return f"{int(value):,}".replace(",", ".")


def format_date_id(value: date | datetime | None) -> str:
    if value is None:
        return "—"
    if isinstance(value, datetime):
        value = value.date()
    return f"{value.day:02d} {MONTHS_ID[value.month]} {value.year}"


def season_id(value: date | datetime | None) -> str:
    """Return the season label for a date, e.g. 2026/27."""
    if value is None:
        return "—"
    if isinstance(value, datetime):
        value = value.date()
    start = value.year if value.month >= 7 else value.year - 1
    return f"{start}/{(start + 1) % 100:02d}"


def initials(team: str) -> str:
    parts = [part for part in team.replace("-", " ").replace("/", " ").split() if part]
    if not parts:
        return "?"
    letters = "".join(part[0] for part in parts)
    if len(letters) < 2:
        return team[:3].upper()
    return letters[:3].upper()


def hero_html(
    eyebrow: str,
    title: str,
    description: str,
    chips: list[str],
) -> str:
    template = (TEMPLATE_DIR / "hero.html").read_text(encoding="utf-8")
    chip_html = "".join(
        f'<span class="chip">{escape(chip)}</span>' for chip in chips
    )
    return (
        template.replace("{{EYEBROW}}", escape(eyebrow))
        .replace("{{TITLE}}", escape(title))
        .replace("{{DESCRIPTION}}", escape(description))
        .replace("{{CHIPS}}", chip_html)
    )


def hero(
    eyebrow: str,
    title: str,
    description: str,
    chips: list[str],
) -> None:
    st.iframe(
        hero_html(eyebrow, title, description, chips),
        height=260,
    )


def section_header(
    title: str,
    eyebrow: str = "",
    description: str = "",
) -> None:
    eyebrow_html = (
        f'<span class="ucl-eyebrow">{escape(eyebrow)}</span>' if eyebrow else ""
    )
    description_html = f"<p>{escape(description)}</p>" if description else ""
    st.markdown(
        f'<div class="ucl-section">{eyebrow_html}<h2>{escape(title)}</h2>'
        f"{description_html}</div>",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, sub: str = "") -> str:
    sub_html = f'<span class="sub">{escape(sub)}</span>' if sub else ""
    return (
        '<div class="ucl-card ucl-kpi">'
        f'<span class="label">{escape(label)}</span>'
        f'<span class="value">{escape(value)}</span>'
        f"{sub_html}</div>"
    )


def metric_grid(cards: list[str]) -> None:
    st.markdown(
        f'<div class="ucl-kpi-grid">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )


def favorite_card(
    rank: int,
    team: str,
    champion: float,
    ci_low: float,
    ci_high: float,
    final_probability: float,
    semi_probability: float,
) -> str:
    leader = " is-leader" if rank == 1 else ""
    tag = "Favorit juara" if rank == 1 else "Pesaing"
    return (
        f'<div class="ucl-fav{leader}">'
        '<div class="ucl-fav-top">'
        f'<span class="ucl-rank">Peringkat {rank}</span>'
        f'<span class="ucl-fav-tag">{tag}</span>'
        "</div>"
        '<div class="ucl-team">'
        f'<span class="ucl-badge">{escape(initials(team))}</span>'
        '<div><div class="ucl-team-name">'
        f"{escape(team)}"
        '</div><div class="ucl-team-sub">Peluang juara</div></div>'
        "</div>"
        f'<div class="ucl-fav-value">{pct(champion, 2)}</div>'
        f'<div class="ucl-fav-ci">CI 95%: {pct(ci_low, 2)} – {pct(ci_high, 2)}</div>'
        '<div class="ucl-fav-split">'
        f'<div><span>Final</span><strong>{pct(final_probability)}</strong></div>'
        f'<div><span>Semifinal</span><strong>{pct(semi_probability)}</strong></div>'
        "</div></div>"
    )


def note(text: str) -> None:
    st.markdown(f'<div class="ucl-note">{escape(text)}</div>', unsafe_allow_html=True)


def chip_row(items: list[str], dark: bool = False) -> None:
    css = "ucl-chip dark" if dark else "ucl-chip"
    html = "".join(
        f'<span class="{css}">{escape(item)}</span>' for item in items
    )
    st.markdown(f'<div class="ucl-pill-row">{html}</div>', unsafe_allow_html=True)
