async function loadLocations() {
    try {
        const response = await fetch('/get_location_names');
        const data = await response.json();
        const dropdown = document.getElementById('uiLocation');
        data.locations.forEach(loc => {
            let opt = document.createElement('option');
            opt.value = loc;
            opt.innerHTML = loc;
            dropdown.appendChild(opt);
        });
    } catch (e) { console.error("Could not load locations"); }
}

async function predictPrice() {
    const loc = document.getElementById('uiLocation').value;
    const sqft = document.getElementById('uiSqft').value;
    const bhk = document.getElementById('uiBHK').value;
    const bath = document.getElementById('uiBath').value;

    if(!loc || !sqft) {
        alert("Please enter location and area!");
        return;
    }

    // Show loading state on button
    const btn = document.querySelector('.predict-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span>Processing...</span>';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                location: loc, total_sqft: parseFloat(sqft),
                bath: parseInt(bath), bhk: parseInt(bhk)
            })
        });

        const data = await response.json();
        document.getElementById('uiEstimatedPrice').innerText = `₹ ${data.estimated_price} Lakhs`;
        
        // REVEAL RESULT
        document.getElementById('result-container').classList.remove('hidden');
    } catch (e) {
        alert("Server Error");
    } finally {
        btn.innerHTML = originalText;
    }
}

// Copy Functionality
document.getElementById('copyIcon').addEventListener('click', function() {
    const price = document.getElementById('uiEstimatedPrice').innerText;
    navigator.clipboard.writeText(price).then(() => {
        this.style.color = '#2ecc71';
        setTimeout(() => this.style.color = '', 2000);
    });
});

window.onload = loadLocations;