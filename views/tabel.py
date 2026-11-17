"""Full probability table with search, sorting, and CSV export."""

from __future__ import annotations

import streamlit as st

from core.pipeline import ModelRun
from ui.components import int_id, note, pct, section_header


def _display_frame(model: ModelRun, query: str):
    table = model.table.copy()
    table.insert(0, "rank", range(1, len(table) + 1))
    appearances = dict(zip(model.ratings.teams, model.ratings.n_matches))
    table["laga"] = table["team"].map(appearances).fillna(0).astype(int)
    table["ci"] = table.apply(
        lambda row: f'{pct(row["ci_low"], 2)} – {pct(row["ci_high"], 2)}',
        axis=1,
    )
    view = table[
        [
            "rank",
            "team",
            "laga",
            "champion",
            "ci",
            "final",
            "semi",
            "quarter",
            "r16",
            "top8",
            "top24",
            "avg_points",
            "avg_position",
        ]
    ].rename(
        columns={
            "rank": "Peringkat",
            "team": "Tim",
            "laga": "Laga",
            "champion": "Juara",
            "ci": "CI 95%",
            "final": "Final",
            "semi": "Semifinal",
            "quarter": "Perempat",
            "r16": "16 Besar",
            "top8": "Top 8",
            "top24": "Top 24",
            "avg_points": "Poin",
            "avg_position": "Posisi",
        }
    )
    if query:
        view = view[view["Tim"].str.contains(query, case=False, na=False)]
    return view


def _csv_bytes(model: ModelRun) -> bytes:
    table = model.table.copy()
    appearances = dict(zip(model.ratings.teams, model.ratings.n_matches))
    table["laga"] = table["team"].map(appearances).fillna(0).astype(int)
    table = table.rename(
        columns={
            "team": "team",
            "laga": "matches_played",
            "champion": "champion_pct",
            "ci_low": "ci_low_pct",
            "ci_high": "ci_high_pct",
            "final": "final_pct",
            "semi": "semi_pct",
            "quarter": "quarter_pct",
            "r16": "r16_pct",
            "top8": "top8_pct",
            "top24": "top24_pct",
            "avg_points": "avg_points",
            "avg_position": "avg_position",
        }
    )
    numeric = [column for column in table.columns if column != "team"]
    table[numeric] = table[numeric].round(4)
    return table.to_csv(index=False).encode("utf-8-sig")


def render(model: ModelRun) -> None:
    section_header(
        "Tabel probabilitas",
        "36 tim",
        "Peluang setiap tim menembus tiap babak sampai juara. Kolom bisa "
        "diurutkan dengan mengklik judulnya.",
    )

    left, right = st.columns([2.2, 1.0], vertical_alignment="bottom")
    with left:
        query = st.text_input(
            "Cari tim",
            placeholder="Ketik nama tim, misalnya Madrid…",
            label_visibility="collapsed",
        )
    with right:
        st.download_button(
            "Unduh CSV lengkap",
            data=_csv_bytes(model),
            file_name=f"sikupingbesar_probabilitas_{model.n_sims}sim.csv",
            mime="text/csv",
            type="primary",
            width="stretch",
        )

    view = _display_frame(model, query)
    st.caption(
        f"{len(view)} tim ditampilkan · {int_id(model.n_sims)} simulasi · "
        f"seed {model.settings.seed}"
    )

    st.dataframe(
        view,
        hide_index=True,
        width="stretch",
        height=680,
        column_config={
            "Peringkat": st.column_config.NumberColumn("Peringkat", width="small"),
            "Tim": st.column_config.TextColumn("Tim", width="medium"),
            "Laga": st.column_config.NumberColumn(
                "Laga",
                width="small",
                help="Jumlah laga domestik + histori UCL yang dipakai untuk rating",
            ),
            "Juara": st.column_config.NumberColumn("Juara", format="%.2f%%"),
            "CI 95%": st.column_config.TextColumn("CI 95%", width="medium"),
            "Final": st.column_config.NumberColumn("Final", format="%.2f%%"),
            "Semifinal": st.column_config.NumberColumn("Semifinal", format="%.2f%%"),
            "Perempat": st.column_config.NumberColumn("Perempat", format="%.2f%%"),
            "16 Besar": st.column_config.NumberColumn("16 Besar", format="%.2f%%"),
            "Top 8": st.column_config.NumberColumn("Top 8", format="%.2f%%"),
            "Top 24": st.column_config.NumberColumn("Top 24", format="%.2f%%"),
            "Poin": st.column_config.NumberColumn("Poin", format="%.2f"),
            "Posisi": st.column_config.NumberColumn("Posisi", format="%.2f"),
        },
    )

    note(
        "Interval kepercayaan 95% dihitung dengan metode Wilson untuk peluang "
        "juara. Jumlah peluang juara seluruh tim selalu 100%; jumlah peluang "
        "Top 8 selalu 8 tim dan Top 24 selalu 24 tim."
    )

    appearances = dict(zip(model.ratings.teams, model.ratings.n_matches))
    without_matches = sorted(team for team, n in appearances.items() if n == 0)
    if without_matches:
        note(
            f"{len(without_matches)} tim tanpa satu pun laga "
            f"({', '.join(without_matches)}). Peluang mereka berasal dari nilai "
            "awal rating 1,0 dan jauh lebih tidak pasti daripada tim lain."
        )
