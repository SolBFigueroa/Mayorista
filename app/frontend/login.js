document.getElementById("boton-ingresar").addEventListener("click", async function() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (email === "" || password === "") {
    console.log("completá todos los campos");
    return;
  }
    // armamos los datos para mandar al backend
    const formData = new FormData(); //mi backend espera form-data, por eso usamos FormData y no JSON
    formData.append("username", email);
    formData.append("password", password);

    // mandamos petición
    const response = await fetch("http://127.0.0.1:8000/usuarios/login", {
        method: "POST",
        body: formData
    });

    // convertimos la respuesta a objeto JS, luego podremos acceder a cada campo
    const data = await response.json();

    if (response.ok) { //es true si el backend respondió con exito
        localStorage.setItem("access_token", data.access_token);
        window.location.href = "/dashboard.html";
    } else {
        const errorDiv = document.getElementById("error-msg");
        errorDiv.textContent = data.detail;
        errorDiv.classList.remove("hidden");
    }
});


