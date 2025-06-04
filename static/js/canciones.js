document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-cancion');
    const btnConsultaId = document.getElementById('btn-consulta-id');
    const btnConsultaTodos = document.getElementById('btn-consulta-todos');
    const spotifyBtn = document.getElementById('spotify-cancion-btn');


    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                titulo: form.titulo.value,
                genero: form.genero.value,
                duracion: parseFloat(form.duracion.value),
                artista: form.artista.value,
                explicita: form.explicita.checked,
                eliminado: false
            };
            try {
                const res = await fetch('/api/canciones_db', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (!res.ok) throw new Error('Error al agregar');
                alert('Canción agregada');
            } catch (err) {
                alert('Error al enviar la canción');
            }
        });
    }

    if (btnConsultaId) {
        btnConsultaId.addEventListener('click', async () => {
            const id = document.getElementById('consulta-id').value;
            try {
                const res = await fetch(`/api/canciones_db/${id}`);
                if (!res.ok) throw new Error('No encontrado');
                const data = await res.json();
                document.getElementById('resultado-consulta-id').innerText = `Título: ${data.titulo}, Género: ${data.genero}, Artista: ${data.artista}`;
            } catch (err) {
                alert('Error al consultar la canción');
            }
        });
    }
document.getElementById('btn-put-actualizar').addEventListener('click', async () => {
    const id = document.getElementById('put-id').value;
    const titulo = document.getElementById('put-titulo').value;
    const genero = document.getElementById('put-genero').value;
    const duracion = document.getElementById('put-duracion').value;
    const artista = document.getElementById('put-artista').value;

    if (!id || !titulo || !genero || !duracion || !artista) {
        alert("Todos los campos son obligatorios");
        return;
    }

    const data = {
        titulo: titulo,
        genero: genero,
        duracion: parseFloat(duracion),
        artista: artista
    };

    try {
        const res = await fetch(`/api/canciones_db/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!res.ok) {
            const error = await res.json();
            alert(`Error: ${error.detail}`);
        } else {
            alert('Canción actualizada completamente');
        }
    } catch (error) {
        console.error("Error en PUT:", error);
        alert("Ocurrió un error al actualizar");
    }
});
    if (btnConsultaTodos) {
        btnConsultaTodos.addEventListener('click', async () => {
            try {
                const res = await fetch('/api/canciones_db');
                if (!res.ok) throw new Error('Error en la petición');
                const data = await res.json();
                const tbody = document.querySelector('#tabla-todos-canciones tbody');
                tbody.innerHTML = '';
                if (!data.length) return tbody.innerHTML = '<tr><td colspan="5">Sin resultados</td></tr>';
                data.forEach(c => {
                    const row = `<tr><td>${c.id}</td><td>${c.titulo}</td><td>${c.genero}</td><td>${c.duracion}</td><td>${c.artista}</td></tr>`;
                    tbody.innerHTML += row;
                });
            } catch (err) {
                alert('Error al mostrar canciones');
            }
        });
    }
document.getElementById('btn-consulta-genero').addEventListener('click', async () => {
    const genero = document.getElementById('consulta-genero').value;
    const res = await fetch(`/api/canciones_db/genero/${encodeURIComponent(genero)}`);
    const data = await res.json();
    const tbody = document.querySelector('#tabla-genero-canciones tbody');
    tbody.innerHTML = '';
    data.forEach(c => {
        const row = `<tr><td>${c.id}</td><td>${c.titulo}</td><td>${c.genero}</td><td>${c.duracion}</td><td>${c.artista}</td></tr>`;
        tbody.innerHTML += row;
    });
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
});