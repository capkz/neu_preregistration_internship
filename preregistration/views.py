from django.shortcuts import render
from django.utils import timezone
from .forms import student_form, parent_form, sibling_form, transportation_form, pickup_backup_form
from .models import student, parent, sibling, transportation, pickup_backup
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.forms import formset_factory, modelformset_factory
from django.core.mail import send_mail
from django.contrib.auth.decorators import permission_required, login_required

@login_required
@permission_required('preregistration.add_student', raise_exception=True)
def student_add(request):
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
                student_save = student_form(request.session.pop('student_form')).save(commit=False)
                student_save.user = request.user
                student_save.save()
                student_id = student_save.id
                
                mother_details = request.session.pop('mother_form')
                mother_uncommitted = parent_form(mother_details).save(commit=False)
                mother_uncommitted.related_student_id = student_id
                
                father_details = request.session.pop('father_form')
                father_uncommitted = parent_form(father_details).save(commit=False)
                father_uncommitted.related_student_id = student_id
                
                siblings_details = request.session.pop('siblings_form')
                for detail in siblings_details:
                    uncommitted = sibling_form(detail).save(commit=False)
                    uncommitted.related_student_id = student_id
                    uncommitted.save()
                
                transportation_details = request.session.pop('transportation_form')
                transportation_uncommitted = transportation_form(transportation_details).save(commit=False)
                transportation_uncommitted.related_student_id = student_id
                
                pickup_details = request.session.pop('pickup_backups')
                for detail in pickup_details:
                    uncommitted = pickup_backup_form(detail).save(commit=False)
                    uncommitted.related_student_id = student_id
                    uncommitted.save()

                mother_uncommitted.save()
                father_uncommitted.save()
                transportation_uncommitted.save()
                
                send_mail(
                    'Registration Successful',
                    'Dear '+student_save.name+' '+student_save.surname+',\nYou have successfully registered to NEC \nYour password is '+student_save.password,
                    'necstajnoreply@gmail.com',
                    [student_save.email],
                    fail_silently=False,
                )
                
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
        
        elif buttonName == 'submit_parent_details':
            print('rn in submit parents')
            mother_form_request = parent_form(request.POST,request.FILES or None, prefix="mother")
            dad_form_request = parent_form(request.POST,request.FILES or None, prefix="dad")
            siblingFormsetRequest = siblingFormset(request.POST, prefix="sibling")
            if mother_form_request.is_valid() and dad_form_request.is_valid() and siblingFormsetRequest.is_valid():
                request.session['mother_form'] = mother_form_request.cleaned_data
                request.session['father_form'] = dad_form_request.cleaned_data
                request.session['siblings_form'] = siblingFormsetRequest.cleaned_data

                request.session['2'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                #TODO seperate errors and return them
                return JsonResponse({'error':mother_form_request.errors})
        
        elif buttonName == 'submit_transportation_details':
            print('rn in submit transportation')
            transportation_form_request = transportation_form(request.POST,request.FILES or None)
            pickupBackupFormsetRequest = pickupBackupFormset(request.POST, prefix="pickup")
            if transportation_form_request.is_valid() and pickupBackupFormsetRequest.is_valid():
                request.session['transportation_form'] = transportation_form_request.cleaned_data
                request.session['pickup_backups'] = pickupBackupFormsetRequest.cleaned_data
                
                request.session['3'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                return JsonResponse({'error':transportation_form_request.errors})
        
        else:
            print("no submit button in POST")
       
    else:
        q = request.GET.get('q',False)
        if q != False:
            print("searched")
            student_query = get_object_or_404(student, pk=q)
            
            mother_query= get_object_or_404(parent.objects.filter(relation='mom'), related_student_id=q)
            father_query= get_object_or_404(parent.objects.filter(relation='dad'), related_student_id=q)
            
            transportation_query= get_object_or_404(transportation, related_student_id=q)
            
            sibling_query= get_list_or_404(sibling, related_student_id=q)
            
            pickup_query= get_object_or_404(pickup_backup, related_student_id=q)
            student_form_request = student_form(instance= student_query)
            mother_form_request = parent_form(prefix="mother", instance=mother_query)
            dad_form_request = parent_form(prefix="dad", instance=father_query)
            transportation_form_request = transportation_form(instance=transportation_query)
            
            siblingFormset = modelformset_factory(sibling, exclude=('related_student',))
            siblingEditFormset = siblingFormset(queryset=sibling.objects.filter(related_student=q))
            
            #siblingFormset = siblingFormset(prefix="sibling")
            
            pickupBackupFormset = pickupBackupFormset(prefix="pickup")
            return render(request, 'preregistration/student_add.html', {'student_form': student_form_request,
                                                                        'mother_form': mother_form_request,
                                                                        'dad_form': dad_form_request,
                                                                        'transportation_form': transportation_form_request,
                                                                        'sibling_forms': siblingEditFormset,
                                                                        'pickup_backup_forms': pickupBackupFormset})
        else:
            print("outter else if")
            student_form_request = student_form()
            mother_form_request = parent_form(prefix="mother")
            dad_form_request = parent_form(prefix="dad")
            transportation_form_request = transportation_form()
            siblingFormset = siblingFormset(prefix="sibling")
            pickupBackupFormset = pickupBackupFormset(prefix="pickup")
    return render(request, 'preregistration/student_add.html', {'student_form': student_form_request,
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

def student_edit(request):
    siblingFormset = modelformset_factory(sibling, form=sibling_form ,extra=0)
    pickupBackupFormset = modelformset_factory(pickup_backup, form=pickup_backup_form ,extra=0)
    if request.method == 'POST':
        buttonName = request.POST['buttonName']
            
        if buttonName == 'submit_student_details': #If student_details button is pressed
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
            siblingFormsetRequest = siblingFormset(request.POST, prefix='sibling')
            if mother_form_request.is_valid() and dad_form_request.is_valid() and siblingFormsetRequest.is_valid():
                request.session['siblings_form'] = request.POST
                request.session['2'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                #TODO seperate errors and return them
                return JsonResponse({'error':siblingFormsetRequest.errors})
            
        elif buttonName == 'submit_transportation_details':
            print('rn in submit transportation')
            transportation_form_request = transportation_form(request.POST,request.FILES or None)
            pickupBackupFormsetRequest = pickupBackupFormset(request.POST, prefix='pickup')
            if transportation_form_request.is_valid() and pickupBackupFormsetRequest.is_valid():
                request.session['transportation_form'] = transportation_form_request.cleaned_data
                request.session['pickup_backups'] = request.POST.copy()
                
                request.session['3'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                return JsonResponse({'error':transportation_form_request.errors})
            
    elif request.method == 'GET':
            
        q = request.GET.get('q')
        student_query = get_object_or_404(student, pk=q)
                
        mother_query= get_object_or_404(parent.objects.filter(relation='mom'), related_student_id=q)
        father_query= get_object_or_404(parent.objects.filter(relation='dad'), related_student_id=q)
        
        transportation_query= get_object_or_404(transportation, related_student_id=q)
        
        student_form_request = student_form(instance= student_query)
        mother_form_request = parent_form(prefix="mother", instance=mother_query)
        dad_form_request = parent_form(prefix="dad", instance=father_query)
        transportation_form_request = transportation_form(instance=transportation_query)
        
        
        siblingEditFormset = siblingFormset(queryset=sibling.objects.filter(related_student=q), prefix="sibling")
        pickupBackupEditFormset = pickupBackupFormset(queryset=pickup_backup.objects.filter(related_student=q), prefix="pickup")
        
        #siblingFormset = siblingFormset(prefix="sibling")
        
        #pickupBackupFormset = pickupBackupFormset(prefix="pickup")
        return render(request, 'preregistration/student_add.html', {'student_form': student_form_request,
                                                                    'mother_form': mother_form_request,
                                                                    'dad_form': dad_form_request,
                                                                    'transportation_form': transportation_form_request,
                                                                    'sibling_forms': siblingEditFormset,
                                                                    'pickup_backup_forms': pickupBackupEditFormset})

def form_success(request,pk):
    student_details = get_object_or_404(student, pk=pk)
    return render(request, 'preregistration/form_success.html', {'student':student_details})

 