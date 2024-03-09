from chat.models import Message
from django.conf import settings
from openai import OpenAI



def get_llm_response(query, conver_id):

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
            ]
    )
    return response.choices[0].message.content


def test(query, conver_id): 
    from langchain import OpenAI as o, ConversationChain

    llm = o(temperature=0, openai_api_key=settings.OPENAI_API_KEY,
                model_name="gpt-3.5-turbo")
    conversation = ConversationChain(
        llm=llm,
        verbose=True,
    )
    output = conversation.predict(input="Who is the prime Minister of Pakistan?")
    return output
