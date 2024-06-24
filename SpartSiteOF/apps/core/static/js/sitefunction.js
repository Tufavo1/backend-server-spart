document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.slide');
    const logoutButton = document.getElementById("Perfil");
    const detallesToggle = document.querySelector('.ver-detalles');
    const ingredientesToggle = document.querySelector('.ver-ingredientes');
    const detallesSection = document.querySelector('.detalles');
    const ingredientesSection = document.querySelector('.ingredientes');

    // Verificar si los elementos existen antes de agregar eventos
    if (detallesToggle && detallesSection) {
        detallesToggle.addEventListener('click', function () {
            detallesSection.classList.toggle('mostrar');
        });
    }

    if (ingredientesToggle && ingredientesSection) {
        ingredientesToggle.addEventListener('click', function () {
            ingredientesSection.classList.toggle('mostrar');
        });
    }

    var configDropdown = document.getElementById("config-dropdown");
    var configButton = document.getElementById("config-button");

    configButton.addEventListener("click", function (event) {
        event.stopPropagation();
        configDropdown.style.display = (configDropdown.style.display === 'none') ? 'block' : 'none';
    });

    document.addEventListener("click", function () {
        configDropdown.style.display = 'none';
    });

    if (logoutButton) {
        logoutButton.addEventListener("click", function () {
            const modal = document.getElementById("myModal");
            modal.style.display = "block";

            const confirmButton = document.getElementById("confirmButton");
            const cancelButton = document.getElementById("cancelButton");

            confirmButton.onclick = function () {
                window.location.reload();
                modal.style.display = "none";
            }

            cancelButton.onclick = function () {
                modal.style.display = "none";
            }
        });
    }

    window.addEventListener('scroll', function () {
        slides.forEach(slide => {
            const slideTop = slide.offsetTop;
            const slideBottom = slideTop + slide.offsetHeight;

            const isHalfShown = slideTop < (window.scrollY + window.innerHeight / 2);
            const isNotScrolledPast = window.scrollY < slideBottom;

            if (isHalfShown && isNotScrolledPast) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });
    });

    interact('#clock-container').draggable({
        inertia: true,
        autoScroll: true,
        onmove: dragMoveListener
    });

    function dragMoveListener(event) {
        var target = event.target;
        var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
        var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

        target.style.webkitTransform = target.style.transform = 'translate(' + x + 'px, ' + y + 'px)';

        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);
    }

    interact.maxInteractions(Infinity);

    function updateClock() {
        var now = new Date();
        var hours = now.getHours();
        var minutes = now.getMinutes();
        var seconds = now.getSeconds();

        hours = String(hours).padStart(2, '0');
        minutes = String(minutes).padStart(2, '0');
        seconds = String(seconds).padStart(2, '0');

        document.getElementById('clock').textContent = hours + ':' + minutes + ':' + seconds;
    }

    setInterval(updateClock, 3000);

    updateClock();

    function showAlert(message) {
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('Alerta-custom');
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
    }

    function getLocationAndUpdateButton() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json&addressdetails=1`)
                    .then(response => response.json())
                    .then(data => {
                        const city = data.address.city || data.address.town || data.address.village || data.address.hamlet || data.address.suburb || data.address.county;

                        document.getElementById("getLocationBtn").innerHTML = `${city}, `;

                        document.cookie = `city=${city}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;

                        fetchWeather(city);
                    })
                    .catch(error => {
                        console.error('Error al obtener la ubicación:', error);
                        showAlert('Hubo un error al obtener la ubicación. Por favor, intenta nuevamente.');
                    });
            }, function (error) {
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        showAlert("El usuario denegó la solicitud de geolocalización.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        showAlert("La información de ubicación no está disponible.");
                        break;
                    case error.TIMEOUT:
                        showAlert("Se ha agotado el tiempo de espera para obtener la ubicación del usuario.");
                        break;
                    case error.UNKNOWN_ERROR:
                        showAlert("Se produjo un error desconocido al obtener la ubicación.");
                        break;
                }
            });
        } else {
            showAlert("Geolocalización no es soportada por este navegador.");
        }
    }

    function fetchWeather(city) {
        fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&lang=es&appid=e7583f9125c2a26e1db48919d23bfc61`)
            .then(response => response.json())
            .then(info => {
                const temperature = (info.main.temp - 273.15).toFixed(1);
                const weatherIcon = info.weather[0].icon;

                document.getElementById("getLocationBtn").innerHTML += `${temperature} °C <img src='https://openweathermap.org/img/wn/${weatherIcon}.png'>`;
            })
            .catch(error => {
                console.error('Error al obtener la información del clima:', error);
                showAlert('Hubo un error al obtener la información del clima. Por favor, intenta nuevamente.');
            });
    }

    function loadCityAndWeatherFromCookie() {
        const cookies = document.cookie.split(';').map(cookie => cookie.trim());
        const cityCookie = cookies.find(cookie => cookie.startsWith('city='));

        if (cityCookie) {
            const city = cityCookie.split('=')[1];
            document.getElementById("getLocationBtn").innerHTML = `${city}, `;
            fetchWeather(city);
        }
    }

    document.getElementById("getLocationBtn").addEventListener("click", getLocationAndUpdateButton);
    window.addEventListener('load', loadCityAndWeatherFromCookie);
});