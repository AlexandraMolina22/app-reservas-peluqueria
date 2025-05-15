window.onload = async function () {
    try {
        const response = await fetch('/api/citas');
        if (!response.ok) throw new Error('Error al cargar citas');
        const citas = await response.json();

        const lista = document.getElementById('lista-citas');
        lista.innerHTML = ''; // limpiar por si acaso

        citas.forEach(cita => {
            const li = document.createElement('li');
            li.textContent = `${cita.nombre_clienta} - ${cita.servicio} - ${cita.fecha} a las ${cita.hora}`;
            lista.appendChild(li);
        });
    } catch (error) {
        alert('No se pudieron cargar las citas');
    }
};
