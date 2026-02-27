from django.shortcuts import render, redirect, get_object_or_404

from Admin.models import Student

from django.urls import reverse_lazy

from django.views.generic import DeleteView

# Create your views here.
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


