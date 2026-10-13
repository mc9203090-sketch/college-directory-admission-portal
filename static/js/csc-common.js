
document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("csc-menu-toggle");
    const navbar = document.getElementById("csc-navbar");
    const backToTop = document.getElementById("back-to-top");

    if (menuToggle && navbar) {
        menuToggle.addEventListener("click", function () {
            const isOpen = navbar.classList.toggle("active");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });

        document.querySelectorAll(".csc-dropdown-toggle").forEach(function (link) {
            link.addEventListener("click", function (event) {
                if (window.innerWidth <= 767) {
                    event.preventDefault();

                    const dropdown = this.closest(".csc-dropdown");
                    if (!dropdown) return;

                    document.querySelectorAll(".csc-dropdown").forEach(function (item) {
                        if (item !== dropdown) item.classList.remove("open");
                    });

                    dropdown.classList.toggle("open");
                }
            });
        });

        navbar.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                if (
                    window.innerWidth <= 767 &&
                    !this.classList.contains("csc-dropdown-toggle")
                ) {
                    navbar.classList.remove("active");
                    menuToggle.setAttribute("aria-expanded", "false");
                }
            });
        });

        window.addEventListener("resize", function () {
            if (window.innerWidth > 767) {
                navbar.classList.remove("active");
                menuToggle.setAttribute("aria-expanded", "false");

                document.querySelectorAll(".csc-dropdown").forEach(function (item) {
                    item.classList.remove("open");
                });
            }
        });
    }

    if (backToTop) {
        window.addEventListener("scroll", function () {
            backToTop.style.display = window.scrollY > 200 ? "block" : "none";
        });

        backToTop.addEventListener("click", function (event) {
            event.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // Undergraduate page accordion
    document.querySelectorAll(".degree-header").forEach(function (header) {
        header.addEventListener("click", function () {
            const item = this.closest(".degree-item");
            if (!item) return;

            item.classList.toggle("open");
            this.setAttribute(
                "aria-expanded",
                String(item.classList.contains("open"))
            );
        });
    });
});
