"""Top navigation bar: brand plus a pill menu, without Streamlit's sidebar."""

from __future__ import annotations

import streamlit as st

from ui.logos import app_mark_data_uri

PAGES = (
    "Dashboard",
    "Tabel",
    "Simulator",
    "Head-to-Head",
    "Statistik",
    "Metodologi",
)

DEFAULT_PAGE = "Dashboard"

_NAVBAR_SCROLL_SCRIPT = """
<!doctype html>
<html lang="id">
<head><meta charset="utf-8" /></head>
<body>
<script>
(function () {
  var win = window.parent;
  if (!win || win === window) return;

  var doc = win.document;
  var KEY = "__uclNavbarFloating";
  var FLOATING = "is-floating";
  var SPACER = "ucl-navbar-spacer";
  var ENTER_AT = 32;
  var EXIT_AT = 10;

  // Streamlit reruns recreate this iframe: keep one controller per page.
  if (win[KEY] && typeof win[KEY].refresh === "function") {
    win[KEY].refresh();
    return;
  }

  var currentNav = null;
  var resizeObserver = null;
  var frame = 0;

  function findScrollParent(el) {
    var node = el.parentElement;
    while (node && node !== doc.body && node !== doc.documentElement) {
      var overflowY = win.getComputedStyle(node).overflowY;
      if (
        (overflowY === "auto" || overflowY === "scroll" || overflowY === "overlay") &&
        node.scrollHeight > node.clientHeight + 1
      ) {
        return node;
      }
      node = node.parentElement;
    }
    return null;
  }

  function currentScrollTop(nav) {
    var scroller = findScrollParent(nav);
    if (scroller) return scroller.scrollTop;
    return (
      win.scrollY ||
      win.pageYOffset ||
      doc.documentElement.scrollTop ||
      doc.body.scrollTop ||
      0
    );
  }

  function removeSpacers() {
    var stale = doc.querySelectorAll("." + SPACER);
    for (var i = 0; i < stale.length; i += 1) stale[i].remove();
  }

  function ensureSpacer(nav) {
    var previous = nav.previousElementSibling;
    if (previous && previous.classList.contains(SPACER)) return previous;

    removeSpacers();
    var spacer = doc.createElement("div");
    spacer.className = SPACER;
    spacer.setAttribute("aria-hidden", "true");
    nav.parentNode.insertBefore(spacer, nav);
    return spacer;
  }

  function measure(nav) {
    return nav.getBoundingClientRect().height;
  }

  function sync() {
    frame = 0;
    var nav = doc.querySelector(".st-key-navbar");
    if (!nav) return;

    if (nav !== currentNav) {
      currentNav = nav;
      if (resizeObserver) resizeObserver.disconnect();
      resizeObserver = null;
      if (typeof win.ResizeObserver === "function") {
        resizeObserver = new win.ResizeObserver(function () {
          if (!nav.classList.contains(FLOATING)) return;
          var spacer = nav.previousElementSibling;
          if (spacer && spacer.classList.contains(SPACER)) {
            spacer.style.height = measure(nav) + "px";
          }
        });
        resizeObserver.observe(nav);
      }
    }

    var floating = nav.classList.contains(FLOATING);
    var scrollTop = currentScrollTop(nav);
    var next = floating;

    if (!floating && scrollTop > ENTER_AT) {
      next = true;
    } else if (floating && scrollTop < EXIT_AT) {
      next = false;
    }

    if (next === floating) {
      if (next) {
        var existing = ensureSpacer(nav);
        existing.style.display = "block";
      }
      return;
    }

    if (next) {
      // Measure before switching to fixed so the spacer exactly replaces the
      // navbar's old flow height: the page below never jumps.
      var restingHeight = measure(nav);
      var spacer = ensureSpacer(nav);
      spacer.style.height = restingHeight + "px";
      spacer.style.display = "block";
      nav.classList.add(FLOATING);
    } else {
      nav.classList.remove(FLOATING);
      removeSpacers();
    }
  }

  function schedule() {
    if (frame) return;
    frame = win.requestAnimationFrame(sync);
  }

  win[KEY] = { refresh: schedule };

  win.addEventListener("scroll", schedule, { passive: true, capture: true });
  win.addEventListener("resize", schedule, { passive: true });
  win.addEventListener("orientationchange", schedule, { passive: true });

  if (typeof win.MutationObserver === "function") {
    var observer = new win.MutationObserver(schedule);
    observer.observe(doc.documentElement, { childList: true, subtree: true });
  }

  if (doc.readyState === "complete") {
    schedule();
  } else {
    doc.addEventListener("DOMContentLoaded", schedule, { once: true });
    schedule();
  }
})();
</script>
</body>
</html>
"""


def _mount_scroll_behavior() -> None:
    """Run the scroll listener inside a hidden same-origin iframe."""
    with st.container(key="navbar-runtime"):
        st.iframe(_NAVBAR_SCROLL_SCRIPT, height=1)


def render_navbar() -> str:
    state = st.session_state
    if state.get("page") not in PAGES:
        state["page"] = DEFAULT_PAGE

    with st.container(key="navbar"):
        brand_col, menu_col = st.columns([1.25, 3.4], vertical_alignment="center")
        with brand_col:
            mark_uri = app_mark_data_uri()
            mark_html = (
                f'<img class="ucl-mark" src="{mark_uri}" alt="" aria-hidden="true" />'
                if mark_uri
                else ""
            )
            st.markdown(
                f"""
<div class="ucl-brand">
  {mark_html}
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

    _mount_scroll_behavior()

    return state["page"]
