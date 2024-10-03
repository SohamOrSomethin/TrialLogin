from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from login.models import Student, Faculty, Batch, Subject,StudentSubject
from .forms import StudentForm

def index(request):
    return render(request, 'index.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                student = Student.objects.get(registration_number=user.username)
                subjects = student.subjects.all()
                student_subjects = StudentSubject.objects.filter(student=student)
                student_subjects_info = []
                attendance_total=0
                attendance_lab_total=0
                for student_subject in student_subjects:
                    attendance_total = attendance_total + student_subject.subject_attendance
                    attendance_lab_total = attendance_lab_total + student_subject.subject_lab_attendance 
                    student_subjects_info.append({
                    'subject': student_subject.subject,
                    'noc_signed': student_subject.noc_signed,
                    'subject_attendance':student_subject.subject_attendance,
                    'subject_lab_attendance':student_subject.subject_lab_attendance,
                    'assignments_submitted':student_subject.assignments_submitted,
                    })
                login(request, user)
                avg_att =int(attendance_total/7)
                avg_lab_att= int(attendance_lab_total/7)
                context = {
                    'prn_number': student.registration_number,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'avg_att':avg_att,
                    'avg_lab_att':avg_lab_att,
                    #'attendance': student.attendance,
                    'cie_marks': student.cie_marks,
                    'batch': student.batch,
                    'roll_number': student.roll_number,
                    'subjects': subjects,
                    'student_subjects': student_subjects,
                    'student_subjects_info': student_subjects_info,
                }
                return render(request, 'student_success.html', context)
            except Student.DoesNotExist:
                messages.error(request, 'Invalid credentials or not a student account.')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'student_login.html')

def faculty_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                faculty = Faculty.objects.get(email=user.username)
                batches = faculty.batches.all()
                subjects = faculty.subjects.all()
                subjects_name = ', '.join([subject.subject_name for subject in subjects])
                batch_names = ', '.join([batch.name for batch in batches])
                login(request, user)
                context = {
                    'first_name': faculty.first_name,
                    'last_name': faculty.last_name,
                    'subjects': subjects_name,
                    'batches': batch_names,
                }
                return render(request, 'teacher_success.html', context)
            except Faculty.DoesNotExist:
                messages.error(request, 'Invalid credentials or not a faculty account.')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'faculty_login.html')


@login_required
def show_batch_data(request):
    user = request.user

    faculty = Faculty.objects.get(email=user.username)
    print(f"Faculty Found: {faculty}")  
    batches = faculty.batches.all()
    subjects = faculty.subjects.all()
    students = Student.objects.filter(batch__in=batches)
    subjects_names = ', '.join([subject.subject_name for subject in subjects])
    batch_names = ', '.join([batch.name for batch in batches])
         
    context = {
            'students': students,
            'batches': batch_names,
            'subjects':subjects_names,
        }
    return render(request, 'show_batch_data.html', context)

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            registration_number = form.cleaned_data['registration_number']
            roll_number = form.cleaned_data['roll_number']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            attendance = form.cleaned_data['attendance']
            cie_marks = form.cleaned_data['cie_marks']
            batch = form.cleaned_data['batch']
            division = form.cleaned_data['division']
            subjects = form.cleaned_data['subjects']

            # Create the User associated with the Student
            user, created = User.objects.get_or_create(username=registration_number)
            if created:
                user.set_password(registration_number)
                user.save()

            student_user, created = Student.objects.update_or_create(
                registration_number=registration_number,
                defaults={
                    'registration_number': registration_number,
                    'roll_number': roll_number,
                    'first_name': first_name,
                    'last_name': last_name,
                    'attendance': attendance,
                    'cie_marks': cie_marks,
                    'batch': batch,
                    'division': division,
                }
            )
            student_user.subjects.set(subjects)
            student_user.save()
            return redirect('faculty')

    else:
        form = StudentForm() 

    return render(request, 'add_student.html', {'form': form})
    
@login_required
def view_student(request, registration_number):
    student = Student.objects.get(registration_number=registration_number)
    student_subjects = StudentSubject.objects.filter(student=student)
    teacher_subjects = request.user.faculty.subjects.all() 

    # Create a list of subjects with a flag indicating if the teacher is assigned
    student_subjects_info = []
    attendance_total=0
    attendance_lab_total=0
    for student_subject in student_subjects:
        attendance_total = attendance_total + student_subject.subject_attendance
        attendance_lab_total = attendance_lab_total + student_subject.subject_lab_attendance
        is_teacher_assigned = teacher_subjects.filter(subject_id=student_subject.subject.subject_id).exists()
        student_subjects_info.append({
            'subject_attendance':student_subject.subject_attendance,
            'subject_lab_attendance':student_subject.subject_lab_attendance,
            'assignments_submitted':student_subject.assignments_submitted,
            'subject': student_subject.subject,
            'noc_signed': student_subject.noc_signed,
            'is_teacher_assigned': is_teacher_assigned
        })
        avg_att =int(attendance_total/7)
        avg_lab_att= int(attendance_lab_total/7)

    return render(request, 'view_student.html', {
        'student': student,
        'avg_att':avg_att,
        'avg_lab_att':avg_lab_att,
        'student_subjects_info': student_subjects_info,
    })


@login_required
def sign_noc_for_subject(request, registration_number, subject_id):
    student = Student.objects.get(registration_number=registration_number)
    subject = Subject.objects.get(subject_id=subject_id)
    
    if request.user.faculty.subjects.filter(subject_id=subject.subject_id).exists():
        student_subject = StudentSubject.objects.get(student=student, subject=subject)
        student_subject.noc_signed = True
        student_subject.save()
        messages.success(request, "NOC signed successfully!")
    else:
        messages.error(request, "You are not authorized to sign this NOC.")

    return redirect('view_student', registration_number=registration_number)

@login_required
def assignments_status(request, registration_number, subject_id):
    student = Student.objects.get(registration_number=registration_number)
    subject = Subject.objects.get(subject_id=subject_id)

    
    if request.user.faculty.subjects.filter(subject_id=subject.subject_id).exists():
        student_subject = StudentSubject.objects.get(student=student, subject=subject)
        student_subject.assignments_submitted = True
        student_subject.save()
        messages.success(request, "Assignments Collected")

    return redirect('view_student', registration_number=registration_number)


def student_success(request):
    return render(request, 'student_success.html')


def teacher_success(request):
    return render(request, 'teacher_success.html')
