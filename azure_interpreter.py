import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# read .env file
load_dotenv()

client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],
    azure_endpoint=os.environ["AZURE_API_BASE"],
    api_version=os.environ["AZURE_API_VERSION"],
)

# Create an assistant
assistant = client.beta.assistants.create(
    name="Math Assist",
    #instructions="You are an AI assistant that can write code to help answer math questions.",
    instructions="あなたは、数学の質問に答えるためのコードを書くことができるAIアシスタントです。",
    tools=[{"type": "code_interpreter"}],
    model=os.environ["AZURE_API_ENGINE"], # You must replace this value with the deployment name for your model.
)

# Create a thread
thread = client.beta.threads.create()

# Add a user question to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    #content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
    content="方程式 `3x + 11 = 14` を解きたいです。助けてくれますか？"
)

# Run the thread and poll for the result

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    #instructions="Please address the user as Jane Doe. The user has a premium account.",
    instructions="Please address the user as shuu san. The user has a premium account.",
    #instructions="ユーザー名を'Jane Doe'としてください。このユーザーはプレミアムアカウントを持っています。",
)

print("Run completed with status: " + run.status)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.to_json(indent=2))