from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

from .models import College, AdmissionApplication, StudentProfile


# =========================
# MAIN WEBSITE
# =========================

def home(request):
    colleges = College.objects.all()

    return render(
        request,
        'index.html',
        {'colleges': colleges}
    )


def college_detail(request, id):
    college = get_object_or_404(
        College,
        id=id
    )

    return render(
        request,
        'college_detail.html',
        {'college': college}
    )


# =========================
# COLLEGES
# =========================

def superior(request):
    return render(
        request,
        'superior.html'
    )


def pgc(request):
    return render(
        request,
        'pgc.html'
    )


def chishtian_science(request):
    return render(
        request,
        'chishtian science.html'
    )


def ripah(request):
    return render(
        request,
        'ripah.html'
    )


# =========================
# CHOOSE COLLEGE
# =========================

@login_required
def choose_college(request):
    colleges = College.objects.all()

    return render(
        request,
        'choose-college.html',
        {'colleges': colleges}
    )


# =========================
# SIGN UP / LOGIN
# =========================

def application_form(request):

    if request.method == 'POST':

        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # =========================
        # LOGIN
        # =========================

        if request.POST.get('full_name') is None:

            user = authenticate(
                request,
                username=user_id,
                password=password
            )

            if user is not None:

                login(
                    request,
                    user
                )

                return redirect(
                    'dashboard'
                )

            messages.error(
                request,
                'Invalid User ID or Password.'
            )

            return render(
                request,
                'application-form.html'
            )

        # =========================
        # SIGN UP
        # =========================

        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        full_name = request.POST.get('full_name')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return render(
                request,
                'application-form.html'
            )

        if User.objects.filter(
            username=user_id
        ).exists():

            messages.error(
                request,
                'This User ID already exists.'
            )

            return render(
                request,
                'application-form.html'
            )

        user = User.objects.create_user(
            username=user_id,
            email=email,
            password=password,
            first_name=full_name
        )

        login(
            request,
            user
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'application-form.html'
    )


# =========================
# STUDENT DASHBOARD
# =========================

@login_required
def dashboard(request):

    applications = AdmissionApplication.objects.filter(
        student=request.user
    ).order_by(
        '-created_at'
    )

    total_applications = applications.count()

    pending_applications = applications.filter(
        status='Pending'
    ).count()

    approved_applications = applications.filter(
        status='Approved'
    ).count()

    rejected_applications = applications.filter(
        status='Rejected'
    ).count()

    return render(
        request,
        'dashboard.html',
        {
            'applications': applications,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'approved_applications': approved_applications,
            'rejected_applications': rejected_applications,
        }
    )


# =========================
# STUDENT PROFILE
# =========================

