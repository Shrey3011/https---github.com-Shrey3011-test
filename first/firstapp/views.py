from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# from .forms import CreateUserForm
from django.contrib import messages
# Create your views here.

def  index(request):
    return render(request,'index.html')

def about(request):
    text=(request.GET.get('text','defalut'))
    remove_punc=request.GET.get('remove_punc','off')
    capi=request.GET.get('capi','off')

    ans=""
    if remove_punc!='off' and capi!='off':
        for ch in text:
            if ch!=';':
                ans=ans + ch.upper()
        
        params= {'purpose':'remove_punc and capi','analysed':ans}
        return render(request,'analyse.html',params)
   
    elif remove_punc!='off':
        for ch in text:
            if ch!=';':
                ans=ans + ch
        
        params= {'purpose':'remove_punc','analysed':ans}
        return render(request,'analyse.html',params)
    
    elif capi!='off':
        for ch in text:
                ans=ans + ch.upper()
        
        params= {'purpose':'capi','analysed':ans}
        return render(request,'analyse.html',params)
    
    else:
        return HttpResponse('Error')