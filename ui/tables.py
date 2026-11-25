"""Custom SiKupingBesar HTML tables matching the yellow, cream, and ink theme."""

from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st

from ui.components import initials, number, pct
from ui.logos import team_badge_html


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def _meter_cell(value: float, digits: int = 1, tone: str = "gold", scale_max: float = 100.0) -> str:
    width = _clamp((float(value) / scale_max) * 100.0 if scale_max > 0 else 0.0)
    return (
        '<div class="ucl-meter">'
        '<div class="ucl-meter-track">'
        f'<span class="ucl-meter-fill fill-{tone}" style="width:{width:.1f}%"></span>'
        "</div>"
        f'<span class="ucl-meter-val">{pct(value, digits)}</span>'
        "</div>"
    )


def _rating_meter_cell(value: float, max_val: float, tone: str = "gold") -> str:
    width = _clamp((float(value) / max_val) * 100.0 if max_val > 0 else 0.0)
    return (
        '<div class="ucl-meter">'
        '<div class="ucl-meter-track">'
        f'<span class="ucl-meter-fill fill-{tone}" style="width:{width:.1f}%"></span>'
        "</div>"
        f'<span class="ucl-meter-val">{number(value, 3)}</span>'
        "</div>"
    )


def _heat_cell(value: float, digits: int = 1, bold: bool = False) -> str:
    ratio = _clamp(value) / 100.0
    alpha = 0.04 + ratio * 0.42
    border_alpha = 0.10 + ratio * 0.38
    cls = "ucl-heat is-strong" if bold else "ucl-heat"
    style = (
        f"background:rgba(255,184,0,{alpha:.3f});"
        f"border-color:rgba(224,158,0,{border_alpha:.3f});"
    )
    return f'<span class="{cls}" style="{style}">{pct(value, digits)}</span>'


def _team_cell(team: str, tag_html: str = "") -> str:
    badge = team_badge_html(team, initials(team), css_class="ucl-badge sm")
    return (
        '<div class="ucl-td-team">'
        f"{badge}"
        '<div class="ucl-td-team-meta">'
        f'<span class="ucl-td-team-name">{escape(team)}</span>'
        f"{tag_html}"
        "</div></div>"
    )


def standings_table_html(table: pd.DataFrame) -> str:
    """Build a single unified 36-team UCL League Phase standings table."""
    standings = table.sort_values(
        ["avg_points", "avg_position"], ascending=[False, True]
    ).reset_index(drop=True)

    max_champion = max(float(standings["champion"].max() or 25.0), 10.0)

    rows_html: list[str] = []
    for idx, row in standings.iterrows():
        pos = idx + 1
        team = str(row["team"])
        if pos <= 8:
            zone_cls = "zone-top8"
            pos_cls = "ucl-pos top8"
            tag = '<span class="ucl-zone-tag tag-top8">Lolos 16 Besar</span>'
        elif pos <= 24:
            zone_cls = "zone-playoff"
            pos_cls = "ucl-pos playoff"
            tag = '<span class="ucl-zone-tag tag-playoff">Playoff</span>'
        else:
            zone_cls = "zone-out"
            pos_cls = "ucl-pos out"
            tag = '<span class="ucl-zone-tag tag-out">Tersingkir</span>'

        cutoff = " zone-cutoff" if pos in (8, 24) else ""
        rows_html.append(
            f'<tr class="{zone_cls}{cutoff}">'
            f'<td class="col-rank"><span class="{pos_cls}">{pos}</span></td>'
            f'<td class="col-team">{_team_cell(team, tag)}</td>'
            f'<td class="col-num is-bold">{number(float(row["avg_points"]), 2)}</td>'
            f'<td class="col-num is-muted">{number(float(row["avg_position"]), 1)}</td>'
            f'<td class="col-bar">{_meter_cell(float(row["top8"]), 1, "ink", 100.0)}</td>'
            f'<td class="col-bar">{_meter_cell(float(row["top24"]), 1, "green", 100.0)}</td>'
            f'<td class="col-bar">{_meter_cell(float(row["champion"]), 2, "gold", max_champion)}</td>'
            "</tr>"
        )

    legend = (
        '<div class="ucl-table-legend">'
        '<div class="ucl-zone-pills">'
        '<span class="ucl-zone-item"><i class="dot dot-top8"></i>1–8 Lolos langsung 16 Besar</span>'
        '<span class="ucl-zone-item"><i class="dot dot-playoff"></i>9–24 Playoff knockout</span>'
        '<span class="ucl-zone-item"><i class="dot dot-out"></i>25–36 Tersingkir</span>'
        "</div>"
        f'<span class="ucl-table-meta">{len(standings)} tim · diurutkan dari rata-rata poin</span>'
        "</div>"
    )

    header = (
        "<thead><tr>"
        '<th class="col-rank">#</th>'
        '<th class="col-team">Klub</th>'
        '<th class="col-num is-sorted">Poin</th>'
        '<th class="col-num">Posisi</th>'
        '<th class="col-bar">Top 8</th>'
        '<th class="col-bar">Top 24</th>'
        '<th class="col-bar is-sorted">Juara</th>'
        "</tr></thead>"
    )

    return (
        '<div class="ucl-table-card">'
        f"{legend}"
        '<div class="ucl-table-wrap">'
        f'<table class="ucl-table">{header}<tbody>{"".join(rows_html)}</tbody></table>'
        "</div></div>"
    )


def render_standings_table(table: pd.DataFrame) -> None:
    st.markdown(standings_table_html(table), unsafe_allow_html=True)


