// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDczW3d0RbphdiXQHzjS8rAQrUGNku0iYc",
    authDomain: "birds-2b89b.firebaseapp.com",
    databaseURL: "https://birds-2b89b-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "birds-2b89b",
    storageBucket: "birds-2b89b.firebasestorage.app",
    messagingSenderId: "179072348631",
    appId: "1:179072348631:web:64e6bc3e5ca763cf98db92",
    measurementId: "G-6NGMSSL7PP"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const dbcon = firebase.database().ref('/userBird/');
let birdStrikesData = [];

// Fetch bird strike data
fetch('bird_strikes.json')
    .then(response => response.json())
    .then(data => {
        birdStrikesData = data;
        console.log("Bird strike data loaded:", birdStrikesData);
        showTable2();
    })
    .catch(error => console.error("Error loading bird strike data:", error));

// Save data to Firebase
document.getElementById("sendToFb").addEventListener("click", saveData);

function saveData() {
    let nameValue = document.getElementById("name").value.trim();
    let breedFieldVal = document.getElementById("breed").value.trim();
    let sizeFieldVal = document.getElementById("size").value.trim();
    let cloudFieldVal = document.getElementById("cloud").value.trim();
    
    let airlines = [];
    for (let i = 1; i <= 5; i++) {
        let checkbox = document.getElementById(`al${i}`);
        if (checkbox && checkbox.checked) {
            airlines.push(checkbox.value);
            checkbox.checked = false;
        }
    }

    if (!nameValue || !breedFieldVal || !sizeFieldVal) {
        alert("Please fill in all required fields.");
        return;
    }

    let data = { Name: nameValue, Breed: breedFieldVal, Size: sizeFieldVal, Airlines: airlines, Clouds: cloudFieldVal };

    dbcon.push(data)
        .then(() => {
            showTable1();
            showTable2();
        })
        .catch(error => console.error("Error saving data: ", error));
}

// Display Table 1 (Firebase Data)
function showTable1() {
    dbcon.once("value", snapshot => {
        const data = snapshot.val();
        console.log("Firebase Data:", data);
        const tbody = document.getElementById("ar2data");
        tbody.innerHTML = "";
        
        if (!data) return;

        for (let key in data) {
            const row = data[key];
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${row.Name || "N/A"}</td><td>${row.Breed || "N/A"}</td><td>${row.Size || "N/A"}</td><td>${Array.isArray(row.Airlines) ? row.Airlines.join(", ") : "None"}</td><td>${row.Clouds || "N/A"}</td>`;
            tbody.appendChild(tr);
        }
    });
}

// Display Table 2 (Recommendations)
function showTable2() {
    if (birdStrikesData.length === 0) {
        console.warn("Bird strike data not loaded yet. Retrying...");
        setTimeout(showTable2, 1000);
        return;
    }

    dbcon.once("value", snapshot => {
        const data = snapshot.val();
        const tbody = document.getElementById("ar3data");
        tbody.innerHTML = "";
        
        if (!data) return;

        for (let key in data) {
            const row = data[key];
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${row.Name || "N/A"}</td><td>${generateRecommendation(row.Breed, row.Size, row.Airlines, row.Clouds)}</td>`;
            tbody.appendChild(tr);
        }
    });
}

// Generate Recommendations
function generateRecommendation(breed, size, airlines, clouds) {
    if (!birdStrikesData.length) return "Data not available";
    if (!breed || typeof breed !== "string") return "Breed not specified.";

    let relevantStrikes = birdStrikesData.filter(entry =>
        entry.WildlifeSpecies && typeof entry.WildlifeSpecies === "string" &&
        entry.WildlifeSpecies.trim().toLowerCase() === breed.trim().toLowerCase()
    );

    console.log("Searching for breed:", breed, "| Matches found:", relevantStrikes.length);

    if (relevantStrikes.length === 0) {
        return `No known risk for ${breed}.`;
    }

    relevantStrikes.sort((a, b) => b.Strikes - a.Strikes);
    let highRiskAirports = relevantStrikes.slice(0, 3).map(entry => entry.AirportName || "Unknown");
    let saferAirports = relevantStrikes.slice(-3).map(entry => entry.AirportName || "Unknown");

    return `Avoid: ${highRiskAirports.join(", ")} | Prefer: ${saferAirports.join(", ")}`;
}

// Run on page load
document.addEventListener("DOMContentLoaded", () => {
    showTable1();
    showTable2();
});



