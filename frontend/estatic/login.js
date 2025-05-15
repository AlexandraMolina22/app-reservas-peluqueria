document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const response = await fetch('/login', {
        method: 'POST',
        body: formData
    });

    const text = await response.text();
    if (response.ok) {
        document.open();
        document.write(text);
        document.close();
    } else {
        alert("Credenciales inválidas");
    }
});
