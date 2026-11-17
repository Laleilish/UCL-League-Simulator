"""Head-to-head: 1X2 odds, score matrix, and two-leg qualification."""

from __future__ import annotations

import streamlit as st

from core.pipeline import ModelRun
from core.stats import head_to_head, two_leg_qualification
from ui import charts
from ui.components import metric_card, note, number, pct, section_header
from ui.theme import PLOTLY_CONFIG


def render(model: ModelRun) -> None:
    section_header(
        "Head-to-Head",
        "Duel dua tim",
        "Peluang menang, seri, dan kalah dari model Poisson yang sama, plus "
        "matriks skor lengkap.",
    )

    teams = model.table["team"].tolist()
    default_b = 1 if len(teams) > 1 else 0
    select_a, select_b, venue_col = st.columns([1.2, 1.2, 1.1])
    with select_a:
        team_a = st.selectbox(
            "Tim A", teams, index=0, key="h2h_team_a"
        )
    with select_b:
        team_b = st.selectbox(
            "Tim B", teams, index=default_b, key="h2h_team_b"
        )
    with venue_col:
        venue = st.radio(
            "Lokasi laga",
            ("Kandang Tim A", "Netral"),
            horizontal=True,
            key="h2h_venue",
        )

    if team_a == team_b:
        st.info("Pilih dua tim yang berbeda untuk melihat peluang duel.")
        return

    neutral = venue == "Netral"
    result = head_to_head(model.ratings, team_a, team_b, neutral=neutral)

    columns = st.columns(3)
    cards = [
        (
            f"Menang {team_a}",
            pct(result.p_a * 100.0),
            "peluang menang dalam 90 menit",
        ),
        ("Seri", pct(result.p_draw * 100.0), "peluang skor imbang"),
        (
            f"Menang {team_b}",
            pct(result.p_b * 100.0),
            "peluang menang dalam 90 menit",
        ),
    ]
    for column, (label, value, sub) in zip(columns, cards):
        with column:
            st.markdown(metric_card(label, value, sub), unsafe_allow_html=True)

    st.caption(
        f"Total peluang: {pct(result.outcome_total * 100.0)} · "
        f"venue: {'netral' if neutral else f'kandang {team_a}'} · "
        f"home advantage ×{number(model.ratings.home_advantage, 2)}"
    )

    goals_a, goals_b, likely, info = st.columns(4)
    with goals_a:
        st.markdown(
            metric_card(
                f"Ekspektasi gol {team_a}",
                number(result.exp_goals_a, 2),
                "λ tim A",
            ),
            unsafe_allow_html=True,
        )
    with goals_b:
        st.markdown(
            metric_card(
                f"Ekspektasi gol {team_b}",
                number(result.exp_goals_b, 2),
                "λ tim B",
            ),
            unsafe_allow_html=True,
        )
    with likely:
        st.markdown(
            metric_card(
                "Skor paling mungkin",
                f"{result.most_likely_score[0]} – {result.most_likely_score[1]}",
                "dari matriks Poisson",
            ),
            unsafe_allow_html=True,
        )
    with info:
        st.markdown(
            metric_card(
                "Rating serang",
                f"{number(model.ratings.attack_of(team_a), 2)} vs "
                f"{number(model.ratings.attack_of(team_b), 2)}",
                "kekuatan menyerang",
            ),
            unsafe_allow_html=True,
        )

    st.write("")
    section_header(
        "Matriks skor",
        "Distribusi gabungan",
        "Setiap sel adalah peluang skor akhir tersebut terjadi. Gol kedua tim "
        "dianggap independen.",
    )
    st.plotly_chart(
        charts.score_matrix_figure(
            result.matrix, team_a, team_b, max_goals=6
        ),
        config=PLOTLY_CONFIG,
        width="stretch",
    )

    with st.expander("Peluang lolos dua leg"):
        two_leg = two_leg_qualification(model.ratings, team_a, team_b)
        col_a, col_b, col_draw = st.columns(3)
        with col_a:
            st.markdown(
                metric_card(
                    f"{team_a} lolos",
                    pct(two_leg["a"] * 100.0),
                    "leg 1 di kandang A",
                ),
                unsafe_allow_html=True,
            )
        with col_b:
            st.markdown(
                metric_card(
                    f"{team_b} lolos",
                    pct(two_leg["b"] * 100.0),
                    "leg 2 di kandang B",
                ),
                unsafe_allow_html=True,
            )
        with col_draw:
            st.markdown(
                metric_card(
                    "Agregat imbang",
                    pct(two_leg["aggregate_draw"] * 100.0),
                    "dilanjutkan 50:50",
                ),
                unsafe_allow_html=True,
            )
        st.caption(
            f"Ekspektasi gol dua leg: {team_a} {number(two_leg['exp_goals_a'], 2)} · "
            f"{team_b} {number(two_leg['exp_goals_b'], 2)}. Jika agregat imbang, "
            "pemenang ditentukan 50:50 untuk mewakili perpanjangan waktu dan penalti."
        )

    note(
        "Matriks memakai asumsi independensi gol antartim dan kekuatan tim yang "
        "tetap. Hasil adalah peluang, bukan prediksi satu skor pasti."
    )
