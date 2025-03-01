async function askAI() {
    let city = document.getElementById("city").value;
    let question = document.getElementById("question").value;

    if (!question.trim()) {
        alert("Please enter a question!");
        return;
    }

    let responseDiv = document.getElementById("response");
    responseDiv.innerHTML = "<b>Fetching response...</b> ⏳";

    let formData = new FormData();
    formData.append("city", city);
    formData.append("question", question);

    let response = await fetch('/ask', {
        method: 'POST',
        body: formData
    });

    let data = await response.json();
    responseDiv.innerHTML = `<b>${city}:</b> ${data.answer}`;
}

async function showTrending() {
    let city = document.getElementById("city").value;

    let response = await fetch('/trending', {
        method: 'POST',
        body: new FormData(document.querySelector("form"))
    });

    let data = await response.json();
    document.getElementById("response").innerHTML = `<b>Top 5 Places in ${city}:</b> ${data.top_places.join(", ")}`;
}
