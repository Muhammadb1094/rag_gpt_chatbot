import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .llm_gpt import (get_llm, get_openai_qdrant, get_llm_qdrant)



logger = logging.getLogger(__name__)


class ConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        serializer = ConversationSerializer(
            Conversation.objects.filter(user=request.user).order_by('-created_at'),
            many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        conversation_id =  request.data.get('conversation_id', 0)
        conversation = Conversation.objects.filter(id=conversation_id, user=request.user).first()
        
        if conversation is None:
            return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ConversationSerializer(conversation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        conversation_id =  request.data.get('conversation_id', 0)
        conversation = Conversation.objects.filter(id=conversation_id, user=request.user).first()

        if conversation is None:
            return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        conversation_id =  request.data.get('conversation_id', 0)
        conversation = Conversation.objects.filter(id=conversation_id, user=request.user).first()
        
        if conversation is None:
            return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        prompt = request.data.get("prompt")
        response = get_llm_qdrant(prompt, conversation_id)
        # response = get_openai_qdrant(prompt, conversation_id)
        message = Message(
            conversation=conversation,
            query=prompt,
            response=response
        )
        message.save()
        
        # Saving the last message to get conversations more faster
        conversation.last_message = response
        conversation.save()
        logger.info(f"Answer from GPT for prompt '{prompt}' Asked By User {request.user}  is {response}")
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        conversation_id =  request.query_params.get('conversation_id', 0)
        conversation = Conversation.objects.filter(id=conversation_id, user=request.user).first()
        
        if conversation is None:
            return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        messages = Message.objects.filter(conversation__id=conversation_id)
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    