from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
@require_POST
def delete_user(request):
    user = request.user
    logout(request)         # log out first so session is gone
    user.delete()           # triggers pre_delete/post_delete signals
    return redirect('home') 
