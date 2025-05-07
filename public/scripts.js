async function retrieve() {
    let origin = document.getElementById("origin").value.trim();
    let destination = document.getElementById("destination").value.trim();
    let departDate = document.getElementById("departDate").value.trim(); 
    let returnDate = document.getElementById("returnDate").value.trim();
    let email = document.getElementById("email").value.trim(); 

    if (returnDate === '') returnDate = null;

    const data = {origin, destination, departDate, returnDate, email};

    const resultSection = document.getElementById("result");
    resultSection.style.display = "block";
    resultSection.textContent = 'Searching...';

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const responseData = await response.json();

        resultSection.textContent = `Cheapest: ${responseData.cheapest}`;
    } catch (err) {
        console.error(err);
    }
}

window.onload = function() {
    document.getElementById('search').addEventListener('click', retrieve);
};