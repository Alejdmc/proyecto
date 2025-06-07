document.addEventListener('DOMContentLoaded', () => {
    // --- AGREGAR ARTISTA ---
    document.getElementById('form-artista').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const nombre = form.nombre.value.trim();
        const pais = form.pais.value.trim();
        const genero_principal = form.genero_principal.value.trim();
        const activo = form.activo ? form.activo.checked : true;
        if (!nombre || !pais || !genero_principal) {
            alert("Todos los campos son obligatorios.");
            return;
        }
        try {
            const res = await fetch('/api/artistas_db/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    nombre,
                    pais,
                    genero_principal,  // CORRECTO: coincidir con tu modelo y base de datos
                    activo,
                    eliminado: !activo
                })
            });
            if (!res.ok) throw new Error(await res.text());
            form.reset();
            cargarArtistas();
        } catch (err) {
            alert("Error agregando artista: " + err.message);
        }
    });

    // --- CONSULTAR POR ID ---
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
                div.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            } else {
                div.innerHTML = "Artista no encontrado";
            }
        } catch {
            div.innerHTML = "Error al consultar por ID";
        }
    });

    // --- BUSCAR POR PAÍS ---
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
                resultadoDiv.innerHTML = `<pre>${JSON.stringify(data[0], null, 2)}</pre>`;
            } else {
                resultadoDiv.innerHTML = "Artista no encontrado para ese país";
            }
        } catch {
            resultadoDiv.innerHTML = "Error al buscar por país";
        }
    });

    // --- CONSULTAR TODOS ---
    document.getElementById('btn-consulta-todos').addEventListener('click', async () => {
        await cargarArtistas();
    });

    async function cargarArtistas() {
        let url = '/api/artistas_db';
        const res = await fetch(url);
        const data = await res.json();
        const tbody = document.querySelector('#tabla-todos-artistas tbody');
        tbody.innerHTML = '';
        if (!data.length) {
            tbody.innerHTML = '<tr><td colspan="4">No hay artistas registrados</td></tr>';
        } else {
            data.forEach(a => {
                const row = `<tr>
                    <td>${a.id}</td>
                    <td>${a.nombre}</td>
                    <td>${a.pais}</td>
                    <td>${a.genero_principal || a.genero || ""}</td>
                </tr>`;
                tbody.innerHTML += row;
            });
        }
    }

    // --- ACTUALIZAR (PUT) ---
    document.getElementById('btn-put-actualizar').addEventListener('click', async () => {
        const id = document.getElementById('put-id').value.trim();
        const nombre = document.getElementById('put-nombre').value.trim();
        const pais = document.getElementById('put-pais').value.trim();
        const genero_principal = document.getElementById('put-genero').value.trim();
        if (!id || !nombre || !pais || !genero_principal) {
            alert("Completa todos los campos para actualizar.");
            return;
        }
        try {
            const res = await fetch(`/api/artistas_db/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: Number(id),
                    nombre,
                    pais,
                    genero_principal  // CORRECTO
                })
            });
            if (!res.ok) throw new Error(await res.text());
            cargarArtistas();
        } catch (err) {
            alert("Error al actualizar artista: " + err.message);
        }
    });

    // --- ACTUALIZAR (PATCH) ---
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

    // --- ELIMINAR (LÓGICO) ---
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

    // --- SPOTIFY ---
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

    // Inicializar tabla al cargar
    cargarArtistas();
});