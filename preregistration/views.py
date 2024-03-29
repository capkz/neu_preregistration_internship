from django.shortcuts import render
from django.utils import timezone
from .forms import student_form, parent_form, sibling_form, transportation_form, pickup_backup_form
from .models import student, parent, sibling, transportation, pickup_backup
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.forms import formset_factory, modelformset_factory
from django.core.mail import send_mail
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User, Group

def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data


def _sendMail(subject,message,toEmail):
    send_mail(
    subject,
    message,
    'necstajnoreply@gmail.com',
    [toEmail],
    fail_silently=False,
    )


@login_required
@permission_required('preregistration.add_student', raise_exception=True)
def student_add(request):
    siblingFormset = formset_factory(sibling_form,extra=1,can_delete=True)
    pickupBackupFormset = formset_factory(pickup_backup_form,extra=1,can_delete=True)
    
    pickupBackupFormset()
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

                user = User.objects.create_user(
                    username = student_save.id,
                    password = student_save.password,
                    email = student_save.email
                )
                user.save()
                
                group = Group.objects.get(name='Student')
                user.groups.add(group)

                mother_details = request.session.pop('mother_form')
                mother_uncommitted = parent_form(mother_details).save(commit=False)
                mother_uncommitted.related_student_id = student_id
                mother_uncommitted.relation = 'mom'
                
                father_details = request.session.pop('father_form')
                father_uncommitted = parent_form(father_details).save(commit=False)
                father_uncommitted.related_student_id = student_id
                father_uncommitted.relation = 'dad'
                
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

                #Register mother to system
                mother_register = User.objects.create_user(
                    username = mother_uncommitted.email,
                    password = mother_uncommitted.password,
                    email = mother_uncommitted.email
                )
                mother_register.save()
                
                group = Group.objects.get(name='Guardian')
                mother_register.groups.add(group)

                #Register father to system
                father_register = User.objects.create_user(
                    username = father_uncommitted.email,
                    password = father_uncommitted.password,
                    email = father_uncommitted.email
                )
                father_register.save()
                
                group = Group.objects.get(name='Guardian')
                father_register.groups.add(group)

                transportation_uncommitted.save()
                
                #Send a mail to student
                _sendMail(subject='Registration Successful',
                          message='Dear '+student_save.name+' '+student_save.surname+',\nYou have successfully registered to NEC \nYour username is your ID: '+str(student_save.id)+'\nYour password is: '+student_save.password,
                          toEmail=student_save.email)
                
                # #Send a mail to mother
                # _sendMail(subject='Registration Successful',
                #           message='Dear '+mother_uncommitted.name+' '+mother_uncommitted.surname+',\nRegistration of '+student_save.name+' '+student_save.surname+' is complete.  \nYour username is your ID '+mother_uncommitted.id+'\nYour password is '+mother_uncommitted.password,
                #           toEmail=mother_uncommitted.email)
                
                # #Send a mail to father
                # _sendMail(subject='Registration Successful',
                #           message='Dear '+father_uncommitted.name+' '+father_uncommitted.surname+',\nRegistration of '+student_save.name+' '+student_save.surname+' is complete.  \nYour username is your ID '+father_uncommitted.id+'\nYour password is '+father_uncommitted.password,
                #           toEmail=father_uncommitted.email)

                return JsonResponse({'success':True,
                                     'pk': student_save.id,
                                     'action': 'add',
                                     'status': 'success'})
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
            siblingFormsetRequest = siblingFormset(request.POST, prefix="sibling", )
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
                                                                        'pickup_backup_forms': pickupBackupFormset,
                                                                        'nbar': 'student'})
        else:
            print("outter else if")
            student_form_request = student_form()
            mother_form_request = parent_form(prefix="mother")
            dad_form_request = parent_form(prefix="dad")
            transportation_form_request = transportation_form()
            siblingFormset = siblingFormset(prefix="sibling")
            pickupBackupFormset = pickupBackupFormset(prefix="pickup")
            request.session['1'] = False
            request.session['2'] = False
            request.session['3'] = False
    return render(request, 'preregistration/student_add.html', {'student_form': student_form_request,
                                                                        'mother_form': mother_form_request,
                                                                        'dad_form': dad_form_request,
                                                                        'transportation_form': transportation_form_request,
                                                                        'sibling_forms': siblingFormset,
                                                                        'pickup_backup_forms': pickupBackupFormset,
                                                                        'nbar': 'student'})
 
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

