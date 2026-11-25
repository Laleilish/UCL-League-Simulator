"""Club logo loader and HTML badge helper for UCL teams."""

from __future__ import annotations

import base64
import re
import unicodedata
from functools import lru_cache
from html import escape
from pathlib import Path

LOGO_DIR = Path(__file__).resolve().parent.parent / "assets" / "logos"

# Common alternative names mapped to canonical logo slugs.
SLUG_ALIASES: dict[str, str] = {
    "aek": "aek-athens",
    "atletico-madrid": "atletico-de-madrid",
    "ath-madrid": "atletico-de-madrid",
    "bayern-munich": "bayern-munchen",
    "bodo-glimt": "bodo-glimt",
    "dortmund": "borussia-dortmund",
    "fenerbahce": "fenerbahce",
    "inter-milan": "inter",
    "internazionale": "inter",
    "lask-linz": "lask",
    "rb-leipzig": "leipzig",
    "rc-lens": "lens",
    "man-city": "manchester-city",
    "man-united": "manchester-united",
    "psg": "paris-saint-germain",
    "paris-sg": "paris-saint-germain",
    "fc-porto": "porto",
    "psv-eindhoven": "psv",
    "betis": "real-betis",
    "as-roma": "roma",
    "sabah-fk": "sabah",
    "shakhtar": "shakhtar-donetsk",
    "slavia-prague": "slavia-praha",
    "sporting": "sporting-cp",
    "stuttgart": "vfb-stuttgart",
    "viking-fk": "viking",
}


def slugify_team(team: str) -> str:
    """Convert a team name into a normalized ASCII filename slug."""
    cleaned = team.replace("ø", "o").replace("Ø", "O").replace("đ", "d").replace("Đ", "D")
    normalized = unicodedata.normalize("NFKD", cleaned)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return SLUG_ALIASES.get(slug, slug)


def logo_path(team: str) -> Path | None:
    """Return the local PNG path for a team logo if available."""
    if not team:
        return None
    candidate = LOGO_DIR / f"{slugify_team(team)}.png"
    return candidate if candidate.is_file() else None


@lru_cache(maxsize=128)
def logo_data_uri(team: str) -> str | None:
    """Return a cached base64 PNG data URI for a team logo, or None if missing."""
    path = logo_path(team)
    if path is None:
        return None
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def team_badge_html(
    team: str,
    fallback_text: str,
    css_class: str = "ucl-badge",
) -> str:
    """Render an HTML club logo badge, falling back to escaped initials."""
    uri = logo_data_uri(team)
    if uri:
        return (
            f'<span class="{css_class} has-logo">'
            f'<img src="{uri}" alt="{escape(team)}" loading="lazy" />'
            "</span>"
        )
    return f'<span class="{css_class}">{escape(fallback_text)}</span>'
