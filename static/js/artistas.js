document.getElementById('form-artista').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = {
        nombre: form.nombre.value,
        pais: form.pais.value,
        genero_principal: form.genero_principal.value,
        activo: form.activo.checked
    };

    const res = await fetch('/api/artistas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert('Artista agregado');
        loadArtistas();
        form.reset();
    } else {
        const err = await res.json();
        alert('Error: ' + err.detail);
    }
});

async function loadArtistas() {
    const res = await fetch('/api/artistas');
    const lista = await res.json();
    const tbody = document.querySelector('#tabla-artistas tbody');
    tbody.innerHTML = '';
    lista.forEach(a => {
        const row = `<tr><td>${a.nombre}</td><td>${a.pais}</td><td>${a.genero_principal}</td><td>${a.activo ? 'Sí' : 'No'}</td></tr>`;
        tbody.innerHTML += row;
    });
}

document.addEventListener('DOMContentLoaded', loadArtistas);
