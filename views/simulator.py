"""Simulator page: dataset upload plus all model settings."""

from __future__ import annotations

import hashlib
import io

import streamlit as st

from core.pipeline import (
    DataValidationError,
    ModelRun,
    Settings,
    dataset_summary,
    load_matches,
)
from ui.components import (
    chip_row,
    format_date_id,
    int_id,
    metric_card,
    metric_grid,
    note,
    number,
    section_header,
)
from ui.state import (
    DATA_PATH,
    get_matches,
    set_matches,
    use_bundled_dataset,
)


def _show_upload_error(error: object) -> None:
    if isinstance(error, DataValidationError):
        st.error("Dataset ditolak. Perbaiki hal berikut lalu unggah lagi.")
        for issue in error.issues:
            st.markdown(f"- {issue}")
    elif error:
        st.error(str(error))


def _handle_upload(uploaded) -> None:
    raw = uploaded.getvalue()
    signature = hashlib.sha1(raw).hexdigest()
    if st.session_state.get("upload_sig") == signature:
        return
    try:
        matches = load_matches(io.BytesIO(raw))
    except (DataValidationError, Exception) as exc:  # noqa: BLE001
        st.session_state["upload_error"] = exc
        return
    set_matches(matches, f"Unggahan · {uploaded.name}")
    st.session_state["upload_sig"] = signature
    st.session_state["upload_error"] = None
    st.rerun()


def _settings_form(settings: Settings) -> None:
    sim_options = [1_000, 2_500, 5_000, 10_000, 25_000, 50_000, 100_000]
    current_sims = (
        settings.n_sims if settings.n_sims in sim_options else 10_000
    )

    with st.form("simulator_settings"):
        left, right = st.columns(2)
        with left:
            n_sims = st.select_slider(
                "Jumlah simulasi",
                options=sim_options,
                value=current_sims,
                format_func=int_id,
                help="Lebih banyak simulasi membuat interval kepercayaan lebih sempit.",
            )
            half_life = st.slider(
                "Half-life form (hari)",
                min_value=90,
                max_value=1095,
                step=15,
                value=int(settings.half_life_days),
                help="Laga yang lebih tua diberi bobot eksponensial yang lebih kecil.",
            )
            domestic_weight = st.slider(
                "Bobot liga domestik",
                min_value=0.05,
                max_value=1.0,
                step=0.05,
                value=float(settings.domestic_weight),
                help="Laga UCL selalu berbobot 1,0 sebagai penghubung antarliga.",
            )
        with right:
            seed = st.number_input(
                "Seed acak",
                min_value=0,
                max_value=2_000_000_000,
                value=int(settings.seed),
                step=1,
                help="Seed yang sama dan parameter yang sama menghasilkan hasil identik.",
            )
            home_mode = st.radio(
                "Home advantage",
                options=("auto", "manual"),
                index=0 if settings.home_advantage_mode == "auto" else 1,
                format_func=lambda value: (
                    "Estimasi dari data" if value == "auto" else "Atur manual"
                ),
                horizontal=True,
            )
            manual_home = st.slider(
                "Nilai home advantage",
                min_value=0.80,
                max_value=1.60,
                step=0.01,
                value=float(settings.home_advantage),
                help=(
                    "Hanya dipakai jika mode manual dipilih. Mode estimasi "
                    "memakai nilai yang dihitung dari data."
                ),
            )

        with st.expander("Pengaturan lanjutan"):
            shrinkage = st.slider(
                "Shrinkage rating",
                min_value=0,
                max_value=20,
                step=1,
                value=int(settings.shrinkage),
                help=(
                    "Semakin besar, rating tim dengan sedikit laga makin ditarik "
                    "ke nilai rata-rata 1."
                ),
            )

        submitted = st.form_submit_button(
            "Terapkan & jalankan simulasi", type="primary"
        )

    if submitted:
        try:
            updated = Settings(
                n_sims=int(n_sims),
                seed=int(seed),
                half_life_days=float(half_life),
                domestic_weight=float(domestic_weight),
                shrinkage=float(shrinkage),
                home_advantage_mode=str(home_mode),
                home_advantage=float(manual_home),
            )
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.session_state["settings"] = updated
            st.rerun()


