async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    document.getElementById("user-input").value = "";

    try {
        let response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput }),
        });

        let data = await response.json();
        if (data.response) {
            chatBox.innerHTML += `<p><strong>Assistant:</strong> ${data.response}</p>`;
        } else {
            chatBox.innerHTML += `<p><strong>Assistant:</strong> Error: ${data.error}</p>`;
        }
    } catch (error) {
        chatBox.innerHTML += `<p><strong>Assistant:</strong> Failed to fetch response. Check server.</p>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}
