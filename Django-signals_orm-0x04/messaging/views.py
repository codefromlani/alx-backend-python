from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.shortcuts import redirect

from .models import Message

@login_required
@require_POST
def delete_user(request):
    user = request.user
    logout(request)         # log out first so session is gone
    user.delete()           # triggers pre_delete/post_delete signals
    return redirect('home') 

top_messages = (
    Message.objects.filter(parent_message__isnull=True)   # only top-level messages
    .select_related("sender", "receiver")                 # avoids extra queries for users
    .prefetch_related("replies__sender", "replies__receiver")  # prefetch nested replies
)