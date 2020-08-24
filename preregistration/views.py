from django.shortcuts import render
from django.utils import timezone
from .forms import student_form, parent_form, sibling_form, transportation_form, pickup_backup_form
from .models import student, parent, sibling, transportation, pickup_backup
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms import formset_factory

def student_information(request):
    siblingFormset = formset_factory(sibling_form,extra=1,can_delete=True)
    pickupBackupFormset = formset_factory(pickup_backup_form,extra=1,can_delete=True)
    if request.method == "POST":
        print("request is post")
        buttonName = request.POST['buttonName']
        if buttonName == 'complete_registration':
            if (request.session.get('1',False) == True and request.session.get('2',False) == True and request.session.get('3',False) == True):
                del request.session["1"]
                del request.session["2"]
                del request.session["3"]
                student = student_form(request.session.pop('student_form')).save(commit=False)
                student.user = request.user
                student.save()
                student_id = student.id
                mother_details = request.session.pop('mother_form')
                mother_uncommitted = mother_form(mother_details).save(commit=False)
                mother_uncommitted.related_student_id = student_id
                
                father_details = request.session.pop('father_form')
                father_uncommitted = father_form(father_details).save(commit=False)
                father_uncommitted.related_student_id = student_id
                
                transportation_details = request.session.pop('transportation_form')
                transportation_uncommitted = transportation_form(transportation_details).save(commit=False)
                transportation_uncommitted.related_student_id = student_id
                
                parent_uncommitted_form().save()
                transportation_uncommitted().save()
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
            mother_form_request = parent_form(request.POST,request.FILES or None, prefix="mother")
            dad_form_request = parent_form(request.POST,request.FILES or None, prefix="dad")
            pickupBackupFormset = pickupBackupFormset(request.POST)
            if mother_form_request.is_valid() and dad_form_request.is_valid() and pickupBackupFormset.is_valid():
                request.session['mother_form'] = mother_form_request.cleaned_data()
                request.session['dad_form'] = dad_form_request.cleaned_data()
                request.session['2'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                print(mother_form_request.is_valid())
                print(dad_form_request.is_valid())
                print(pickupBackupFormset.is_valid())
                
                #TODO seperate errors and return them
                return JsonResponse({'error':mother_form_request.errors})
        
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
        mother_form_request = parent_form(prefix="mother")
        dad_form_request = parent_form(prefix="dad")
        transportation_form_request = transportation_form()
        siblingFormset = siblingFormset(prefix="sibling")
        pickupBackupFormset = pickupBackupFormset(prefix="pickup")
    return render(request, 'preregistration/student_information.html', {'student_form': student_form_request,
                                                                        'mother_form': mother_form_request,
                                                                        'dad_form': dad_form_request,
                                                                        'transportation_form': transportation_form_request,
                                                                        'sibling_forms': siblingFormset,
                                                                        'pickup_backup_forms': pickupBackupFormset})
 
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

 