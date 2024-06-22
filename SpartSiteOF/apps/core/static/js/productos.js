const filterForm = document.getElementById('filter-form');
const searchInput = document.getElementById('search-input');
const productList = document.getElementById('lista');

filterForm.addEventListener('submit', (event) => {
    event.preventDefault();
    filterProducts();
});

searchInput.addEventListener('input', () => {
    filterProducts();
});

const filterProducts = () => {
    const priceMin = parseFloat(document.getElementById('price-min').value) || 0;
    const priceMax = parseFloat(document.getElementById('price-max').value) || 1000000;
    const searchText = searchInput.value.toLowerCase();
    const selectedPlatillos = Array.from(filterForm.querySelectorAll('input[name="platillo"]:checked')).map(el => el.value);

    for (let product of productList) {
        const productName = product.querySelector('.card-title').innerText.toLowerCase();
        const productPrice = parseFloat(product.getAttribute('data-precio'));
        const productPlatillo = product.getAttribute('data-platillo');

        const matchesPrice = productPrice >= priceMin && productPrice <= priceMax;
        const matchesSearch = productName.includes(searchText);
        const matchesPlatillo = selectedPlatillos.length === 0 || selectedPlatillos.includes(productPlatillo);

        if (matchesPrice && matchesSearch && matchesPlatillo) {
            product.style.display = '';
        } else {
            product.style.display = 'none';
        }
    }
};

const minRangeInput = document.getElementById('min-range');
const maxRangeInput = document.getElementById('max-range');
const minPriceInput = document.getElementById('price-min');
const maxPriceInput = document.getElementById('price-max');

minRangeInput.addEventListener('input', () => {
    minPriceInput.value = minRangeInput.value;
    filterProducts();
});

maxRangeInput.addEventListener('input', () => {
    maxPriceInput.value = maxRangeInput.value;
    filterProducts();
});

minPriceInput.addEventListener('input', () => {
    minRangeInput.value = minPriceInput.value;
    filterProducts();
});

maxPriceInput.addEventListener('input', () => {
    maxRangeInput.value = maxPriceInput.value;
    filterProducts();
});