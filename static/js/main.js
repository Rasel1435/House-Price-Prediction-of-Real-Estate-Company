async function loadLocations() {
    try {
        const response = await fetch('/get_location_names');
        const data = await response.json();
        const dropdown = document.getElementById('uiLocation');
        
        // Clear "Select neighborhood..." placeholder if needed or keep it
        data.locations.forEach(loc => {
            let opt = document.createElement('option');
            opt.value = loc;
            opt.innerHTML = loc;
            dropdown.appendChild(opt);
        });
    } catch (error) {
        console.error("Error loading locations:", error);
    }
}

async function predictPrice() {
    const loc = document.getElementById('uiLocation').value;
    const sqft = document.getElementById('uiSqft').value;
    const bhk = document.getElementById('uiBHK').value;
    const bath = document.getElementById('uiBath').value;
    const btn = document.querySelector('.predict-btn');
    const resultDiv = document.getElementById('result-container');

    // Validation with a cleaner UI feel
    if(!loc || !sqft || sqft <= 0) {
        alert("Please provide a valid location and area.");
        return;
    }

    // UI State: Loading
    btn.innerHTML = `<span>Processing...</span> <i class="fas fa-spinner fa-spin"></i>`;
    btn.style.opacity = "0.7";
    btn.style.pointerEvents = "none";

    try {
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
        
        // UI State: Success
        document.getElementById('uiEstimatedPrice').innerText = `₹ ${data.estimated_price} Lakhs`;
        resultDiv.classList.remove('hidden');
        
        // Smooth scroll to result on mobile
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        alert("Prediction failed. Please try again.");
    } finally {
        // Reset Button
        btn.innerHTML = `<span>Calculate Market Value</span> <i class="fas fa-arrow-right"></i>`;
        btn.style.opacity = "1";
        btn.style.pointerEvents = "auto";
    }
}

// Logic for the Copy Icon in your CSS
function copyPrice() {
    const price = document.getElementById('uiEstimatedPrice').innerText;
    navigator.clipboard.writeText(price).then(() => {
        const icon = document.getElementById('copyIcon');
        icon.classList.replace('fa-copy', 'fa-check');
        icon.style.color = "#10b981"; // Success Green
        
        setTimeout(() => {
            icon.classList.replace('fa-check', 'fa-copy');
            icon.style.color = ""; 
        }, 2000);
    });
}

// Event Listeners
window.onload = loadLocations;
// Adding listener for copy icon if it exists
document.getElementById('copyIcon')?.addEventListener('click', copyPrice);
