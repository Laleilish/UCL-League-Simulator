"""SiKupingBesar entry point: theme, navbar, and page routing."""

from __future__ import annotations

import streamlit as st

from core.pipeline import DataValidationError
from ui.navbar import render_navbar
from ui.state import get_model, init_state
from ui.theme import configure_page, inject_css
from views import dashboard, head_to_head, metodologi, simulator, statistik, tabel


def _render_error(error: Exception | None) -> None:
    st.error("Halaman belum bisa ditampilkan karena dataset atau model bermasalah.")
    if isinstance(error, DataValidationError):
        for issue in error.issues:
            st.markdown(f"- {issue}")
    elif error is not None:
        st.write(str(error))
    with st.expander("Detail teknis"):
        if error is not None:
            st.exception(error)
    st.info(
        "Buka halaman Simulator untuk memuat dataset yang valid atau memakai "
        "kembali dataset bawaan."
    )


def _footer() -> None:
    st.markdown(
        '<div class="ucl-note" style="margin-top:2.4rem">'
        "SiKupingBesar · proyek Probabilitas dan Statistika · "
        "data domestik 2026/27 + histori UCL 2025/26 · "
        "angka adalah peluang, bukan jaminan."
        "</div>",
        unsafe_allow_html=True,
    )


def main() -> None:
    configure_page()
    inject_css()
    init_state()
    page = render_navbar()

    with st.container(key="page"):
        model, error = get_model()

        if page == "Simulator":
            simulator.render(model, error)
        elif model is None:
            _render_error(error)
        elif page == "Dashboard":
            dashboard.render(model)
        elif page == "Tabel":
            tabel.render(model)
        elif page == "Head-to-Head":
            head_to_head.render(model)
        elif page == "Statistik":
            statistik.render(model)
        elif page == "Metodologi":
            metodologi.render()
        else:
            dashboard.render(model)

        _footer()


if __name__ == "__main__":
    main()