def probability_table_html(view: pd.DataFrame, active_sort: str = "Juara") -> str:
    """Build the full stage-by-stage probability table."""
    if view.empty:
        return (
            '<div class="ucl-table-card">'
            '<div class="ucl-table-empty">Tidak ada tim yang cocok dengan pencarian tersebut.</div>'
            "</div>"
        )

    columns = [
        ("Peringkat", "#", "col-rank"),
        ("Tim", "Klub", "col-team"),
        ("Laga", "Laga", "col-num"),
        ("Juara", "Juara", "col-num"),
        ("CI 95%", "CI 95%", "col-ci"),
        ("Final", "Final", "col-num"),
        ("Semifinal", "Semifinal", "col-num"),
        ("Perempat", "Perempat", "col-num"),
        ("16 Besar", "16 Besar", "col-num"),
        ("Top 8", "Top 8", "col-num"),
        ("Top 24", "Top 24", "col-num"),
        ("Poin", "Poin", "col-num"),
        ("Posisi", "Posisi", "col-num"),
    ]

    th_cells = []
    for key, label, cls in columns:
        sorted_cls = f"{cls} is-sorted" if key == active_sort else cls
        th_cells.append(f'<th class="{sorted_cls}">{escape(label)}</th>')
    header = f'<thead><tr>{"".join(th_cells)}</tr></thead>'

    rows_html: list[str] = []
    for _, row in view.iterrows():
        rank = int(row["Peringkat"])
        team = str(row["Tim"])
        laga = int(row["Laga"])
        if rank == 1:
            pos_cls = "ucl-pos gold"
        elif rank <= 3:
            pos_cls = "ucl-pos top8"
        else:
            pos_cls = "ucl-pos"

        laga_cls = "ucl-pill-count is-zero" if laga == 0 else "ucl-pill-count"
        rows_html.append(
            "<tr>"
            f'<td class="col-rank"><span class="{pos_cls}">{rank}</span></td>'
            f'<td class="col-team">{_team_cell(team)}</td>'
            f'<td class="col-num"><span class="{laga_cls}">{laga}</span></td>'
            f'<td class="col-num">{_heat_cell(float(row["Juara"]), 2, bold=True)}</td>'
            f'<td class="col-ci"><span class="ucl-ci-pill">{escape(str(row["CI 95%"]))}</span></td>'
            f'<td class="col-num">{_heat_cell(float(row["Final"]), 1)}</td>'
            f'<td class="col-num">{_heat_cell(float(row["Semifinal"]), 1)}</td>'
            f'<td class="col-num">{_heat_cell(float(row["Perempat"]), 1)}</td>'
            f'<td class="col-num">{_heat_cell(float(row["16 Besar"]), 1)}</td>'
            f'<td class="col-num">{_heat_cell(float(row["Top 8"]), 1)}</td>'
            f'<td class="col-num">{_heat_cell(float(row["Top 24"]), 1)}</td>'
            f'<td class="col-num is-bold">{number(float(row["Poin"]), 2)}</td>'
            f'<td class="col-num is-muted">{number(float(row["Posisi"]), 2)}</td>'
            "</tr>"
        )

    return (
        '<div class="ucl-table-card">'
        '<div class="ucl-table-wrap">'
        f'<table class="ucl-table is-dense">{header}<tbody>{"".join(rows_html)}</tbody></table>'
        "</div></div>"
    )


def render_probability_table(view: pd.DataFrame, active_sort: str = "Juara") -> None:
    st.markdown(probability_table_html(view, active_sort=active_sort), unsafe_allow_html=True)


def ratings_table_html(ratings_df: pd.DataFrame) -> str:
    """Build the themed team attack/defence ratings table for the Simulator page."""
    frame = ratings_df.copy()
    frame["net"] = frame["attack"] / frame["defence"].clip(lower=1e-6)
    frame = frame.sort_values("net", ascending=False).reset_index(drop=True)

    max_att = max(float(frame["attack"].max() or 2.0), 1.5)
    max_def = max(float(frame["defence"].max() or 1.5), 1.2)

    header = (
        "<thead><tr>"
        '<th class="col-rank">#</th>'
        '<th class="col-team">Klub</th>'
        '<th class="col-bar">Serang (a)</th>'
        '<th class="col-bar">Bertahan (d)</th>'
        '<th class="col-num is-sorted">Rasio a/d</th>'
        '<th class="col-num">Laga</th>'
        "</tr></thead>"
    )

    rows_html: list[str] = []
    for idx, row in frame.iterrows():
        rank = idx + 1
        team = str(row["team"])
        matches_n = int(row["matches"])
        pos_cls = "ucl-pos gold" if rank == 1 else ("ucl-pos top8" if rank <= 3 else "ucl-pos")
        laga_cls = "ucl-pill-count is-zero" if matches_n == 0 else "ucl-pill-count"
        rows_html.append(
            "<tr>"
            f'<td class="col-rank"><span class="{pos_cls}">{rank}</span></td>'
            f'<td class="col-team">{_team_cell(team)}</td>'
            f'<td class="col-bar">{_rating_meter_cell(float(row["attack"]), max_att, "gold")}</td>'
            f'<td class="col-bar">{_rating_meter_cell(float(row["defence"]), max_def, "warm")}</td>'
            f'<td class="col-num is-bold">{number(float(row["net"]), 2)}</td>'
            f'<td class="col-num"><span class="{laga_cls}">{matches_n}</span></td>'
            "</tr>"
        )

    return (
        '<div class="ucl-table-card">'
        '<div class="ucl-table-wrap is-compact-scroll">'
        f'<table class="ucl-table">{header}<tbody>{"".join(rows_html)}</tbody></table>'
        "</div></div>"
    )


def render_ratings_table(ratings_df: pd.DataFrame) -> None:
    st.markdown(ratings_table_html(ratings_df), unsafe_allow_html=True)
