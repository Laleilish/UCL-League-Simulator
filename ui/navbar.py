"""Top navigation bar: brand plus a pill menu, without Streamlit's sidebar."""

from __future__ import annotations

import streamlit as st

PAGES = (
    "Dashboard",
    "Tabel",
    "Simulator",
    "Head-to-Head",
    "Statistik",
    "Metodologi",
)

DEFAULT_PAGE = "Dashboard"


def render_navbar() -> str:
    state = st.session_state
    if state.get("page") not in PAGES:
        state["page"] = DEFAULT_PAGE

    with st.container(key="navbar"):
        brand_col, menu_col = st.columns([1.25, 3.4], vertical_alignment="center")
        with brand_col:
            st.markdown(
                """
<div class="ucl-brand">
  <span class="ucl-mark" aria-hidden="true">
    <svg viewBox="0 0 44 44" focusable="false">
      <defs>
        <path id="skb-star" d="M0-2.7 0.68-0.93 2.57-0.84 1.09 0.36 1.59 2.18 0 1.15 -1.59 2.18 -1.09 0.36 -2.57-0.84 -0.68-0.93Z"/>
      </defs>
      <circle cx="22" cy="22" r="21" fill="#1A1400"/>
      <circle cx="22" cy="22" r="17.8" fill="none" stroke="#FFB800" stroke-opacity="0.28" stroke-width="0.9"/>
      <g fill="#FFB800">
        <use href="#skb-star" transform="translate(22 8.8)"/>
        <use href="#skb-star" transform="rotate(45 22 22) translate(22 8.8)"/>
        <use href="#skb-star" transform="rotate(90 22 22) translate(22 8.8)"/>
        <use href="#skb-star" transform="rotate(135 22 22) translate(22 8.8)"/>
        <use href="#skb-star" transform="rotate(180 22 22) translate(22 8.8)"/>
        <use href="#skb-star" transform="rotate(225 22 22) translate(22 8.8)"/>
        <use href="#skb-star" transform="rotate(270 22 22) translate(22 8.8)"/>
        <use href="#skb-star" transform="rotate(315 22 22) translate(22 8.8)"/>
      </g>
    </svg>
  </span>
  <span class="ucl-brand-text">
    <strong>SiKupingBesar</strong>
    <small>UCL League Simulator</small>
  </span>
</div>
                """,
                unsafe_allow_html=True,
            )
        with menu_col:
            choice = st.pills(
                "Navigasi",
                PAGES,
                default=state["page"],
                format_func=lambda page: "H2H" if page == "Head-to-Head" else page,
                label_visibility="collapsed",
                key="nav_pills",
            )
            if choice and choice != state["page"]:
                state["page"] = choice

    return state["page"]
