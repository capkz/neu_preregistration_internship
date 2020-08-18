from django.shortcuts import render
from django.utils import timezone
from .forms import student_form, parent_form, sibling_form, transportation_form, pickup_backup_form
from .models import student, parent, sibling, transportation, pickup_backup
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

def student_information(request):
    disposable_response = 0
    print("request")
    if request.method == "POST":
        print("request is post")
        buttonName = request.POST['buttonName']
        if buttonName == 'complete_registration':
            if (request.session.pop('1') == True and request.session.pop('2') == True and request.session.pop('3') == True):
                student = student_form(request.session.pop('student_form')).save(commit=False)
                student.user = request.user
                student.save()
                student_id = student.id
                parent_details = request.session.pop('parent_form')
                parent_details['related_student']= student_id
                transportation_details = request.session.pop('transportation_form')
                transportation_details['related_student']= student_id
                parent_form(parent_details).save()
                transportation_form(transportation_details).save()
            else:
                error = {
                    'error': {0 : "Please fill all the forms"}
                }
                return JsonResponse({'error':error})
        
        elif buttonName == 'submit_student_details': #If student_details button is pressed
            print('rn in submit_student_details')
            student_form_request = student_form(request.POST,request.FILES or None)
            if student_form_request.is_valid():
                request.session['student_form'] = request.POST.copy()
                request.session['1'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")  
                return JsonResponse({'error':student_form_request.errors})
        
        elif buttonName == 'submit_parent_details':
            print('rn in submit parents')
            parent_form_request = parent_form(request.POST,request.FILES or None)
            if parent_form_request.is_valid():
                request.session['parent_form'] = request.POST.copy()
                request.session['2'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                return JsonResponse({'error':parent_form_request.errors})
        
        elif buttonName == 'submit_transportation_details':
            print('rn in submit transportation')
            transportation_form_request = transportation_form(request.POST,request.FILES or None)
            if transportation_form_request.is_valid():
                request.session['transportation_form'] = request.POST.copy()
                request.session['3'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                return JsonResponse({'error':transportation_form_request.errors})
        
        else:
            print("no submit button in POST")
       
    else:
        print("outter else if")
        student_form_request = student_form()
        parent_form_request = parent_form()
        transportation_form_request = transportation_form()
        sibling_form_request = sibling_form()
        pickup_backup_form_request = pickup_backup_form()
        return render(request, 'preregistration/student_information.html', {'student_form': student_form_request,
                                                                        'parent_form': parent_form_request,
                                                                        'transportation_form': transportation_form_request,
                                                                        'sibling_form': sibling_form_request,
                                                                        'pickup_backup_form': pickup_backup_form_request})
 
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

 