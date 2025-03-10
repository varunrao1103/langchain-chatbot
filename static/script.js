function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return; // Ignore empty input

    let chatBox = document.getElementById("chat-box");

    let userMessage = document.createElement("div");
    userMessage.classList.add("user-message");
    userMessage.innerText = userInput;
    chatBox.appendChild(userMessage);

    document.getElementById("user-input").value = ""; // Clear input


    fetch("http://127.0.0.1:5000/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: userInput })
        })
        .then(response => response.json())
        .then(data => {
            let botMessage = document.createElement("div");
            botMessage.classList.add("bot-message");

            if (data.error) {
                botMessage.innerText = "Error: " + data.error;
            } else if (data.results.length > 0) {
                botMessage.innerHTML = data.results.map(course =>
                    `📌 <strong>${course.title}</strong><br>
                    ${course.description}<br>
                    💰 <strong>Price:</strong> ${course.price}<br>
                    🔗 <a href="${course.link}" target="_blank">View Course</a>`
                ).join("<br><br>");
            } else {
                botMessage.innerText = "No matching courses found.";
            }

            chatBox.appendChild(botMessage);
            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
        })
        .catch(error => console.error("Error:", error));
}