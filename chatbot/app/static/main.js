document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const promptInput = document.getElementById("prompt");
    const historyInput = document.getElementById("history");
    const chatBox = document.getElementById("chat-box");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const prompt = promptInput.value;
        let history = JSON.parse(historyInput.value);

        // Hiển thị câu hỏi của người dùng
        const userMsgDiv = document.createElement("div");
        userMsgDiv.className = "message user";
        userMsgDiv.textContent = "User: " + prompt;
        chatBox.appendChild(userMsgDiv);

        // Gửi request đến endpoint /chat dưới dạng JSON
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt: prompt, history: history })
        });
        const data = await response.json();

        // Hiển thị phản hồi của chatbot
        const botMsgDiv = document.createElement("div");
        botMsgDiv.className = "message bot";
        if (data.response) {
            botMsgDiv.textContent = "Bot: " + data.response;
        } else {
            botMsgDiv.textContent = "Error: " + data.error;
        }
        chatBox.appendChild(botMsgDiv);

        // Cập nhật history
        history.push([prompt, data.response || ""]);
        historyInput.value = JSON.stringify(history);

        // Xóa prompt sau khi gửi
        promptInput.value = "";
    });
});
