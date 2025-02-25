from together import Together

def build_messages(prompt: str, history: list) -> list:
    """
    Xây dựng danh sách messages dựa theo:
      - Một message hệ thống
      - Lịch sử hội thoại (danh sách các tuple: (user, bot))
      - Prompt moowis
    """
    messages = [{"role": "system", "content": "You are a helpful assistaint AI"}]
    for user,bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": prompt})
    return messages

def get_chat_response(
    client: Together,
    prompt: str, 
    history: list, 
    model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    max_tokens: str = 1300
) ->str:
    messages = build_messages(prompt, history)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content