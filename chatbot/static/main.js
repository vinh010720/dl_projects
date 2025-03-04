document.addEventListener('DOMContentLoaded', () => {
  const chatBox = document.getElementById('chat-box');
  const form = document.getElementById('chat-form');
  const promptInput = document.getElementById('prompt');
  const submitBtn = document.getElementById('submit-btn');

  // Các phần tử cho chức năng ghi âm
  const recordBtn = document.getElementById('record-btn');
  const recordStatus = document.getElementById('record-status');

  // Sử dụng marked với tùy chọn breaks để hỗ trợ xuống dòng
  marked.setOptions({ breaks: true });

  // Khôi phục lịch sử chat từ localStorage (lưu dưới dạng mảng các đối tượng {role, content})
  let chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
  chatHistory.forEach(msg => addMessage(msg.content, msg.role));

  // Tự động điều chỉnh chiều cao textarea theo nội dung
  promptInput.addEventListener('input', () => {
    promptInput.style.height = 'auto';
    promptInput.style.height = `${promptInput.scrollHeight}px`;
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    // Hiển thị tin nhắn của người dùng
    addMessage(prompt, 'user');

    // Hiển thị loader trong nút gửi
    submitBtn.innerHTML = '<div class="loader"></div>';

    try {
      // Chuyển đổi chatHistory thành danh sách các cặp [user, bot] (nếu backend yêu cầu)
      let pairs = [];
      for (let i = 0; i < chatHistory.length; i += 2) {
        if (i + 1 < chatHistory.length) {
          pairs.push([chatHistory[i].content, chatHistory[i + 1].content]);
        }
      }
      pairs = pairs.slice(-5);

      // Gửi request đến endpoint /chat
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // Lưu ý: trường "prompt" vì backend dùng alias để map sang "text"
        body: JSON.stringify({
          prompt: prompt,
          history: pairs
        })
      });
      
      if (!response.ok) throw new Error(`HTTP error! ${response.status}`);
      const data = await response.json();
      console.log("Response data:", data);
      
      // Hiển thị phản hồi của chatbot từ data.data.response
      addMessage(data.data.response || data.error || "", 'bot');

      // Cập nhật chatHistory
      chatHistory.push(
        { role: 'user', content: prompt },
        { role: 'bot', content: data.data.response }
      );
      localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
      
    } catch (error) {
      addMessage(`Lỗi: ${error.message}`, 'error');
    } finally {
      // Reset input, nút gửi và cuộn chat xuống cuối
      promptInput.value = '';
      promptInput.style.height = 'auto';
      submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Gửi';
      scrollToBottom();
    }
  });

  function addMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    // Ép kiểu content thành chuỗi, nếu content là undefined hoặc null thì trở thành chuỗi rỗng
    const safeContent = String(content || "");
    messageDiv.innerHTML = marked.parse(safeContent);
    chatBox.appendChild(messageDiv);
    scrollToBottom();
  }
  
  // Hàm tự động cuộn chat box xuống cuối
  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // ======= PHẦN GHI ÂM MICROPHONE =======
  let mediaRecorder;
  let audioChunks = [];

  recordBtn.addEventListener('click', async () => {
    // Nếu đang ghi âm, thì dừng ghi và xử lý audio
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      recordBtn.textContent = "Start Recording";
    } else {
      // Bắt đầu ghi âm
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        recordBtn.textContent = "Stop Recording";
        recordStatus.textContent = "Recording...";
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
          recordStatus.textContent = "Processing audio...";
          const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
          
          // Gửi audioBlob đến endpoint /speaking/evaluate
          const formData = new FormData();
          formData.append("audio", audioBlob, "recording.webm");
          // Bạn có thể đặt thêm trường language nếu cần, ví dụ: "en" hoặc "vi"
          formData.append("language", "en");

          fetch('/speaking/evaluate', {
            method: 'POST',
            body: formData
          })
          .then(response => response.json())
          .then(data => {
            console.log("Speech evaluation response:", data);
            // Hiển thị kết quả đánh giá của speech endpoint
            if (data.status === "success" && data.data) {
              addMessage(`Speech Evaluation:\nTranscript: ${data.data.transcript}\nPronunciation: ${data.data.pronunciation}\nFluency: ${data.data.fluency}\nGrammar: ${data.data.grammar}\nFeedback: ${data.data.feedback.join(', ')}`, 'bot');
            } else {
              addMessage(`Speech evaluation error: ${data.error || "Unknown error"}`, 'error');
            }
            recordStatus.textContent = "Idle";
          })
          .catch(error => {
            console.error("Error evaluating speech:", error);
            addMessage(`Error evaluating speech: ${error.message}`, 'error');
            recordStatus.textContent = "Idle";
          });
        });
      } catch (err) {
        console.error("Error accessing microphone:", err);
        recordStatus.textContent = "Error accessing microphone";
      }
    }
  });
});
