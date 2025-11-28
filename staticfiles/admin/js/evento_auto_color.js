document.addEventListener("DOMContentLoaded", function () {
    const categoriaSelect = document.getElementById("id_categoria");
    const colorInput = document.getElementById("id_color");

    function cargarColorCategoria() {
        const categoriaId = categoriaSelect.value;

        if (!categoriaId) return;

        fetch(`/admin/lineatiempo/categoria/${categoriaId}/color/`)
            .then(response => response.json())
            .then(data => {
                if (data.color) {
                    colorInput.value = data.color;
                }
            });
    }

    categoriaSelect.addEventListener("change", cargarColorCategoria);

    // Al cargar el formulario por primera vez
    cargarColorCategoria();
});