@login_required
def profile(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        action = request.POST.get(
            'action'
        )

        # =========================
        # UPLOAD / CHANGE PICTURE
        # =========================

        if action == 'upload_picture':

            picture = request.FILES.get(
                'profile_picture'
            )

            if picture:

                profile.profile_picture = picture
                profile.save()

                messages.success(
                    request,
                    'Profile picture updated successfully.'
                )

            else:

                messages.error(
                    request,
                    'Please select a picture first.'
                )

            return redirect(
                'profile'
            )

        # =========================
        # REMOVE PICTURE
        # =========================

        if action == 'remove_picture':

            if profile.profile_picture:

                profile.profile_picture.delete(
                    save=False
                )

                profile.profile_picture = None
                profile.save()

                messages.success(
                    request,
                    'Profile picture removed successfully.'
                )

            else:

                messages.info(
                    request,
                    'You do not have a profile picture.'
                )

            return redirect(
                'profile'
            )

    applications_count = AdmissionApplication.objects.filter(
        student=request.user
    ).count()

    return render(
        request,
        'profile.html',
        {
            'applications_count': applications_count,
            'student_profile': profile,
        }
    )


# =========================
# APPLICATION DETAILS
# =========================

@login_required
def application_detail(request, id):

    application = get_object_or_404(
        AdmissionApplication,
        id=id,
        student=request.user
    )

    return render(
        request,
        'application-detail.html',
        {
            'application': application
        }
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect(
        'application-form'
    )


# =========================
# ADMISSION FORM VALIDATION
# =========================

def validate_admission_form(request):

    guardian_cnic = request.POST.get(
        'guardian_cnic',
        ''
    ).strip()

    student_cnic = request.POST.get(
        'student_cnic',
        ''
    ).strip()

    guardian_contact = request.POST.get(
        'guardian_contact',
        ''
    ).strip()

    student_contact = request.POST.get(
        'student_contact',
        ''
    ).strip()

    # =========================
    # GUARDIAN CNIC
    # =========================

    if guardian_cnic:

        if not re.fullmatch(
            r'\d{13}',
            guardian_cnic
        ):

            return (
                'Guardian CNIC must contain exactly 13 digits.'
            )

    # =========================
    # STUDENT CNIC
    # =========================

    if student_cnic:

        if not re.fullmatch(
            r'\d{13}',
            student_cnic
        ):

            return (
                'Student CNIC must contain exactly 13 digits.'
            )

    # =========================
    # GUARDIAN CONTACT
    # =========================

    if guardian_contact:

        if not re.fullmatch(
            r'\d{11}',
            guardian_contact
        ):

            return (
                'Guardian contact number must contain exactly 11 digits.'
            )

    # =========================
    # STUDENT CONTACT
    # =========================

    if student_contact:

        if not re.fullmatch(
            r'\d{11}',
            student_contact
        ):

            return (
                'Student contact number must contain exactly 11 digits.'
            )

    return None


# =========================
# PGC ADMISSION APPLICATION
# =========================

@login_required
def admission_application(request):

    if request.method == 'POST':

        validation_error = validate_admission_form(request)

        if validation_error:

            messages.error(
                request,
                validation_error
            )

            return render(
                request,
                'applypgc.html'
            )

        college = get_object_or_404(
            College,
            name='Punjab College Chishtian'
        )

        AdmissionApplication.objects.create(

            student=request.user,

            college=college,

            gender=request.POST.get('gender', ''),

            location=request.POST.get('location', ''),

            course=request.POST.get('course', ''),

            full_name=request.POST.get('full_name', ''),

            father_name=request.POST.get('father_name', ''),

            relationship=request.POST.get('relationship', ''),

            guardian_cnic=request.POST.get('guardian_cnic', ''),

            student_cnic=request.POST.get('student_cnic', ''),

            date_of_birth=(
                request.POST.get('date_of_birth')
                or None
            ),

            guardian_contact=request.POST.get(
                'guardian_contact',
                ''
            ),

            student_contact=request.POST.get(
                'student_contact',
                ''
            ),

            email=request.POST.get(
                'email',
                ''
            ),

            address=request.POST.get(
                'address',
                ''
            ),

            degree=request.POST.get(
                'degree',
                ''
            ),

            passing_year=request.POST.get(
                'passing_year',
                ''
            ),

            board=request.POST.get(
                'board',
                ''
            ),

            group=request.POST.get(
                'group',
                ''
            ),

            obtained_marks=request.POST.get(
                'obtained_marks',
                ''
            ),

            total_marks=request.POST.get(
                'total_marks',
                ''
            ),

            board_roll_no=request.POST.get(
                'board_roll_no',
                ''
            ),

            previous_school=request.POST.get(
                'previous_school',
                ''
            ),

            heard_about_us=request.POST.get(
                'heard_about_us',
                ''
            )
        )

        messages.success(
            request,
            'Your admission application has been submitted successfully!'
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'applypgc.html'
    )


# =========================
# CSC ADMISSION APPLICATION
# =========================

@login_required
def admission_application_csc(request):

    if request.method == 'POST':

        validation_error = validate_admission_form(request)

        if validation_error:

            messages.error(
                request,
                validation_error
            )

            return render(
                request,
                'applycsc.html'
            )

        college = get_object_or_404(
            College,
            name='Chishtian Science College'
        )

        AdmissionApplication.objects.create(

            student=request.user,

            college=college,

            gender=request.POST.get('gender', ''),

            location=request.POST.get('location', ''),

            course=request.POST.get('course', ''),

            full_name=request.POST.get('full_name', ''),

            father_name=request.POST.get('father_name', ''),

            relationship=request.POST.get('relationship', ''),

            guardian_cnic=request.POST.get('guardian_cnic', ''),

            student_cnic=request.POST.get('student_cnic', ''),

            date_of_birth=(
                request.POST.get('date_of_birth')
                or None
            ),

            guardian_contact=request.POST.get(
                'guardian_contact',
                ''
            ),

            student_contact=request.POST.get(
                'student_contact',
                ''
            ),

            email=request.POST.get(
                'email',
                ''
            ),

            address=request.POST.get(
                'address',
                ''
            ),

            degree=request.POST.get(
                'degree',
                ''
            ),

            passing_year=request.POST.get(
                'passing_year',
                ''
            ),

            board=request.POST.get(
                'board',
                ''
            ),

            group=request.POST.get(
                'group',
                ''
            ),

            obtained_marks=request.POST.get(
                'obtained_marks',
                ''
            ),

            total_marks=request.POST.get(
                'total_marks',
                ''
            ),

            board_roll_no=request.POST.get(
                'board_roll_no',
                ''
            ),

            previous_school=request.POST.get(
                'previous_school',
                ''
            ),

            heard_about_us=request.POST.get(
                'heard_about_us',
                ''
            )
        )

        messages.success(
            request,
            'Your CSC admission application has been submitted successfully!'
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'applycsc.html'
    )


# =========================
# RIPHAH ADMISSION APPLICATION
# =========================

@login_required
def admission_application_ripah(request):

    if request.method == 'POST':

        validation_error = validate_admission_form(request)

        if validation_error:

            messages.error(
                request,
                validation_error
            )

            return render(
                request,
                'applyrip.html'
            )

        college = get_object_or_404(
            College,
            name='Riphah International College'
        )

        AdmissionApplication.objects.create(

            student=request.user,

            college=college,

            gender=request.POST.get('gender', ''),

            location=request.POST.get('location', ''),

            course=request.POST.get('course', ''),

            full_name=request.POST.get('full_name', ''),

            father_name=request.POST.get('father_name', ''),

            relationship=request.POST.get('relationship', ''),

            guardian_cnic=request.POST.get('guardian_cnic', ''),

            student_cnic=request.POST.get('student_cnic', ''),

            date_of_birth=(
                request.POST.get('date_of_birth')
                or None
            ),

            guardian_contact=request.POST.get(
                'guardian_contact',
                ''
            ),

            student_contact=request.POST.get(
                'student_contact',
                ''
            ),

            email=request.POST.get(
                'email',
                ''
            ),

            address=request.POST.get(
                'address',
                ''
            ),

            degree=request.POST.get(
                'degree',
                ''
            ),

            passing_year=request.POST.get(
                'passing_year',
                ''
            ),

            board=request.POST.get(
                'board',
                ''
            ),

            group=request.POST.get(
                'group',
                ''
            ),

            obtained_marks=request.POST.get(
                'obtained_marks',
                ''
            ),

            total_marks=request.POST.get(
                'total_marks',
                ''
            ),

            board_roll_no=request.POST.get(
                'board_roll_no',
                ''
            ),

            previous_school=request.POST.get(
                'previous_school',
                ''
            ),

            heard_about_us=request.POST.get(
                'heard_about_us',
                ''
            )
        )

        messages.success(
            request,
            'Your Riphah International College admission application has been submitted successfully!'
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'applyrip.html'
    )


# =========================
# SUPERIOR COLLEGE ADMISSION APPLICATION
# =========================

@login_required
def admission_application_superior(request):

    if request.method == 'POST':

        validation_error = validate_admission_form(request)

        if validation_error:

            messages.error(
                request,
                validation_error
            )

            return render(
                request,
                'applysuperior.html'
            )

        college = get_object_or_404(
            College,
            name='Superior College Chishtian'
        )

        AdmissionApplication.objects.create(

            student=request.user,

            college=college,

            gender=request.POST.get('gender', ''),

            location=request.POST.get('location', ''),

            course=request.POST.get('course', ''),

            full_name=request.POST.get('full_name', ''),

            father_name=request.POST.get('father_name', ''),

            relationship=request.POST.get('relationship', ''),

            guardian_cnic=request.POST.get('guardian_cnic', ''),

            student_cnic=request.POST.get('student_cnic', ''),

            date_of_birth=(
                request.POST.get('date_of_birth')
                or None
            ),

            guardian_contact=request.POST.get(
                'guardian_contact',
                ''
            ),

            student_contact=request.POST.get(
                'student_contact',
                ''
            ),

            email=request.POST.get(
                'email',
                ''
            ),

            address=request.POST.get(
                'address',
                ''
            ),

            degree=request.POST.get(
                'degree',
                ''
            ),

            passing_year=request.POST.get(
                'passing_year',
                ''
            ),

            board=request.POST.get(
                'board',
                ''
            ),

            group=request.POST.get(
                'group',
                ''
            ),

            obtained_marks=request.POST.get(
                'obtained_marks',
                ''
            ),

            total_marks=request.POST.get(
                'total_marks',
                ''
            ),

            board_roll_no=request.POST.get(
                'board_roll_no',
                ''
            ),

            previous_school=request.POST.get(
                'previous_school',
                ''
            ),

            heard_about_us=request.POST.get(
                'heard_about_us',
                ''
            )
        )

        messages.success(
            request,
            'Your Superior College admission application has been submitted successfully!'
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'applysuperior.html'
    )


# =========================
# CUSTOM ERROR PAGES
# =========================

def error_404(request, exception):

    return render(
        request,
        '404.html',
        status=404
    )


def error_403(request, exception):

    return render(
        request,
        '403.html',
        status=403
    )


def error_500(request):

    return render(
        request,
        '500.html',
        status=500
    )