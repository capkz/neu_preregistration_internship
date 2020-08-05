from django.shortcuts import render
from django.utils import timezone
from .forms import student_information_form
from .models import student
from django.shortcuts import redirect, get_object_or_404


def student_information(request):
    student_form_request = student_information_form(request.POST)
    if student_form_request.is_valid():
        form = student_form_request.save(commit=False)
        form.user = request.user
        form.registration_date = timezone.now()
        form.save()
        return redirect('form_success', pk=form.pk)
    else:
        print("ERROR")
    return render(request, 'preregistration/student_information.html', {'student_form': student_form_request})


def form_success(request,pk):
    student_details = get_object_or_404(student, pk=pk)
    return render(request, 'preregistration/form_success.html', {'student':student_details})

 