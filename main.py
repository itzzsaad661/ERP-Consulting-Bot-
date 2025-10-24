import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model = "meta/Llama-4-Scout-17B-16E-Instruct"

token = os.getenv("GITHUB_TOKEN")

if not token:
    print("ERROR: GITHUB_TOKEN not found. Please set it before running this script.")
    exit(1)

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

system_prompt = """
You are an AI ERP Consultant Assistant.
Your role is to guide businesses on ERP (Enterprise Resource Planning) systems.
Explain ERP modules, implementation strategies, customization, integration with CRMs,
and provide advice on how ERP improves operational efficiency.
Always respond professionally and clearly.
"""

print("AI Consulting Bot is now active \nAsk about ERP (type 'exit' to quit)\n")

while True:
    user_input = input("What do you want to know about ERP? ")

    if user_input.strip().lower() in ["exit", "quit"]:
        print("Bot:Byee")
        break

    try:
        response = client.complete(
            messages=[
                SystemMessage(system_prompt),
                UserMessage(user_input),
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024,
            model=model
        )

        bot_reply = response.choices[0].message.content
        print(f"Bot: {bot_reply}\n")

    except Exception as e:
        print(f"Error communicating with API: {e}\n")
