from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Message


@login_required
@require_POST
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')


@login_required
def threaded_messages(request):
    top_messages = (
        Message.objects.filter(sender=request.user, parent_message__isnull=True)
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
    )

    return {"messages": [msg.get_thread() for msg in top_messages]}
