document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form#form-agregar-carrito').forEach(function (form) {
        const restarBtn = form.parentElement.querySelector('#restar-cantidad');
        const sumarBtn = form.parentElement.querySelector('#sumar-cantidad');
        const cantidadInput = form.parentElement.querySelector('#cantidad');
        const maxCantidad = parseInt(cantidadInput.getAttribute('max'));

        restarBtn.addEventListener('click', function () {
            let valorActual = parseInt(cantidadInput.value);
            cantidadInput.value = Math.max(1, valorActual - 1);
        });

        sumarBtn.addEventListener('click', function () {
            let valorActual = parseInt(cantidadInput.value);
            cantidadInput.value = Math.min(maxCantidad, valorActual + 1);
        });

        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(form);

            const cantidad = parseInt(cantidadInput.value);
            formData.append('cantidad', cantidad);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la solicitud');
                    }
                    return response.json();
                })
                .then(data => {
                })
                .catch(error => {
                });
        });
    });
});
