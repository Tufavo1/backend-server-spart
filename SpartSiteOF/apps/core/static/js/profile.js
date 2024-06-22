function copyToClipboard() {
    var textField = document.getElementById("descuento");
    textField.select();
    document.execCommand("copy");
    alert("Texto copiado: " + textField.value);
}