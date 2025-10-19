from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect
from django.shortcuts import *
from django.views import View
from pawsitting.models import *
from django.db.models import *
from django.db.models.functions import  *
from pawsitting.forms import *
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


    
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        form = UserForm(instance=user)
        return render(request, 'user_profile.html', {
            'form': form
        })
    
    def post(self, request):
        user = request.user
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'user_profile.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class SitterCentreView(View):
    def get(self, request):
        profile = SitterProfile.objects.filter(user=request.user).first()

        if profile:
            booking = Booking.objects.filter(sitter=request.user).prefetch_related('review')

            form = SitterRegistrationForm(instance=profile)
            status = StatusForm(instance=profile)

            if booking:
                return render(request, 'sitter_profile.html', {
                    'booking': booking,
                    'total': booking.count(),
                    'form': form, 
                    'sitter': profile, 
                    'status': status
                })
            
            return render(request, 'sitter_profile.html', {
                'form': form, 
                'sitter': profile
            })
        else:
            return redirect('sitterregis')

    def post(self, request):
        profile = SitterProfile.objects.filter(user=request.user).first()
        form = SitterRegistrationForm(request.POST, request.FILES, instance=profile)
        try:
            with transaction.atomic():
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    form.save_m2m()
                    return redirect('sittercentre')
                raise transaction.TransactionManagementError("Sitter update form invalid")
        except Exception as e:
            print("Error:", e)
            return render(request, "sitter_profile.html", {"form": form})
        
@method_decorator(login_required, name='dispatch')
class SitterRegistrationView(View):
    def post(self, request):
        user = request.user
        form = SitterRegistrationForm(request.POST, request.FILES)
        try:
            with transaction.atomic():
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.user = user
                    profile.save()
                    form.save_m2m()
                    return redirect('sittercentre')
                raise transaction.TransactionManagementError("Sitter Registration form invalid")
        except Exception as e:
            print("Error:", e)
            return render(request, "sitter_registration.html", {"form": form})
    def get(self, request):
        profile = SitterProfile.objects.filter(user=request.user).first()
        if profile:
            return redirect('sittercentre')
        else:
            form = SitterRegistrationForm()
            return render(request, "sitter_registration.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class VerifySitterView(PermissionRequiredMixin, View):
    permission_required = 'pawsitting.delete_sitterprofile'
    def get(self, request):
        search_txt = request.GET.get("search", "")
        filter_type = request.GET.get("filter", "name")

        filters = {}
        if search_txt:
            if filter_type == "name":
                filters["full_name__icontains"] = search_txt
            elif filter_type == "address":
                filters["user__address__icontains"] = search_txt
            elif filter_type == "service":
                filters["service__name__icontains"] = search_txt
            elif filter_type == "rating":
                filters["avg_rating"] = search_txt
            elif filter_type == "verify":
                is_verified_bool = search_txt.lower() in ['true', 'True', 'tru', 't']
                filters["is_verified"] = is_verified_bool

        sitter_list = SitterProfile.objects.annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"), avg_rating=Avg("user__sit__review__rating")).filter(**filters)

        return render(request, "verify_sitter.html", context={
            "total": sitter_list.count(),
            "sitter_list": sitter_list,
            "filter": filter_type,
            "search": search_txt
        })
    
@method_decorator(login_required, name='dispatch')
class VerifyDetailView(PermissionRequiredMixin, View):
    permission_required = 'pawsitting.delete_sitterprofile'
    def get(self, request, id):
        sitter_detail = SitterProfile.objects.annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"), avg_rating=Avg("user__sit__review__rating")).get(id=id)
        form = VerifySitterForm(instance=sitter_detail)
        return render(request, 'verify_detail.html', context={
            'sitter_detail':sitter_detail, "form": form
        })
    def post(self, request, id):
        profile = SitterProfile.objects.filter(id=id).first()
        booking = Booking.objects.filter(sitter=profile.user)
        form = VerifySitterForm(request.POST, instance=profile)
        action = request.POST.get("action")

        if action == "delete":
            profile.delete()
            booking.delete()
            return redirect("verifysitter")
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect('verifysitter')
                raise transaction.TransactionManagementError("Sitter Verification form invalid")
        except Exception as e:
            print("Error:", e)
            return render(request, "verify_detail.html", {"form": form, 'sitter_detail': profile})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('verifysitter')
            return redirect('index_page')
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.is_staff:
                return redirect('verifysitter')
            next_url = request.GET.get('next', 'index_page')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {"form":form})
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index_page')

