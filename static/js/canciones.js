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
});

// static/js/artistas.js

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
});
