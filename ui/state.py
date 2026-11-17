"""Shared Streamlit state, cached data loading, and cached model runs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from core.pipeline import (
    DataValidationError,
    ModelRun,
    Settings,
    load_matches,
    run_pipeline,
)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "matches.csv"


@st.cache_data(show_spinner=False)
def _load_bundled(path: str, modified_at: float) -> pd.DataFrame:
    return load_matches(path)


@st.cache_data(show_spinner="Menjalankan simulasi Monte Carlo…", max_entries=4)
def _run_cached(matches: pd.DataFrame, settings: Settings) -> ModelRun:
    return run_pipeline(matches, settings)


def init_state() -> None:
    state = st.session_state
    state.setdefault("page", "Dashboard")
    state.setdefault("settings", Settings())
    state.setdefault("dataset_label", "Dataset 2026/27 · 11 liga domestik + UCL")
    state.setdefault("upload_error", None)
    state.setdefault("upload_sig", None)
    state.setdefault("uploader_key", 0)

    if "matches" not in state:
        if not DATA_PATH.exists():
            state["matches"] = None
            state["dataset_error"] = (
                "Dataset bawaan belum tersedia. Jalankan "
                "`python build_dataset.py` lalu muat ulang halaman."
            )
            return
        try:
            state["matches"] = _load_bundled(
                str(DATA_PATH), DATA_PATH.stat().st_mtime
            )
            state["dataset_error"] = None
        except (DataValidationError, Exception) as exc:  # noqa: BLE001
            state["matches"] = None
            state["dataset_error"] = str(exc)


def get_matches() -> pd.DataFrame | None:
    return st.session_state.get("matches")


def set_matches(matches: pd.DataFrame, label: str) -> None:
    st.session_state["matches"] = matches
    st.session_state["dataset_label"] = label
    st.session_state["dataset_error"] = None
    st.session_state["upload_error"] = None


def use_bundled_dataset() -> None:
    if not DATA_PATH.exists():
        st.session_state["dataset_error"] = (
            "Dataset bawaan tidak ditemukan. Jalankan build_dataset.py."
        )
        return
    matches = _load_bundled(str(DATA_PATH), DATA_PATH.stat().st_mtime)
    set_matches(matches, "Dataset 2026/27 · 11 liga domestik + UCL")
    st.session_state["upload_sig"] = None
    st.session_state["uploader_key"] = int(st.session_state["uploader_key"]) + 1


def get_model() -> tuple[ModelRun | None, Exception | None]:
    matches = get_matches()
    if matches is None:
        message = st.session_state.get("dataset_error") or "Dataset belum dimuat."
        return None, DataValidationError([message])
    settings = st.session_state.get("settings", Settings())
    try:
        return _run_cached(matches, settings), None
    except Exception as exc:  # noqa: BLE001
        return None, exc
