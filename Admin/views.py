from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django_daraja.mpesa.core import MpesaClient

from Admin.models import Student


# Create your views here.
@login_required
def index(request):
    students = Student.objects.all()
    return render(request, 'index.html', context={'students': students} )
def add_record(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        course = request.POST.get('course')
        age = request.POST.get('age')
        email = request.POST.get('email')
        date = request.POST.get('date')
        Student.objects.create(
            image=image,
            name=name,
            course=course,
            age=age,
            email=email,
            date=date)
        return  redirect('index')
    return render(request, 'add_record.html')

def update_record(request,id):
    students = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        students.name = request.POST.get('name')
        students.course = request.POST.get('course')
        students.age = request.POST.get('age')
        students.email = request.POST.get('email')
        students.date = request.POST.get('date')
        if request.files.get('image'):
            students.image = request.FILES.get('image')
        students.save()
        return redirect('index')
    return render(request, 'update_record.html',context={'students':students})


def delete_record(request,id):
        student = get_object_or_404(Student, id=id)
        student.delete()
        return redirect('index')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('sign_up')
        user = User.objects.create_user(username=username, email=email, password=password)

        login(request, user)
        return redirect('index')
    return render(request, 'sign_up.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'log_in.html')
def logout_view(request):
    logout(request)
    return redirect('login')


def payment(request,id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        if not phone or not amount:
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'payment.html',{'student':student})
        try:
            client = MpesaClient()
            response = client.stk_push(phone,int(amount),'eMobilis','Payment for fee','https://example.com/callback').json()
            payment.objects.create(student=student,amount=amount,response=response,checkout_request_id=response.get('checkout_request_id',''),
                                   status = 'pending')
            messages.success(request, 'STK PUSH SENT!Check your Phone')
        except Exception:
            messages.error(request, 'Payment Failed')


    return render(request, 'payment.html')


