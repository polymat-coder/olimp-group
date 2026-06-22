document.addEventListener(
  "click",
  (event) => {
    if (
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }

    const link = event.target.closest("a[href]");
    if (!link || link.target === "_blank" || link.hasAttribute("download")) {
      return;
    }

    const destination = new URL(link.href, window.location.href);
    if (
      destination.origin === window.location.origin &&
      destination.pathname.endsWith(".html")
    ) {
      event.preventDefault();
      event.stopImmediatePropagation();
      window.location.assign(destination.href);
    }
  },
  true,
);

window.__staticNavigationReady = true;
