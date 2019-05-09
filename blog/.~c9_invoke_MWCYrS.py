# -*- coding: utf-8 -*-
try:
    from django.utils import simplejson as json
except ImportError:
    import json
    
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Request
from .forms import PostForm, RequestForm,SignupForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
#from django.contrib.auth.decorations import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string
    if request.method=="POST":
from .tokens import account_activation_token

from django.core.mail import EmailMessage
from django.http import HttpResponse

from django.views.decorators.http import require_POST
# Create your views here.
def home(request):
    posts = Post.objects.all
    return render(request, 'main.html', {'posts':posts})
    
def apply(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            category = request.POST.getlist('category')
            post.save()
            return redirect('main')
    else :
        form=PostForm()
    return render(request, 'class_apply.html', {'form':form})

#@login_required
#@require_POST
def request(request):
    posts = Request.objects.all
    if request.method=="POST":
        form = RequestForm(request.POST)
#        user = request.user #get logined user
#        memo_id = request.POST.get('pk', None)
#        memo = Request.objects.get(pk=memo_id) #get that object
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            category = request.POST.getlist('category')
            post.save()
            return redirect('request')
    else :
        form=RequestForm()
    return render(request,'class_request.html', {'form':form, 'posts':posts})
    
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('이제 로그인 하실 수 있습니다~~.')
    else:
        return HttpResponse('Activation link is invalid!')