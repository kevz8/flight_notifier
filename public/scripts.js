async function retrieve() {
    let origin = document.getElementById("origin").value.trim();
    let destination = document.getElementById("destination").value.trim();
    let departDate = document.getElementById("departDate").value.trim(); 
    // let returnDate = document.getElementById("returnDate").value.trim();
    let email = document.getElementById("email").value.trim(); 

    // if (returnDate === '') returnDate = null;

    const data = {origin, destination, departDate, email};

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

async function clear_db() {
    const res = await fetch('/clear', {method: 'POST'});
    const json = await res.json();
    const resultSection = document.getElementById("result");
    resultSection.style.display = "block";
    resultSection.textContent = 'Successfully cleared';
}

async function graph() {
    let origin = document.getElementById("origin").value.trim();
    let destination = document.getElementById("destination").value.trim();
    let departDate = document.getElementById("departDate").value.trim();

    if (!origin || !destination || !departDate) {
        const resultSection = document.getElementById("result");
        resultSection.style.display = "block";
        resultSection.textContent = 'Please fill in missing values';
        return;
    }

    let params = new URLSearchParams({origin, destination, departDate});
    window.open(`/graph?${params.toString()}`, '_blank');
}

window.onload = function() {
    document.getElementById('search').addEventListener('click', retrieve);
    document.getElementById('graph').addEventListener('click', graph);
    document.getElementById('clear').addEventListener('click', clear_db);
};