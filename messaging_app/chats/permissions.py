from rest_framework import permissions  

class IsOwner(permissions.BasePermission):
    """
    Allow access only to objects owned by the requesting user.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants in a conversation to view, send,
    update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        """
        - For a Message: check if the requesting user is in the conversation participants.
        - For a Conversation: check if the requesting user is a participant.
        """
        if hasattr(obj, "conversation"):  
            return request.user in obj.conversation.participants.all()
        if hasattr(obj, "participants"):  
            return request.user in obj.participants.all()
        return False