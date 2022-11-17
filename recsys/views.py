from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import *

def index(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.vote_date = timezone.now()
            user.save()
            return redirect(reverse("recsys:vote", kwargs={'user_id': user.id}))
    
    form=UserProfileForm()
    return render(request, 'recsys/index.html', {'form':form})

def vote(request, user_id):
    if request.method == 'POST':
        user = UserProfile.objects.get(id=user_id)
        like_id_list = request.POST.getlist('movie[]')
        like_list = []
        if like_id_list and len(like_id_list) == 5:
            for like_id in like_id_list:
                movie = MovieInfo.objects.get(id=like_id)
                user_like = UserLike(user=user, movie=movie)
                user_like.save()
                like_list.append(movie)
            # return redirect(reverse("recsys:result", kwargs=context))
            return redirect(reverse("recsys:result", kwargs={'user_id': user_id}))
    choice_list = list(map(
        lambda x: MovieInfo.objects.get(id=x.movie.id), 
        MovieChoice.objects.order_by('order')
    ))
    context = {'choice_list': choice_list}
    return render(request, 'recsys/vote.html', context)

def result(request, user_id):
    like_list = list(set(map(lambda x: x.movie, UserLike.objects.filter(user__id=user_id))))[:5]
    context = {'like_list': like_list}
    return render(request, 'recsys/result.html', context)
