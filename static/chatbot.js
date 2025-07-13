function sendMessage() {
    const msg = document.getElementById("message").value;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    })
        .then(res => res.json())
        .then(data => {
            const box = document.getElementById("chatbox");
            box.innerHTML += `<p><strong>You:</strong> ${msg}</p>`;
            box.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
            document.getElementById("message").value = '';
        });
}
