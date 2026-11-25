"""Visual theme for SiKupingBesar: UCL-inspired yellow, cream, and dark brown."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from ui.logos import APP_ICON_PATH

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
        page_icon=str(APP_ICON_PATH) if APP_ICON_PATH.is_file() else "⚽",
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
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  width: 100%;
  box-sizing: border-box;
  background: transparent;
  border-radius: 0 0 24px 24px;
  padding: 0.65rem clamp(1rem, 4vw, 3.2rem);
  transition:
    top 0.42s cubic-bezier(0.22, 1, 0.36, 1),
    left 0.42s cubic-bezier(0.22, 1, 0.36, 1),
    right 0.42s cubic-bezier(0.22, 1, 0.36, 1),
    padding 0.42s cubic-bezier(0.22, 1, 0.36, 1),
    border-radius 0.42s cubic-bezier(0.22, 1, 0.36, 1);
}

/* Streamlit places the injected <style> and the hidden runtime iframe in
   zero-height flex items. Take them out of flow so their flex-gap stops
   pushing the navbar down and the page content away. */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has(style),
[data-testid="stLayoutWrapper"]:has(> .st-key-navbar-runtime) {
  position: absolute !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  pointer-events: none !important;
}

/* Two stacked surfaces cross-fade so the rest -> glass change stays smooth:
   ::before is the resting gradient bar, ::after the floating glass pill. */
.st-key-navbar::before,
.st-key-navbar::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  box-sizing: border-box;
  border-radius: inherit;
  pointer-events: none;
  transition:
    opacity 0.38s ease,
    border-radius 0.42s cubic-bezier(0.22, 1, 0.36, 1);
}

.st-key-navbar::before {
  background: linear-gradient(100deg, #FFC21F 0%, #FFB800 55%, #F2A900 100%);
  box-shadow: 0 12px 30px rgba(26, 20, 0, 0.10);
  opacity: 1;
}

.st-key-navbar::after {
  background:
    linear-gradient(
      115deg,
      rgba(255, 198, 34, 0.50) 0%,
      rgba(255, 248, 230, 0.62) 46%,
      rgba(246, 242, 231, 0.70) 100%
    );
  border: 1px solid rgba(255, 255, 255, 0.55);
  box-shadow:
    0 18px 42px rgba(26, 20, 0, 0.16),
    0 2px 8px rgba(26, 20, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.62);
  -webkit-backdrop-filter: blur(18px) saturate(165%);
  backdrop-filter: blur(18px) saturate(165%);
  opacity: 0;
}

.st-key-navbar > * { position: relative; z-index: 1; }

/* Floating state, toggled by the scroll listener in ui/navbar.py. */
.st-key-navbar.is-floating {
  position: fixed;
  top: clamp(8px, 1.4vw, 16px);
  left: clamp(10px, 2vw, 26px);
  right: clamp(10px, 2vw, 26px);
  width: auto;
  border-radius: 999px;
  padding-left: clamp(0.9rem, 2.4vw, 1.8rem);
  padding-right: clamp(0.9rem, 2.4vw, 1.8rem);
}

.st-key-navbar.is-floating::before { opacity: 0; }
.st-key-navbar.is-floating::after { opacity: 1; }

/* Invisible embed that owns the scroll listener (see ui/navbar.py). */
.st-key-navbar-runtime {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

/* Reserves the navbar's normal-flow space while it is fixed, so nothing below jumps. */
.ucl-navbar-spacer {
  display: none;
  width: 100%;
  margin: 0 !important;
  padding: 0 !important;
  border: 0 !important;
  pointer-events: none;
}

.st-key-navbar [data-testid="stHorizontalBlock"] {
  align-items: center;
  min-height: 42px;
}

/* The brand mark is 42px tall, taller than Streamlit's default markdown
   line box. Give that column the same height so both halves share a
   baseline and the logo no longer hangs below the bar. */
.st-key-navbar [data-testid="stColumn"]:first-child [data-testid="stMarkdown"] {
  min-height: 42px;
}
.st-key-navbar [data-testid="stColumn"]:first-child [data-testid="stMarkdown"] > div {
  min-height: 42px;
  display: flex;
  align-items: center;
}
/* Streamlit trims markdown blocks with a negative bottom margin, which
   makes the 42px brand look 8px lower than the menu. */
.st-key-navbar [data-testid="stColumn"]:first-child [data-testid="stMarkdownContainer"] {
  margin-bottom: 0 !important;
}
@media (max-width: 720px) {
  .st-key-navbar [data-testid="stColumn"]:first-child [data-testid="stMarkdown"],
  .st-key-navbar [data-testid="stColumn"]:first-child [data-testid="stMarkdown"] > div {
    min-height: 38px;
  }
}

/* Brand left, menu centred in the bar regardless of brand width. */
@media (min-width: 1100px) {
  .st-key-navbar [data-testid="stHorizontalBlock"] {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    gap: 0;
  }
  .st-key-navbar [data-testid="stColumn"] {
    width: auto !important;
    min-width: 0 !important;
    flex: none !important;
  }
  .st-key-navbar [data-testid="stColumn"]:first-child {
    grid-column: 1;
    justify-self: start;
  }
  .st-key-navbar [data-testid="stColumn"]:last-child {
    grid-column: 2;
    justify-self: center;
  }
  .st-key-navbar .st-key-nav_pills { width: auto !important; }
}

.st-key-page {
  max-width: 1320px;
  margin: 0 auto;
  padding: 1.6rem clamp(1rem, 3.2vw, 2.4rem) 4rem;
}
@keyframes uclPageFade {
  0% { opacity: 0.86; transform: translateY(4px); }
  100% { opacity: 1; transform: translateY(0); }
}
.st-key-page.is-switching {
  animation: uclPageFade 0.28s cubic-bezier(0.22, 1, 0.36, 1);
}

@media (max-width: 768px) {
  .st-key-navbar {
    padding: 0.5rem 0.9rem;
    border-radius: 0 0 18px 18px;
  }
  .st-key-navbar.is-floating {
    top: 6px;
    left: 8px;
    right: 8px;
    border-radius: 22px;
    padding: 0.45rem 0.75rem;
  }
  .st-key-navbar [data-testid="stHorizontalBlock"] {
    gap: 0.25rem !important;
    min-height: 0;
  }
  .st-key-navbar [data-testid="stColumn"]:first-child [data-testid="stMarkdown"],
  .st-key-navbar [data-testid="stColumn"]:first-child [data-testid="stMarkdown"] > div {
    min-height: 34px;
  }
  .st-key-page {
    padding: 1rem 0.85rem 3rem;
  }
}

@media (max-width: 480px) {
  .st-key-navbar {
    padding: 0.45rem 0.7rem;
    border-radius: 0 0 16px 16px;
  }
  .st-key-navbar.is-floating {
    top: 5px;
    left: 6px;
    right: 6px;
    border-radius: 18px;
    padding: 0.4rem 0.65rem;
  }
  .st-key-page {
    padding: 0.8rem 0.65rem 2.5rem;
  }
}

.ucl-brand { display: flex; align-items: center; gap: 0.65rem; min-width: 0; }
.ucl-mark {
  display: block; flex: 0 0 42px;
  width: 42px; height: 42px;
  object-fit: contain;
  filter: drop-shadow(0 2px 5px rgba(26,20,0,0.18));
}
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
  overflow-x: auto;
  scrollbar-width: none;
  padding: 4px 2px;
}
.st-key-navbar [data-testid="stButtonGroup"]::-webkit-scrollbar { display: none; }
.st-key-navbar [data-testid="stButtonGroup"] > div,
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"] {
  position: relative;
  isolation: isolate;
  flex-wrap: nowrap;
  gap: 0.22rem !important;
  align-items: center;
}

/* Sliding capsule indicator driven by JS custom properties in ui/navbar.py */
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"].has-glider::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: var(--glider-w, 0px);
  height: var(--glider-h, 0px);
  transform: translate3d(var(--glider-x, 0px), var(--glider-y, 0px), 0);
  border-radius: 999px;
  background: var(--ink);
  box-shadow: 0 4px 14px rgba(26, 20, 0, 0.20);
  z-index: 0;
  pointer-events: none;
  will-change: transform, width;
}
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"].has-glider.is-ready::before {
  transition:
    transform 0.38s cubic-bezier(0.22, 1, 0.36, 1),
    width 0.38s cubic-bezier(0.22, 1, 0.36, 1),
    height 0.26s cubic-bezier(0.22, 1, 0.36, 1),
    background-color 0.2s ease,
    box-shadow 0.22s ease;
}
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"].has-glider:has(button[aria-checked="true"]:hover)::before,
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"].has-glider:has(button.is-gliding-to:hover)::before {
  background: #261D02;
  box-shadow: 0 6px 16px rgba(26, 20, 0, 0.24);
}

.st-key-navbar [data-testid="stButtonGroup"] button {
  position: relative;
  z-index: 1;
  border-radius: 999px !important;
  border: 1px solid transparent !important;
  background: transparent !important;
  box-shadow: none !important;
  outline: none !important;
  color: rgba(26, 20, 0, 0.78) !important;
  font-weight: 700 !important;
  font-size: 0.84rem !important;
  letter-spacing: -0.01em !important;
  padding: 0.42rem 0.96rem !important;
  white-space: nowrap;
  min-height: 0 !important;
  transition:
    background-color 0.22s cubic-bezier(0.22, 1, 0.36, 1),
    color 0.26s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.22s ease,
    transform 0.16s cubic-bezier(0.22, 1, 0.36, 1) !important;
}
.st-key-navbar [data-testid="stButtonGroup"] button:not([aria-checked="true"]):not(.is-gliding-to):hover {
  background: rgba(26, 20, 0, 0.09) !important;
  border-color: transparent !important;
  color: var(--ink) !important;
  box-shadow: none !important;
  transform: none !important;
}
.st-key-navbar [data-testid="stButtonGroup"] button:not([aria-checked="true"]):not(.is-gliding-to):active {
  background: rgba(26, 20, 0, 0.15) !important;
  color: var(--ink) !important;
  transform: scale(0.96) !important;
}

/* Fallback before JS mounts .has-glider */
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"]:not(.has-glider) button[aria-checked="true"] {
  background: var(--ink) !important;
  color: var(--ucl-yellow) !important;
  border-color: transparent !important;
  box-shadow: 0 4px 12px rgba(26, 20, 0, 0.18) !important;
}

/* Active & in-flight target text colour when sliding glider is active */
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"].has-glider button[aria-checked="true"]:not(.is-gliding-away),
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"].has-glider button.is-gliding-to {
  background: transparent !important;
  color: var(--ucl-yellow) !important;
  border-color: transparent !important;
  box-shadow: none !important;
}
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"].has-glider button.is-gliding-away {
  background: transparent !important;
  color: rgba(26, 20, 0, 0.78) !important;
  box-shadow: none !important;
}
.st-key-navbar [data-testid="stButtonGroup"] button[aria-checked="true"]:active,
.st-key-navbar [data-testid="stButtonGroup"] button.is-gliding-to:active {
  transform: scale(0.97) !important;
}
.st-key-navbar [data-testid="stButtonGroup"] button:focus:not(:focus-visible) {
  outline: none !important;
  box-shadow: none !important;
}
.st-key-navbar [data-testid="stButtonGroup"] [role="radiogroup"]:not(.has-glider) button[aria-checked="true"]:focus:not(:focus-visible) {
  box-shadow: 0 4px 12px rgba(26, 20, 0, 0.18) !important;
}
.st-key-navbar [data-testid="stButtonGroup"] button:focus-visible {
  outline: 2px solid rgba(26, 20, 0, 0.45) !important;
  outline-offset: 2px !important;
}
@media (max-width: 768px) {
  .st-key-navbar [data-testid="stButtonGroup"] {
    width: 100%;
    -webkit-overflow-scrolling: touch;
    padding: 2px 0;
  }
  .st-key-navbar [data-testid="stButtonGroup"] button {
    font-size: 0.78rem !important;
    padding: 0.35rem 0.76rem !important;
  }
}
@media (max-width: 480px) {
  .st-key-navbar [data-testid="stButtonGroup"] button {
    font-size: 0.75rem !important;
    padding: 0.32rem 0.66rem !important;
  }
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
@media (max-width: 1000px) { .ucl-kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.7rem; } }
@media (max-width: 640px) {
  .ucl-section { margin: 1.5rem 0 0.75rem; }
  .ucl-section h2 { font-size: 1.24rem; }
  .ucl-section p { font-size: 0.84rem; }
  .ucl-card { padding: 0.9rem 0.95rem; border-radius: 15px; }
  .ucl-kpi .label { font-size: 0.65rem; }
  .ucl-kpi .value { font-size: 1.32rem; }
  .ucl-kpi .sub { font-size: 0.72rem; }
  .ucl-fav { padding: 1.05rem 1.1rem; border-radius: 18px; }
  .ucl-fav-value { font-size: 1.95rem; }
  .ucl-badge { width: 38px; height: 38px; }
  .st-key-page [data-testid="stHorizontalBlock"] { gap: 0.65rem; }
  [data-testid="stForm"] { padding: 0.95rem 0.95rem 0.5rem; border-radius: 16px; }
}
@media (max-width: 380px) { .ucl-kpi-grid { grid-template-columns: 1fr; } }

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

[data-testid="stElementContainer"]:has([data-testid="stPlotlyChart"]) {
  overflow: visible !important;
}
[data-testid="stPlotlyChart"] {
  background: var(--card) !important;
  border: none !important;
  border-radius: 20px !important;
  padding: 0 !important;
  overflow: hidden !important;
  box-shadow:
    inset 0 0 0 1px var(--line),
    0 12px 28px rgba(26, 20, 0, 0.045) !important;
}

/* Custom SiKupingBesar Tables & Markdown Tables */
.ucl-table-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 14px 34px rgba(26, 20, 0, 0.055);
  margin: 0.35rem 0 1rem;
}
.ucl-table-legend {
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.65rem;
  padding: 0.75rem 1.15rem;
  background: linear-gradient(180deg, #FCF9F2 0%, #F5EFE0 100%);
  border-bottom: 1px solid var(--line);
}
.ucl-zone-pills { display: flex; align-items: center; flex-wrap: wrap; gap: 0.85rem; }
.ucl-zone-item {
  display: inline-flex; align-items: center; gap: 0.4rem;
  font-size: 0.74rem; font-weight: 700; color: var(--ink);
}
.ucl-zone-item .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.ucl-zone-item .dot-top8 { background: var(--ink); box-shadow: 0 0 0 2px var(--ucl-yellow); }
.ucl-zone-item .dot-playoff { background: var(--ucl-yellow); }
.ucl-zone-item .dot-out { background: #CFC6AE; }
.ucl-table-meta {
  font-size: 0.72rem; font-weight: 600; color: var(--muted);
}
.ucl-table-wrap { width: 100%; overflow-x: auto; }
.ucl-table-wrap.is-compact-scroll { max-height: 440px; overflow-y: auto; }
.ucl-table-empty {
  padding: 2rem 1.2rem; text-align: center; color: var(--muted); font-size: 0.9rem; font-weight: 600;
}

table.ucl-table {
  width: 100%; border-collapse: collapse; border-spacing: 0;
  font-size: 0.84rem; font-variant-numeric: tabular-nums;
}
table.ucl-table thead th {
  background: var(--ink); color: rgba(255, 248, 230, 0.88);
  font-size: 0.68rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;
  padding: 0.82rem 0.85rem; text-align: left; white-space: nowrap; border: none;
  position: sticky; top: 0; z-index: 2;
}
table.ucl-table thead th.is-sorted { color: var(--ucl-yellow); }
table.ucl-table thead th.col-rank { text-align: center; width: 52px; }
table.ucl-table thead th.col-num { text-align: right; }
table.ucl-table thead th.col-ci { text-align: center; }

table.ucl-table tbody tr {
  border-bottom: 1px solid #EFE9D8;
  transition: background-color 0.12s ease;
}
table.ucl-table tbody tr:last-child { border-bottom: none; }
table.ucl-table tbody tr:hover { background: rgba(255, 184, 0, 0.085); }
table.ucl-table tbody tr.zone-top8 { box-shadow: inset 4px 0 0 var(--ucl-yellow); }
table.ucl-table tbody tr.zone-playoff { box-shadow: inset 4px 0 0 rgba(224, 158, 0, 0.42); }
table.ucl-table tbody tr.zone-out { box-shadow: inset 4px 0 0 #E5DEC9; background: rgba(246, 242, 231, 0.36); }
table.ucl-table tbody tr.zone-out:hover { background: rgba(255, 184, 0, 0.085); }
table.ucl-table tbody tr.zone-cutoff td { border-bottom: 2px dashed rgba(26, 20, 0, 0.20); }

table.ucl-table td {
  padding: 0.62rem 0.85rem; vertical-align: middle; color: var(--ink); border: none;
}
table.ucl-table.is-dense td { padding: 0.52rem 0.68rem; }
table.ucl-table.is-dense thead th { padding: 0.76rem 0.68rem; }
table.ucl-table td.col-rank { text-align: center; width: 52px; }
table.ucl-table td.col-num { text-align: right; white-space: nowrap; }
table.ucl-table td.col-ci { text-align: center; white-space: nowrap; }
table.ucl-table td.col-bar { min-width: 132px; }
table.ucl-table td.is-bold { font-weight: 800; color: var(--ink); }
table.ucl-table td.is-muted { color: var(--muted); font-weight: 600; }

.ucl-pos {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 28px; height: 26px; padding: 0 6px; border-radius: 8px;
  font-size: 0.74rem; font-weight: 800;
  background: #F3EEE0; color: var(--ink);
}
.ucl-pos.gold { background: var(--ucl-yellow); color: var(--ink); box-shadow: 0 2px 6px rgba(255, 184, 0, 0.35); }
.ucl-pos.top8 { background: var(--ink); color: var(--ucl-yellow); }
.ucl-pos.playoff { background: rgba(255, 184, 0, 0.22); color: #6B4800; border: 1px solid rgba(224, 158, 0, 0.35); }
.ucl-pos.out { background: #EFEAE0; color: var(--muted); }

.ucl-badge.sm { width: 30px; height: 30px; font-size: 0.64rem; padding: 3px; }
.ucl-td-team { display: flex; align-items: center; gap: 0.62rem; min-width: 170px; }
.ucl-td-team-meta { display: flex; flex-direction: column; line-height: 1.18; min-width: 0; }
.ucl-td-team-name { font-weight: 700; font-size: 0.86rem; color: var(--ink); white-space: nowrap; }
.ucl-zone-tag {
  font-size: 0.63rem; font-weight: 700; letter-spacing: 0.04em; margin-top: 2px;
}
.ucl-zone-tag.tag-top8 { color: #0E7B4F; }
.ucl-zone-tag.tag-playoff { color: #9A6700; }
.ucl-zone-tag.tag-out { color: var(--muted); }

.ucl-meter { display: flex; align-items: center; justify-content: flex-end; gap: 0.55rem; }
.ucl-meter-track {
  flex: 1 1 56px; max-width: 84px; height: 7px; border-radius: 999px;
  background: #EDE6D3; overflow: hidden;
}
.ucl-meter-fill { display: block; height: 100%; border-radius: 999px; }
.ucl-meter-fill.fill-gold { background: linear-gradient(90deg, #FFC21F 0%, #E09E00 100%); }
.ucl-meter-fill.fill-ink { background: linear-gradient(90deg, #1A1400 0%, #534214 100%); }
.ucl-meter-fill.fill-green { background: linear-gradient(90deg, #0E7B4F 0%, #1CA36C 100%); }
.ucl-meter-fill.fill-warm { background: linear-gradient(90deg, #D89B1C 0%, #9A6700 100%); }
.ucl-meter-val { min-width: 46px; text-align: right; font-weight: 700; font-size: 0.8rem; color: var(--ink); }

.ucl-heat {
  display: inline-block; min-width: 54px; text-align: right;
  padding: 0.2rem 0.48rem; border-radius: 8px;
  border: 1px solid transparent;
  font-size: 0.8rem; font-weight: 600; color: var(--ink);
}
.ucl-heat.is-strong { font-weight: 800; min-width: 60px; }

.ucl-ci-pill {
  display: inline-block; padding: 0.18rem 0.52rem; border-radius: 999px;
  background: #F6F1E3; border: 1px solid #E7DFC9;
  font-size: 0.74rem; font-weight: 600; color: var(--muted);
}
.ucl-pill-count {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 28px; padding: 0.14rem 0.45rem; border-radius: 999px;
  background: #F4EFE2; font-size: 0.75rem; font-weight: 700; color: var(--ink);
}
.ucl-pill-count.is-zero {
  background: rgba(224, 158, 0, 0.16); color: #8A5B00;
}

/* Style plain Markdown tables (Simulator CSV schema & Metodologi) to match theme */
[data-testid="stMarkdownContainer"] table:not(.ucl-table) {
  width: 100%; border-collapse: separate; border-spacing: 0;
  background: var(--card); border: 1px solid var(--line); border-radius: 18px;
  overflow: hidden; box-shadow: 0 12px 28px rgba(26,20,0,0.045);
  margin: 0.5rem 0 1rem; font-size: 0.85rem;
}
[data-testid="stMarkdownContainer"] table:not(.ucl-table) thead th {
  background: var(--ink); color: var(--ucl-yellow);
  font-size: 0.7rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;
  padding: 0.78rem 1rem; border: none; text-align: left;
}
[data-testid="stMarkdownContainer"] table:not(.ucl-table) tbody td {
  padding: 0.68rem 1rem; border-top: 1px solid #EFE9D8; border-left: none; border-right: none; border-bottom: none;
  color: var(--ink);
}
[data-testid="stMarkdownContainer"] table:not(.ucl-table) tbody tr:hover td {
  background: rgba(255, 184, 0, 0.07);
}

/* Mobile & Tablet Responsive Table Adjustments */
@media (max-width: 768px) {
  .ucl-table-card { border-radius: 16px; }
  .ucl-table-legend { padding: 0.6rem 0.85rem; gap: 0.45rem; }
  .ucl-zone-pills { gap: 0.55rem; }
  .ucl-zone-item { font-size: 0.68rem; }
  .ucl-table-meta { font-size: 0.68rem; width: 100%; }
  .ucl-table-wrap { -webkit-overflow-scrolling: touch; }
  table.ucl-table { font-size: 0.78rem; }
  table.ucl-table thead th { padding: 0.68rem 0.55rem; font-size: 0.62rem; }
  table.ucl-table td { padding: 0.5rem 0.55rem; }
  table.ucl-table.is-dense thead th { padding: 0.62rem 0.48rem; }
  table.ucl-table.is-dense td { padding: 0.44rem 0.48rem; }
  table.ucl-table thead th.col-rank,
  table.ucl-table td.col-rank { width: 38px; padding-left: 0.35rem; padding-right: 0.25rem; }
  table.ucl-table td.col-bar { min-width: 112px; }
  .ucl-td-team { min-width: 138px; gap: 0.45rem; }
  .ucl-td-team-name { font-size: 0.78rem; max-width: 112px; overflow: hidden; text-overflow: ellipsis; }
  .ucl-badge.sm { width: 26px; height: 26px; padding: 2px; }
  .ucl-pos { min-width: 24px; height: 22px; font-size: 0.68rem; border-radius: 6px; }
  .ucl-meter { gap: 0.4rem; }
  .ucl-meter-track { flex-basis: 42px; max-width: 60px; height: 6px; }
  .ucl-meter-val { min-width: 40px; font-size: 0.74rem; }
  .ucl-heat { min-width: 46px; padding: 0.16rem 0.36rem; font-size: 0.74rem; }
  .ucl-heat.is-strong { min-width: 52px; }
  .ucl-ci-pill { font-size: 0.68rem; padding: 0.14rem 0.42rem; }

  /* Sticky club column when scrolling horizontally on mobile/tablet */
  table.ucl-table thead th.col-team {
    position: sticky;
    left: 0;
    z-index: 4;
    background: var(--ink);
    box-shadow: 3px 0 8px rgba(26, 20, 0, 0.12);
  }
  table.ucl-table tbody td.col-team {
    position: sticky;
    left: 0;
    z-index: 1;
    background: var(--card);
    box-shadow: 3px 0 8px rgba(26, 20, 0, 0.05);
  }
  table.ucl-table tbody tr.zone-out td.col-team {
    background: #FBF9F3;
  }
  table.ucl-table tbody tr:hover td.col-team {
    background: #FFF6DF;
  }

  [data-testid="stMarkdownContainer"] table:not(.ucl-table) {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    font-size: 0.78rem;
    border-radius: 14px;
  }
  [data-testid="stMarkdownContainer"] table:not(.ucl-table) thead th,
  [data-testid="stMarkdownContainer"] table:not(.ucl-table) tbody td {
    padding: 0.55rem 0.75rem;
  }
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
   ABOUT PAGE: EDITORIAL CREDITS, DEVELOPERS & LECTURER
   ========================================================= */
.ucl-ab-wrap {
  margin: 0.4rem 0 1.2rem;
}
.ucl-ab-hero {
  padding: 0.4rem 0 0.2rem;
}
.ucl-ab-eyebrow-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.7rem;
  margin-bottom: 0.9rem;
}
.ucl-ab-kredit-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.42rem;
  padding: 0.28rem 0.75rem;
  border-radius: 999px;
  background: rgba(255, 184, 0, 0.20);
  border: 1px solid rgba(224, 158, 0, 0.35);
  color: #6B4800;
  font-size: 0.74rem;
  font-weight: 700;
}
.ucl-ab-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--ink);
  display: inline-block;
}
.ucl-ab-version {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.76rem;
  font-weight: 600;
  color: var(--muted);
}
.ucl-ab-title {
  margin: 0;
  font-size: clamp(2rem, 3.8vw, 2.85rem);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.035em;
  color: var(--ink) !important;
}
.ucl-ab-lede {
  margin: 0.95rem 0 0;
  max-width: 610px;
  font-size: 0.92rem;
  line-height: 1.65;
  color: var(--muted);
}
.ucl-ab-divider {
  border: none;
  border-top: 1px solid var(--line);
  margin: 1.75rem 0 1.85rem;
}

.ucl-ab-sec-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.ucl-ab-sec-bar.is-spaced {
  margin-top: 2.2rem;
}
.ucl-ab-sec-left {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}
.ucl-ab-sec-title {
  margin: 0 !important;
  font-size: 1.25rem !important;
  font-weight: 800 !important;
  color: var(--ink) !important;
  letter-spacing: -0.02em;
}
.ucl-ab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--ink);
  color: var(--ucl-yellow);
  font-size: 0.74rem;
  font-weight: 800;
}
.ucl-ab-sec-sub {
  font-size: 0.76rem;
  font-weight: 600;
  color: var(--muted);
}

/* 3-COLUMN MAHASISWA PENGEMBANG CARDS */
.ucl-ab-dev-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.1rem;
}
.ucl-ab-dev-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 1.35rem 1.35rem 1.15rem;
  box-shadow: 0 12px 28px rgba(26, 20, 0, 0.045);
  display: flex;
  flex-direction: column;
  transition: transform 0.16s ease, box-shadow 0.16s ease;
}
.ucl-ab-dev-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(26, 20, 0, 0.08);
}
.ucl-ab-dev-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}
.ucl-ab-dev-photo {
  width: 64px;
  height: 64px;
  border-radius: 14px;
  overflow: hidden;
  flex: 0 0 64px;
  border: 1px solid rgba(26, 20, 0, 0.10);
  box-shadow: 0 4px 10px rgba(26, 20, 0, 0.07);
}
.ucl-ab-dev-photo svg {
  width: 100%;
  height: 100%;
  display: block;
}
.ucl-ab-dev-id {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.73rem;
  font-weight: 600;
  color: var(--muted);
  letter-spacing: 0.03em;
  margin-top: 2px;
}
.ucl-ab-dev-name {
  margin: 0.95rem 0 0.4rem !important;
  font-size: 1.12rem !important;
  font-weight: 800 !important;
  color: var(--ink) !important;
  line-height: 1.22;
}
.ucl-ab-role-wrap {
  margin-bottom: 0.75rem;
}
.ucl-ab-role-pill {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 999px;
  background: rgba(255, 184, 0, 0.18);
  border: 1px solid rgba(224, 158, 0, 0.32);
  color: #7A5200;
  font-size: 0.71rem;
  font-weight: 700;
}
.ucl-ab-dev-desc {
  margin: 0 0 1.15rem;
  font-size: 0.81rem;
  line-height: 1.6;
  color: var(--muted);
  flex: 1 1 auto;
}
.ucl-ab-dev-foot {
  border-top: 1px solid #EFE9D8;
  padding-top: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}
.ucl-ab-cohort {
  font-size: 0.74rem;
  font-weight: 600;
  color: var(--muted);
}
.ucl-ab-icon-group {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.ucl-ab-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: #FAF7EE;
  color: var(--muted);
  transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}
.ucl-ab-icon-btn:hover {
  background: var(--ink);
  color: var(--ucl-yellow);
  border-color: var(--ink);
}

/* WIDE DOSEN PENGAMPU CARD */
.ucl-ab-lec-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.55rem 1.7rem;
  box-shadow: 0 14px 32px rgba(26, 20, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1.65rem;
}
.ucl-ab-lec-photo {
  flex: 0 0 152px;
  width: 152px;
  height: 164px;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(26, 20, 0, 0.12);
  box-shadow: 0 8px 20px rgba(26, 20, 0, 0.10);
}
.ucl-ab-lec-photo svg {
  width: 100%;
  height: 100%;
  display: block;
}
.ucl-ab-lec-body {
  flex: 1 1 0;
  min-width: 0;
}
.ucl-ab-lec-badges {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.65rem;
}
.ucl-ab-lec-pill {
  display: inline-block;
  padding: 0.22rem 0.7rem;
  border-radius: 999px;
  background: var(--ink);
  color: var(--ucl-yellow);
  font-size: 0.69rem;
  font-weight: 800;
  letter-spacing: 0.04em;
}
.ucl-ab-lec-nidn {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--muted);
}
.ucl-ab-lec-name {
  margin: 0.5rem 0 0.2rem !important;
  font-size: 1.48rem !important;
  font-weight: 800 !important;
  color: var(--ink) !important;
  letter-spacing: -0.025em;
  line-height: 1.2;
}
.ucl-ab-lec-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #8A5B00;
  margin-bottom: 0.65rem;
}
.ucl-ab-lec-desc {
  margin: 0;
  max-width: 680px;
  font-size: 0.84rem;
  line-height: 1.62;
  color: var(--muted);
}
.ucl-ab-lec-foot {
  border-top: 1px solid #EFE9D8;
  margin-top: 1.05rem;
  padding-top: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.ucl-ab-lec-dept {
  font-size: 0.76rem;
  font-weight: 600;
  color: var(--muted);
}
.ucl-ab-lec-actions,
.ucl-ab-tech-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.ucl-ab-btn-light,
.ucl-ab-btn-dark {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.42rem 0.85rem;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
}
.ucl-ab-btn-light {
  background: #FAF7EE;
  border: 1px solid var(--line);
  color: var(--ink);
}
.ucl-ab-btn-dark {
  background: var(--ink);
  border: 1px solid var(--ink);
  color: var(--ucl-yellow);
}

/* TEKNOLOGI & LISENSI BANNER */
.ucl-ab-tech-bar {
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 1.2rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
.ucl-ab-tech-title {
  margin: 0 0 0.25rem !important;
  font-size: 1rem !important;
  font-weight: 800 !important;
  color: var(--ink) !important;
}
.ucl-ab-tech-sub {
  margin: 0;
  font-size: 0.8rem;
  color: var(--muted);
  line-height: 1.5;
}

@media (max-width: 980px) {
  .ucl-ab-dev-grid { grid-template-columns: 1fr; }
}
@media (max-width: 720px) {
  .ucl-ab-lec-card {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.2rem 1.15rem;
    gap: 1.1rem;
  }
  .ucl-ab-lec-photo {
    width: 110px;
    height: 118px;
    flex-basis: auto;
  }
  .ucl-ab-lec-name { font-size: 1.24rem !important; }
  .ucl-ab-dev-card { padding: 1.1rem 1.1rem 1rem; }
  .ucl-ab-tech-bar { padding: 1.05rem 1.1rem; }
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
    padding: 1rem 0.85rem;
    gap: 0.85rem;
  }
  .ps2-zone-left, .ps2-zone-right {
    width: 100%;
    justify-content: center;
  }
  .ps2-tactical-arrow { display: none; }
  .ps2-card-float {
    width: 100%;
    max-width: 360px;
  }
  .ps2-card-float.ps2-float-right {
    flex-direction: row-reverse;
  }
  .ps2-card-float.ps2-float-right .ps2-team-info.ps2-text-right {
    text-align: left;
    align-items: flex-start;
  }
  .ps2-card-float.ps2-float-right .ps2-mini-stats.ps2-stats-right {
    justify-content: flex-start;
  }
  .ps2-attr-label { flex: 0 0 140px; font-size: 0.6rem; }
}

@media (max-width: 600px) {
  .ps2-versus-wrapper { border-radius: 14px; margin: 0.8rem 0 1.2rem; }
  .ps2-top-bar { flex-direction: column; gap: 0.35rem; text-align: center; padding: 0.55rem 0.8rem; }
  .ps2-pitch-container { min-height: 0; }
  .ps2-pitch-content { padding: 0.85rem 0.7rem; gap: 0.7rem; }
  .ps2-card-float { padding: 0.68rem 0.8rem; gap: 0.7rem; max-width: 100%; }
  .ps2-crest { width: 52px; height: 52px; padding: 5px; }
  .ps2-team-name { font-size: 0.98rem; }
  .ps2-vs-badge { width: 50px; height: 50px; }
  .ps2-vs-text { font-size: 1.1rem; }
  .ps2-score-prediction { padding: 0.3rem 0.7rem; }
  .ps2-pred-score { font-size: 1rem; }
  .ps2-attributes-panel { padding: 0.85rem 0.8rem 0.7rem; }
  .ps2-panel-header { text-align: center; }
  .ps2-header-title { font-size: 0.62rem; }
  .ps2-attribute-grid { gap: 0.7rem; }
  .ps2-attr-row { gap: 0.45rem; align-items: flex-end; }
  .ps2-attr-val { width: 44px; font-size: 0.74rem; }
  .ps2-attr-val.highlight-a, .ps2-attr-val.highlight-b { font-size: 0.78rem; }
  .ps2-attr-bar-wrap { flex-wrap: wrap; gap: 0.25rem 0.4rem; }
  .ps2-attr-label { flex: 1 1 100%; order: -1; font-size: 0.58rem; }
  .ps2-footer-bar { flex-direction: column; gap: 0.35rem; text-align: center; font-size: 0.62rem; }
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
        margin=dict(l=22, r=26, t=28, b=42),
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