def render(model: ModelRun | None, error: Exception | None) -> None:
    section_header(
        "Simulator",
        "Kontrol model",
        "Unggah dataset dan atur parameter. Pengaturan yang diterapkan langsung "
        "dipakai oleh semua halaman.",
    )

    matches = get_matches()
    summary = dataset_summary(matches) if matches is not None else None

    if summary:
        metric_grid(
            [
                metric_card(
                    "Dataset aktif",
                    str(summary["matches"]),
                    st.session_state.get("dataset_label", "—"),
                ),
                metric_card(
                    "Laga dimainkan",
                    str(summary["played"]),
                    (
                        f"UCL {summary['ucl_played']} · domestik "
                        f"{summary['played'] - summary['ucl_played'] - summary['ucl_history']}"
                        f" · histori {summary['ucl_history']}"
                    ),
                ),
                metric_card(
                    "Jadwal UCL tersisa",
                    str(summary["ucl_remaining"]),
                    f"data per {format_date_id(summary['last_played'])}",
                ),
                metric_card(
                    "Tim UCL",
                    str(summary["teams"]),
                    f"{summary['competitions']} liga domestik",
                ),
            ]
        )

    _show_upload_error(st.session_state.get("upload_error"))
    if error is not None:
        st.error(f"Simulasi belum bisa dijalankan: {error}")

    st.write("")
    dataset_col, action_col = st.columns([2.2, 1.0], vertical_alignment="center")
    with dataset_col:
        uploaded = st.file_uploader(
            "Unggah dataset CSV",
            type=["csv"],
            key=f"uploader_{st.session_state.get('uploader_key', 0)}",
            help=(
                "Kolom wajib: date, home, away, home_goals, away_goals, "
                "competition. Kosongkan gol untuk laga yang belum dimainkan. "
                "Pakai competition = UCL untuk laga musim ini dan UCL 2025/26 "
                "untuk histori rating."
            ),
        )
        if uploaded is not None:
            _handle_upload(uploaded)
    with action_col:
        if DATA_PATH.exists():
            st.download_button(
                "Unduh dataset bawaan",
                data=DATA_PATH.read_bytes(),
                file_name="matches.csv",
                mime="text/csv",
                width="stretch",
            )
        if st.button("Pakai dataset bawaan", width="stretch"):
            use_bundled_dataset()
            st.rerun()

    with st.expander("Skema CSV dan aturan validasi"):
        st.markdown(
            """
| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `date` | tanggal | Tanggal pertandingan |
| `home` | teks | Tim kandang |
| `away` | teks | Tim tandang |
| `home_goals` | angka | Kosongkan jika belum dimainkan |
| `away_goals` | angka | Kosongkan jika belum dimainkan |
| `competition` | teks | `UCL` untuk laga UCL musim ini; `UCL 2025/26` untuk histori; selain itu nama liga |

Hanya baris `competition = UCL` yang dihitung sebagai league phase berjalan dan
menentukan aturan **36 tim**. Baris `UCL 2025/26` ikut menimbang rating tetapi
tidak masuk klasemen maupun simulasi 2026/27. Nama tim harus sama persis di
semua baris. Gol diisi keduanya atau dikosongkan keduanya.
            """
        )

    st.write("")
    _settings_form(st.session_state.get("settings", Settings()))

    if model is not None:
        st.write("")
        chip_row(
            [
                f"{int_id(model.n_sims)} simulasi",
                f"seed {model.settings.seed}",
                f"half-life {int(model.settings.half_life_days)} hari",
                f"bobot domestik {number(model.settings.domestic_weight, 2)}",
                f"shrinkage {model.settings.shrinkage:g}",
                f"home advantage ×{number(model.ratings.home_advantage, 3)}",
            ]
        )

        metric_grid(
            [
                metric_card(
                    "Waktu jalan",
                    f"{number(model.duration_seconds, 2)} s",
                    f"{int_id(model.n_sims)} simulasi",
                ),
                metric_card(
                    "Rata-rata gol dasar",
                    f"μ = {number(model.ratings.mu, 2)}",
                    "per tim per laga",
                ),
                metric_card(
                    "Home advantage",
                    f"×{number(model.ratings.home_advantage, 2)}",
                    "dipakai di simulasi",
                ),
                metric_card(
                    "Laga dipakai",
                    str(model.ratings.matches_used),
                    f"rating {len(model.ratings.teams)} tim",
                ),
            ]
        )

        with st.expander("Rating kekuatan tim"):
            ratings = model.ratings.to_frame().rename(
                columns={
                    "team": "Tim",
                    "attack": "Serang",
                    "defence": "Bertahan",
                    "matches": "Laga",
                }
            )
            ratings["Serang"] = ratings["Serang"].round(3)
            ratings["Bertahan"] = ratings["Bertahan"].round(3)
            st.dataframe(
                ratings,
                hide_index=True,
                width="stretch",
                height=360,
                column_config={
                    "Tim": st.column_config.TextColumn("Tim", width="medium"),
                    "Serang": st.column_config.NumberColumn("Serang", format="%.3f"),
                    "Bertahan": st.column_config.NumberColumn("Bertahan", format="%.3f"),
                    "Laga": st.column_config.NumberColumn("Laga", format="%d"),
                },
            )
            st.caption(
                "Nilai bertahan lebih besar berarti pertahanan lebih lemah. "
                "Rating di-shrink ke 1 agar tim dengan sedikit laga tidak ekstrem."
            )

    if model is not None and model.n_sims >= 50_000:
        note(
            f"Simulasi {int_id(model.n_sims)} memakan waktu lebih lama. "
            "Turunkan jumlah simulasi untuk eksplorasi cepat."
        )
