async function loadLocations() {
    const response = await fetch('/get_location_names');
    const data = await response.json();
    const dropdown = document.getElementById('uiLocation');
    
    data.locations.forEach(loc => {
        let opt = document.createElement('option');
        opt.value = loc;
        opt.innerHTML = loc;
        dropdown.appendChild(opt);
    });
}

async function predictPrice() {
    const loc = document.getElementById('uiLocation').value;
    const sqft = document.getElementById('uiSqft').value;
    const bhk = document.getElementById('uiBHK').value;
    const bath = document.getElementById('uiBath').value;

    if(!loc || !sqft) {
        alert("Please fill in the location and area!");
        return;
    }

    const response = await fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            location: loc,
            total_sqft: parseFloat(sqft),
            bath: parseInt(bath),
            bhk: parseInt(bhk)
        })
    });

    const data = await response.json();
    const resultDiv = document.getElementById('result-container');
    document.getElementById('uiEstimatedPrice').innerText = `₹ ${data.estimated_price} Lakhs`;
    resultDiv.classList.remove('hidden');
}

window.onload = loadLocations;