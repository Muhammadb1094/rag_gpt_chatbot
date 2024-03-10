from chat.models import Message
from django.conf import settings
from langchain import OpenAI, ConversationChain
from langchain.memory import ConversationBufferMemory


# def get_llm_response(query, conver_id):
#     from openai import OpenAI
#     client = OpenAI(api_key=settings.OPENAI_API_KEY)

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": query},
#             ]
#     )
#     return response.choices[0].message.content


def get_llm_response(query, conver_id):
    memory = ConversationBufferMemory()
    try:
        if not conver_id == "" or not conver_id is None:
            memorybuffer = Message.objects.filter(
                conversation_id=conver_id).order_by('-created_at')

            for item in memorybuffer:
                memory.chat_memory.add_user_message(item.query)
                memory.chat_memory.add_ai_message(item.response)
            memory.load_memory_variables({})
    except Exception as e:
        print(e)

    llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        memory=memory,
    )
    output = conversation.predict(input=query)
    return output
