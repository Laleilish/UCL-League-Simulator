"""Statistics page: convergence, Poisson goodness-of-fit, and Brier score."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.pipeline import ModelRun
from core.stats import brier_score, convergence_curve, poisson_chi_square
from ui import charts
from ui.components import (
    int_id,
    metric_card,
    metric_grid,
    note,
    number,
    pct,
    section_header,
)
from ui.theme import INK, PLOTLY_CONFIG, YELLOW, style_fig


def _convergence_tab(model: ModelRun) -> None:
    teams = model.table["team"].tolist()
    team = st.selectbox("Tim fokus", teams, index=0, key="convergence_team")
    team_index = model.result.teams.index(team)
    curve = convergence_curve(model.result, team_index)
    last = curve.iloc[-1]
    width = last["batas_atas"] - last["batas_bawah"]

    st.plotly_chart(
        charts.convergence_figure(model.result, team_index, team),
        config=PLOTLY_CONFIG,
        width="stretch",
    )

    first = curve.iloc[0]
    metric_grid(
        [
            metric_card(
                "Peluang juara",
                pct(last["peluang"], 2),
                f"{team} · {int_id(model.n_sims)} simulasi",
            ),
            metric_card(
                "CI 95% akhir",
                f'{pct(last["batas_bawah"], 2)} – {pct(last["batas_atas"], 2)}',
                "metode Wilson",
            ),
            metric_card(
                "Lebar CI akhir",
                f"{pct(width, 2)}",
                "menyempit saat N bertambah",
            ),
            metric_card(
                "Lebar CI awal",
                f'{pct(first["batas_atas"] - first["batas_bawah"], 2)}',
                f'pada {int_id(first["simulasi"])} simulasi',
            ),
        ]
    )
    note(
        "Grafik ini adalah Law of Large Numbers dalam praktik: estimasi melompat "
        "di awal, lalu menstabilkan diri dan pita kepercayaan menyempit seiring "
        "jumlah simulasi bertambah."
    )


def _chi_square_tab(model: ModelRun) -> None:
    played = model.matches.dropna(subset=["home_goals", "away_goals"])
    goals = np.concatenate(
        [played["home_goals"].to_numpy(dtype=float), played["away_goals"].to_numpy(dtype=float)]
    )
    try:
        chi = poisson_chi_square(goals)
    except ValueError as exc:
        st.warning(str(exc))
        return

    metric_grid(
        [
            metric_card(
                "Statistik χ²",
                number(chi.statistic, 3),
                "semakin kecil semakin cocok",
            ),
            metric_card("Derajat bebas", str(chi.dof), "bin - 1 - parameter"),
            metric_card(
                "p-value",
                number(chi.p_value, 4) if chi.p_value >= 0.0001 else "< 0,0001",
                "α = 0,05",
            ),
            metric_card("Observasi", int_id(chi.n_observations), "gol per tim per laga"),
        ]
    )

    st.write("")
    with st.expander("Hipotesis dan cara membaca", expanded=True):
        st.markdown(
            f"""
**H₀:** jumlah gol satu tim dalam satu laga berdistribusi Poisson dengan
rata-rata μ = **{number(chi.mean_goals, 3)}**.

**H₁:** distribusi gol tidak mengikuti Poisson dengan rata-rata tersebut.

Uji dilakukan pada {int_id(chi.n_observations)} observasi gol per tim per laga.
"""
        )
        if chi.reject_null:
            st.warning(
                "H₀ ditolak pada α = 0,05. Ada bukti bahwa distribusi gol "
                "menyimpang dari Poisson; pertimbangkan Dixon-Coles sebagai "
                "pengembangan."
            )
        else:
            st.success(
                "H₀ gagal ditolak pada α = 0,05. Tidak ada bukti cukup bahwa "
                "distribusi gol menyimpang dari Poisson untuk dataset ini."
            )

    st.plotly_chart(
        charts.chi_square_figure(chi),
        config=PLOTLY_CONFIG,
        width="stretch",
    )
    st.caption(
        "Batang hitam adalah frekuensi observasi; batang kuning adalah frekuensi "
        "harapan dari distribusi Poisson dengan μ yang sama."
    )


def _brier_tab(model: ModelRun) -> None:
    result = brier_score(model.matches, model.ratings)
    difference = result.score - result.baseline

    metric_grid(
        [
            metric_card(
                "Brier score",
                number(result.score, 3),
                "1X2, in-sample",
            ),
            metric_card(
                "Baseline seragam",
                number(result.baseline, 3),
                "tanpa informasi",
            ),
            metric_card(
                "Selisih vs baseline",
                f"{'-' if difference < 0 else '+'}{number(abs(difference), 3)}",
                "negatif berarti lebih baik",
            ),
            metric_card(
                "Laga dievaluasi",
                int_id(result.n_matches),
                "laga dengan rating kedua tim",
            ),
        ]
    )

    fig = go.Figure(
        go.Bar(
            x=["Menang kandang", "Seri", "Menang tandang"],
            y=[result.home, result.draw, result.away],
            marker_color=[INK, YELLOW, "#C68A00"],
            text=[number(value, 3) for value in (result.home, result.draw, result.away)],
            textposition="outside",
            hovertemplate="%{x}<br>Kontribusi Brier: %{y:.4f}<extra></extra>",
        )
    )
    fig = style_fig(fig, height=360, y_grid=True)
    fig.update_layout(
        showlegend=False,
        margin=dict(l=22, r=24, t=30, b=46),
        xaxis=dict(ticklabelstandoff=6, automargin=True),
        yaxis=dict(title="Kontribusi Brier"),
    )
    st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")

    total = result.home + result.draw + result.away
    st.caption(
        f"Jumlah komponen: {number(total, 3)} (sama dengan Brier score). "
        "Semakin kecil, semakin baik kalibrasi peluang 1X2."
    )
    note(
        "Brier score ini dihitung pada data yang sama dengan estimasi rating "
        "(in-sample), sehingga cenderung terlalu optimistis. Backtest "
        "walk-forward adalah pengembangan lanjutan yang disarankan."
    )


def render(model: ModelRun) -> None:
    section_header(
        "Statistik",
        "Validasi model",
        "Tiga cara memeriksa simulasi: konvergensi Monte Carlo, kecocokan "
        "distribusi Poisson, dan kalibrasi peluang 1X2.",
    )

    tab_convergence, tab_chi, tab_brier = st.tabs(
        ["Konvergensi", "Uji Chi-square", "Brier score"]
    )
    with tab_convergence:
        _convergence_tab(model)
    with tab_chi:
        _chi_square_tab(model)
    with tab_brier:
        _brier_tab(model)
