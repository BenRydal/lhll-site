/* Learning How to Look & Listen — site behaviour.
   Two jobs, no dependencies:
     1. <site-nav> / <site-footer> so the chrome is written once.
     2. Click-to-load video facades, so 19 YouTube players don't
        load until someone actually wants to watch one.
   Custom elements render into light DOM, so site.css styles them
   normally and there is no shadow-boundary CSS to duplicate. */

(function () {
  "use strict";

  var PAGES = [
    ["index.html", "Introduction"],
    ["individualsessions.html", "Individual Viewing Sessions"],
    ["groupsession.html", "Group Viewing Session"],
    ["presentations.html", "Presentations"],
    ["futuredirections.html", "Future Directions"],
    ["publications.html", "Publications"]
  ];

  /* Works for /foo, /foo.html and /  — Vercel serves clean URLs,
     local file:// browsing uses the .html names. */
  function currentFile() {
    var last = location.pathname.split("/").pop();
    if (!last) return "index.html";
    return last.indexOf(".") === -1 ? last + ".html" : last;
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  class SiteNav extends HTMLElement {
    connectedCallback() {
      var here = currentFile();
      var items = PAGES.map(function (p) {
        var current = p[0] === here ? ' aria-current="page"' : "";
        return '<li><a href="' + p[0] + '"' + current + ">" + esc(p[1]) + "</a></li>";
      }).join("");

      this.innerHTML =
        '<header class="masthead">' +
          '<div class="wrap masthead__inner">' +
            '<a class="masthead__title" href="index.html">Learning How to Look &amp; Listen</a>' +
            '<nav aria-label="Sections"><ul class="nav">' + items + "</ul></nav>" +
          "</div>" +
        "</header>";
    }
  }

  class SiteFooter extends HTMLElement {
    connectedCallback() {
      this.innerHTML =
        '<footer class="foot">' +
          '<div class="wrap">' +
            "<p>Supported by the Spencer Foundation &amp; Arizona State University. " +
            "Website, visualizations, videography and commentary designed by " +
            '<a href="https://benrydal.com">Ben Rydal Shapiro</a>, Rogers Hall, ' +
            "Frederick Erickson, Sherman Dorn and Alfredo Artiles.</p>" +
            '<p>All material is published under a ' +
            '<a href="https://creativecommons.org/licenses/by-nc-sa/3.0/" rel="license">' +
            "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.</p>" +
          "</div>" +
        "</footer>";
    }
  }

  customElements.define("site-nav", SiteNav);
  customElements.define("site-footer", SiteFooter);

  /* ---- video facades ------------------------------------------------ */

  function play(btn) {
    var id = btn.getAttribute("data-video");
    if (!id) return;

    var frame = document.createElement("iframe");
    /* nocookie host: no YouTube tracking cookie until playback starts */
    frame.src = "https://www.youtube-nocookie.com/embed/" + id +
                "?autoplay=1&rel=0&modestbranding=1";
    frame.title = btn.getAttribute("data-title") || "Video";
    frame.allow = "accelerometer; autoplay; encrypted-media; picture-in-picture; fullscreen";
    frame.allowFullscreen = true;
    frame.referrerPolicy = "strict-origin-when-cross-origin";

    /* Swap the button out entirely rather than nesting the iframe inside
       it — an iframe inside a <button> is invalid and swallows clicks
       meant for the player controls. */
    var shell = document.createElement("div");
    shell.className = "facade is-playing";
    shell.appendChild(frame);
    btn.replaceWith(shell);
    frame.focus();
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".facade");
    if (btn) play(btn);
  });

  /* Warm the connection on hover so the player starts faster,
     without loading anything on page view. */
  var warmed = false;
  document.addEventListener("pointerover", function (e) {
    if (warmed || !e.target.closest(".facade")) return;
    warmed = true;
    ["https://www.youtube-nocookie.com", "https://i.ytimg.com",
     "https://www.google.com"].forEach(function (host) {
      var l = document.createElement("link");
      l.rel = "preconnect";
      l.href = host;
      document.head.appendChild(l);
    });
  }, { passive: true });
})();
