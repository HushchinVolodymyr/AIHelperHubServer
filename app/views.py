import json

from aiohttp import web
from openai.types.beta import Assistant

from AI import AIHelperHub
from DTOs.messageDto import MessageDto


def find_assistant_by_id(chatExample, chatAssitants):
   for assistant in chatAssitants:
      if assistant['id'] == chatExample['id']:
         return assistant


async def index(request):
   try:
      data = await request.json()

      chatExample = data.get("chatExample")
      chatHistory = data.get("chatHistory")

      with open('config.json', 'r') as f:
         config = json.load(f)

      chatAssistants = config["AI"]["assistants"]

      assistantCfg = find_assistant_by_id(chatExample, chatAssistants)

      assistant = AIHelperHub(api_key=config['AI']['apiKey'], organization_key=config['AI']['organizationKey'],
                              chat_history=chatHistory, assistant=assistantCfg)

      message = assistant.generate_response()

      messageDto = MessageDto(id = chatHistory[-1]['id'] + 1, messageType=False , message=message)

      message_response = json.dumps(messageDto.to_dict())

      return web.json_response({"data" : json.loads(message_response)}, status=200)
   except Exception as e:
      print(f"Error: {e}")
      return web.json_response({"error": "Unable to parse request"}, status=400)