@login_required
@permission_required('preregistration.edit_student', raise_exception=True)
def student_edit(request):
    
    siblingFormset = modelformset_factory(sibling, form=sibling_form ,extra=0)
    pickupBackupFormset = modelformset_factory(pickup_backup, form=pickup_backup_form ,extra=0)
    
    q = request.GET.get('q')
    student_query = get_object_or_404(student, pk=q)
    mother_query= get_object_or_404(parent.objects.filter(relation='mom'), related_student_id=q)
    father_query= get_object_or_404(parent.objects.filter(relation='dad'), related_student_id=q)
    transportation_query= get_object_or_404(transportation, related_student_id=q)
    sibling_query =sibling.objects.filter(related_student=q)
    pickup_backup_query =pickup_backup.objects.filter(related_student=q)
        
    if request.method == 'POST':
        buttonName = request.POST['buttonName']
        
        if buttonName == 'complete_registration':
            if (request.session.get('1',False) == True or request.session.get('2',False) == True or request.session.get('3',False) == True):
                if request.session.pop('1',False) == True:
                    student_save = student_form(request.session.pop('student_form'),instance=student_query).save(commit=False)
                    if request.session.get('student_form','') is not '':
                        print('theres is a new photo')
                        student_save.delete()
                        student_save.photo = request.session.get('student_form')['photo']
                    
                    student_save.user = request.user
                    student_save.save()
                
                if request.session.pop('2',False) == True:
                    mother_details = request.session.pop('mother_form')
                    mother_uncommitted = parent_form(mother_details, instance=mother_query).save()
                    
                    father_details = request.session.pop('father_form')
                    father_uncommitted = parent_form(father_details, instance=father_query).save()
                    
                    siblings_details = request.session.pop('siblings_form')
                    siblingFormset(siblings_details, queryset=sibling_query, prefix="sibling").save()
                
                if request.session.pop('3',False) == True:
                    transportation_details = request.session.pop('transportation_form')
                    transportation_uncommitted = transportation_form(transportation_details, instance=transportation_query).save()
                    
                    pickup_details = request.session.pop('pickup_backups')
                    pickupBackupFormset(pickup_details, queryset=pickup_backup_query, prefix="pickup").save()

                
                # send_mail(
                #     'Registration Successful',
                #     'Dear '+student_save.name+' '+student_save.surname+',\nYour student details have been successfully changed!',
                #     'necstajnoreply@gmail.com',
                #     [student_save.email],
                #     fail_silently=False,
                # )
                
                return JsonResponse({'success':True,
                                     'pk': q,
                                     'action': 'edit',
                                     'status': 'success'})
            
            else:
                error = {
                    'error': {0 : "Please fill all the forms"}
                }
                return JsonResponse({'error':error})
        
        elif buttonName == 'submit_student_details': #If student_details button is pressed
            print('rn in submit_student_details')
            student_form_request = student_form(request.POST,request.FILES, instance=student_query)
            if student_form_request.is_valid():
                request.session['student_form'] = request.POST.copy()
                request.session['1'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                return JsonResponse({'error':student_form_request.errors})
            
        elif buttonName == 'submit_parent_details':
            print('rn in submit parents')
            mother_form_request = parent_form(request.POST,request.FILES, instance=mother_query, prefix="mother")
            dad_form_request = parent_form(request.POST,request.FILES, instance=father_query , prefix="dad")
            siblingFormsetRequest = siblingFormset(request.POST, queryset=sibling_query ,prefix='sibling')
            if mother_form_request.is_valid() and dad_form_request.is_valid() and siblingFormsetRequest.is_valid():
                request.session['siblings_form'] = querydict_to_dict(siblingFormsetRequest.data)
                print (querydict_to_dict(siblingFormsetRequest.data))
                request.session['mother_form'] = mother_form_request.cleaned_data
                request.session['father_form'] = dad_form_request.cleaned_data
                request.session['2'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                #TODO seperate errors and return them
                return JsonResponse({'error':siblingFormsetRequest.errors})
            
        elif buttonName == 'submit_transportation_details':
            print('rn in submit transportation')
            transportation_form_request = transportation_form(request.POST,request.FILES, instance=transportation_query)
            pickupBackupFormsetRequest = pickupBackupFormset(request.POST, queryset=pickup_backup_query, prefix='pickup')
            if transportation_form_request.is_valid() and pickupBackupFormsetRequest.is_valid():
                request.session['transportation_form'] = transportation_form_request.cleaned_data
                request.session['pickup_backups'] = querydict_to_dict(pickupBackupFormsetRequest.data)
    
                request.session['3'] = True
                return JsonResponse({'success':True})
            else:
                print("ERROR")
                return JsonResponse({'error':transportation_form_request.errors})
            
    elif request.method == 'GET':
        
        mother_query= get_object_or_404(parent.objects.filter(relation='mom'), related_student_id=q)
        father_query= get_object_or_404(parent.objects.filter(relation='dad'), related_student_id=q)
        
        transportation_query= get_object_or_404(transportation, related_student_id=q)
        
        student_form_request = student_form(instance= student_query)
        mother_form_request = parent_form(prefix="mother", instance=mother_query)
        dad_form_request = parent_form(prefix="dad", instance=father_query)
        transportation_form_request = transportation_form(instance=transportation_query)
        
        siblingEditFormset = siblingFormset(queryset= sibling_query, prefix="sibling")
        pickupBackupEditFormset = pickupBackupFormset(queryset= pickup_backup_query, prefix="pickup")
        
        #siblingFormset = siblingFormset(prefix="sibling")
        
        #pickupBackupFormset = pickupBackupFormset(prefix="pickup")
        
        request.session['1'] = False
        request.session['2'] = False
        request.session['3'] = False
        return render(request, 'preregistration/student_edit.html', {'student_form': student_form_request,
                                                                    'mother_form': mother_form_request,
                                                                    'dad_form': dad_form_request,
                                                                    'transportation_form': transportation_form_request,
                                                                    'sibling_forms': siblingEditFormset,
                                                                    'pickup_backup_forms': pickupBackupEditFormset,
                                                                    'nbar': 'student'})

@login_required
def form_complete(request,pk,action,status):
    student_details = get_object_or_404(student, pk=pk)
    return render(request, 'preregistration/student_success.html', {'student':student_details,
                                                                    'action': action})

 