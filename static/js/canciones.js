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

    const res = await fetch('/api/canciones', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert('Canción agregada');
        loadCanciones();
        form.reset();
    } else {
        const err = await res.json();
        alert('Error: ' + err.detail);
    }
});

async function loadCanciones() {
    const res = await fetch('/api/canciones');
    const lista = await res.json();
    const tbody = document.querySelector('#tabla-canciones tbody');
    tbody.innerHTML = '';
    lista.forEach(c => {
        const row = `<tr><td>${c.titulo}</td><td>${c.genero}</td><td>${c.duracion}</td><td>${c.artista}</td><td>${c.explicita ? 'Sí' : 'No'}</td></tr>`;
        tbody.innerHTML += row;
    });
}

document.addEventListener('DOMContentLoaded', loadCanciones);