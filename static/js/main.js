document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const userMessageInput = document.getElementById("user-message");
    const sendButton = document.getElementById("send-button");
    const questionButtons = document.querySelectorAll(".question-btn");
    const loadingIndicator = document.getElementById("loading");

    // Smooth scrolling for nav links
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            document.getElementById(targetId).scrollIntoView({ behavior: "smooth" });
        });
    });

    // Event listener for quick question buttons
    questionButtons.forEach(button => {
        button.addEventListener("click", function () {
            userMessageInput.value = this.getAttribute("data-question");
            userMessageInput.focus();
        });
    });

    // Function to send user message
    sendButton.addEventListener("click", async function () {
        const userMessage = userMessageInput.value.trim();
        if (!userMessage) return;

        appendMessage("You", userMessage);
        userMessageInput.value = "";

        try {
            loadingIndicator.style.display = "block"; // Show loading

            const response = await fetch("https://code-crusaders-demo.onrender.com/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            appendMessage("FinWise", data.response);
        } catch (error) {
            appendMessage("FinWise", "⚠️ Oops! Something went wrong. Please try again.");
        } finally {
            loadingIndicator.style.display = "none"; // Hide loading
        }
    });

    // Function to append chat messages
    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", sender === "You" ? "user" : "bot");
        messageElement.innerHTML = `<div class="message-content"><strong>${sender}:</strong> ${message}</div>`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
    }
});
