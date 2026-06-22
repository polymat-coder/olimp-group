const navigateToStaticPage = (event) => {
    if (
      (typeof event.button === "number" && event.button !== 0) ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }

    const link =
      event.currentTarget instanceof HTMLAnchorElement
        ? event.currentTarget
        : event.target instanceof Element
          ? event.target.closest("a[href]")
          : null;
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
};

const bindStaticLinks = () => {
  document.querySelectorAll("a[href]").forEach((link) => {
    if (link.dataset.staticNavigationBound === "true") return;

    const destination = new URL(link.href, window.location.href);
    if (
      destination.origin === window.location.origin &&
      destination.pathname.endsWith(".html")
    ) {
      link.dataset.staticNavigationBound = "true";
      link.addEventListener("click", navigateToStaticPage, true);
    }
  });
};

window.addEventListener("click", navigateToStaticPage, true);
bindStaticLinks();
window.addEventListener("load", bindStaticLinks, { once: true });

window.__staticNavigationReady = true;
document.documentElement.dataset.staticNavigationReady = "true";
