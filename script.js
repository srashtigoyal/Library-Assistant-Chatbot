const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const typing = document.getElementById("typing");

input.addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

function timeNow() {
  return new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });
}

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;

  const content = sender === "bot"
    ? marked.parse(text)   // Markdown → HTML
    : text;                // User text stays plain

  div.innerHTML = `
    <div class="content">${content}</div>
    <div class="time">${timeNow()}</div>
  `;

  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}



function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";
  typing.style.display = "block";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
  .then(res => res.json())
  .then(data => {
    typing.style.display = "none";
    addMessage(data.reply, "bot");
  });
}
document.getElementById("year").textContent = new Date().getFullYear();

