document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("volverBtn").addEventListener("click", function (event) {
        event.preventDefault();
        window.history.back();
    });
    document.querySelectorAll('.abrir-resenas').forEach(button => {
        button.addEventListener('click', function () {
            const url = button.dataset.url;
            window.location.href = url;
        });
    });

    const slides = document.querySelectorAll("[data-slide]");
    const buttons = document.querySelectorAll("[data-button]");
    const botones = document.querySelectorAll(".btn-select");
    const sections = document.querySelectorAll(".row");

    let currSlide = 0;
    let maxSlide = slides.length - 1;

    const updateCarousel = (number = 0) => {
        slides.forEach((slide, index) => {
            slide.style.transform = `translateX(${(index - number) * 100}%)`;
        });
    };

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            button.dataset.button == "next" ? ++currSlide : --currSlide;

            if (currSlide > maxSlide) {
                currSlide = 0;
            } else if (currSlide < 0) {
                currSlide = maxSlide;
            }

            updateCarousel(currSlide);
        });
    });

    updateCarousel();

    botones.forEach(button => {
        button.addEventListener("change", () => {
            const id = button.value;
            sections.forEach(section => {
                section.style.display = (section.id === id) ? "block" : "none";
            });
        });
    });

    $("#filter-button").click(function () {
        $("#filter-panel").css("left", "0");
    });

    $("#close-filter").click(function () {
        $("#filter-panel").css("left", "-100%");
    });

    $("#filter-panel").click(function (e) {
        e.stopPropagation();
    });

    $("#filter-button").click(function (e) {
        e.stopPropagation();
    });

    $("#filter-button").click(function () {
        $("#filter-form").css("display", "block");
    });

    $("#close-filter").click(function () {
        $("#filter-form").css("display", "none");
    });
});