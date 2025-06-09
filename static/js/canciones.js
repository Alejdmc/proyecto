document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-cancion');
    const btnConsultaTodos = document.getElementById('btn-consulta-todos');
    const spotifyBtn = document.getElementById('spotify-cancion-btn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            // Asegura que el campo explicita se mande como string "true" o "false"
            formData.delete('explicita');
            formData.append('explicita', form.querySelector('[name="explicita"]').checked ? "true" : "false");
            try {
                const res = await fetch('/api/canciones_db/', {
                    method: 'POST',
                    body: formData
                });
                if (!res.ok) throw new Error(await res.text());
                alert('Canción agregada');
                form.reset();
                cargarCanciones();
            } catch (err) {
                alert('Error al enviar la canción: ' + err.message);
            }
        });
    }

    // Mostrar todas las canciones
    async function cargarCanciones() {
        let res = await fetch('/api/canciones_db/');
        if (!res.ok) return;
        const data = await res.json();
        const tbody = document.querySelector('#tabla-todos-canciones tbody');
        tbody.innerHTML = '';
        if (!data.length) return tbody.innerHTML = '<tr><td colspan="7">Sin resultados</td></tr>';
        data.forEach(c => {
            const estado = c.eliminado ? "Eliminada" : "Activa";
            const row = `<tr${c.eliminado ? ' style="background:#900;color:#fff;"' : ''}>
                <td>${c.id}</td>
                <td>${c.titulo}</td>
                <td>${c.genero}</td>
                <td>${c.duracion}</td>
                <td>${c.artista}</td>
                <td>${estado}</td>
                <td>${c.imagen_url ? `<img src="${c.imagen_url}" class="cancion-img" style="max-width:80px;max-height:80px;border-radius:6px;">` : ''}</td>
            </tr>`;
            tbody.innerHTML += row;
        });
    }

    if (btnConsultaTodos) {
        btnConsultaTodos.addEventListener('click', cargarCanciones);
    }

    // PUT actualización total con imagen
    document.getElementById('btn-put-actualizar').addEventListener('click', async () => {
        const id = document.getElementById('put-id').value.trim();
        const titulo = document.getElementById('put-titulo').value.trim();
        const genero = document.getElementById('put-genero').value.trim();
        const duracion = document.getElementById('put-duracion').value.trim();
        const artista = document.getElementById('put-artista').value.trim();
        const explicita = document.getElementById('put-explicita').checked ? "true" : "false";
        const imagenInput = document.getElementById('put-imagen');
        if (!id || !titulo || !genero || !duracion || !artista) {
            alert("Todos los campos son obligatorios");
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
                method: 'PUT',
                body: formData
            });
            if (!res.ok) throw new Error(await res.text());
            alert('Canción actualizada completamente');
            cargarCanciones();
        } catch (error) {
            alert("Ocurrió un error al actualizar: " + error.message);
        }
    });

    // PATCH y DELETE sin imagen
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
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ [campo]: valor })
            });
            if (!res.ok) throw new Error(await res.text());
            alert('Canción actualizada parcialmente');
            cargarCanciones();
        } catch (err) {
            alert("Ocurrió un error al actualizar: " + err.message);
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
            const res = await fetch(`/api/canciones_db/${id}`, { method: 'DELETE' });
            if (!res.ok) throw new Error(await res.text());
            alert('Canción eliminada');
            cargarCanciones();
        } catch (err) {
            alert("Ocurrió un error al eliminar: " + err.message);
        }
    });
    if (spotifyBtn) {
        spotifyBtn.addEventListener('click', async () => {
            const query = document.getElementById('spotify-cancion-query').value;
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
    }
    cargarCanciones();
});