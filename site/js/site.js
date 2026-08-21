/* Learning How to Look & Listen — site behaviour.
   One job, no dependencies: click-to-load video facades, so 19 YouTube
   players don't load until someone actually wants to watch one.

   The header and footer used to be rendered here as custom elements.
   They are plain HTML in each page now: the chrome is the one thing a
   reader cannot do without, and it should not depend on this file
   loading. The duplication is the cheaper half of that trade. */

(function () {
  "use strict";

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
