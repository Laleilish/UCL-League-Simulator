"""Visual theme for SiKupingBesar: UCL-inspired yellow, cream, and dark brown."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

YELLOW = "#FFB800"
YELLOW_DEEP = "#E09E00"
INK = "#1A1400"
CREAM = "#F6F2E7"
CARD = "#FFFFFF"
LINE = "#E7DFC9"
MUTED = "#6F6450"
GREEN = "#0E7B4F"

COLORWAY = [YELLOW, INK, "#C68A00", "#8C7A50", "#F3D37A", "#5E5136"]

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
    "responsive": True,
}


def configure_page() -> None:
    st.set_page_config(
        page_title="SiKupingBesar · UCL League Simulator",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def inject_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --ucl-yellow: #FFB800;
  --ucl-yellow-deep: #E09E00;
  --ucl-yellow-soft: #FFE9AD;
  --ink: #1A1400;
  --muted: #6F6450;
  --cream: #F6F2E7;
  --card: #FFFFFF;
  --line: #E7DFC9;
  --green: #0E7B4F;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"] {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

.stApp {
  background-color: var(--cream);
  background-image:
    radial-gradient(circle at 6% -4%, rgba(255,184,0,0.20), transparent 32%),
    radial-gradient(circle at 102% 8%, rgba(255,184,0,0.10), transparent 26%);
  background-attachment: fixed;
  color: var(--ink);
}

[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], footer { display: none !important; }
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none !important; }

.block-container {
  max-width: 100% !important;
  padding: 0 !important;
}

.st-key-navbar {
  width: 100%;
  background: linear-gradient(100deg, #FFC21F 0%, #FFB800 55%, #F2A900 100%);
  border-radius: 0 0 24px 24px;
  padding: 0.65rem clamp(1rem, 4vw, 3.2rem);
  box-shadow: 0 12px 30px rgba(26, 20, 0, 0.10);
  position: sticky;
  top: 0;
  z-index: 999;
}

.st-key-navbar [data-testid="stHorizontalBlock"] { align-items: center; }

.st-key-page {
  max-width: 1320px;
  margin: 0 auto;
  padding: 1.6rem clamp(1rem, 3.2vw, 2.4rem) 4rem;
}

@media (max-width: 640px) {
  .st-key-navbar { border-radius: 0 0 18px 18px; }
  .st-key-page { padding-top: 1rem; }
}

.ucl-brand { display: flex; align-items: center; gap: 0.65rem; min-width: 0; }
.ucl-mark {
  display: inline-flex; flex: 0 0 42px;
  width: 42px; height: 42px; border-radius: 50%;
  filter: drop-shadow(0 2px 5px rgba(26,20,0,0.18));
}
.ucl-mark svg { width: 100%; height: 100%; display: block; }
.ucl-brand-text { display: flex; flex-direction: column; line-height: 1.05; }
.ucl-brand-text strong {
  font-size: 1.04rem; font-weight: 800; letter-spacing: -0.025em; color: var(--ink);
  white-space: nowrap;
}
.ucl-brand-text small {
  font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: rgba(26,20,0,0.58); margin-top: 3px;
  white-space: nowrap;
}

@media (max-width: 720px) {
  .ucl-mark { flex-basis: 38px; width: 38px; height: 38px; }
  .ucl-brand-text small { display: none; }
}

.st-key-navbar [data-testid="stButtonGroup"] {
  overflow-x: auto; scrollbar-width: none; padding-bottom: 2px;
}
.st-key-navbar [data-testid="stButtonGroup"]::-webkit-scrollbar { display: none; }
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"] {
  flex-wrap: nowrap;
}
.st-key-navbar [data-testid="stButtonGroup"] button {
  border-radius: 999px !important;
  border: 1px solid rgba(26,20,0,0.16) !important;
  background: rgba(255,255,255,0.42) !important;
  color: var(--ink) !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
  padding: 0.3rem 0.72rem !important;
  white-space: nowrap;
  min-height: 0 !important;
}
.st-key-navbar [data-testid="stButtonGroup"] button:hover {
  background: rgba(255,255,255,0.70) !important;
  border-color: rgba(26,20,0,0.28) !important;
}
.st-key-navbar [data-testid="stButtonGroup"] button[aria-checked="true"] {
  background: var(--ink) !important;
  color: var(--ucl-yellow) !important;
  border-color: var(--ink) !important;
}

h1, h2, h3, h4 { color: var(--ink) !important; letter-spacing: -0.025em; }
p, li, label, span { color: inherit; }
a { color: #8A5B00; }

.ucl-eyebrow {
  display: inline-flex; align-items: center; gap: 0.45rem;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--muted);
}
.ucl-eyebrow::before {
  content: ""; width: 20px; height: 3px; border-radius: 2px; background: var(--ucl-yellow);
}
.ucl-section { margin: 2.2rem 0 1rem; }
.ucl-section h2 { font-size: 1.45rem; font-weight: 800; margin: 0.25rem 0 0.2rem; }
.ucl-section p { color: var(--muted); margin: 0; font-size: 0.92rem; max-width: 760px; }
.ucl-section-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }

.ucl-kpi-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.85rem; margin: 0.2rem 0 0.4rem; }
@media (max-width: 1000px) { .ucl-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 520px) { .ucl-kpi-grid { grid-template-columns: 1fr; } }

.ucl-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 18px;
  padding: 1.15rem 1.2rem; box-shadow: 0 12px 28px rgba(26,20,0,0.045);
  height: 100%;
}
.ucl-kpi { display: flex; flex-direction: column; gap: 0.2rem; }
.ucl-kpi .label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.ucl-kpi .value { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; }
.ucl-kpi .sub { font-size: 0.78rem; color: var(--muted); }

.ucl-favorites { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
@media (max-width: 980px) { .ucl-favorites { grid-template-columns: 1fr; } }

.ucl-fav {
  background: var(--card); border: 1px solid var(--line); border-radius: 22px;
  padding: 1.25rem 1.3rem; box-shadow: 0 14px 34px rgba(26,20,0,0.055);
  position: relative; overflow: hidden;
}
.ucl-fav::after {
  content: ""; position: absolute; right: -30px; top: -30px; width: 120px; height: 120px;
  border-radius: 50%; background: rgba(255,184,0,0.12);
}
.ucl-fav.is-leader { background: var(--ink); border-color: var(--ink); color: #FFF8E6; }
.ucl-fav.is-leader::after { background: rgba(255,184,0,0.18); }
.ucl-fav-top { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; }
.ucl-rank {
  font-size: 0.68rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--muted);
}
.is-leader .ucl-rank { color: var(--ucl-yellow); }
.ucl-fav-tag { font-size: 0.66rem; font-weight: 700; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; }
.is-leader .ucl-fav-tag { color: rgba(255,248,230,0.65); }
.ucl-team { display: flex; align-items: center; gap: 0.7rem; margin: 0.8rem 0 0.7rem; }
.ucl-badge {
  display: inline-flex; align-items: center; justify-content: center; flex: 0 0 auto;
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--ucl-yellow); color: var(--ink);
  font-weight: 800; font-size: 0.78rem; letter-spacing: 0.02em;
  overflow: hidden;
}
.ucl-badge.has-logo {
  background: #FFFFFF;
  border: 1px solid rgba(26,20,0,0.10);
  padding: 5px;
  box-shadow: 0 2px 6px rgba(26,20,0,0.08);
}
.ucl-badge img {
  width: 100%; height: 100%; object-fit: contain; display: block;
}
.is-leader .ucl-badge { box-shadow: 0 0 0 3px rgba(255,184,0,0.22); }
.is-leader .ucl-badge.has-logo {
  background: #FFFFFF;
  border-color: rgba(255,184,0,0.45);
  box-shadow: 0 0 0 3px rgba(255,184,0,0.32);
}

.ucl-matchup {
  display: flex; align-items: center; justify-content: space-between; gap: 1rem;
  background: var(--card); border: 1px solid var(--line); border-radius: 20px;
  padding: 1rem 1.4rem; margin: 0.4rem 0 1rem;
  box-shadow: 0 12px 28px rgba(26,20,0,0.045);
}
.ucl-matchup-side {
  display: flex; align-items: center; gap: 0.75rem; flex: 1 1 0; min-width: 0;
}
.ucl-matchup-side.right { justify-content: flex-end; text-align: right; }
.ucl-matchup-side .ucl-badge { width: 52px; height: 52px; }
.ucl-matchup-name { font-weight: 800; font-size: 1.05rem; line-height: 1.2; color: var(--ink); }
.ucl-matchup-role { font-size: 0.72rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
.ucl-matchup-vs {
  display: flex; flex-direction: column; align-items: center; gap: 0.2rem; flex: 0 0 auto;
}
.ucl-matchup-vs strong {
  font-size: 0.85rem; font-weight: 800; letter-spacing: 0.12em;
  background: var(--ink); color: var(--ucl-yellow);
  padding: 0.25rem 0.7rem; border-radius: 999px;
}
.ucl-matchup-vs span { font-size: 0.72rem; color: var(--muted); font-weight: 600; }
@media (max-width: 640px) {
  .ucl-matchup { flex-direction: column; text-align: center; padding: 1rem; }
  .ucl-matchup-side, .ucl-matchup-side.right { justify-content: center; text-align: center; }
}
.ucl-team-name { font-weight: 700; font-size: 1rem; line-height: 1.2; }
.ucl-team-sub { font-size: 0.72rem; color: var(--muted); margin-top: 2px; }
.is-leader .ucl-team-sub { color: rgba(255,248,230,0.62); }
.ucl-fav-value { font-size: 2.35rem; font-weight: 800; letter-spacing: -0.045em; line-height: 1; }
.ucl-fav-ci { font-size: 0.76rem; color: var(--muted); margin-top: 0.4rem; }
.is-leader .ucl-fav-ci { color: rgba(255,248,230,0.70); }
.ucl-fav-split {
  display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;
  border-top: 1px solid var(--line); margin-top: 0.9rem; padding-top: 0.75rem;
}
.is-leader .ucl-fav-split { border-top-color: rgba(255,248,230,0.16); }
.ucl-fav-split div { display: flex; flex-direction: column; gap: 2px; }
.ucl-fav-split span { font-size: 0.67rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
.is-leader .ucl-fav-split span { color: rgba(255,248,230,0.6); }
.ucl-fav-split strong { font-size: 0.95rem; }

.ucl-pill-row { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.8rem; }
.ucl-chip {
  display: inline-flex; align-items: center; gap: 0.35rem;
  border-radius: 999px; padding: 0.3rem 0.7rem;
  background: rgba(255,184,0,0.14); border: 1px solid rgba(224,158,0,0.30);
  font-size: 0.74rem; font-weight: 600; color: #7A5200;
}
.ucl-chip.dark { background: var(--ink); border-color: var(--ink); color: var(--ucl-yellow); }

.ucl-note {
  border-left: 4px solid var(--ucl-yellow); background: rgba(255,255,255,0.7);
  border-radius: 0 12px 12px 0; padding: 0.8rem 1rem; color: var(--muted);
  font-size: 0.82rem; line-height: 1.55;
}

[data-testid="stPlotlyChart"] {
  background: var(--card); border: 1px solid var(--line); border-radius: 18px;
  padding: 0.55rem 0.55rem 0.15rem; box-shadow: 0 12px 28px rgba(26,20,0,0.045);
}
[data-testid="stDataFrame"] {
  border: 1px solid var(--line); border-radius: 16px; overflow: hidden;
  box-shadow: 0 12px 28px rgba(26,20,0,0.04);
}

.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius: 999px !important; font-weight: 700 !important;
  border: 1px solid rgba(26,20,0,0.18) !important;
  padding: 0.45rem 1.1rem !important;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
  transform: translateY(-1px); box-shadow: 0 8px 18px rgba(26,20,0,0.10);
}
[data-testid="stFormSubmitButton"] > button[kind="primary"],
.stButton > button[kind="primary"] {
  background: var(--ink) !important; color: var(--ucl-yellow) !important; border-color: var(--ink) !important;
}

[data-testid="stForm"] {
  background: var(--card); border: 1px solid var(--line); border-radius: 20px;
  padding: 1.2rem 1.3rem 0.6rem; box-shadow: 0 12px 28px rgba(26,20,0,0.045);
}

[data-testid="stTabs"] [data-baseweb="tab-list"] { gap: 0.4rem; }
[data-testid="stTabs"] button[role="tab"] {
  border-radius: 999px; padding: 0.35rem 0.9rem; font-weight: 600; color: var(--muted);
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  background: var(--ink); color: var(--ucl-yellow);
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"], [data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

[data-testid="stExpander"] {
  border: 1px solid var(--line) !important; border-radius: 14px !important; background: rgba(255,255,255,0.55);
}

[data-testid="stAlert"] { border-radius: 14px; }

.stSlider [data-baseweb="slider"] div[role="slider"] { background: var(--ink); }
.stSelectbox [data-baseweb="select"] > div, .stNumberInput input, .stTextInput input {
  border-radius: 12px !important;
}

.ucl-formula-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 18px;
  padding: 1rem 1.2rem; box-shadow: 0 12px 28px rgba(26,20,0,0.045);
}

.ucl-mono {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.82rem;
}

/* =========================================================
   NATURAL PRE-MATCH VERSUS ARENA & PITCH
   ========================================================= */
.ps2-versus-wrapper {
  background: #141A24;
  border: 1px solid #283344;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
  margin: 1.2rem 0 1.6rem;
  color: #FFFFFF;
  position: relative;
}

.ps2-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.65rem 1.25rem;
  background: #10151E;
  border-bottom: 1px solid #232B3A;
  font-size: 0.75rem;
  letter-spacing: 0.06em;
}

.ps2-status-led {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  color: #94A3B8;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.72rem;
}

.ps2-led-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22C55E;
}

.ps2-competition-title {
  font-weight: 800;
  color: #F59E0B;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.ps2-venue-pill {
  background: #1A2230;
  border: 1px solid #334155;
  border-radius: 6px;
  padding: 0.2rem 0.65rem;
  font-weight: 600;
  color: #CBD5E1;
  font-size: 0.72rem;
}

/* PITCH CONTAINER */
.ps2-pitch-container {
  position: relative;
  width: 100%;
  min-height: 380px;
  background-color: #276937;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.ps2-svg-turf {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  width: 100%; height: 100%;
  pointer-events: none;
}

.ps2-pitch-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(ellipse at 50% 50%, transparent 65%, rgba(0,0,0,0.2) 100%);
  pointer-events: none;
}

/* TACTICAL FORMATION DOTS (NATURAL) */
.ps2-tactic-dot {
  position: absolute;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.42);
  border: 1px solid rgba(0, 0, 0, 0.2);
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 2;
}

/* PITCH CONTENT ROW */
.ps2-pitch-content {
  position: relative;
  z-index: 5;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.4rem 1.8rem;
  gap: 1rem;
}

.ps2-team-zone {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1 1 0;
  min-width: 0;
}

.ps2-zone-left {
  justify-content: flex-start;
}

.ps2-zone-right {
  justify-content: flex-end;
}

/* SOLID TEAM CARDS */
.ps2-card-float {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  background: rgba(16, 22, 33, 0.94);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 0.85rem 1.1rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
  max-width: 370px;
}

.ps2-float-right {
  border-color: #334155;
}

.ps2-crest {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  flex-shrink: 0;
  border: 2px solid #CBD5E1;
  box-shadow: 0 2px 6px rgba(0,0,0,0.18);
}

.ps2-crest-a {
  border-color: #3B82F6;
}

.ps2-crest-b {
  border-color: #EF4444;
}

.ps2-crest img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.ps2-crest-fallback {
  background: #1E293B;
  color: #F8FAFC;
  font-weight: 800;
  font-size: 1.3rem;
}

.ps2-team-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}

.ps2-text-right {
  text-align: right;
  align-items: flex-end;
}

.ps2-role-tag {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #60A5FA;
}

.ps2-float-right .ps2-role-tag {
  color: #F87171;
}

.ps2-team-name {
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: #FFFFFF;
  line-height: 1.15;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ps2-mini-stats {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.25rem;
  flex-wrap: wrap;
}

.ps2-stats-right {
  justify-content: flex-end;
}

.ps2-stat-chip {
  background: #1E293B;
  border: 1px solid #334155;
  border-radius: 5px;
  padding: 0.15rem 0.45rem;
  font-size: 0.68rem;
  font-weight: 700;
  color: #CBD5E1;
}

.ps2-chip-odds {
  background: #1E3A8A;
  border-color: #2563EB;
  color: #DBEAFE;
}

.ps2-chip-odds-b {
  background: #7F1D1D;
  border-color: #DC2626;
  color: #FEE2E2;
}

/* NATURAL TACTICAL ARROWS */
.ps2-tactical-arrow {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 1.3rem;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.35);
  user-select: none;
}

.ps2-arrow-left {
  color: rgba(255, 255, 255, 0.35);
}

/* CENTER CLASH (VS & PREDIKSI SKOR) */
.ps2-center-clash {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.45rem;
  flex-shrink: 0;
  z-index: 6;
}

.ps2-vs-badge {
  width: 66px;
  height: 66px;
  border-radius: 50%;
  background: #1E293B;
  border: 2px solid #D97706;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
}

.ps2-vs-text {
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: 0.05em;
  color: #F59E0B;
}

.ps2-score-prediction {
  background: rgba(17, 24, 39, 0.95);
  border: 1px solid #374151;
  border-radius: 10px;
  padding: 0.35rem 0.85rem;
  text-align: center;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.22);
}

.ps2-pred-label {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #94A3B8;
  text-transform: uppercase;
}

.ps2-pred-score {
  font-size: 1.15rem;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: 0.05em;
  line-height: 1.1;
  margin-top: 2px;
}

.ps2-pred-sub {
  font-size: 0.72rem;
  font-weight: 600;
  color: #CBD5E1;
}

.ps2-alt-scores {
  font-size: 0.62rem;
  font-weight: 600;
  color: #94A3B8;
  margin-top: 3px;
  white-space: nowrap;
}

.ps2-win-bar-container {
  display: flex;
  width: 140px;
  height: 7px;
  background: #334155;
  border-radius: 4px;
  overflow: hidden;
}

.ps2-bar-seg.a { background: #3B82F6; }
.ps2-bar-seg.draw { background: #64748B; }
.ps2-bar-seg.b { background: #EF4444; }

/* ATTRIBUTES COMPARISON PANEL (NATURAL BROADCAST STYLE) */
.ps2-attributes-panel {
  padding: 1rem 1.4rem 0.8rem;
  background: #10151E;
  border-top: 1px solid #232B3A;
}

.ps2-panel-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  margin-bottom: 0.85rem;
}

.ps2-header-bracket {
  color: #D97706;
  font-weight: 800;
  font-size: 0.85rem;
}

.ps2-header-title {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #94A3B8;
}

.ps2-attribute-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 820px;
  margin: 0 auto;
}

.ps2-attr-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.ps2-attr-val {
  width: 55px;
  font-size: 0.82rem;
  font-weight: 700;
  color: #E2E8F0;
}

.ps2-attr-val.left {
  text-align: right;
  color: #93C5FD;
}

.ps2-attr-val.right {
  text-align: left;
  color: #FCA5A5;
}

.ps2-attr-val.highlight-a {
  color: #60A5FA;
  font-size: 0.88rem;
  font-weight: 800;
}

.ps2-attr-val.highlight-b {
  color: #F87171;
  font-size: 0.88rem;
  font-weight: 800;
}

.ps2-attr-bar-wrap {
  display: flex;
  align-items: center;
  flex: 1 1 0;
  gap: 0.6rem;
}

.ps2-attr-label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #94A3B8;
  white-space: nowrap;
  text-align: center;
  flex: 0 0 200px;
}

.ps2-meter {
  flex: 1 1 0;
  height: 7px;
  background: #1E293B;
  border-radius: 4px;
  overflow: hidden;
  display: flex;
}

.ps2-meter.left {
  justify-content: flex-end;
}

.ps2-meter.right {
  justify-content: flex-start;
}

.ps2-meter-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.ps2-meter-fill.a {
  background: #3B82F6;
}

.ps2-meter-fill.b {
  background: #EF4444;
}

/* FOOTER BAR */
.ps2-footer-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.9rem;
  padding-top: 0.6rem;
  border-top: 1px solid #1E293B;
  font-size: 0.68rem;
  color: #64748B;
  letter-spacing: 0.05em;
}

.ps2-footer-hint {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.ps2-btn-badge {
  background: #334155;
  color: #E2E8F0;
  font-weight: 700;
  font-size: 0.58rem;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  letter-spacing: 0.06em;
}

.ps2-footer-tag {
  font-weight: 600;
  color: #94A3B8;
}

/* RESPONSIVE DESIGN */
@media (max-width: 860px) {
  .ps2-pitch-content {
    flex-direction: column;
    padding: 1.1rem 0.9rem;
    gap: 1rem;
  }
  .ps2-zone-left, .ps2-zone-right {
    width: 100%;
    justify-content: center;
  }
  .ps2-tactical-arrow { display: none; }
  .ps2-card-float { width: 100%; max-width: 320px; }
  .ps2-center-clash { order: -1; }
  .ps2-attr-label { flex: 0 0 140px; font-size: 0.6rem; }
}

@media (max-width: 600px) {
  .ps2-top-bar { flex-direction: column; gap: 0.35rem; text-align: center; }
  .ps2-attr-row { flex-wrap: wrap; justify-content: center; }
  .ps2-attr-label { flex: 1 1 100%; order: -1; }
  .ps2-footer-bar { flex-direction: column; gap: 0.35rem; text-align: center; }
}

</style>
        """,
        unsafe_allow_html=True,
    )


def style_fig(
    fig: go.Figure,
    height: int = 380,
    x_grid: bool = False,
    y_grid: bool = False,
) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=18, t=22, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color=INK,
            size=12,
        ),
        colorway=COLORWAY,
        hoverlabel=dict(
            bgcolor=INK,
            font_color="#FFF8E6",
            bordercolor=INK,
            font_family="Inter, Segoe UI, sans-serif",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    fig.update_xaxes(
        showgrid=x_grid,
        gridcolor="#EEE6D2",
        zeroline=False,
        linecolor="#E4DAC2",
        tickcolor="#E4DAC2",
        ticks="outside",
        title_font=dict(size=11, color=MUTED),
        tickfont=dict(size=11, color=MUTED),
    )
    fig.update_yaxes(
        showgrid=y_grid,
        gridcolor="#EEE6D2",
        zeroline=False,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(size=11, color=MUTED),
        title_font=dict(size=11, color=MUTED),
    )
    return fig
