"""Clean, natural football pitch versus matchup component for Head-to-Head view."""

from __future__ import annotations

from html import escape

import numpy as np

from core.pipeline import ModelRun
from core.stats import HeadToHeadResult
from ui.components import initials, number, pct
from ui.logos import logo_data_uri


def clean_html(raw_html: str) -> str:
    """Strip blank lines and indentation so Streamlit Markdown renders pure HTML without code blocks."""
    lines = [line.strip() for line in raw_html.splitlines() if line.strip()]
    return "".join(lines)


def generate_stadium_pitch_svg() -> str:
    """Generate a clean, natural SVG soccer pitch with lawn mowing stripes and crisp markings."""
    stripes = []
    width_per_stripe = 10.0  # 10 stripes across 100%
    for i in range(10):
        color = "#2a6f3b" if i % 2 == 0 else "#307941"
        x = i * width_per_stripe
        stripes.append(
            f'<rect x="{x:.1f}%" y="0" width="{width_per_stripe:.1f}%" height="100%" fill="{color}" />'
        )
    stripes_svg = "".join(stripes)

    return f"""<svg viewBox="0 0 900 520" width="100%" height="100%" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="natural-vignette" cx="50%" cy="50%" r="65%">
<stop offset="60%" stop-color="rgba(0,0,0,0)" />
<stop offset="100%" stop-color="rgba(0,0,0,0.18)" />
</radialGradient>
</defs>
<g>{stripes_svg}</g>
<rect width="100%" height="100%" fill="url(#natural-vignette)" />
<g stroke="rgba(255,255,255,0.85)" stroke-width="2.5" fill="none">
<rect x="35" y="25" width="830" height="470" rx="2" />
<line x1="450" y1="25" x2="450" y2="495" />
<circle cx="450" cy="260" r="70" />
<circle cx="450" cy="260" r="4.5" fill="rgba(255,255,255,0.9)" />
<rect x="35" y="135" width="135" height="250" />
<rect x="35" y="195" width="48" height="130" />
<circle cx="135" cy="260" r="4" fill="rgba(255,255,255,0.9)" />
<path d="M 170 210 A 70 70 0 0 1 170 310" />
<rect x="730" y="135" width="135" height="250" />
<rect x="817" y="195" width="48" height="130" />
<circle cx="765" cy="260" r="4" fill="rgba(255,255,255,0.9)" />
<path d="M 730 210 A 70 70 0 0 0 730 310" />
<path d="M 35 42 A 17 17 0 0 1 52 25" />
<path d="M 35 478 A 17 17 0 0 0 52 495" />
<path d="M 865 42 A 17 17 0 0 0 848 25" />
<path d="M 865 478 A 17 17 0 0 1 848 495" />
</g>
</svg>"""


def _team_crest_html(team: str, is_team_a: bool = True) -> str:
    """Render clean, solid circular club badge without glowing neon."""
    uri = logo_data_uri(team)
    accent_class = "ps2-crest-a" if is_team_a else "ps2-crest-b"
    if uri:
        return (
            f'<div class="ps2-crest {accent_class}">'
            f'<img src="{uri}" alt="{escape(team)}" loading="lazy" />'
            f"</div>"
        )
    return (
        f'<div class="ps2-crest ps2-crest-fallback {accent_class}">'
        f"<span>{escape(initials(team))}</span>"
        f"</div>"
    )


def _team_tactical_dots(is_team_a: bool = True) -> str:
    """Generate subtle natural tactical formation markers on the pitch."""
    if is_team_a:
        coords = [
            (14, 50),
            (24, 20), (22, 40), (22, 60), (24, 80),
            (34, 30), (32, 50), (34, 70),
            (42, 25), (43, 50), (42, 75),
        ]
    else:
        coords = [
            (86, 50),
            (76, 20), (78, 40), (78, 60), (76, 80),
            (66, 30), (68, 50), (66, 70),
            (58, 25), (57, 50), (58, 75),
        ]

    dots = [
        f'<div class="ps2-tactic-dot" style="left:{x}%; top:{y}%;"></div>'
        for x, y in coords
    ]
    return "".join(dots)


