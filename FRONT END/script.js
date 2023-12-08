function checkOnlyOne(clickedCheckbox) {
    const checkboxes = document.getElementsByName('restriccion');

    checkboxes.forEach(checkbox => {
        if (checkbox !== clickedCheckbox) {
            checkbox.checked = false;
        }
    });
}

function ingresar() {
    const conRestriccionCheckbox = document.getElementById('conRestriccion');
    const sinRestriccionCheckbox = document.getElementById('sinRestriccion');

    if (conRestriccionCheckbox.checked) {
        window.location.href = 'con_restriccion.html';
    } else if (sinRestriccionCheckbox.checked) {
        window.location.href = 'sin_restriccion.html';
    } else {
        alert('Por favor, seleccione una opción antes de hacer clic en "Ingresar".');
    }
}