document.addEventListener('DOMContentLoaded', () => {
        document.getElementById('form-artista').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);

        formData.delete('activo');
        formData.append("activo", document.querySelector('[name="activo"]:checked') ? "true" : "false");

        if (!formData.get("nombre") || !formData.get("pais") || !formData.get("genero_principal")) {
            alert("Todos los campos son obligatorios.");
            return;
        }

        try {
            const res = await fetch('/api/artistas_db/', {
                method: 'POST',
                body: formData
            });
            if (!res.ok) throw new Error(await res.text());
            form.reset();
            cargarArtistas();
        } catch (err) {
            alert("Error agregando artista: " + err.message);
        }
    });

    document.getElementById('btn-consulta-id').addEventListener('click', async () => {
        const id = document.getElementById('consulta-id').value.trim();
        const div = document.getElementById('resultado-consulta-id');
        div.innerHTML = '';
        if (!id) {
            div.innerHTML = "Introduce un ID.";
            return;
        }
        try {
            const res = await fetch(`/api/artistas_db/${id}`);
            if (res.ok) {
                const data = await res.json();
                div.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>${data.imagen_url ? `<img src="${data.imagen_url}" class="artista-img"/>` : ''}`;
            } else {
                div.innerHTML = "Artista no encontrado";
            }
        } catch {
            div.innerHTML = "Error al consultar por ID";
        }
    });

    document.getElementById('btn-buscar-pais').addEventListener('click', async () => {
        const pais = document.getElementById('buscar-pais').value.trim();
        const resultadoDiv = document.getElementById('resultado-busqueda-pais');
        resultadoDiv.innerHTML = '';
        if (!pais) {
            resultadoDiv.innerHTML = "Introduce un país para buscar.";
            return;
        }
        try {
            const res = await fetch(`/api/artistas_db?pais=${encodeURIComponent(pais)}`);
            const data = await res.json();
            if (Array.isArray(data) && data.length > 0) {
                resultadoDiv.innerHTML = `<pre>${JSON.stringify(data[0], null, 2)}</pre>${data[0].imagen_url ? `<img src="${data[0].imagen_url}" class="artista-img"/>` : ''}`;
            } else {
                resultadoDiv.innerHTML = "Artista no encontrado para ese país";
            }
        } catch {
            resultadoDiv.innerHTML = "Error al buscar por país";
        }
    });

    // Mostrar todos los artistas
    document.getElementById('btn-consulta-todos').addEventListener('click', async () => {
        await cargarArtistas();
    });

    async function cargarArtistas() {
        let url = '/api/artistas_db/';
        const res = await fetch(url);
        const data = await res.json();
        const tbody = document.querySelector('#tabla-todos-artistas tbody');
        tbody.innerHTML = '';
        if (!data.length) {
            tbody.innerHTML = '<tr><td colspan="5">No hay artistas registrados</td></tr>';
        } else {
            data.forEach(a => {
                const row = `<tr>
                    <td>${a.id}</td>
                    <td>${a.nombre}</td>
                    <td>${a.pais}</td>
                    <td>${a.genero_principal || a.genero || ""}</td>
                    <td>${a.imagen_url ? `<img src="${a.imagen_url}" class="artista-img" style="max-width:80px;max-height:80px;border-radius:6px;">` : ''}</td>
                </tr>`;
                tbody.innerHTML += row;
            });
        }
    }

    document.getElementById('btn-put-actualizar').addEventListener('click', async () => {
        const id = document.getElementById('put-id').value.trim();
        const nombre = document.getElementById('put-nombre').value.trim();
        const pais = document.getElementById('put-pais').value.trim();
        const genero_principal = document.getElementById('put-genero').value.trim();
        const activo = document.getElementById('put-activo').checked ? "true" : "false";
        const imagenInput = document.getElementById('put-imagen');
        if (!id || !nombre || !pais || !genero_principal) {
            alert("Completa todos los campos para actualizar.");
            return;
        }

        const formData = new FormData();
        formData.append("nombre", nombre);
        formData.append("pais", pais);
        formData.append("genero_principal", genero_principal);
        formData.append("activo", activo);
        if (imagenInput && imagenInput.files[0]) {
            formData.append("imagen", imagenInput.files[0]);
        }

        try {
            const res = await fetch(`/api/artistas_db/${id}`, {
                method: "PUT",
                body: formData
            });
            if (!res.ok) throw new Error(await res.text());
            cargarArtistas();
        } catch (err) {
            alert("Error al actualizar artista: " + err.message);
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
            const res = await fetch(`/api/artistas_db/${id}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ [campo]: valor })
            });
            if (!res.ok) throw new Error(await res.text());
            cargarArtistas();
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
        if (!confirm("¿Seguro que deseas eliminar el artista?")) return;
        try {
            const res = await fetch(`/api/artistas_db/${id}`, { method: "DELETE" });
            if (!res.ok) throw new Error(await res.text());
            cargarArtistas();
        } catch (err) {
            alert("Error al eliminar artista: " + err.message);
        }
    });

    document.getElementById('spotify-search-btn').addEventListener('click', buscarSpotify);
    document.getElementById('spotify-query').addEventListener('keyup', function(e) {
        if (e.key === "Enter") buscarSpotify();
    });

    async function buscarSpotify() {
        const nombre = document.getElementById('spotify-query').value.trim();
        const tbody = document.querySelector('#tabla-spotify-artistas tbody');
        const div = document.getElementById('resultado-busqueda-spotify');
        tbody.innerHTML = '';
        div.innerHTML = '';
        if (!nombre) {
            div.innerHTML = "Introduce un nombre de artista para buscar en Spotify.";
            return;
        }
        try {
            const res = await fetch(`/api/spotify/artistas?nombre=${encodeURIComponent(nombre)}`);
            if (!res.ok) throw new Error(await res.text());
            const data = await res.json();
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(a => {
                    const row = `<tr>
                        <td>${a.nombre}</td>
                        <td>${a.generos && a.generos.length ? a.generos.join(", ") : "-"}</td>
                        <td>${a.popularidad ?? "-"}</td>
                    </tr>`;
                    tbody.innerHTML += row;
                });
            } else {
                div.innerHTML = "No se encontraron artistas en Spotify.";
            }
        } catch (err) {
            div.innerHTML = `Error al buscar en Spotify: ${err.message}`;
        }
    }

    cargarArtistas();
});