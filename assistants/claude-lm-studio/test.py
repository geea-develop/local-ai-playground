from anthropic import Anthropic

client = Anthropic(
    base_url="http://localhost:1234",
    api_key="lmstudio",
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello from LM Studio",
        }
    ],
    # model="ibm/granite-4-micro",
    model="qwen/qwen3.5-9b"
)

print(message.content)
