"""Plotly chart builders (kept out of views so pages stay readable)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from core.simulate import STAGE_LABELS, SimulationResult, STAGES
from core.stats import ChiSquareResult, convergence_curve, stage_matrix
from ui.components import pct
from ui.theme import INK, MUTED, YELLOW, style_fig


def champion_bar_figure(table: pd.DataFrame, top_n: int = 12) -> go.Figure:
    data = table.head(top_n).iloc[::-1]
    colors = []
    for index in range(len(data)):
        rank = len(data) - index
        colors.append(INK if rank == 1 else (YELLOW if rank <= 3 else "#E9DFC4"))

    fig = go.Figure(
        go.Bar(
            x=data["champion"],
            y=data["team"],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            cliponaxis=False,
            error_x=dict(
                type="data",
                symmetric=False,
                array=(data["ci_high"] - data["champion"]).tolist(),
                arrayminus=(data["champion"] - data["ci_low"]).tolist(),
                color=MUTED,
                thickness=1.1,
                width=4,
            ),
            customdata=np.column_stack(
                [data["ci_low"], data["ci_high"], data["final"]]
            ),
            hovertemplate=(
                "<b>%{y}</b><br>Peluang juara: %{x:.2f}%"
                "<br>CI 95%: %{customdata[0]:.2f}% – %{customdata[1]:.2f}%"
                "<br>Peluang final: %{customdata[2]:.2f}%<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data["ci_high"] + float(data["ci_high"].max()) * 0.012,
            y=data["team"],
            mode="text",
            text=[pct(value) for value in data["champion"]],
            textposition="middle right",
            textfont=dict(size=11, color=INK),
            showlegend=False,
            hoverinfo="skip",
            cliponaxis=False,
        )
    )
    fig = style_fig(fig, height=max(410, top_n * 31 + 108), x_grid=True)
    fig.update_layout(
        showlegend=False,
        bargap=0.3,
        margin=dict(l=24, r=52, t=22, b=46),
        xaxis=dict(
            ticksuffix="%",
            range=[0, float(data["ci_high"].max()) * 1.3],
            ticklabelstandoff=6,
            automargin=True,
        ),
    )
    fig.update_yaxes(showgrid=False, automargin=True)
    return fig


def stage_heatmap_figure(
    result: SimulationResult, table: pd.DataFrame, top_n: int = 14
) -> go.Figure:
    data = table.head(top_n)
    order = [result.teams.index(team) for team in data["team"]]
    matrix = stage_matrix(result)[order]
    text = [[pct(value) for value in row] for row in matrix]

    fig = go.Figure(
        go.Heatmap(
            z=matrix,
            x=[STAGE_LABELS[stage] for stage in STAGES],
            y=data["team"].tolist(),
            text=text,
            texttemplate="%{text}",
            textfont=dict(size=10, color=INK),
            colorscale=[
                [0.0, "#FFFDF6"],
                [0.25, "#FFEFC2"],
                [0.55, "#FFD766"],
                [0.8, "#FFC21F"],
                [1.0, "#EDA700"],
            ],
            zmin=0,
            zmax=100,
            xgap=3,
            ygap=3,
            colorbar=dict(
                title=dict(text="%", font=dict(size=11, color=MUTED)),
                thickness=10,
                len=0.7,
                ticksuffix="%",
                tickfont=dict(size=10, color=MUTED),
                outlinewidth=0,
            ),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f}%<extra></extra>",
        )
    )
    fig = style_fig(fig, height=max(455, top_n * 30 + 150))
    fig.update_layout(margin=dict(l=22, r=22, t=30, b=26))
    fig.update_xaxes(side="top", showgrid=False, ticks="")
    fig.update_yaxes(autorange="reversed", showgrid=False, automargin=True, ticks="")
    return fig


def convergence_figure(
    result: SimulationResult, team_index: int, team: str
) -> go.Figure:
    curve = convergence_curve(result, team_index)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curve["simulasi"],
            y=curve["batas_atas"],
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=curve["simulasi"],
            y=curve["batas_bawah"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(255,184,0,0.22)",
            name="Interval kepercayaan 95%",
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=curve["simulasi"],
            y=curve["peluang"],
            mode="lines+markers",
            line=dict(color=INK, width=2.4),
            marker=dict(size=7, color=YELLOW, line=dict(color=INK, width=1.2)),
            name=f"Peluang {team}",
            hovertemplate=(
                "%{x:,.0f} simulasi<br>Peluang: %{y:.2f}%<extra></extra>"
            ),
        )
    )
    fig = style_fig(fig, height=420, y_grid=True)
    tick_values = curve["simulasi"].tolist()
    fig.update_layout(
        margin=dict(l=22, r=26, t=24, b=52),
        xaxis=dict(
            type="log",
            tickmode="array",
            tickvals=tick_values,
            ticktext=[f"{int(value):,}".replace(",", ".") for value in tick_values],
            title="Jumlah simulasi",
            ticksuffix="",
            ticklabelstandoff=6,
            automargin=True,
        ),
        yaxis=dict(ticksuffix="%", rangemode="tozero", title="Peluang juara"),
        hovermode="x unified",
    )
    return fig


def chi_square_figure(chi: ChiSquareResult) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=chi.labels,
            y=chi.observed,
            name="Observasi",
            marker_color=INK,
            hovertemplate="Gol %{x}<br>Observasi: %{y:.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=chi.labels,
            y=chi.expected,
            name="Harapan Poisson",
            marker_color=YELLOW,
            hovertemplate="Gol %{x}<br>Harapan: %{y:.1f}<extra></extra>",
        )
    )
    fig = style_fig(fig, height=360, y_grid=True)
    fig.update_layout(
        barmode="group",
        bargap=0.28,
        margin=dict(l=22, r=24, t=24, b=52),
        xaxis=dict(title="Gol per tim per laga", ticklabelstandoff=6, automargin=True),
        yaxis=dict(title="Frekuensi"),
    )
    return fig


def score_matrix_figure(
    matrix: np.ndarray,
    team_a: str,
    team_b: str,
    max_goals: int = 6,
) -> go.Figure:
    subset = matrix[: max_goals + 1, : max_goals + 1] * 100.0
    labels = [str(value) for value in range(max_goals + 1)]
    text = [[pct(value) for value in row] for row in subset]
    fig = go.Figure(
        go.Heatmap(
            z=subset,
            x=labels,
            y=labels,
            text=text,
            texttemplate="%{text}",
            textfont=dict(size=10, color=INK),
            colorscale=[
                [0.0, "#FFFDF6"],
                [0.3, "#FFEFC2"],
                [0.7, "#FFC21F"],
                [1.0, "#EDA700"],
            ],
            xgap=2,
            ygap=2,
            colorbar=dict(
                title=dict(text="%", font=dict(size=11, color=MUTED)),
                thickness=10,
                ticksuffix="%",
                tickfont=dict(size=10, color=MUTED),
                outlinewidth=0,
            ),
            hovertemplate=(
                f"{team_a} %{{y}} - %{{x}} {team_b}"
                "<br>Peluang: %{z:.2f}%<extra></extra>"
            ),
        )
    )
    fig = style_fig(fig, height=405)
    fig.update_layout(margin=dict(l=22, r=22, t=28, b=52))
    fig.update_xaxes(
        title=f"Gol {team_b}",
        side="bottom",
        showgrid=False,
        ticks="",
        ticklabelstandoff=6,
        automargin=True,
    )
    fig.update_yaxes(
        title=f"Gol {team_a}", autorange="reversed", showgrid=False, ticks=""
    )
    return fig
