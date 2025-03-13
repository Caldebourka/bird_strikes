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

firebase.initializeApp(firebaseConfig);
const dbcon = firebase.database().ref('/GraphingInfo/');

function displayChart() {
    let graph = document.getElementById("gph").value;
    let chart = document.getElementById("chart");
    let svgchart = document.getElementById("svgchart");
    let BirdInputBox = document.getElementById("bird_input-box");
    let CostInputBox = document.getElementById("cost_input-box");
    let graphBox = document.getElementById("graphBox");

    chart.style.display = "none";
    svgchart.style.display = "none";
    BirdInputBox.style.display = "none";
    CostInputBox.style.display = "none";
    if (graphBox) graphBox.style.display = "none";

    switch (graph) {
        case "choice":
            break;
        case "1":
            fetch("https://your-flask-backend.com/check_updates") // Update with correct Flask URL
                .then(response => response.json())
                .then(() => {
                    chart.style.display = "block";
                    chart.src = "static/graph.png?t=" + new Date().getTime(); // Force refresh
                    BirdInputBox.style.display = "block";
                    if (graphBox) graphBox.style.display = "block";
                })
                .catch(error => console.error("Error updating graph:", error));
            break;
        case "2":
            svgchart.style.display = "block";
            svgchart.src = "Number of Strikes in Each State.svg?t=" + new Date().getTime();
            break;
        case "3":
            svgchart.style.display = "block";
            svgchart.src = "Expensive_Strikes.svg";
            CostInputBox.style.display = "block";
            break;
    }
}

document.getElementById("bird_n_btn").addEventListener("click", function() {
    let n = document.getElementById("bird_n").value;
    if (!/^\d+$/.test(n)) {
        alert("Please enter a valid integer for n.");
        return;
    }
    document.getElementById("bird_n").value = "";

    let fb_data = dbcon.child("birds").push();
    fb_data.set({ n: n }).then(() => {
        console.log("Data sent to Firebase:", n);
        setTimeout(displayChart, 1500);
    });
});

