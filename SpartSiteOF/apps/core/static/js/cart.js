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
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(response => {
                if (response.status === 200) {
                    if (response.body.success) {
                        mensajeExito.style.display = "block";
                        setTimeout(function () {
                            mensajeExito.style.display = "none";
                        }, 3000);
                    }
                } else {
                    if (response.body.error === "out_of_stock") {
                        mensajeStock.style.display = "block";
                        setTimeout(function () {
                            mensajeStock.style.display = "none";
                        }, 3000);
                    } else if (response.body.error === "invalid_quantity") {
                        console.error('Error en el servidor: cantidad inválida');
                    } else {
                        console.error('Error en el servidor:', response.body.error);
                    }
                }
            })
            .catch(error => console.error('Error en la solicitud fetch:', error));
    });
});
