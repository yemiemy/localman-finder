from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from blog.models import Post
from finder.models import Place

# Create your views here.
@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'user.html', {'p_form':p_form, 'u_form':u_form})

@login_required
def dashboard(request):
    places = Place.objects.filter(author=request.user)
    place_count = 0
    for place in places:
        place_count = place_count + 1
    
    posts = Post.objects.filter(author=request.user)
    post_count = 0
    for post in posts:
        post_count = post_count + 1

    context = {
        'place_count':place_count,
        'post_count':post_count
    }
    return render(request, 'dashboard.html', context)