def render_ps2_matchup_html(
    model: ModelRun,
    result: HeadToHeadResult,
    team_a: str,
    team_b: str,
    venue_label: str,
) -> str:
    """Build the single, natural pre-match versus arena with clean football pitch."""
    att_a = model.ratings.attack_of(team_a)
    att_b = model.ratings.attack_of(team_b)
    def_a = model.ratings.defence_of(team_a)
    def_b = model.ratings.defence_of(team_b)

    # In Poisson, lower defence means stronger defence (fewer conceded). Solidity = 1 / def
    solidity_a = 1.0 / max(def_a, 0.01)
    solidity_b = 1.0 / max(def_b, 0.01)

    total_att = att_a + att_b
    bar_att_a = (att_a / total_att * 100.0) if total_att > 0 else 50.0
    bar_att_b = 100.0 - bar_att_a

    total_sol = solidity_a + solidity_b
    bar_def_a = (solidity_a / total_sol * 100.0) if total_sol > 0 else 50.0
    bar_def_b = 100.0 - bar_def_a

    total_exp = result.exp_goals_a + result.exp_goals_b
    bar_exp_a = (result.exp_goals_a / total_exp * 100.0) if total_exp > 0 else 50.0
    bar_exp_b = 100.0 - bar_exp_a

    p_a_pct = result.p_a * 100.0
    p_draw_pct = result.p_draw * 100.0
    p_b_pct = result.p_b * 100.0

    try:
        rank_a = model.table.index[model.table["team"] == team_a].tolist()[0] + 1
        rank_a_str = f"#{rank_a}"
    except Exception:
        rank_a_str = ""

    try:
        rank_b = model.table.index[model.table["team"] == team_b].tolist()[0] + 1
        rank_b_str = f"#{rank_b}"
    except Exception:
        rank_b_str = ""

    pitch_svg = generate_stadium_pitch_svg()
    badge_a = _team_crest_html(team_a, is_team_a=True)
    badge_b = _team_crest_html(team_b, is_team_a=False)
    dots_a = _team_tactical_dots(is_team_a=True)
    dots_b = _team_tactical_dots(is_team_a=False)

    # Extract top 3 most probable scores from the Poisson matrix
    flat_indices = np.argsort(result.matrix.ravel())[::-1][:3]
    top_scores = []
    for idx in flat_indices:
        ga, gb = np.unravel_index(idx, result.matrix.shape)
        top_scores.append((ga, gb, result.matrix[ga, gb] * 100.0))

    main_score = f"{top_scores[0][0]} – {top_scores[0][1]}"
    main_score_pct = pct(top_scores[0][2])

    alt_text = " · ".join(
        f"{ga}–{gb} ({pct(prob)})" for ga, gb, prob in top_scores[1:3]
    )

    raw_html = f"""
    <div class="ps2-versus-wrapper">
      <div class="ps2-top-bar">
        <div class="ps2-status-led">
          <span class="ps2-led-dot"></span>
          <span class="ps2-led-text">PRE-MATCH VERSUS</span>
        </div>
        <div class="ps2-competition-title">
          ★ UEFA CHAMPIONS LEAGUE ★
        </div>
        <div class="ps2-venue-pill">
          🏟️ {escape(venue_label.upper())}
        </div>
      </div>
      <div class="ps2-pitch-container">
        <div class="ps2-svg-turf">{pitch_svg}</div>
        <div class="ps2-pitch-overlay"></div>
        {dots_a}
        {dots_b}
        <div class="ps2-pitch-content">
          <div class="ps2-team-zone ps2-zone-left">
            <div class="ps2-card-float">
              {badge_a}
              <div class="ps2-team-info">
                <div class="ps2-role-tag">{escape(rank_a_str)} TIM A · KANDANG</div>
                <div class="ps2-team-name">{escape(team_a)}</div>
                <div class="ps2-mini-stats">
                  <span class="ps2-stat-chip ps2-chip-odds">Menang {pct(p_a_pct)}</span>
                  <span class="ps2-stat-chip">xG {number(result.exp_goals_a, 2)}</span>
                </div>
              </div>
            </div>
            <div class="ps2-tactical-arrow ps2-arrow-right">
              <span>›</span><span>›</span>
            </div>
          </div>
          <div class="ps2-center-clash">
            <div class="ps2-vs-badge">
              <span class="ps2-vs-text">VS</span>
            </div>
            <div class="ps2-score-prediction">
              <div class="ps2-pred-label">PREDIKSI SKOR</div>
              <div class="ps2-pred-score">{main_score} <span class="ps2-pred-sub">({main_score_pct})</span></div>
              <div class="ps2-alt-scores">Lainnya: {alt_text}</div>
            </div>
            <div class="ps2-win-bar-container" title="Menang {pct(p_a_pct)} | Seri {pct(p_draw_pct)} | Menang {pct(p_b_pct)}">
              <div class="ps2-bar-seg a" style="width: {p_a_pct:.1f}%;"></div>
              <div class="ps2-bar-seg draw" style="width: {p_draw_pct:.1f}%;"></div>
              <div class="ps2-bar-seg b" style="width: {p_b_pct:.1f}%;"></div>
            </div>
          </div>
          <div class="ps2-team-zone ps2-zone-right">
            <div class="ps2-tactical-arrow ps2-arrow-left">
              <span>‹</span><span>‹</span>
            </div>
            <div class="ps2-card-float ps2-float-right">
              <div class="ps2-team-info ps2-text-right">
                <div class="ps2-role-tag">{escape(rank_b_str)} TIM B · TANDANG</div>
                <div class="ps2-team-name">{escape(team_b)}</div>
                <div class="ps2-mini-stats ps2-stats-right">
                  <span class="ps2-stat-chip ps2-chip-odds-b">Menang {pct(p_b_pct)}</span>
                  <span class="ps2-stat-chip">xG {number(result.exp_goals_b, 2)}</span>
                </div>
              </div>
              {badge_b}
            </div>
          </div>
        </div>
      </div>
      <div class="ps2-attributes-panel">
        <div class="ps2-panel-header">
          <span class="ps2-header-bracket">[</span>
          <span class="ps2-header-title">PERBANDINGAN KEKUATAN &amp; PROBABILITAS</span>
          <span class="ps2-header-bracket">]</span>
        </div>
        <div class="ps2-attribute-grid">
          <div class="ps2-attr-row">
            <div class="ps2-attr-val left">{number(att_a, 2)}</div>
            <div class="ps2-attr-bar-wrap">
              <div class="ps2-meter left">
                <div class="ps2-meter-fill left a" style="width: {bar_att_a:.1f}%;"></div>
              </div>
              <div class="ps2-attr-label">DAYA SERANG (ATT)</div>
              <div class="ps2-meter right">
                <div class="ps2-meter-fill right b" style="width: {bar_att_b:.1f}%;"></div>
              </div>
            </div>
            <div class="ps2-attr-val right">{number(att_b, 2)}</div>
          </div>
          <div class="ps2-attr-row">
            <div class="ps2-attr-val left">{number(solidity_a, 2)}</div>
            <div class="ps2-attr-bar-wrap">
              <div class="ps2-meter left">
                <div class="ps2-meter-fill left a" style="width: {bar_def_a:.1f}%;"></div>
              </div>
              <div class="ps2-attr-label">KEKOKOHAN BERTAHAN (DEF)</div>
              <div class="ps2-meter right">
                <div class="ps2-meter-fill right b" style="width: {bar_def_b:.1f}%;"></div>
              </div>
            </div>
            <div class="ps2-attr-val right">{number(solidity_b, 2)}</div>
          </div>
          <div class="ps2-attr-row">
            <div class="ps2-attr-val left">{number(result.exp_goals_a, 2)}</div>
            <div class="ps2-attr-bar-wrap">
              <div class="ps2-meter left">
                <div class="ps2-meter-fill left a" style="width: {bar_exp_a:.1f}%;"></div>
              </div>
              <div class="ps2-attr-label">EKSPEKTASI GOL (xG)</div>
              <div class="ps2-meter right">
                <div class="ps2-meter-fill right b" style="width: {bar_exp_b:.1f}%;"></div>
              </div>
            </div>
            <div class="ps2-attr-val right">{number(result.exp_goals_b, 2)}</div>
          </div>
          <div class="ps2-attr-row">
            <div class="ps2-attr-val left highlight-a">{pct(p_a_pct)}</div>
            <div class="ps2-attr-bar-wrap">
              <div class="ps2-meter left">
                <div class="ps2-meter-fill left a" style="width: {p_a_pct:.1f}%;"></div>
              </div>
              <div class="ps2-attr-label">PELUANG MENANG (SERI {pct(p_draw_pct)})</div>
              <div class="ps2-meter right">
                <div class="ps2-meter-fill right b" style="width: {p_b_pct:.1f}%;"></div>
              </div>
            </div>
            <div class="ps2-attr-val right highlight-b">{pct(p_b_pct)}</div>
          </div>
        </div>
        <div class="ps2-footer-bar">
          <div class="ps2-footer-hint">
            <span class="ps2-btn-badge">SELECT</span> LIHAT MATRIKS SKOR &amp; DUA LEG DI BAWAH
          </div>
          <div class="ps2-footer-tag">
            POISSON ENGINE · SiKupingBesar v26.1
          </div>
        </div>
      </div>
    </div>
    """
    return clean_html(raw_html)
