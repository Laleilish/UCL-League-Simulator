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
    "About",
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
  var KEY = "__uclNavbarControllerV2";
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
  var currentGroup = null;
  var resizeObserver = null;
  var groupResizeObserver = null;
  var frame = 0;
  var glideState = {
    lastIdx: -1,
    pendingIdx: -1,
    pendingUntil: 0,
    x: 0,
    y: 0,
    w: 0,
    h: 0,
    initialized: false
  };

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

  function measureButton(group, btn) {
    var gRect = group.getBoundingClientRect();
    var bRect = btn.getBoundingClientRect();
    return {
      x: bRect.left - gRect.left + group.scrollLeft,
      y: bRect.top - gRect.top + group.scrollTop,
      w: bRect.width,
      h: bRect.height
    };
  }

  function scrollPillIntoView(group, btn, smooth) {
    var scroller = group.closest('[data-testid="stButtonGroup"]') || group;
    if (!scroller || scroller.scrollWidth <= scroller.clientWidth + 2) return;
    var sRect = scroller.getBoundingClientRect();
    var bRect = btn.getBoundingClientRect();
    var targetLeft =
      scroller.scrollLeft +
      (bRect.left - sRect.left) -
      (sRect.width / 2 - bRect.width / 2);
    var maxScroll = Math.max(0, scroller.scrollWidth - scroller.clientWidth);
    var clamped = Math.max(0, Math.min(maxScroll, targetLeft));
    if (typeof scroller.scrollTo === "function") {
      scroller.scrollTo({ left: clamped, behavior: smooth ? "smooth" : "auto" });
    } else {
      scroller.scrollLeft = clamped;
    }
  }

  function applyGliderVars(group, box) {
    group.style.setProperty("--glider-x", box.x.toFixed(2) + "px");
    group.style.setProperty("--glider-y", box.y.toFixed(2) + "px");
    group.style.setProperty("--glider-w", box.w.toFixed(2) + "px");
    group.style.setProperty("--glider-h", box.h.toFixed(2) + "px");
    glideState.x = box.x;
    glideState.y = box.y;
    glideState.w = box.w;
    glideState.h = box.h;
  }

  function syncGlider(instant) {
    var nav = doc.querySelector(".st-key-navbar");
    if (!nav) return;
    var group = nav.querySelector('[data-testid="stButtonGroup"] [role="radiogroup"]');
    if (!group) return;

    var buttons = Array.prototype.slice.call(group.querySelectorAll("button"));
    if (!buttons.length) return;

    var isNewGroup = group !== currentGroup;
    if (isNewGroup) {
      currentGroup = group;
      if (groupResizeObserver) groupResizeObserver.disconnect();
      groupResizeObserver = null;
      if (typeof win.ResizeObserver === "function") {
        groupResizeObserver = new win.ResizeObserver(function () {
          syncGlider(true);
        });
        groupResizeObserver.observe(group);
        for (var r = 0; r < buttons.length; r += 1) {
          groupResizeObserver.observe(buttons[r]);
        }
      }
    }

    var checkedIdx = -1;
    for (var i = 0; i < buttons.length; i += 1) {
      if (buttons[i].getAttribute("aria-checked") === "true") {
        checkedIdx = i;
        break;
      }
    }

    var now = win.performance ? win.performance.now() : Date.now();
    var targetIdx = checkedIdx;
    if (glideState.pendingIdx >= 0 && glideState.pendingIdx < buttons.length) {
      if (checkedIdx === glideState.pendingIdx) {
        glideState.pendingIdx = -1;
        for (var c = 0; c < buttons.length; c += 1) {
          buttons[c].classList.remove("is-gliding-to", "is-gliding-away");
        }
      } else if (now < glideState.pendingUntil) {
        targetIdx = glideState.pendingIdx;
      } else {
        glideState.pendingIdx = -1;
        for (var k = 0; k < buttons.length; k += 1) {
          buttons[k].classList.remove("is-gliding-to", "is-gliding-away");
        }
      }
    }

    if (targetIdx < 0) targetIdx = 0;
    var targetBtn = buttons[targetIdx];
    var nextBox = measureButton(group, targetBtn);
    if (nextBox.w <= 0) return;

    group.classList.add("has-glider");

    // First mount: snap without animation, then arm transitions.
    if (!glideState.initialized) {
      group.classList.remove("is-ready");
      applyGliderVars(group, nextBox);
      glideState.lastIdx = targetIdx;
      glideState.initialized = true;
      scrollPillIntoView(group, targetBtn, false);
      win.requestAnimationFrame(function () {
        group.classList.add("is-ready");
      });
      return;
    }

    // If Streamlit recreated the radiogroup DOM across a rerun while changing tabs,
    // seed from the previous pill rect first so the glide still animates smoothly.
    if (isNewGroup && glideState.lastIdx !== targetIdx && glideState.w > 0 && !instant) {
      group.classList.remove("is-ready");
      group.style.setProperty("--glider-x", glideState.x.toFixed(2) + "px");
      group.style.setProperty("--glider-y", glideState.y.toFixed(2) + "px");
      group.style.setProperty("--glider-w", glideState.w.toFixed(2) + "px");
      group.style.setProperty("--glider-h", glideState.h.toFixed(2) + "px");
      group.getBoundingClientRect();
      group.classList.add("is-ready");
      applyGliderVars(group, nextBox);
      glideState.lastIdx = targetIdx;
      return;
    }

    if (instant) {
      var wasReady = group.classList.contains("is-ready");
      if (wasReady && now >= glideState.pendingUntil) {
        group.classList.remove("is-ready");
        applyGliderVars(group, nextBox);
        group.getBoundingClientRect();
        group.classList.add("is-ready");
      } else {
        applyGliderVars(group, nextBox);
      }
      glideState.lastIdx = targetIdx;
      return;
    }

    group.classList.add("is-ready");
    applyGliderVars(group, nextBox);
    glideState.lastIdx = targetIdx;
  }

  function onNavClick(event) {
    var nav = doc.querySelector(".st-key-navbar");
    if (!nav || !nav.contains(event.target)) return;
    var btn = event.target.closest('[data-testid="stButtonGroup"] [role="radiogroup"] button');
    if (!btn) return;
    var group = btn.closest('[role="radiogroup"]');
    if (!group) return;

    // Prevent accidental deselection when clicking the already-active pill.
    if (btn.getAttribute("aria-checked") === "true" && glideState.pendingIdx < 0) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    var buttons = Array.prototype.slice.call(group.querySelectorAll("button"));
    var nextIdx = buttons.indexOf(btn);
    if (nextIdx < 0) return;

    for (var i = 0; i < buttons.length; i += 1) {
      var b = buttons[i];
      if (i === nextIdx) {
        b.classList.add("is-gliding-to");
        b.classList.remove("is-gliding-away");
      } else if (b.getAttribute("aria-checked") === "true") {
        b.classList.add("is-gliding-away");
        b.classList.remove("is-gliding-to");
      } else {
        b.classList.remove("is-gliding-to", "is-gliding-away");
      }
    }

    var now = win.performance ? win.performance.now() : Date.now();
    glideState.pendingIdx = nextIdx;
    glideState.pendingUntil = now + 600;
    group.classList.add("has-glider", "is-ready");
    applyGliderVars(group, measureButton(group, btn));
    glideState.lastIdx = nextIdx;
    scrollPillIntoView(group, btn, true);

    var page = doc.querySelector(".st-key-page");
    if (page) {
      page.classList.remove("is-switching");
      page.getBoundingClientRect();
      page.classList.add("is-switching");
    }
  }

  function sync() {
    frame = 0;
    syncGlider(false);
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

  doc.addEventListener("click", onNavClick, true);
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
    <small>UCL League Predictor</small>
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
