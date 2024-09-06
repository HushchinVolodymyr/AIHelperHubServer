import json
import time

from openai import OpenAI


class AIHelperHub:
    def __init__(self, api_key: str, chat_history: list, assistant: list) -> None:
        self.API_KEY = api_key
        self.chat_history = chat_history
        self.client = OpenAI(api_key=self.API_KEY)
        self.assistant = assistant
        self.assistant_id = str(assistant['assistantId'])


    def generate_response(self) -> str:
        run_object = self.client.beta.threads.create_and_run(
            assistant_id=self.assistant_id,
            thread={
                "messages": [
                    {"role": "user", "content": self.chat_history[-1]["message"]},
                ]
            }
        )

        run_result = json.loads(run_object)

        run_id = run_result['id']
        thread_id = run_result['thread_id']

        run_status = run_object.status

        while run_status not in ["completed", "cancelled", "expired", "failed"]:
            run_status = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id).status
            print(f"Run status: {run_status}")
            time.sleep(2)

        thread_messages = self.client.beta.threads.messages.list(thread_id=thread_id)

        data = json.loads(thread_messages.data[0])

        message_response = data['content'][0]['text']['value']

        return message_response

