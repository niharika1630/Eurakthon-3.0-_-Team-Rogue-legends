let isPaused = false;

function startSimulation() {
    setInterval(() => {
        if (!isPaused) {
            fetchTransaction();
        }
    }, 3000);
}

function fetchTransaction() {

    fetch("/generate")
    .then(res => res.json())
    .then(data => {

        document.getElementById("total").innerText = data.stats.total;
        document.getElementById("flagged").innerText = data.stats.flagged;
        document.getElementById("blocked").innerText = data.stats.blocked;

        document.getElementById("transactionBox").innerHTML =
            `<strong>Sender:</strong> ${data.transaction.sender}<br>
             <strong>Receiver:</strong> ${data.transaction.receiver}<br>
             <strong>Amount:</strong> ₹${data.transaction.amount}<br>
             <strong>Location:</strong> ${data.transaction.location}<br>
             <strong>Time:</strong> ${data.transaction.hour}:00`;

        let colorClass = "green";
        if (data.risk === "Medium") colorClass = "orange";
        if (data.risk === "High") colorClass = "red";

        let reasons = data.reasons.join("<br>");

        if (data.risk === "High") {

            isPaused = true;
            document.getElementById("alertSound").play();

            document.getElementById("riskBox").classList.add("high-risk");

            document.getElementById("riskBox").innerHTML =
                `<h3 class="red">🚨 HIGH RISK - TRANSACTION PAUSED</h3>
                 Risk Score: ${data.risk_score}<br>
                 Rule Score: ${data.rule_score}<br>
                 ML Score: ${data.ml_score}<br><br>
                 <strong>Reasons:</strong><br>${reasons}
                 <br><br>
                 <button class="approve" onclick="approve()">Approve</button>
                 <button class="block" onclick="block()">Block</button>`;
        } else {

            document.getElementById("riskBox").classList.remove("high-risk");

            document.getElementById("riskBox").innerHTML =
                `<h3 class="${colorClass}">${data.risk} Risk</h3>
                 Risk Score: ${data.risk_score}<br>
                 Rule Score: ${data.rule_score}<br>
                 ML Score: ${data.ml_score}<br><br>
                 <strong>Reasons:</strong><br>${reasons}`;
        }

        addToHistory(data);
    });
}

function approve() {
    isPaused = false;
    document.getElementById("riskBox").classList.remove("high-risk");
}

function block() {
    isPaused = false;
    document.getElementById("riskBox").classList.remove("high-risk");
}

function addToHistory(data) {

    let table = document.getElementById("historyTable");
    let row = table.insertRow(1);

    row.insertCell(0).innerText = data.transaction.sender;
    row.insertCell(1).innerText = data.transaction.receiver;
    row.insertCell(2).innerText = "₹" + data.transaction.amount;

    let riskCell = row.insertCell(3);
    riskCell.innerText = data.risk;

    if (data.risk === "Low") riskCell.style.color = "#00ff88";
    if (data.risk === "Medium") riskCell.style.color = "orange";
    if (data.risk === "High") riskCell.style.color = "red";
}

window.onload = startSimulation;