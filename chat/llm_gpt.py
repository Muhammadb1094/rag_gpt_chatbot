from chat.models import Message
from django.conf import settings
from langchain import OpenAI, ConversationChain
from langchain.memory import ConversationBufferMemory
import openai as open_ai
from qdrant_client import QdrantClient



def get_final_prompt(query):
        # Get Embeddings
    open_ai.api_key = settings.OPENAI_API_KEY
    response = open_ai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']
    
    # Qdrant Client search
    connection = QdrantClient("localhost", port=6333)
    all_collections = [
                    'HubSpot_Certification_Study_Guide_2014_pro_ent',
                    'hubspot-ebook_river-pools-blogging-case-study',
                    'impromptu-rh',
                    'small-business-social-media-ebook-hubspot'
                ]
    
    search_results = []
    for collection_name in all_collections:
        try:
            result = connection.search(
                collection_name=collection_name,
                query_vector=embeddings,
                limit=3
            )
            search_results.extend(result)
        except Exception as e:
            print(f"Error searching in collection {collection_name}: {e}")
    
    # get final query to pass open_ai
    prompt=""
    for search_result in search_results:
        prompt += search_result.payload["text"]
    
    concatenated_string = f""" This is the previous data or context. \n
            {prompt}
            \n
            Here's the user query from the data or context I have provided. \n
            Question: {query} 
        """

    return concatenated_string


def get_llm(query, conver_id):
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


def get_openai_qdrant(query, conver_id):
    
    prompt = get_final_prompt(query)
    
    completion = open_ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
    return completion.choices[0].message.content


def get_llm_qdrant(query, conver_id):
    memory = ConversationBufferMemory()
    try:
        prompt = get_final_prompt(query)
        memory.chat_memory.add_user_message(prompt)
        memory.load_memory_variables({})
    except Exception as e:
        print(e)
    print(prompt)
    llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        memory=memory,
    )
    output = conversation.predict(input=query)
    return output