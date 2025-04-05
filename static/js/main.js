document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const userMessageInput = document.getElementById("user-message");
    const sendButton = document.getElementById("send-button");
    const questionButtons = document.querySelectorAll(".question-btn");
    const loadingIndicator = document.getElementById("loading");

    // 1. STRICT CLIENT-SIDE GREETING DETECTION (NEW)
    const GREETINGS = new Set(['hi', 'hello', 'hey', 'hola', 'hey there']);
    
    function isGreeting(message) {
        const cleanMsg = message.trim().toLowerCase();
        return cleanMsg.split(/\s+/).length <= 2 && GREETINGS.has(cleanMsg);
    }

    function displayGreeting() {
        const greetings = [
            "Hi! How can I assist with your finances today?",
            "Hello! What financial topics interest you?",
            "Hey! Ready to discuss your investments?"
        ];
        const randomResponse = greetings[Math.floor(Math.random() * greetings.length)];
        appendMessage("FinWise", randomResponse);
    }

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

    // Modified send message handler
    sendButton.addEventListener("click", async function () {
        const userMessage = userMessageInput.value.trim();
        if (!userMessage) return;

        // 2. INTERCEPT GREETINGS BEFORE SENDING TO SERVER (NEW)
        if (isGreeting(userMessage)) {
            displayGreeting();
            userMessageInput.value = "";
            return;
        }

        appendMessage("You", userMessage);
        userMessageInput.value = "";

        try {
            loadingIndicator.style.display = "block";

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
            loadingIndicator.style.display = "none";
        }
    });

    // Original appendMessage function (unchanged)
    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", sender === "You" ? "user" : "bot");
        messageElement.innerHTML = `<div class="message-content"><strong>${sender}:</strong> ${message}</div>`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
