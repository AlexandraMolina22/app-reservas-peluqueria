document.getElementById('reserva-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const response = await fetch('/reservar', {
        method: 'POST',
        body: formData
    });

    const text = await response.text();
    document.open();
    document.write(text);
    document.close();
});
