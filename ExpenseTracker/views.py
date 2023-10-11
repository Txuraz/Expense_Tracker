from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from .models import Transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout


# Create your views here.


def SignupPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the same email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return redirect('signup')

        # Create a new user and save it to the database
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name  # Set the user's first name to the 'name' field
        user.save()

        messages.success(request, 'User has been created successfully. You can now log in.')
        return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'login.html')


def LogoutView(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        transaction_type = request.POST.get('type')
        date = request.POST.get('date')

        # Validate and save the data
        if amount and category and transaction_type and date:
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                category=category,
                type=transaction_type,
                date=date,
            )

        return redirect('dashboard')

    # Get all transactions for the current user
    transaction_data = Transaction.objects.filter(user=request.user).order_by('-date')

    # Define the number of items to display per page
    items_per_page = 7

    # Create a Paginator instance
    paginator = Paginator(transaction_data, items_per_page)

    # Get the current page number from the request's GET parameter
    page_number = request.GET.get('page')

    try:
        # Get the Page object for the current page
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, deliver the first page
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., page_number is too high), deliver the last page
        page = paginator.page(paginator.num_pages)

    # Calculate total income and total expenses for all transactions (not just the displayed ones)
    total_income = Transaction.objects.filter(user=request.user, type='Income').aggregate(total_income=Sum('amount'))[
                       'total_income'] or 0
    total_expenses = \
        Transaction.objects.filter(user=request.user, type='Expenses').aggregate(total_expenses=Sum('amount'))[
            'total_expenses'] or 0

    # Calculate total balance
    total_balance = total_income - total_expenses

    context = {
        'transaction_data': page,  # Pass the current page to the template
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_balance': total_balance,
    }

    return render(request, 'dashboard.html', context)


def save_transaction(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        transaction_type = request.POST.get('type')  # Extract the 'type' field
        date = request.POST.get('date')

        # Validate and save the data
        if amount and category and transaction_type and date:
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                category=category,
                type=transaction_type,
                date=date,
            )

    return redirect('dashboard')


def filter_transactions(request):
    # Calculate total income and total expenses for all transactions (not filtered)
    total_income = Transaction.objects.filter(user=request.user, type='Income').aggregate(total_income=Sum('amount'))[
                       'total_income'] or 0
    total_expenses = \
        Transaction.objects.filter(user=request.user, type='Expenses').aggregate(total_expenses=Sum('amount'))[
            'total_expenses'] or 0
    total_balance = total_income - total_expenses

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        filter_type = request.POST.get('filter_type')
        filter_category = request.POST.get('filter_category')

        # Build the filter criteria using Q objects
        filter_criteria = Q()
        if start_date:
            filter_criteria &= Q(date__gte=start_date)
        if end_date:
            filter_criteria &= Q(date__lte=end_date)
        if filter_type:
            filter_criteria &= Q(type=filter_type)
        if filter_category:
            filter_criteria &= Q(category=filter_category)

        if not (start_date or end_date or filter_type or filter_category):
            return redirect('dashboard')

        # Get filtered transactions based on the criteria
        filtered_transactions = Transaction.objects.filter(user=request.user).filter(filter_criteria)

        # Render the dashboard with the filtered data and the unchanged total values
        return render(request, 'dashboard.html', {
            'transaction_data': filtered_transactions,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_balance': total_balance,
        })

    return redirect('dashboard')
