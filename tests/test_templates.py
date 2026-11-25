from __future__ import annotations

import base64
import csv
import os
from datetime import date
from pathlib import Path

import ui.logos as logos

from ui.components import (
    favorite_card,
    format_date_id,
    hero_html,
    initials,
    pct,
    season_id,
)
from ui.logos import logo_data_uri, logo_path, team_badge_html


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


def test_all_ucl_teams_have_local_png_logos():
    teams_csv = Path(__file__).resolve().parent.parent / "data" / "ucl_2026_27_teams.csv"
    with teams_csv.open(encoding="utf-8") as handle:
        teams = [row["team_name"] for row in csv.DictReader(handle)]

    assert len(teams) == 36
    for team in teams:
        path = logo_path(team)
        assert path is not None and path.is_file(), f"Missing logo for {team}"
        uri = logo_data_uri(team)
        assert uri is not None and uri.startswith("data:image/png;base64,")


def test_favorite_card_renders_logo_and_escapes_fallback():
    known_html = favorite_card(1, "Arsenal", 18.5, 17.0, 20.0, 31.0, 48.0)
    assert 'class="ucl-badge has-logo"' in known_html
    assert 'src="data:image/png;base64,' in known_html

    unknown_html = team_badge_html("<Unknown FC>", initials("<Unknown FC>"))
    assert "has-logo" not in unknown_html
    assert "&lt;F" in unknown_html
    assert "<Unknown" not in unknown_html


def test_app_mark_data_uri_reloads_when_file_changes(tmp_path, monkeypatch):
    mark = tmp_path / "logo-app-mark.png"
    monkeypatch.setattr(logos, "APP_MARK_PATH", mark)

    assert logos.app_mark_data_uri() is None

    mark.write_bytes(b"v1-bytes")
    expected_v1 = "data:image/png;base64," + base64.b64encode(b"v1-bytes").decode("ascii")
    assert logos.app_mark_data_uri() == expected_v1

    st = mark.stat()
    mark.write_bytes(b"v2-bytes")
    os.utime(mark, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000))
    expected_v2 = "data:image/png;base64," + base64.b64encode(b"v2-bytes").decode("ascii")
    assert logos.app_mark_data_uri() == expected_v2

    mark.write_bytes(b"v3-longer-bytes")
    expected_v3 = "data:image/png;base64," + base64.b64encode(b"v3-longer-bytes").decode("ascii")
    assert logos.app_mark_data_uri() == expected_v3

    mark.unlink()
    assert logos.app_mark_data_uri() is None


def test_logo_data_uri_reloads_when_file_changes(tmp_path, monkeypatch):
    monkeypatch.setattr(logos, "LOGO_DIR", tmp_path)
    badge = tmp_path / "arsenal.png"

    badge.write_bytes(b"badge-v1")
    expected_v1 = "data:image/png;base64," + base64.b64encode(b"badge-v1").decode("ascii")
    assert logos.logo_data_uri("Arsenal") == expected_v1

    st = badge.stat()
    badge.write_bytes(b"badge-v2")
    os.utime(badge, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000))
    expected_v2 = "data:image/png;base64," + base64.b64encode(b"badge-v2").decode("ascii")
    assert logos.logo_data_uri("Arsenal") == expected_v2
