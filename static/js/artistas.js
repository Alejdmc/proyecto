document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-artista');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            nombre: form.nombre.value,
            pais: form.pais.value,
            genero_principal: form.genero_principal.value,
            activo: form.activo.checked,
            eliminado: false
        };
        const res = await fetch('/api/artistas_db/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (res.ok) alert('Artista agregado');
        else alert('Error al agregar artista');
    });

    document.getElementById('btn-consulta-id').addEventListener('click', async () => {
        const id = document.getElementById('consulta-id').value;
        const res = await fetch(`/api/artistas_db/${id}`);
        const data = await res.json();
        document.getElementById('resultado-consulta-id').innerText = `Nombre: ${data.nombre}, País: ${data.pais}, Género: ${data.genero_principal}`;
    });

    document.getElementById('btn-consulta-todos').addEventListener('click', async () => {
        const res = await fetch('/api/artistas_db/');
        const data = await res.json();
        const tbody = document.querySelector('#tabla-todos-artistas tbody');
        tbody.innerHTML = '';
        data.forEach(a => {
            const row = `<tr><td>${a.id}</td><td>${a.nombre}</td><td>${a.pais}</td><td>${a.genero_principal}</td></tr>`;
            tbody.innerHTML += row;
        });
    });

    document.getElementById('btn-consulta-pais').addEventListener('click', async () => {
        const pais = document.getElementById('consulta-pais').value;
        const res = await fetch(`/api/artistas_db/pais/${encodeURIComponent(pais)}`);
        const data = await res.json();
        const tbody = document.querySelector('#tabla-pais-artistas tbody');
        tbody.innerHTML = '';
        data.forEach(a => {
            const row = `<tr><td>${a.id}</td><td>${a.nombre}</td><td>${a.pais}</td><td>${a.genero_principal}</td></tr>`;
            tbody.innerHTML += row;
        });
    });

    document.getElementById('btn-put-actualizar').addEventListener('click', async () => {
        const id = document.getElementById('put-id').value;
        const data = {
            nombre: document.getElementById('put-nombre').value,
            pais: document.getElementById('put-pais').value,
            genero_principal: document.getElementById('put-genero').value
        };
        await fetch(`/api/artistas_db/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        alert('Artista actualizado completamente');
    });

    document.getElementById('btn-patch-actualizar').addEventListener('click', async () => {
        const id = document.getElementById('patch-id').value;
        const campo = document.getElementById('patch-campo').value;
        const valor = document.getElementById('patch-valor').value;
        const data = { [campo]: valor };
        await fetch(`/api/artistas_db/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        alert('Artista actualizado parcialmente');
    });

    document.getElementById('btn-eliminar').addEventListener('click', async () => {
        const id = document.getElementById('delete-id').value;
        await fetch(`/api/artistas_db/${id}`, { method: 'DELETE' });
        alert('Artista eliminado');
    });

    document.getElementById('spotify-search-btn').addEventListener('click', async () => {
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
