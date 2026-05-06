// TEMP CHAT (NO STORAGE)
const chatBox = document.getElementById("chat-box");

/* -----------------------------
   ADD MESSAGE
------------------------------ */
function addMessage(text, sender) {
    const message = document.createElement("div");
    message.classList.add("message", sender);
    message.innerText = text;

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* -----------------------------
   SEND MESSAGE
------------------------------ */
async function sendMessage() {
    const input = document.getElementById("user-input");
    const query = input.value.trim();

    if (!query) return;

    addMessage(query, "user");
    input.value = "";

    const typingMsg = document.createElement("div");
    typingMsg.classList.add("message", "bot");
    typingMsg.innerText = "Typing...";
    chatBox.appendChild(typingMsg);

    try {
        const response = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        typingMsg.innerText = data.answer;

    } catch (error) {
        typingMsg.innerText = "❌ Error connecting to server";
    }
}

/* -----------------------------
   ENTER KEY
------------------------------ */
document.getElementById("user-input")
.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});

/* -----------------------------
   PDF UPLOAD
------------------------------ */
document.getElementById("pdf-upload").addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    const uploadMsg = document.createElement("div");
    uploadMsg.classList.add("message", "bot");
    uploadMsg.innerText = "Uploading PDF...";
    chatBox.appendChild(uploadMsg);

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        uploadMsg.innerText = "📄 " + file.name + " uploaded";

    } catch (error) {
        uploadMsg.innerText = "❌ Upload failed";
    }

    this.value = "";
});

/* -----------------------------
   MENU
------------------------------ */
function toggleMenu() {
    const menu = document.getElementById("upload-menu");
    menu.style.display = menu.style.display === "flex" ? "none" : "flex";
}

function selectPDF() {
    document.getElementById("pdf-upload").click();
    document.getElementById("upload-menu").style.display = "none";
}

function selectImage() {
    alert("Image upload coming soon 🚀");
}