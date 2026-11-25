from __future__ import annotations

from core.pipeline import Settings, load_matches, run_pipeline
from core.stats import head_to_head
from ui.pitch import clean_html, generate_stadium_pitch_svg, render_ps2_matchup_html


def test_clean_html_strips_indents_and_empty_lines():
    raw = """
    <div class="test">
      <span>hello</span>

      <div>world</div>
    </div>
    """
    cleaned = clean_html(raw)
    assert "\n\n" not in cleaned
    assert "  " not in cleaned
    assert cleaned == '<div class="test"><span>hello</span><div>world</div></div>'


def test_stadium_pitch_svg():
    svg = generate_stadium_pitch_svg()
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "<circle" in svg
    assert "<rect" in svg


def test_render_ps2_matchup_html_escapes_and_contains_hud():
    matches = load_matches("data/matches.csv")
    model = run_pipeline(matches, Settings(n_sims=20))
    res = head_to_head(model.ratings, "Arsenal", "Real Madrid")

    html = render_ps2_matchup_html(
        model=model,
        result=res,
        team_a="Arsenal",
        team_b="Real Madrid",
        venue_label="Kandang Arsenal",
    )
    assert "Arsenal" in html
    assert "Real Madrid" in html
    assert "ps2-versus-wrapper" in html
    assert "ps2-attr-row" in html
    assert "UEFA CHAMPIONS LEAGUE" in html
    assert "PREDIKSI SKOR" in html
    assert "Lainnya:" in html
    # Ensure no code block triggers: no \n\n followed by spaces
    assert "\n\n" not in html
