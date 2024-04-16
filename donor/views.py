from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import LoginForm, RegisterForm, PasswordResetForm,BloodDonationForm
from .models import PotentialDonor,County,Constituency,Ward,BloodGroup,DonationCenter,Event,FutureEvent,PastEvent,DonationHistory,DonateBlood
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils import timezone

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            password = form.cleaned_data['password']
            donor = PotentialDonor.objects.filter(email_address=email_address).first()
            if donor and donor.check_password(password):
                # Authentication successful
                request.session['email_address'] = donor.email_address
                return redirect('dashboard')
            else:
                # Authentication failed
                return render(request, self.template_name, {'form': form, 'error': 'Invalid email or password'})
        else:
            return render(request, self.template_name, {'form': form, 'error': 'Invalid email or password'})

class RegisterView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            blood_group_id=form.cleaned_data['blood_group_id']
            email_address = form.cleaned_data['email_address']
            password_hash = form.cleaned_data['password_hash']

            # REQ-1: Check if account already exists
            if PotentialDonor.objects.filter(email_address=email_address).exists():
                form.add_error(None, "This email address has already been used!")
                return render(request, self.template_name, {'form': form})
            else:
                # Create the account
                # Save the application
                new_account = form.save(commit=False)
                new_account.set_password(form.cleaned_data['password_hash'])
                new_account.save()
                return redirect('login')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})

class PasswordResetView(View):
    template_name = 'forgot_password.html'

    def get(self, request):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']

            # REQ-1: Check if the email address exists
            if not PotentialDonor.objects.filter(email_address=email_address).exists():
                form.add_error(None, "Invalid email address!")
            else:
                # Redirect to dashboard
                return redirect('dashboard', email_address=email_address)
            # If there are errors, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        return render(request, self.template_name)

def book_ticket(request):
    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            ticket_number = uuid.uuid4().hex[:10].upper()  # Generate ticket number
            form.instance.ticket_number = ticket_number
            form.save()
            
            # Store the ticket number in the session
            request.session['ticket_number'] = ticket_number
            
            return redirect('booking_success')  # Redirect to booking success page
    else:
        form = BloodDonationForm()
    return render(request, 'book_ticket.html', {'form': form})

def booking_success(request):
    # Retrieve the ticket number from the session (or database, if applicable)
    ticket_number = request.session.get('ticket_number')
    return render(request, 'booking_success.html', {'ticket_number': ticket_number})

def logout_view(request):
    # Log out the user
    logout(request)
    # Clear the session data
    request.session.flush()
    # Redirect the user to a specific page (optional)
    return redirect('login')  # Redirect to the home page after logout

def future_events(request):
    # Retrieve future events from the database
    future_events = FutureEvent.objects.filter(application_deadline__gt=timezone.now())
    return render(request, 'future_events.html', {'future_events': future_events})

def past_events(request):
    past_events = PastEvent.objects.all()
    return render(request, 'past_events.html', {'past_events': past_events})

def donation_history(request):
    donation_history = DonationHistory.objects.all()
    return render(request, 'donation_history.html', {'donation_history': donation_history})
