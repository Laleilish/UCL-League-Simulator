"""About page: developer team, course lecturer, and project credits."""

from __future__ import annotations

from html import escape

import streamlit as st

from ui.components import initials

LECTURER_INFO: dict[str, str] = {
    "name": "Dosen Pengampu Probabilitas & Statistika",
    "badge": "Dosen Pengampu",
    "id_label": "MK · PROBABILITAS & STATISTIKA",
    "title": "Pembimbing Utama · Probabilitas, Statistika & Pemodelan Stokastik",
    "description": (
        "Mengarahkan metodologi pemodelan distribusi Poisson, validasi simulasi "
        "Monte Carlo, pengujian hipotesis Chi-square, serta meninjau ketepatan "
        "interpretasi statistik sepanjang pengembangan aplikasi SiKupingBesar."
    ),
    "department": "Program Studi Teknik Informatika · Fakultas Ilmu Komputer",
}

DEVELOPERS: tuple[dict[str, str], ...] = (
    {
        "name": "Febriansyah Nugraha",
        "id_label": "TIM INTI · 01",
        "role": "Engine & Statistical Modeling",
        "description": (
            "Merancang estimasi parameter serang-bertahan model Poisson, peluruhan "
            "form eksponensial, mesin simulasi Monte Carlo tervektorisasi, serta "
            "validasi skema dataset pertandingan."
        ),
        "cohort": "Probabilitas & Statistika",
        "modules": "core/ratings.py · core/simulate.py · core/pipeline.py",
        "accent": "#FFB800",
    },
    {
        "name": "Ilyassa Putra",
        "id_label": "TIM INTI · 02",
        "role": "UI/UX & Frontend Lead",
        "description": (
            "Merancang sistem desain antarmuka bertema UCL, arsitektur komponen "
            "tabel dan navigasi responsif, kartu kandidat juara, serta panel "
            "kontrol parameter di halaman Simulator."
        ),
        "cohort": "Probabilitas & Statistika",
        "modules": "views/dashboard.py · views/tabel.py · views/simulator.py · ui/",
        "accent": "#E09E00",
    },
    {
        "name": "Raden Hamizan Rizky Kusuma",
        "id_label": "TIM INTI · 03",
        "role": "Analytics & Model Validation",
        "description": (
            "Mengembangkan analisis duel Head-to-Head & arena taktikal, grafik "
            "konvergensi Law of Large Numbers, uji kecocokan Chi-square, evaluasi "
            "Brier score 1X2, dan dokumentasi Metodologi."
        ),
        "cohort": "Probabilitas & Statistika",
        "modules": "views/head_to_head.py · views/statistik.py · views/metodologi.py · core/stats.py",
        "accent": "#C68A00",
    },
)


