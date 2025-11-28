document.addEventListener("DOMContentLoaded", function () {
    const categoriaSelect = document.getElementById("id_categoria");
    const colorInput = document.getElementById("id_color");

    if (!categoriaSelect || !colorInput) {
        return;
    }

    function cargarColorCategoria() {
        const categoriaId = categoriaSelect.value;
        if (!categoriaId) return;

        // OJO: esta URL DEBE coincidir con la que definimos en admin.py
        fetch(`/admin/lineatiempo/evento/get_categoria_color/${categoriaId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.color) {
                    colorInput.value = data.color;
                }
            })
            .catch(err => {
                console.error("Error obteniendo color de categoría:", err);
            });
    }

    // Cuando cambias la categoría
    categoriaSelect.addEventListener("change", cargarColorCategoria);

    // Si querés que al entrar a editar también ajuste el color según la categoría actual:
     cargarColorCategoria();
});
