document.querySelectorAll('form#form-agregar-carrito').forEach(function (form) {
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const contenedorMensajes = document.getElementById("contenedor-mensajes");
        const mensajeExito = contenedorMensajes.querySelector("#mensaje-exito");
        const mensajeStock = contenedorMensajes.querySelector("#mensaje-stock");

        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    mensajeExito.style.display = "block";
                    setTimeout(function () {
                        mensajeExito.style.display = "none";
                    }, 3000);
                } else if (data.error === "invalid_quantity") {
                    console.error('Error en el servidor:', data.error);
                } else if (data.error === "out_of_stock") {
                    mensajeStock.style.display = "block";
                    setTimeout(function () {
                        mensajeStock.style.display = "none";
                    }, 3000);
                } else {
                    console.error('Error en el servidor:', data.error);
                }
            })
            .catch(error => console.error('Error en la solicitud fetch:', error));
    });
});