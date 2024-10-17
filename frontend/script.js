fetch("http://localhost:8080/")
    .then(response => response.json())
    .then(data => {
        document.getElementById("api-message").textContent = data.message;
    })
    .catch(err => console.error("Error fetching API data:", err));

