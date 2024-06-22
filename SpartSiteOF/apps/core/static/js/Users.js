let GlobalSlideNo = 0;

function NextSlide(event, slideNo) {
    event.preventDefault();
    GlobalSlideNo = slideNo;
    const scroller = document.querySelector(".scroller");
    const marginLeft = parseInt(window.getComputedStyle(scroller).getPropertyValue("margin-left"));
    scroller.style.marginLeft = marginLeft - 470 + "px";
    MoveIndicationBar(slideNo);
}

function GoBack(event) {
    event.preventDefault();
    if (GlobalSlideNo > 0) {
        GlobalSlideNo--;
        const scroller = document.querySelector(".scroller");
        const marginLeft = parseInt(window.getComputedStyle(scroller).getPropertyValue("margin-left"));
        scroller.style.marginLeft = marginLeft + 470 + "px";
        MoveIndicationBar(GlobalSlideNo);
    }
}

const IndicatorObj = {
    startVal: 0,
    EndVal: 25,
    currentWidth: 0,
    StepNo: 0
};

function MoveIndicationBar(i) {
    const step = document.querySelectorAll(".steps")[i - 1];
    IndicatorObj.StepNo = i;
    IndicatorObj.EndVal = i * 25;
    ZerotoHeroWidth();
}

function ZerotoHeroWidth() {
    const bar = document.querySelector(".active");
    const step = document.querySelectorAll(".steps")[IndicatorObj.StepNo - 1];
    const barWidth = parseInt(window.getComputedStyle(bar).width);
    if (IndicatorObj.currentWidth > IndicatorObj.EndVal / 2) {
        step.classList.add("PassedStep");
    }
    if (IndicatorObj.currentWidth < IndicatorObj.EndVal) {
        IndicatorObj.currentWidth += 1;
        bar.style.width = IndicatorObj.currentWidth + "%";
        window.requestAnimationFrame(ZerotoHeroWidth);
    }
}

function mostrarRegistro() {
    document.getElementById("formulario-Login").style.display = "none";
    document.getElementById("formulario-registro").style.display = "block";
}

function mostrarLogin() {
    document.getElementById("formulario-registro").style.display = "none";
    document.getElementById("formulario-Login").style.display = "block";
}

$(document).ready(function () {
    $("#formulario-Login").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true
            }
        },
        messages: {
            email: {
                required: "Por favor ingresa tu correo electrónico",
                email: "Por favor ingresa un correo electrónico válido"
            },
            password: {
                required: "Por favor ingresa tu contraseña"
            }
        },
        errorElement: 'div',
        errorPlacement: function (error, element) {
            error.addClass('invalid-feedback');
            element.closest('.input-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid').removeClass('is-valid');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid').addClass('is-valid');
        }
    });

    $("#formulario-registro").validate({
        rules: {
            username: {
                required: true,
                minlength: 4,
                maxlength: 20
            },
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6
            },
            'confirm-password': {
                required: true,
                equalTo: "#password"
            }
        },
        messages: {
            username: {
                required: "Por favor ingresa tu nombre de usuario",
                minlength: "El nombre de usuario debe tener al menos 4 caracteres",
                maxlength: "El nombre de usuario no puede tener más de 20 caracteres"
            },
            email: {
                required: "Por favor ingresa tu correo electrónico",
                email: "Por favor ingresa un correo electrónico válido"
            },
            password: {
                required: "Por favor ingresa tu contraseña",
                minlength: "La contraseña debe tener al menos 6 caracteres"
            },
            'confirm-password': {
                required: "Por favor confirma tu contraseña",
                equalTo: "Las contraseñas no coinciden"
            }
        },
        errorElement: 'div',
        errorPlacement: function (error, element) {
            error.addClass('invalid-feedback');
            if (element.prop('type') === 'checkbox') {
                error.insertAfter(element.next('label'));
            } else {
                error.insertAfter(element);
            }
        },
        highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid').removeClass('is-valid');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid').addClass('is-valid');
        }
    });
});

