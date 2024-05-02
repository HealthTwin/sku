# user_management/views.py
import json

import requests
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view

from .forms import *
from django.contrib import messages


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                user.save()
                messages.success(request, "تم التسجيل  بنجاح")
                return redirect('/account/login/')
        else:
            form = UserRegistrationForm()
        return render(request, 'index/signup.html', {'form': form})
    else:
        return redirect('/home/')


def user_login(request):
    if not request.user.is_authenticated:
        login_state = False
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "مرحبا بك ")
                    return redirect('/home/')
                else:
                    login_state = True
        else:
            form = LoginForm()
        return render(request, 'index/sign.html', {'form': form, 'login_state': login_state})
    else:
        return redirect('/home/')


def logout_out(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج")
    return redirect('/')


def reset_password(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                user_email = form.cleaned_data.get('email')
                user = CustomUser.objects.filter(email=user_email).first()
                if user:
                    form.save(request=request)
                    messages.info(request, "تحقق من بريدك لاعادة تعين كلمة السر")
                    return redirect('/')
                else:

                    form = PasswordResetForm()
                    messages.error(request, "المستخدم غير موجود")
                    return render(request, 'index/password_recover.html', {'form': form})
        else:
            form = PasswordResetForm()
        return render(request, 'index/password_recover.html', {'form': form})
    else:
        return redirect('/home/')


def password_reset_confirm(request, uidb64, token):
    if not request.user.is_authenticated:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    u = CustomUser.objects.get(username__exact=user.email)
                    u.set_password(form.cleaned_data['new_password1'])
                    u.save()
                    update_session_auth_hash(request, u)
                    messages.success(request, "تم تغير كلمة السر بنجاح")
                    return redirect('/')
                else:
                    return render(request, 'index/password_reset_confirm_form.html', {'form': form})
            else:
                form = SetPasswordForm(user)
            return render(request, 'index/password_reset_confirm_form.html', {'form': form})
        else:
            messages.error(request, "خطا ما حدث حاول ثانيتا")
        return redirect('/')
    else:
        return redirect('/home/')


def payment(request):
    url = "https://secure.paytabs.sa/payment/request"
    protocol = 'https' if request.is_secure() else 'http'
    headers = {
        "authorization": "SHJN6LZZLW-J6WZMGDBBZ-9ZJTK2W2TG",
        "content-type": "application/json"
    }
    print( request.META['HTTP_HOST']+"/verify_payment/")
    data = {
        "profile_id": 103718,
        "tran_type": "sale",
        "tran_class": "ecom",
        "cart_id": str(request.user.id),
        "cart_description": "Dummy Order 35925502061445345",
        "cart_currency": "SAR",
        "cart_amount": 46.17,
        "callback": protocol+"://"+request.META['HTTP_HOST']+"/account/verify_payment/",
        "return":  protocol+"://"+request.META['HTTP_HOST']
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = json.loads(response.text)
    try:

        redirect_url = response_data['redirect_url']
        return redirect(redirect_url)
    except:
        messages.error(request, response_data['message'])
        return redirect('/')

@api_view(['POST'])
def verify_payment(request):
    if request.method == 'POST':
        callback_data = json.loads(request.body)
        card_id = callback_data['cart_id']
        payment_result = callback_data.get('payment_result', {})
        if payment_result == 'A':
            user = CustomUser.objects.filter(id=int(card_id)).first()
            if user:
                user.subscript = True
                user.save()
                messages.success(request, "تم الدفع")
        # print(callback_data)
    response_data = {'status': 'ok'}
    return JsonResponse(response_data, status=405)
