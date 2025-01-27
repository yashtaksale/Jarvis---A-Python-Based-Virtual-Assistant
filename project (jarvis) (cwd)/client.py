import openai

# Set your OpenAI API key
openai.api_key = "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"

# Requesting a chat completion
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Cloud."},
        {"role": "user", "content": "What is coding?"}
    ]
)

# Printing the response from the assistant
print(response['choices'][0]['message']['content'])