def _avatar_svg(label: str, is_lecturer: bool = False) -> str:
    """Render a stylized academic/developer portrait tile in SiKupingBesar colours."""
    safe = escape(label)
    if is_lecturer:
        return (
            '<div class="ucl-ab-lec-photo" aria-hidden="true">'
            '<svg viewBox="0 0 160 172" xmlns="http://www.w3.org/2000/svg">'
            "<defs>"
            '<linearGradient id="lecBg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0%" stop-color="#261D02"/>'
            '<stop offset="100%" stop-color="#1A1400"/>'
            "</linearGradient>"
            '<radialGradient id="lecGlow" cx="78%" cy="20%" r="55%">'
            '<stop offset="0%" stop-color="rgba(255,184,0,0.38)"/>'
            '<stop offset="100%" stop-color="rgba(255,184,0,0)"/>'
            "</radialGradient>"
            "</defs>"
            '<rect width="160" height="172" rx="16" fill="url(#lecBg)"/>'
            '<rect width="160" height="172" rx="16" fill="url(#lecGlow)"/>'
            '<circle cx="80" cy="64" r="27" fill="#FFB800" opacity="0.92"/>'
            '<path d="M34 156 C34 122 54 106 80 106 C106 106 126 122 126 156 Z" fill="#FFF4D2" opacity="0.22"/>'
            '<path d="M52 156 L68 114 L80 132 L92 114 L108 156 Z" fill="#FFB800" opacity="0.28"/>'
            f'<text x="80" y="72" text-anchor="middle" fill="#1A1400" font-family="Inter,Segoe UI,sans-serif" font-weight="800" font-size="20">{safe}</text>'
            "</svg>"
            "</div>"
        )
    return (
        '<div class="ucl-ab-dev-photo" aria-hidden="true">'
        '<svg viewBox="0 0 68 68" xmlns="http://www.w3.org/2000/svg">'
        "<defs>"
        '<linearGradient id="devBg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#FFF3CC"/>'
        '<stop offset="100%" stop-color="#F5E6B8"/>'
        "</linearGradient>"
        "</defs>"
        '<rect width="68" height="68" rx="14" fill="url(#devBg)"/>'
        '<circle cx="56" cy="12" r="18" fill="rgba(255,184,0,0.25)"/>'
        '<circle cx="34" cy="26" r="12.5" fill="#1A1400"/>'
        '<path d="M14 64 C14 48 22 42 34 42 C46 42 54 48 54 64 Z" fill="#1A1400" opacity="0.88"/>'
        f'<text x="34" y="30" text-anchor="middle" fill="#FFB800" font-family="Inter,Segoe UI,sans-serif" font-weight="800" font-size="10">{safe}</text>'
        "</svg>"
        "</div>"
    )


def _code_icon_svg() -> str:
    return (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="16 18 22 12 16 6"></polyline>'
        '<polyline points="8 6 2 12 8 18"></polyline>'
        "</svg>"
    )


def _mail_icon_svg() -> str:
    return (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="4" width="20" height="16" rx="3"></rect>'
        '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>'
        "</svg>"
    )


def _external_icon_svg() -> str:
    return (
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>'
        '<polyline points="15 3 21 3 21 9"></polyline>'
        '<line x1="10" y1="14" x2="21" y2="3"></line>'
        "</svg>"
    )


