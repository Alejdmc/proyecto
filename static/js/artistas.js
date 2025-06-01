document.addEventListener("DOMContentLoaded", function() {
    fetch("/artistas")
        .then(response => response.json())
        .then(artistas => {
            const lista = document.getElementById("artistas-lista");
            if (artistas.length === 0) {
                lista.innerHTML = "<p>No hay artistas registrados.</p>";
            } else {
                artistas.forEach(artista => {
                    const item = document.createElement("div");
                    item.classList.add("card", "mb-3", "p-3");
                    item.innerHTML = `
                        <h5>${artista.nombre} (${artista.genero_principal})</h5>
                        <p>País: ${artista.pais}</p>
                        <p>${artista.activo ? "Activo" : "Inactivo"}</p>
                    `;
                    lista.appendChild(item);
                });
            }
        })
        .catch(error => {
            console.error("Error al cargar artistas:", error);
        });

    const form = document.getElementById("form-artista");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const data = {
                nombre: form.nombre.value,
                pais: form.pais.value,
                genero_principal: form.genero_principal.value,
                activo: form.activo.checked
            };

            fetch("/artistas", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(res => {
                alert("Artista agregado correctamente");
                window.location.reload();
            })
            .catch(error => {
                console.error("Error al agregar artista:", error);
            });
        });
    }
});