class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index_page')
        form = EditUserCreationForm()
        return render(request, 'signup.html', {'form':
        form})
    def post(self, request):
        form = EditUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'signup.html', {'form': form})
	
class IndexView(View):
    def get(self, request):
        search_txt = request.GET.get("search", "")
        filter_type = request.GET.get("filter", "name")
        filters = {}
        if search_txt:
            if filter_type == "name":
                filters["full_name__icontains"] = search_txt
            elif filter_type == "service":
                filters["service__name__icontains"] = search_txt
            elif filter_type == "address":
                filters["user__address__icontains"] = search_txt
            elif filter_type == "rating":
                filters["avg_rating"] = search_txt
        sitter_list = SitterProfile.objects.annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"), avg_rating=Avg("user__sit__review__rating")).filter(is_verified=True).filter(**filters)
        return render(request, "find_sitter.html", context={
            "total": sitter_list.count(),
            "sitter_list": sitter_list,
            "filter": filter_type,
            "search": search_txt
        })

@method_decorator(login_required, name='dispatch')
class DetailView(View):
    def get(self, request, id):
        sitter_detail = SitterProfile.objects.annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"), avg_rating=Avg("user__sit__review__rating")).get(id=id)
        form = BookingForm()
        form.fields['service'].queryset = sitter_detail.service.all()
        return render(request, 'booking_process.html', context={
            'sitter_detail':sitter_detail,
            'form': form
        })
    def post(self, request, id):
        sitter_detail = SitterProfile.objects.annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"), avg_rating=Avg("user__sit__review__rating")).get(id=id)
        form = BookingForm(request.POST)
        form.fields['service'].queryset = sitter_detail.service.all()
        if sitter_detail.user != request.user:
            if form.is_valid():
                service = form.cleaned_data['service']
                start = form.cleaned_data['start_date']
                end = form.cleaned_data['end_date']
                total = cal_total(service, start, end)

                booking = form.save(commit=False)
                booking.total = total
                booking.customer = request.user
                booking.sitter = sitter_detail.user
                booking.status = Booking.StatusChoices.PENDING
                booking.save()
                return redirect('userbooking')
            return render(request, 'booking_process.html', {
                'sitter_detail': sitter_detail,
                'form': form})
        else:
            form.add_error(None, 'You can not book your own service.')
            return render(request, 'booking_process.html', {
                'sitter_detail': sitter_detail,
                'form': form})
        
    
@method_decorator(login_required, name='dispatch')
class UserBookingView(View):
    def get(self, request):
        booking = Booking.objects.filter(customer=request.user)
        if booking:
            return render(request, 'user_booking.html', {'booking': booking})
        return render(request, 'user_booking.html')
    

class BookingDetailView(View):
    def get(self, request, id):
        booking = Booking.objects.filter(id=id).first()
        form = StatusForm(instance=booking)
        return render(request, 'booking_detail.html', context={
            'booking':booking, "form": form
        })
    def post(self, request, id):
        booking = Booking.objects.filter(id=id).first()
        form = StatusForm(request.POST, instance=booking)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect('sittercentre')
                raise transaction.TransactionManagementError("Booking Status form invalid")
        except Exception as e:
            print("Error:", e)
            return render(request, "booking_detail.html", {"form": form, 'booking': booking})

@method_decorator(login_required, name='dispatch')
class EditPasswordChangeView(PasswordChangeView):
    template_name = "change_password.html"
    success_url = reverse_lazy('index_page')
    # ไม่ควรใช้ redirect() ใน success_url เพราะ success_url ต้องเป็น URL string หรือ lazy resolver (จะ resolve URL ตอนที่ view ทำงานจริง หรือก็คือ Django จะใช้ตอน runtime) ไม่ใช่ HttpResponseRedirect (response object)

class BookingRatingView(View):
    def get(self, request, id):
        booking = Booking.objects.filter(id=id).first()
        try:
            review = Review.objects.get(booking=booking)
        except Review.DoesNotExist:
            review = Review(booking=booking)
        form = RatingForm(instance=review)
        return render(request, "rating_booking.html", {"form": form, "booking": booking})
    def post(self, request, id):
        booking = Booking.objects.filter(id=id).first()
        try:
            review = Review.objects.get(booking=booking)
        except Review.DoesNotExist:
            review = Review(booking=booking)
        form = RatingForm(request.POST, instance=review)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect('userbooking')
                raise transaction.TransactionManagementError("Rating Booking form invalid")
        except Exception as e:
            print("Error:", e)
            return render(request, "rating_booking.html", {"form": form, 'booking': booking})