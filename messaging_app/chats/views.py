from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']
    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expecting `participants` as a list of user IDs in request.data.
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "Participants must be provided as a list of user IDs."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)

        conversation.participants.add(request.user)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages in a conversation.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']

    def create(self, request, *args, **kwargs):
        """
        Send a message in a conversation.
        Expecting `conversation` (UUID) and `message_body` in request.data.
        """
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body", "").strip()

        if not conversation_id:
            return Response({"error": "Conversation ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        if not message_body:
            return Response({"error": "Message body cannot be empty."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
