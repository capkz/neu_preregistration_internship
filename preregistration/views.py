from django.shortcuts import render
from django.utils import timezone
from .forms import student_information_form, disposable_form
from .models import student, disposable
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

def student_information(request):
    print("request")
    if request.method == "POST":
        print("request is post")
        disposable_form_request = disposable_form(request.POST,request.FILES or None)
        if disposable_form_request.is_valid():
            form = disposable_form_request.save(commit=False)
            form.save()
            return JsonResponse({'success':True})
        else:
            print("ERROR")
            return JsonResponse({'error':disposable_form_request.errors})
    else:
        print("outter else if")
        disposable_form_request = disposable_form()
    return render(request, 'preregistration/student_information.html', {'student_form': disposable_form_request})

    # print("request")
    # if request.method == "POST":
    #     print("request is post")
    #     student_form_request = student_information_form(request.POST,request.FILES or None)
    #     if student_form_request.is_valid():
    #         form = student_form_request.save(commit=False)
    #         form.user = request.user
    #         form.registration_date = timezone.now()
    #         form.save()
    #         return redirect('form_success', pk=form.pk)
    #     else:
    #         print (student_form_request.errors)
    #         print("ERROR")
    # else:
    #     print("outter else if")
    #     student_form_request = student_information_form()
    # return render(request, 'preregistration/student_information.html', {'student_form': student_form_request})



def form_success(request,pk):
    student_details = get_object_or_404(student, pk=pk)
    return render(request, 'preregistration/form_success.html', {'student':student_details})

 