from django.shortcuts import render
from django.utils import timezone
from .forms import student_information_form, disposable_form, parents_form, disposable_form, disposable_parents_form, disposable_transportation_form
from .models import student, disposable, parents, disposable_parents, disposable_transportation
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

def student_information(request):
    id = 0
    disposable_response = 0
    print("request")
    if request.method == "POST":
        print("request is post")
        buttonName = request.POST['buttonName']
        if buttonName == 'submit_student_details': #If student_details button is pressed
            print('rn in submit_student_details')
            disposable_form_request = disposable_form(request.POST,request.FILES or None)
            if disposable_form_request.is_valid():
                request.session['disposable_form'] = request.POST
                return JsonResponse({'success':True})
            else:
                print("ERROR")  
                return JsonResponse({'error':disposable_form_request.errors})
        
        elif buttonName == 'submit_parent_details':
            print('rn in submit parents')
            disposable_parents_form_request = disposable_parents_form(request.POST,request.FILES or None)
            if disposable_parents_form_request.is_valid():
                request.session['disposable_parents_form'] = request.POST
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                return JsonResponse({'error':disposable_parents_form_request.errors})
        
        elif buttonName == 'complete_registration':
            print('rn in submit transportation')
            disposable_transportation_form_request = disposable_transportation_form(request.POST,request.FILES or None)
            if disposable_transportation_form_request.is_valid():
                disposable_transportation_details = request.POST
                student = disposable_form(request.session.get('disposable_form')).save()
                student_id = student.id
                disposable_parents_details = request.session.get('disposable_parents_form')
                disposable_parents_details['related']= student_id
                disposable_transportation_details['related']= student_id
                disposable_parents_form(disposable_parents_details).save()
                disposable_transportation_form(disposable_transportation_details).save()
            else:
                print("ERROR")
                return JsonResponse({'error':disposable_transportation_form_request.errors})
        
        else:
            print("no submit button in POST")
       
    else:
        print("outter else if")
        disposable_form_request = disposable_form()
        disposable_parents_form_request = disposable_parents_form()
        disposable_transportation_form_request = disposable_transportation_form()
    return render(request, 'preregistration/student_information.html', {'student_form': disposable_form_request,
                                                                        'disposable_parents_form': disposable_parents_form_request,
                                                                        'disposable_transportation_form': disposable_transportation_form_request})

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

 