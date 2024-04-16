from django.urls import path
from .views import LoginView, DashboardView, RegisterView, PasswordResetView
from .views import book_ticket,future_events,past_events,donation_history,logout_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('book/', book_ticket, name='book_ticket'),
    path('logout/', logout_view, name='logout'),
    path('future-events/', future_events, name='future_events'),
    path('past-events/', past_events, name='past_events'),
    path('donation-history/', donation_history, name='donation_history'),
]
