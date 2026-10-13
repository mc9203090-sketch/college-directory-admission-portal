document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".riphah-menu-toggle");
    const navbar = document.querySelector(".riphah-navbar");
    const dropdownToggles = document.querySelectorAll(".riphah-dropdown-toggle");
    const backToTop = document.getElementById("riphah-back-to-top");

    // Mobile navigation menu
    if (menuButton && navbar) {
        menuButton.addEventListener("click", function () {
            const isOpen = navbar.classList.toggle("riphah-active");

            menuButton.setAttribute("aria-expanded", String(isOpen));
            menuButton.setAttribute(
                "aria-label",
                isOpen ? "Close navigation menu" : "Open navigation menu"
            );

            const icon = menuButton.querySelector("i");
            if (icon) {
                icon.classList.toggle("fa-bars", !isOpen);
                icon.classList.toggle("fa-times", isOpen);
            }
        });
    }

    // Mobile dropdown menus
    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener("click", function (event) {
            if (window.matchMedia("(max-width: 767px)").matches) {
                event.preventDefault();

                const dropdown = toggle.closest(".riphah-dropdown");
                if (!dropdown) return;

                const isOpen = dropdown.classList.toggle("riphah-open");
                toggle.setAttribute("aria-expanded", String(isOpen));
            }
        });
    });

    // Close mobile menu when a regular navigation link is selected
    if (navbar && menuButton) {
        navbar.querySelectorAll("a:not(.riphah-dropdown-toggle)").forEach(function (link) {
            link.addEventListener("click", function () {
                if (window.matchMedia("(max-width: 767px)").matches) {
                    navbar.classList.remove("riphah-active");
                    menuButton.setAttribute("aria-expanded", "false");

                    const icon = menuButton.querySelector("i");
                    if (icon) {
                        icon.classList.add("fa-bars");
                        icon.classList.remove("fa-times");
                    }
                }
            });
        });
    }

    // Back-to-top button
    if (backToTop) {
        function updateBackToTop() {
            backToTop.classList.toggle(
                "riphah-back-to-top-visible",
                window.scrollY > 300
            );
        }

        window.addEventListener("scroll", updateBackToTop, { passive: true });
        updateBackToTop();

        backToTop.addEventListener("click", function (event) {
            event.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
});