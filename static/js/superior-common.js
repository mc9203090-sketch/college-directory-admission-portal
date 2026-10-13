
document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const navbar = document.getElementById("navbar");
    const dropdowns = document.querySelectorAll(".navbar .dropdown");
    const backToTop = document.getElementById("back-to-top");

    // Mobile navigation menu
    if (menuToggle && navbar) {
        menuToggle.addEventListener("click", function () {
            const isOpen = navbar.classList.toggle("show");

            menuToggle.setAttribute("aria-expanded", String(isOpen));
            menuToggle.setAttribute(
                "aria-label",
                isOpen ? "Close navigation menu" : "Open navigation menu"
            );
            menuToggle.textContent = isOpen ? "✕" : "☰";
        });
    }

    // Mobile dropdown menus
    dropdowns.forEach(function (dropdown) {
        const button = dropdown.querySelector(".dropdown-toggle");

        if (!button) return;

        button.addEventListener("click", function () {
            const isOpen = dropdown.classList.contains("active");

            dropdowns.forEach(function (otherDropdown) {
                otherDropdown.classList.remove("active");

                const otherButton =
                    otherDropdown.querySelector(".dropdown-toggle");

                if (otherButton) {
                    otherButton.setAttribute("aria-expanded", "false");
                }
            });

            if (!isOpen) {
                dropdown.classList.add("active");
                button.setAttribute("aria-expanded", "true");
            } else {
                button.setAttribute("aria-expanded", "false");
            }
        });
    });

    // Back to top button
    if (backToTop) {
        window.addEventListener("scroll", function () {
            backToTop.classList.toggle("visible", window.scrollY > 300);
        });

        backToTop.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
});
