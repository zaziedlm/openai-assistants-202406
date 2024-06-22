from openai import OpenAI
import os
import time
import langchain
from dotenv import load_dotenv

langchain.verbose = True
langchain.debug = True

# read .env file
load_dotenv()

# Assistants API Knowledge Retrieval

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

# Assistants API 読み込みファイルのディレクトリ指定
target_dir = './data/'

# 読み込みファイルのファイルパス・リストを取得する
file_paths = []
for root, dirs, files in os.walk(target_dir):
    for file in files:
        full_path = os.path.join(root, file)
        file_paths.append(full_path)
print(file_paths)

# # Upload a file with an "assistants" purpose
# # get file_id
# file_ids = []
# for file_path in file_paths:
#     file_name = os.path.basename(file_path)
#     aifile = client.files.create(purpose="assistants", file=open(file_path, "rb"))
#     aifile_id = aifile.id
#     file_ids.append(aifile_id)
# print(aifile_id)

# 読み込みファイルのファイルストリームの作成
file_streams = [open(path, "rb") for path in file_paths]

# 読み込みファイルのVector storeの作成
vector_stores = client.beta.vector_stores.create(
    name="vector_store_rag",
    expires_after={
        "anchor": "last_active_at",
        "days": 1,
    }
)
# Vector storeにファイルをアップロード
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_stores.id,
    files=file_streams,
)

print('upload status:',file_batch.status)
print('upfiles count:',file_batch.file_counts)

# assistant作成
assistant = client.beta.assistants.create(
    name="assistant_test",
    description="test",
    instructions=""" 添付で与えられた情報と自分自身の知識の両方を使用して、質問に答えてください。
もし答えが不十分で役に立たない場合は、回答の最初に「その情報は社内には見当たりませんが、」を加えて、自分自身の知識で質問に答えてください。 """,
    # file_ids=file_ids,
    # model="gpt-4-1106-preview",
    model="gpt-4o",
    tools=[{"type": "file_search"}], # tools=[{"type": "retrieval"}],
)
assistant_id = assistant.id
print(assistant_id)

# assistantの更新
update_status = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_stores.id]}},
)


# thread作成
thread = client.beta.threads.create()
thread_id = thread.id
print(thread_id)

client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content="令和5年2月の有効求人倍率は？",
    #content="日本の総人口は？",
)

run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
)
run_id = run.id
print(run_id)

while run.status != 'completed':
    time.sleep(5)
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    print(run.status)
    

# 出力メッセージの取得
output_messages = client.beta.threads.messages.list(
    thread_id=thread.id
)
# print(output_messages.data) #debug用

for message in reversed(output_messages.data):
    print(message.role, ":", message.content[0].text.value)
            
# # ファイル削除
# for file_id in file_ids:
#     delete_status = client.beta.assistants.files.delete(
#         assistant_id=assistant_id,
#         file_id=file_id,
#     )
#     print(delete_status)
   


