from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm

class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            n_url = request.GET.get('next', '/blog')
            return redirect(n_url)
        else:
            return render(request, 'login.html', {"form": form})
            


class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('/authen')