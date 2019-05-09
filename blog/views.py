# -*- coding: utf-8 -*-
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Request, FriendshipRequest
from .forms import PostForm, RequestForm,SignupForm,LoginForm, FriendForm

from django.contrib.auth import authenticate
from django.contrib.auth import login,logout

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template import RequestContext,Context
from django.template.loader import render_to_string, get_template

from .tokens import account_activation_token

from django.core.mail import EmailMessage
from django.http import HttpResponse

from django.views.decorators.http import require_POST
# Create your views here.
def home(request):
    posts = Post.objects.all
    return render(request, 'home.html', {'posts':posts})


def classApply(request):
    posts = Post.objects.all
    if request.method=="POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.tutor_id = request.user
            post.published_date = timezone.now()
            category = request.POST.getlist('category')
            post.save()
            return render(request, 'home.html', {'posts':posts})
    else :
        form=PostForm()
    return render(request, 'class_apply.html', {'form':form})


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
            return redirect('class_request')
    else :
        form=RequestForm()
    return render(request,'class_request.html', {'form':form, 'posts':posts})


def class_detail(request, index):
    post = get_object_or_404(Post, pk=index)
    return render(request, 'class_detail.html',{'post':post})


def class_remove(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if post.tutor_id == request.user.username:
        post.delete()
        return redirect('home')
    else:
        return redirect('home')
    

def class_edit(request, index):
    post=get_object_or_404(Post, pk=index)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('class_detail', post.pk)
    else :
        form=PostForm(instance=post)
    return render(request, 'class_apply.html', {'form':form})
            
    
    
    
    
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
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        # return redirect('home')
        return HttpResponse('이제 로그인 하실 수 있습니다~~.')
    else:
        return HttpResponse('Activation link is invalid!')
        
        
#login
def signin(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            posts = Post.objects.all
            return render(request, 'home.html', {'user':user, 'posts':posts})
            #return redirect('home')
        else :
            return redirect('home')
            
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
        
#def match(request):
    # if request.method=="POST":
    #     form = MatchForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=True)
    #         post.save()
    #         current_site = get_current_site(request)
    #         mail_subject = '당신을 기다려용.'
    #         message = render_to_string('match_email.html', {
    #             'post': post,
    #             'domain': current_site.domain,
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token':account_activation_token.make_token(user),
    #         })
    #         to_email = form.cleaned_data.get('email')
    #         email = EmailMessage(
    #                     mail_subject, message, to=[to_email]
    #         )
    #         email.send()
    #         return redirect('class_detail.html')
    # else :
    #     form=MatchForm()
   
 #   return render(request,'class_detail.html', {'form':form})

def friend_request(request):
    normal_request = FriendshipRequest.objects.filter(to_user=request.user, accepted=False, refused=False)
    choosed = FriendshipRequest.objects.filter(to_user=request.user, accepted=True)
    if request.method=="POST":
        acceptedchk = request.POST.get("accepted")
        fuser = request.POST.get("from_user")
        Relationship = FriendshipRequest.objects.get(to_user=request.user, from_user__pk=fuser)
        if acceptedchk == True:
            Relationship.accepted = True
        else:
            Relationship.refused = True
        Relationship.save()
        return render(request, 'friend_request.html', {'ns': normal_request, 'cs': choosed})  
    return render(request, 'friend_request.html',{'ns': normal_request, 'cs': choosed})

        
        
        
def site_main(request):
    template=get_template('home.html')
    variables = Context({'user':request.user})
    output = template.render(variables)
    return HttpResponse(output)
    
def site_request(request):
    template=get_template('class_request.html')
    variables = Context({'user':request.user})
    output = template.render(variables)
    return HttpResponse(output)

def site_apply(request):
    template=get_template('class_apply.html')
    variables = Context({'user':request.user})
    output = template.render(variables)
    return HttpResponse(output)
    
def site_match(request):
    template=get_template('match_email.html')
    variables = Context({'user':request.user})
    output = template.render(variables)
    return HttpResponse(output)
#def logout_page(request):
#    logout(request)
#    return HttpResponse()