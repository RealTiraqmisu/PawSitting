from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("", IndexView.as_view(), name="index_page"),
    path("detail/<int:id>/", DetailView.as_view(), name="detail_page"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("sittercentre/", SitterCentreView.as_view(), name="sittercentre"),
    path("sitterregis/", SitterRegistrationView.as_view(), name="sitterregis"),
    path("userbooking/", UserBookingView.as_view(), name="userbooking"),
    path("verifysitter/", VerifySitterView.as_view(), name="verifysitter"),
    path("verifydetail/<int:id>/", VerifyDetailView.as_view(), name="verifydetail"),
    path("bookingdetail/<int:id>/", BookingDetailView.as_view(), name="bookingdetail"),
    path("change-password/", EditPasswordChangeView.as_view(), name="change_password"),
    path("rating/<int:id>", BookingRatingView.as_view(), name="rating"),
    path("signup/", SignupView.as_view(), name="signup"),
]