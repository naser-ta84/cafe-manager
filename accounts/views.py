from django.shortcuts import render , redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from .forms import UserForm
from .models import OTP,CustomUser
import random

def login_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            otp_code = str(random.randint(100000, 999999))
            print(f"code for {phone_number}: {otp_code}")

            OTP.objects.filter(phone_number=phone_number).delete()
            OTP.objects.create(phone_number=phone_number, code=otp_code)

            request.session['user_phone'] = phone_number

            return redirect('accounts:verify')
        else:
            print(form.errors)
    else:
        form = UserForm()

    return render(request, 'accounts/login.html', {'form': form})

def verify_view(request):
    phone_number = request.session.get('user_phone')

    if not phone_number:
        return redirect('accounts:login')
    if request.method == "POST":
        user_code = request.POST.get('otp_code')

        otp_exists = OTP.objects.filter(phone_number=phone_number,code=user_code).exists()
        if otp_exists:

            user, created = CustomUser.objects.get_or_create(phone_number=phone_number)

            login(request, user)

            OTP.objects.filter(phone_number=phone_number).delete()

            request.session.pop('user_phone', None)

            return redirect('booking:table_list')
        else:
            return render(request, 'accounts/verify.html', {'error': 'کد وارد شده اشتباه است'  })

    return render(request, 'accounts/verify.html')