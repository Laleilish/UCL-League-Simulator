from __future__ import annotations

from datetime import date

from ui.components import format_date_id, hero_html, initials, pct, season_id


def test_hero_uses_tailwind_and_escapes_input():
    html = hero_html(
        eyebrow="<b>musim</b>",
        title="<script>alert(1)</script>",
        description="Aman & rapi",
        chips=["36 tim", "<img src=x onerror=alert(1)>"],
    )
    assert "cdn.tailwindcss.com" in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<script>alert(1)</script>" not in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html
    assert "{{TITLE}}" not in html
    assert "&amp;" in html


def test_initials():
    assert initials("Paris Saint-Germain") == "PSG"
    assert initials("Ajax") == "AJA"
    assert initials("Bodo/Glimt") == "BG"
    assert initials("FC Copenhagen") == "FC"


def test_percentage_formatting_uses_comma():
    assert pct(12.34) == "12,3%"
    assert pct(0.5, 2) == "0,50%"


def test_indonesian_date():
    assert format_date_id(date(2025, 11, 25)) == "25 Nov 2025"
    assert format_date_id(None) == "—"


def test_season_label():
    assert season_id(date(2026, 11, 8)) == "2026/27"
    assert season_id(date(2027, 1, 28)) == "2026/27"
    assert season_id(date(2026, 5, 30)) == "2025/26"
    assert season_id(None) == "—"
