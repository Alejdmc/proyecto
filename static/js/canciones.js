document.getElementById('form-cancion').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = {
        titulo: form.titulo.value,
        genero: form.genero.value,
        duracion: parseFloat(form.duracion.value),
        artista: form.artista.value,
        explicita: form.explicita.checked
    };

    const res = await fetch('/api/canciones_db', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert('Canción agregada localmente');
        loadCancionesLocal();
        form.reset();
    } else {
        const err = await res.json();
        alert('Error: ' + err.detail);
    }
});

async function loadCancionesLocal() {
    const res = await fetch('/api/canciones_db');
    const lista = await res.json();
    const tbody = document.querySelector('#tabla-canciones tbody');
    tbody.innerHTML = '';
    lista.forEach(c => {
        const row = `<tr><td>${c.titulo}</td><td>${c.genero}</td><td>${c.duracion}</td><td>${c.artista}</td><td>${c.explicita ? 'Sí' : 'No'}</td></tr>`;
        tbody.innerHTML += row;
    });
}

async function searchCancionesSpotify(query) {
    const res = await fetch(`/api/spotify/canciones?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    const tbody = document.querySelector('#tabla-spotify-canciones tbody');
    tbody.innerHTML = '';
    data.tracks.items.forEach(c => {
        const row = `<tr><td>${c.name}</td><td>${c.artists.map(a => a.name).join(', ')}</td><td>${c.album.name}</td></tr>`;
        tbody.innerHTML += row;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadCancionesLocal();
    document.getElementById('spotify-search-btn').addEventListener('click', () => {
        const query = document.getElementById('spotify-query').value;
        searchCancionesSpotify(query);
    });
});