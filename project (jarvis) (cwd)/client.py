import openai

# Set your OpenAI API key
openai.api_key = "<enter your key>"

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
