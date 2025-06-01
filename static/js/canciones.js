document.addEventListener("DOMContentLoaded", function() {
    fetch("/canciones")
        .then(response => response.json())
        .then(canciones => {
            const lista = document.getElementById("canciones-lista");
            if (canciones.length === 0) {
                lista.innerHTML = "<p>No hay canciones registradas.</p>";
            } else {
                canciones.forEach(cancion => {
                    const item = document.createElement("div");
                    item.classList.add("card", "mb-3", "p-3");
                    item.innerHTML = `
                        <h5>${cancion.titulo} (${cancion.genero})</h5>
                        <p>Duración: ${cancion.duracion} min</p>
                        <p>Artista ID: ${cancion.artista_id}</p>
                        <p>${cancion.explicita ? "Explícita" : "No explícita"}</p>
                    `;
                    lista.appendChild(item);
                });
            }
        })
        .catch(error => {
            console.error("Error al cargar canciones:", error);
        });

    const form = document.getElementById("form-cancion");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const data = {
                titulo: form.titulo.value,
                genero: form.genero.value,
                duracion: parseFloat(form.duracion.value),
                artista_id: parseInt(form.artista_id.value),
                explicita: form.explicita.checked
            };

            fetch("/canciones", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(res => {
                alert("Canción agregada correctamente");
                window.location.reload();
            })
            .catch(error => {
                console.error("Error al agregar canción:", error);
            });
        });
    }
});
