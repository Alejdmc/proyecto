document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-cancion');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);

            formData.delete('explicita');
            formData.append("explicita", document.querySelector('[name="explicita"]:checked') ? "true" : "false");

            if (!formData.get("titulo") || !formData.get("genero") || !formData.get("duracion") || !formData.get("artista")) {
                alert("Todos los campos son obligatorios.");
                return;
            }

            try {
                const res = await fetch('/api/canciones_db/', {
                    method: 'POST',
                    body: formData
                });
                if (!res.ok) throw new Error(await res.text());
                form.reset();
                cargarCanciones();
            } catch (err) {
                alert("Error agregando canción: " + err.message);
            }
        });
    }

    async function cargarCanciones() {
        const res = await fetch('/api/canciones_db/');
        const data = await res.json();
        const tbody = document.querySelector('#tabla-todos-canciones tbody');
        tbody.innerHTML = '';
        if (!data.length) {
            tbody.innerHTML = '<tr><td colspan="7">Sin resultados</td></tr>';
        } else {
            data.forEach(c => {
                const estado = c.eliminado ? "Eliminada" : "Activa";
                const row = `<tr${c.eliminado ? ' style="background:#900;color:#fff;"' : ''}>
                    <td>${c.id}</td>
                    <td>${c.titulo}</td>
                    <td>${c.genero}</td>
                    <td>${c.duracion}</td>
                    <td>${c.artista}</td>
                    <td>${estado}</td>
                    <td>${c.id ? `<img src="/api/canciones_db/${c.id}/imagen" class="cancion-img" style="max-width:80px;max-height:80px;border-radius:6px;">` : ''}</td>
                </tr>`;
                tbody.innerHTML += row;
            });
        }
    }

    document.getElementById('btn-put-actualizar').addEventListener('click', async () => {
        const id = document.getElementById('put-id').value.trim();
        const titulo = document.getElementById('put-titulo').value.trim();
        const genero = document.getElementById('put-genero').value.trim();
        const duracion = document.getElementById('put-duracion').value.trim();
        const artista = document.getElementById('put-artista').value.trim();
        const explicita = document.getElementById('put-explicita').checked ? "true" : "false";
        const imagenInput = document.getElementById('put-imagen');
        if (!id || !titulo || !genero || !duracion || !artista) {
            alert("Completa todos los campos para actualizar.");
            return;
        }
        const formData = new FormData();
        formData.append("titulo", titulo);
        formData.append("genero", genero);
        formData.append("duracion", duracion);
        formData.append("artista", artista);
        formData.append("explicita", explicita);
        if (imagenInput && imagenInput.files[0]) {
            formData.append("imagen", imagenInput.files[0]);
        }

        try {
            const res = await fetch(`/api/canciones_db/${id}`, {
                method: "PUT",
                body: formData
            });
            if (!res.ok) throw new Error(await res.text());
            cargarCanciones();
        } catch (err) {
            alert("Error al actualizar canción: " + err.message);
        }
    });

    document.getElementById('btn-patch-actualizar').addEventListener('click', async () => {
        const id = document.getElementById('patch-id').value.trim();
        const campo = document.getElementById('patch-campo').value.trim();
        const valor = document.getElementById('patch-valor').value.trim();
        if (!id || !campo || !valor) {
            alert("Completa todos los campos para actualizar un campo.");
            return;
        }
        try {
            const res = await fetch(`/api/canciones_db/${id}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ [campo]: valor })
            });
            if (!res.ok) throw new Error(await res.text());
            cargarCanciones();
        } catch (err) {
            alert("Error al actualizar campo: " + err.message);
        }
    });

    document.getElementById('btn-eliminar').addEventListener('click', async () => {
        const id = document.getElementById('delete-id').value.trim();
        if (!id) {
            alert("Introduce el ID a eliminar.");
            return;
        }
        if (!confirm("¿Seguro que deseas eliminar la canción?")) return;
        try {
            const res = await fetch(`/api/canciones_db/${id}`, { method: "DELETE" });
            if (!res.ok) throw new Error(await res.text());
            cargarCanciones();
        } catch (err) {
            alert("Error al eliminar canción: " + err.message);
        }
    });

    const spotifyBtn = document.getElementById('spotify-cancion-btn');
    spotifyBtn?.addEventListener('click', async () => {
        const query = document.getElementById('spotify-cancion-query').value.trim();
        if (!query) {
            alert("Escribe un título de canción");
            return;
        }
        try {
            const res = await fetch(`/api/spotify/canciones?titulo=${encodeURIComponent(query)}`);
            if (!res.ok) throw new Error('Error Spotify');
            const data = await res.json();
            const tbody = document.querySelector('#tabla-spotify-canciones tbody');
            tbody.innerHTML = '';
            if (!data.length) return tbody.innerHTML = '<tr><td colspan="3">Sin resultados</td></tr>';
            data.forEach(c => {
                const row = `<tr><td>${c.nombre}</td><td>${c.artista}</td><td>${c.album}</td></tr>`;
                tbody.innerHTML += row;
            });
        } catch (err) {
            alert('Error al buscar en Spotify');
        }
    });

    cargarCanciones();
});