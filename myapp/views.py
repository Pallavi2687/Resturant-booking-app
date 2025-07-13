from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from myapp.models import BookTable, AboutUs, Feedback, ItemList, Items

# ✅ Home page with items, categories, and feedback
def HomeView(request):
    items = Items.objects.all()
    categories = ItemList.objects.all()
    reviews = Feedback.objects.all()
    return render(request, 'home.html', {
        'items': items,
        'list': categories,
        'review': reviews
    })

# ✅ About Us page
def AboutView(request):
    about_data = AboutUs.objects.all()
    return render(request, 'about.html', {'data': about_data})

# ✅ Menu page showing food categories and items
def MenuView(request):
    items = Items.objects.all()
    categories = ItemList.objects.all()
    return render(request, 'menu.html', {
        'items': items,
        'list': categories
    })

# ✅ Table booking form (GET and POST)
def BookTableView(request):
    if request.method == 'POST':
        name = request.POST.get('user_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('user_email', '').strip()
        total_person = request.POST.get('total_person', '').strip()
        booking_date = request.POST.get('booking_data', '').strip()

        if (
            name and email and booking_date and
            phone_number.isdigit() and len(phone_number) == 10 and
            total_person.isdigit() and int(total_person) > 0
        ):
            BookTable.objects.create(
                Name=name,
                Phone_number=phone_number,
                Email=email,
                Total_person=total_person,
                Booking_date=booking_date
            )
            messages.success(request, "Table booked successfully!")
        else:
            messages.error(request, "Invalid input. Please check your form.")
    return render(request, 'book_table.html')

# ✅ Feedback form page
def FeedbackView(request):
    return render(request, 'feedback.html')

# ✅ User login
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')

        login(request, user)
        return redirect('/')  # Update this path if needed

    return render(request, 'login.html')

# ✅ User logout
def logout_page(request):
    logout(request)
    return redirect('/login/')

# ✅ User registration
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('/register/')

    return render(request, 'register.html')
