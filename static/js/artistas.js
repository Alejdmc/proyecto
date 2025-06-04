document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-artista');
    const btnConsultaId = document.getElementById('btn-consulta-id');
    const btnConsultaTodos = document.getElementById('btn-consulta-todos');
    const spotifyBtn = document.getElementById('spotify-search-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            nombre: form.nombre.value,
            pais: form.pais.value,
            genero_principal: form.genero_principal.value,
            activo: form.activo.checked,
            eliminado: false
        };
        await fetch('/api/artistas_db', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        alert('Artista agregado');
    });

    btnConsultaId.addEventListener('click', async () => {
        const id = document.getElementById('consulta-id').value;
        const res = await fetch(`/api/artistas_db/${id}`);
        const data = await res.json();
        document.getElementById('resultado-consulta-id').innerText = `Nombre: ${data.nombre}, País: ${data.pais}, Género: ${data.genero_principal}`;
    });

    btnConsultaTodos.addEventListener('click', async () => {
        const res = await fetch('/api/artistas_db');
        const data = await res.json();
        const tbody = document.querySelector('#tabla-todos-artistas tbody');
        tbody.innerHTML = '';
        data.forEach(a => {
            const row = `<tr><td>${a.id}</td><td>${a.nombre}</td><td>${a.pais}</td><td>${a.genero_principal}</td></tr>`;
            tbody.innerHTML += row;
        });
    });

    spotifyBtn.addEventListener('click', async () => {
        const query = document.getElementById('spotify-query').value;
        const res = await fetch(`/api/spotify/artistas?nombre=${encodeURIComponent(query)}`);
        const data = await res.json();
        const tbody = document.querySelector('#tabla-spotify-artistas tbody');
        tbody.innerHTML = '';
        data.forEach(a => {
            const row = `<tr><td>${a.nombre}</td><td>${a.generos.join(', ')}</td><td>${a.popularidad}</td></tr>`;
            tbody.innerHTML += row;
        });
    });
});