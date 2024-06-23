document.addEventListener("DOMContentLoaded", function () {
    const filterForm = document.getElementById("filter-form");
    const searchInput = document.getElementById("search-input");
    const productList = document.getElementById("lista");

    const priceMinInput = document.getElementById("price-min");
    const priceMaxInput = document.getElementById("price-max");
    const minRangeInput = document.getElementById("min-range");
    const maxRangeInput = document.getElementById("max-range");

    function syncRangeToInput() {
        priceMinInput.value = minRangeInput.value;
        priceMaxInput.value = maxRangeInput.value;
    }

    function syncInputToRange() {
        minRangeInput.value = priceMinInput.value;
        maxRangeInput.value = priceMaxInput.value;
    }

    minRangeInput.addEventListener("input", syncRangeToInput);
    maxRangeInput.addEventListener("input", syncRangeToInput);
    priceMinInput.addEventListener("input", syncInputToRange);
    priceMaxInput.addEventListener("input", syncInputToRange);

    function applyFilters() {
        const priceMin = parseFloat(priceMinInput.value) || 0;
        const priceMax = parseFloat(priceMaxInput.value) || 1000000;
        const selectedPlatillos = Array.from(filterForm.querySelectorAll('input[name="platillo"]:checked')).map(el => el.value);
        const searchText = searchInput.value.toLowerCase();

        const params = new URLSearchParams();
        params.append('precio_min', priceMin);
        params.append('precio_max', priceMax);
        if (selectedPlatillos.length > 0) {
            selectedPlatillos.forEach(platillo => params.append('platillo', platillo));
        }
        if (searchText) {
            params.append('buscar', searchText);
        }

        fetch(`?${params.toString()}`)
            .then(response => response.text())
            .then(html => {
                productList.innerHTML = new DOMParser().parseFromString(html, 'text/html').getElementById('lista').innerHTML;
            })
            .catch(error => console.error('Error:', error));
    }

    filterForm.addEventListener("submit", function (event) {
        event.preventDefault();
        applyFilters();
    });

    searchInput.addEventListener("input", applyFilters);

    applyFilters();

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