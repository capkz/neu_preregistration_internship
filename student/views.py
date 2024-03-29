from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from .forms import student_search
from preregistration.models import student
from django.contrib.auth.decorators import permission_required, login_required
import pdb

@login_required
@permission_required('preregistration.view_student', raise_exception=True)
def student_list(request):
    if request.method == 'GET' and 'q' in request.GET:
        q = request.GET.get('q')
        if q == '':
            return redirect('student_list')
        else:
            students = student.objects.filter(id=q)
            return render(request, 'student/student_list.html', {'students': students,
                                                                 'nbar': 'student_list'})
    else:
        students = student.objects.all()
        return render(request, 'student/student_list.html', {'students': students,
                                                             'nbar': 'student_list'})






    
    # if request.method == 'GET':
    #     query = request.GET.get('q',)
    #     if query == '':
    #         return redirect('ogrenci_listesi',)
    #     ogrenci_detay = get_object_or_404(ogrenci, pk=query)
    #     return render(request, 'ogrenci/ogrenci_arama.html' ,{'ogrenci': ogrenci_detay})
    # return render(request, 'ogrenci/ogrenci_listesi.html')
