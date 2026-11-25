"""Dashboard: the headline title odds, projected table, and stage heatmap."""

from __future__ import annotations

import streamlit as st

from core.pipeline import ModelRun, dataset_summary
from ui import charts
from ui.components import (
    favorite_card,
    format_date_id,
    hero,
    int_id,
    metric_card,
    metric_grid,
    note,
    number,
    pct,
    season_id,
    section_header,
)
from ui.tables import render_standings_table
from ui.theme import PLOTLY_CONFIG


def render(model: ModelRun) -> None:
    table = model.table
    summary = dataset_summary(model.matches)
    leader = table.iloc[0]

    hero(
        eyebrow=f"Musim {season_id(model.latest_played)} · data per {format_date_id(model.latest_played)}",
        title="Peluang juara, bukan tebakan.",
        description=(
            "Model Poisson memakai hasil liga domestik dan UCL untuk memainkan "
            f"sisa musim {int_id(model.n_sims)} kali. Setiap angka disertai "
            "interval kepercayaan 95%."
        ),
        chips=[
            f"{len(model.teams)} tim",
            f"{int_id(model.n_sims)} simulasi",
            "CI 95% Wilson",
            f"{model.n_remaining} laga sisa",
        ],
    )

    metric_grid(
        [
            metric_card(
                "Peluang juara tertinggi",
                pct(leader["champion"], 2),
                str(leader["team"]),
            ),
            metric_card(
                "Tim peserta",
                str(len(model.teams)),
                f"{summary['competitions']} liga domestik + UCL",
            ),
            metric_card(
                "Laga UCL tersisa",
                str(model.n_remaining),
                f"{model.n_played} laga sudah dimainkan",
            ),
            metric_card(
                "Home advantage",
                f"×{number(model.ratings.home_advantage, 2)}",
                "diestimasi dari data"
                if model.settings.home_advantage_mode == "auto"
                else "diatur manual",
            ),
        ]
    )

    section_header(
        "Kandidat juara",
        "Papan atas",
        "Tiga peluang terbesar menjadi juara Eropa, lengkap dengan rentang "
        "ketidakpastiannya.",
    )
    cards = []
    for rank, (_, row) in enumerate(table.head(3).iterrows(), start=1):
        cards.append(
            favorite_card(
                rank=rank,
                team=row["team"],
                champion=row["champion"],
                ci_low=row["ci_low"],
                ci_high=row["ci_high"],
                final_probability=row["final"],
                semi_probability=row["semi"],
            )
        )
    st.markdown(f'<div class="ucl-favorites">{"".join(cards)}</div>', unsafe_allow_html=True)

    section_header(
        "Peluang juara",
        "12 tim teratas",
        "Batang abu-abu menunjukkan selang kepercayaan 95% (Wilson). "
        "Klik legenda untuk menyaring tim.",
    )
    st.plotly_chart(
        charts.champion_bar_figure(table, top_n=12),
        config=PLOTLY_CONFIG,
        width="stretch",
    )

    section_header(
        "Klasemen proyeksi",
        "League phase · 36 tim",
        "Seluruh peserta diurutkan dari rata-rata poin simulasi. Peringkat 1–8 "
        "langsung ke 16 besar, 9–24 ke playoff knockout, dan 25–36 tersingkir.",
    )
    render_standings_table(table)

    section_header(
        "Peluang per babak",
        "Peta jalan",
        "Semakin terang selnya, semakin besar peluang tim mencapai babak tersebut. "
        "Top 24 berarti lolos ke playoff dari league phase.",
    )
    st.plotly_chart(
        charts.stage_heatmap_figure(model.result, table, top_n=14),
        config=PLOTLY_CONFIG,
        width="stretch",
    )

    note(
        "Semua angka adalah peluang hasil simulasi, bukan jaminan. "
        "Model menganggap kekuatan tim tetap dan tidak memakai data cedera, "
        "rotasi, atau motivasi."
    )
