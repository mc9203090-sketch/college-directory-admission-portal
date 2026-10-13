
document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("menu-toggle");
    const navbar = document.getElementById("navbar");
    const backToTop = document.getElementById("back-to-top");

    if (toggle && navbar) {
        toggle.addEventListener("click", function () {
            const opened = navbar.classList.toggle("active");
            toggle.setAttribute("aria-expanded", String(opened));

            const icon = toggle.querySelector("i");
            if (icon) {
                icon.classList.toggle("fa-bars", !opened);
                icon.classList.toggle("fa-xmark", opened);
            }
        });

        navbar.querySelectorAll(".dropdown > a").forEach(function (link) {
            link.addEventListener("click", function (event) {
                if (window.innerWidth > 768) return;

                event.preventDefault();
                const submenu = link.nextElementSibling;
                if (!submenu || !submenu.classList.contains("sub-menu")) return;

                const open = submenu.style.display !== "block";

                navbar.querySelectorAll(".sub-menu").forEach(function (other) {
                    other.style.display = "none";
                });

                submenu.style.display = open ? "block" : "none";
            });
        });

        navbar.querySelectorAll(":scope > a").forEach(function (link) {
            link.addEventListener("click", function () {
                navbar.classList.remove("active");
                toggle.setAttribute("aria-expanded", "false");
            });
        });

        document.addEventListener("click", function (event) {
            if (
                window.innerWidth <= 768 &&
                !navbar.contains(event.target) &&
                !toggle.contains(event.target)
            ) {
                navbar.classList.remove("active");
                toggle.setAttribute("aria-expanded", "false");
            }
        });

        window.addEventListener("resize", function () {
            if (window.innerWidth > 768) {
                navbar.classList.remove("active");
                toggle.setAttribute("aria-expanded", "false");

                navbar.querySelectorAll(".sub-menu").forEach(function (submenu) {
                    submenu.style.display = "";
                });
            }
        });
    }

    function updateBackToTop() {
        if (backToTop) {
            backToTop.style.display = window.scrollY > 250 ? "flex" : "none";
        }
    }

    if (backToTop) {
        updateBackToTop();
        window.addEventListener("scroll", updateBackToTop);

        backToTop.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
});
