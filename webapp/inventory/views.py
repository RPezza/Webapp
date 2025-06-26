from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, ContactForm, AssetForm
from .models import Asset, Booking, UserMessage


def admin_required(user):
    return user.is_staff


def home(request):
    assets = Asset.objects.all()
    for asset in assets:
        latest_booking = (
            Booking.objects.filter(asset=asset, end_date__gte=date.today())
            .order_by("end_date")
            .last()
        )
        asset.next_available = (
            latest_booking.end_date + timedelta(days=1)
            if latest_booking
            else date.today()
        )
    return render(request, "inventory/home.html", {"assets": assets})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")
        messages.error(request, "Invalid username or password.")
    return render(request, "inventory/login.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "inventory/register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


@login_required
def asset_list(request):
    assets = Asset.objects.all()
    for asset in assets:
        latest_booking = (
            Booking.objects.filter(asset=asset, end_date__gte=date.today())
            .order_by("end_date")
            .last()
        )
        asset.next_available = (
            latest_booking.end_date + timedelta(days=1)
            if latest_booking
            else date.today()
        )
    return render(request, "inventory/asset_list.html", {"assets": assets})


@login_required
def book_asset(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Asset booked successfully.")
            return redirect("asset_list")
    else:
        form = BookingForm()
    return render(request, "inventory/book_asset.html", {"form": form})


@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    show_user = request.user.is_staff
    return render(
        request,
        "inventory/booking_list.html",
        {"bookings": bookings, "show_user": show_user},
    )


@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    if booking.user != request.user and not request.user.is_staff:
        messages.error(request, "You are not allowed to edit this booking.")
        return redirect("booking_list")
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect("booking_list")
    else:
        form = BookingForm(instance=booking)
    return render(request, "inventory/edit_booking.html", {"form": form})


@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            send_mail(
                f"Contact Form: {message.subject}",
                f"Name: {message.name}\nEmail: {message.email}\nMessage: {message.message}",
                message.email,
                [admin[1] for admin in settings.ADMINS],
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "inventory/contact.html", {"form": form})


@user_passes_test(admin_required)
def asset_create(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset created successfully.")
            return redirect("asset_list")
    else:
        form = AssetForm()
    return render(request, "inventory/asset_form.html", {"form": form})


@user_passes_test(admin_required)
def asset_update(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset updated successfully.")
            return redirect("asset_list")
    else:
        form = AssetForm(instance=asset)
    return render(request, "inventory/asset_form.html", {"form": form})


@user_passes_test(admin_required)
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        asset.delete()
        messages.success(request, "Asset deleted successfully.")
        return redirect("asset_list")
    return render(request, "inventory/asset_confirm_delete.html", {"asset": asset})
