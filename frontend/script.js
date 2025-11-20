const BASE_URL = "https://finance-platform-b8b7.onrender.com"; // reemplaza con tu URL de FastAPI

async function fetchCorporate() {
    const response = await fetch(`${BASE_URL}/corporate`);
    const data = await response.json();
    document.getElementById("corporate-output").textContent = JSON.stringify(data, null, 2);
}

async function fetchPersonal() {
    const response = await fetch(`${BASE_URL}/personal`);
    const data = await response.json();
    document.getElementById("personal-output").textContent = JSON.stringify(data, null, 2);
}