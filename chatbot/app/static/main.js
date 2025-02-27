document.addEventListener('DOMContentLoaded', () => {
  const chatBox = document.getElementById('chat-box');
  const form = document.getElementById('chat-form');
  const promptInput = document.getElementById('prompt');
  const submitBtn = document.getElementById('submit-btn');

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
      // Ở đây, ví dụ chúng ta gửi 5 cặp cuối nếu cần.
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
        body: JSON.stringify({
          prompt: prompt,
          history: pairs
        })
      });
      
      if (!response.ok) throw new Error(`HTTP error! ${response.status}`);
      const data = await response.json();

      // Hiển thị phản hồi của chatbot
      addMessage(data.response || data.error, 'bot');

      // Cập nhật chatHistory
      chatHistory.push(
        { role: 'user', content: prompt },
        { role: 'bot', content: data.response }
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

  // Hàm thêm tin nhắn vào chat box (sử dụng marked để parse markdown)
  function addMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.innerHTML = marked.parse(content);
    chatBox.appendChild(messageDiv);
    scrollToBottom();
  }

  // Hàm tự động cuộn chat box xuống cuối
  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
