import json

from aiohttp import web, request

from AI import AIHelperHub
from DTOs.messageDto import MessageDto


def find_assistant_by_name(chatExample: str, chatAssistants: list):

   for assistant in chatAssistants:
      if assistant['assistantName'] == chatExample:
         return assistant


async def index(request):
   try:
      data = await request.json()

      print(data)

      chatExample = data.get("assistant")
      messageReq = data.get("message")

      print(chatExample)
      print(messageReq)

      with open('config.json', 'r') as f:
         config = json.load(f)

      chatAssistants = config["AI"]["assistants"]

      assistantCfg = find_assistant_by_name(chatExample, chatAssistants)

      print(assistantCfg)

      assistant = AIHelperHub(api_key=config['AI']['apiKey'],

                              message=messageReq, assistant=assistantCfg)

      message = assistant.generate_response()

      messageDto = MessageDto(id = messageReq['id'] + 1, messageType=False , message=message)

      message_response = json.dumps(messageDto.to_dict())

      return web.json_response({"data" : json.loads(message_response)}, status=200)
   except Exception as e:
      print(f"Error: {e}")
      return web.json_response({"error": "Unable to parse request"}, status=400)

