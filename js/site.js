(function () {
  const header = document.querySelector("[data-header]");
  const menuBtn = document.querySelector("[data-menu-btn]");
  const menu = document.querySelector("[data-menu]");

  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (menuBtn && header) {
    menuBtn.addEventListener("click", function () {
      const open = header.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.body.style.overflow = open ? "hidden" : "";
      const openIcon = menuBtn.querySelector("[data-icon-open]");
      const closeIcon = menuBtn.querySelector("[data-icon-close]");
      if (openIcon && closeIcon) {
        openIcon.hidden = open;
        closeIcon.hidden = !open;
      }
    });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  const gallery = document.querySelector("[data-gallery]");
  if (gallery) {
    const list = gallery.querySelector("[data-gallery-list]");
    const cards = list.querySelectorAll("[data-item]");
    const filters = gallery.querySelectorAll("[data-filter]");
    const lightbox = document.querySelector("[data-lightbox]");
    const lightImg = lightbox.querySelector("img");
    const lightTitle = lightbox.querySelector("[data-light-title]");
    const lightLoc = lightbox.querySelector("[data-light-loc]");
    let current = "all";

    function render() {
      cards.forEach(function (card) {
        const cat = card.getAttribute("data-category");
        card.hidden = !(current === "all" || cat === current);
      });
    }

    function openItem(id) {
      const card = list.querySelector('[data-item="' + id + '"]');
      if (!card) return;
      const img = card.querySelector("img");
      lightImg.src = img.getAttribute("src");
      lightImg.alt = img.getAttribute("alt") || "";
      lightTitle.textContent = card.getAttribute("data-title");
      lightLoc.textContent = card.getAttribute("data-location");
      lightbox.hidden = false;
      document.body.style.overflow = "hidden";
    }

    function closeLight() {
      lightbox.hidden = true;
      document.body.style.overflow = "";
    }

    filters.forEach(function (btn) {
      btn.addEventListener("click", function () {
        current = btn.getAttribute("data-filter");
        filters.forEach(function (other) { other.setAttribute("aria-pressed", other === btn ? "true" : "false"); });
        render();
      });
    });
    list.addEventListener("click", function (event) {
      const btn = event.target.closest("[data-open]");
      if (btn) openItem(btn.getAttribute("data-open"));
    });
    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox || event.target.closest("[data-light-close]")) closeLight();
    });
    window.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !lightbox.hidden) closeLight();
    });
    render();
  }

  const rangeLabels = {
    events: "$650–$2,400",
    property: "$325–$750",
    inspection: "$450–$1,800",
    mapping: "$800–$3,500",
    cinema: "Custom"
  };
  const titles = {
    events: "events & production",
    property: "property & architecture",
    inspection: "inspection",
    mapping: "mapping & orthos",
    cinema: "cinematic & tilt-shift"
  };

  const form = document.querySelector("[data-quote]");
  if (form) {
    const select = form.querySelector("#service");
    const range = form.querySelector("[data-range]");
    const params = new URLSearchParams(window.location.search);
    const initial = params.get("service");
    if (initial && rangeLabels[initial]) select.value = initial;

    function paintRange() {
      const id = select.value;
      range.innerHTML = "Typical range for " + titles[id] + ": <strong>" + rangeLabels[id] + "</strong>";
    }
    select.addEventListener("change", paintRange);
    paintRange();

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const data = new FormData(form);
      const name = String(data.get("name") || "").trim();
      const email = String(data.get("email") || "").trim();
      const nameError = form.querySelector("[data-error-name]");
      const emailError = form.querySelector("[data-error-email]");
      const nameInput = form.querySelector("#name");
      const emailInput = form.querySelector("#email");
      nameError.textContent = "";
      emailError.textContent = "";
      nameInput.removeAttribute("aria-invalid");
      emailInput.removeAttribute("aria-invalid");
      let bad = false;
      if (!name) {
        nameError.textContent = "Name is required.";
        nameInput.setAttribute("aria-invalid", "true");
        bad = true;
      }
      if (!email) {
        emailError.textContent = "Email is required.";
        emailInput.setAttribute("aria-invalid", "true");
        bad = true;
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        emailError.textContent = "Enter a valid email address.";
        emailInput.setAttribute("aria-invalid", "true");
        bad = true;
      }
      if (bad) return;

      const inquiry = {
        ref: "WA-" + Date.now().toString(36).toUpperCase(),
        name: name,
        email: email,
        phone: String(data.get("phone") || "").trim(),
        service: select.value,
        date: String(data.get("date") || ""),
        location: String(data.get("location") || "").trim(),
        message: String(data.get("message") || "").trim(),
        createdAt: new Date().toISOString()
      };
      const existing = JSON.parse(localStorage.getItem("waypoint-inquiries") || "[]");
      localStorage.setItem("waypoint-inquiries", JSON.stringify([inquiry].concat(existing)));
      window.location.href = "/thank-you/?ref=" + encodeURIComponent(inquiry.ref);
    });
  }

  const refSlot = document.querySelector("[data-ref]");
  if (refSlot) {
    const ref = new URLSearchParams(window.location.search).get("ref");
    if (ref) {
      refSlot.hidden = false;
      refSlot.querySelector("strong").textContent = ref;
      const mail = document.querySelector("[data-ref-mail]");
      if (mail) mail.textContent = " and include " + ref + ".";
    }
  }

  const printBtn = document.querySelector("[data-print]");
  if (printBtn) printBtn.addEventListener("click", function () { window.print(); });
})();
