
from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail

from .forms import BookingForm, ContactForm
from .models import Asset, Booking, UserMessage

def admin(request):
    return render(request, 'inventory/admin.html')

class CustomLoginView(LoginView):
    template_name = 'inventory/login.html'
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Change 'home' to your actual homepage
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Make sure this matches your login URL name

    return render(request, 'inventory/login.html')



def asset_list(request):
    assets = Asset.objects.all()

    for asset in assets:
        # Find the latest booking that ends today or later
        latest_booking = Booking.objects.filter(
            asset=asset,
            end_date__gte=date.today()
        ).order_by('end_date').last()

        # If there's a future booking, set next_available to the day after it ends
        if latest_booking:
            asset.next_available = latest_booking.end_date + timedelta(days=1)
        else:
            asset.next_available = date.today()

    return render(request, 'inventory/asset_list.html', {'assets': assets})


def home(request):
    assets = Asset.objects.all()
    return render(request, 'inventory/home.html', {'assets': assets})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save to database with user
            UserMessage.objects.create(
                user=request.user,  # ✅ this is the fix
                email=email,
                subject=subject,
                message=message
            )

            # Send email to admins
            send_mail(
                f"Contact Form: {subject}",
                f"Name: {name}\nEmail: {email}\nMessage: {message}",
                email,
                [admin[1] for admin in settings.ADMINS],
                fail_silently=False,
            )

            return render(request, 'inventory/contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()

    return render(request, 'inventory/contact.html', {'form': form})


@login_required
def book_asset(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('asset_list')
    else:
        form = BookingForm()
    return render(request, 'inventory/book_asset.html', {'form': form})



@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    show_user = request.user.is_staff  # Only staff can see who made the booking
    return render(request, 'inventory/booking_list.html', {
        'bookings': bookings,
        'show_user': show_user
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'inventory/register.html', {'form': form})

def edit_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk)

    if booking.user != request.user:
        messages.error(request, "You are not allowed to edit this booking.")
        return redirect('booking_list')

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'inventory/edit_booking.html', {'form': form})




def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('inventory/login')