def about_cards_html(
    lecturer: dict[str, str] = LECTURER_INFO,
    developers: tuple[dict[str, str], ...] = DEVELOPERS,
) -> str:
    """Build the full reference-inspired About page HTML with Mahasiswa above Dosen Pengampu."""
    header_html = (
        '<div class="ucl-ab-hero">'
        '<div class="ucl-ab-eyebrow-row">'
        '<span class="ucl-ab-kredit-pill"><i class="ucl-ab-dot"></i>Kredit &amp; Kontributor</span>'
        '<span class="ucl-ab-version">v1.0.0 &middot; TA 2026/2027</span>'
        "</div>"
        '<h1 class="ucl-ab-title">Tim Pengembang<br/>&amp; Kredit Aplikasi</h1>'
        '<p class="ucl-ab-lede">'
        "Aplikasi web SiKupingBesar dirancang dan dibangun oleh tiga mahasiswa "
        "pada mata kuliah Probabilitas dan Statistika di bawah bimbingan satu "
        "dosen pengampu sebagai wujud kolaborasi pemodelan stokastik Poisson "
        "dan simulasi Monte Carlo."
        "</p>"
        "</div>"
        '<hr class="ucl-ab-divider" />'
    )

    # 1. MAHASISWA PENGEMBANG (placed FIRST as requested)
    dev_cards: list[str] = []
    for dev in developers:
        name = dev["name"]
        badge_letters = initials(name)
        modules_tip = escape(dev["modules"])
        dev_cards.append(
            '<div class="ucl-ab-dev-card">'
            '<div class="ucl-ab-dev-head">'
            f"{_avatar_svg(badge_letters, is_lecturer=False)}"
            f'<span class="ucl-ab-dev-id">{escape(dev["id_label"])}</span>'
            "</div>"
            f'<h3 class="ucl-ab-dev-name">{escape(name)}</h3>'
            '<div class="ucl-ab-role-wrap">'
            f'<span class="ucl-ab-role-pill">{escape(dev["role"])}</span>'
            "</div>"
            f'<p class="ucl-ab-dev-desc">{escape(dev["description"])}</p>'
            '<div class="ucl-ab-dev-foot">'
            f'<span class="ucl-ab-cohort">{escape(dev["cohort"])}</span>'
            '<div class="ucl-ab-icon-group">'
            f'<span class="ucl-ab-icon-btn" title="Modul: {modules_tip}">{_code_icon_svg()}</span>'
            f'<span class="ucl-ab-icon-btn" title="{escape(name)}">{_mail_icon_svg()}</span>'
            "</div></div></div>"
        )

    students_section = (
        '<div class="ucl-ab-sec-bar">'
        '<div class="ucl-ab-sec-left">'
        '<h2 class="ucl-ab-sec-title">Mahasiswa Pengembang</h2>'
        f'<span class="ucl-ab-count">{len(developers)}</span>'
        "</div>"
        '<span class="ucl-ab-sec-sub">Tim Inti Perancangan &amp; Implementasi</span>'
        "</div>"
        f'<div class="ucl-ab-dev-grid">{"".join(dev_cards)}</div>'
    )

    # 2. DOSEN PENGAMPU (placed BELOW Mahasiswa Pengembang as requested)
    lec_name = lecturer["name"]
    lec_initials = initials(lec_name)
    lecturer_section = (
        '<div class="ucl-ab-sec-bar is-spaced">'
        '<div class="ucl-ab-sec-left">'
        '<h2 class="ucl-ab-sec-title">Dosen Pengampu</h2>'
        "</div>"
        '<span class="ucl-ab-sec-sub">Pembimbing Akademik &amp; Pengarah Proyek</span>'
        "</div>"
        '<div class="ucl-ab-lec-card">'
        f"{_avatar_svg(lec_initials, is_lecturer=True)}"
        '<div class="ucl-ab-lec-body">'
        '<div class="ucl-ab-lec-badges">'
        f'<span class="ucl-ab-lec-pill">{escape(lecturer["badge"])}</span>'
        f'<span class="ucl-ab-lec-nidn">{escape(lecturer["id_label"])}</span>'
        "</div>"
        f'<h3 class="ucl-ab-lec-name">{escape(lec_name)}</h3>'
        f'<div class="ucl-ab-lec-title">{escape(lecturer["title"])}</div>'
        f'<p class="ucl-ab-lec-desc">{escape(lecturer["description"])}</p>'
        '<div class="ucl-ab-lec-foot">'
        f'<span class="ucl-ab-lec-dept">{escape(lecturer["department"])}</span>'
        '<div class="ucl-ab-lec-actions">'
        f'<span class="ucl-ab-btn-light">{_mail_icon_svg()}<span>Surel Akademik</span></span>'
        f'<span class="ucl-ab-btn-dark"><span>Profil Akademik</span>{_external_icon_svg()}</span>'
        "</div></div></div></div>"
    )

    # 3. TEKNOLOGI & LISENSI FOOTER BANNER
    tech_section = (
        '<div class="ucl-ab-tech-bar">'
        '<div class="ucl-ab-tech-text">'
        '<h3 class="ucl-ab-tech-title">Teknologi &amp; Lisensi</h3>'
        '<p class="ucl-ab-tech-sub">'
        "Dibangun menggunakan Python, Streamlit, NumPy, SciPy, pandas, dan Plotly "
        "di bawah lisensi akademik untuk mata kuliah Probabilitas dan Statistika."
        "</p>"
        "</div>"
        '<div class="ucl-ab-tech-actions">'
        '<span class="ucl-ab-btn-light"><span>Model Poisson &amp; MC</span></span>'
        '<span class="ucl-ab-btn-dark"><span>Dokumentasi Teknis</span></span>'
        "</div></div>"
    )

    return f'<div class="ucl-ab-wrap">{header_html}{students_section}{lecturer_section}{tech_section}</div>'


def render() -> None:
    st.markdown(about_cards_html(), unsafe_allow_html=True)
