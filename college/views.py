from django.views.decorators.http import require_http_methods
from datetime import timedelta
import re
import secrets
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect
from .models import TeachingApplication

from .models import (
    College,
    AdmissionApplication,
    StudentProfile,
    Notification,
    EmailOTP,
)


# =========================================================
# MAIN WEBSITE
# =========================================================

def home(request):
    colleges = College.objects.all()
    return render(request, "index.html", {"colleges": colleges})

def college_detail(request, slug):
    college = get_object_or_404(College, slug=slug)
    return render(request, "college_detail.html", {"college": college})

# =========================================================
# COLLEGE PAGES
# =========================================================

def superior(request):
    return render(request, "superior.html")


def pgc(request):
    return render(request, "pgc.html")


def chishtian_science(request):
    return render(request, "chishtian science.html")


def ripah(request):
    return render(request, "ripah.html")


# =========================================================
# CHOOSE COLLEGE
# =========================================================

@login_required
def choose_college(request):
    colleges = College.objects.all()
    return render(
        request,
        "choose-college.html",
        {"colleges": colleges},
    )


# =========================================================
# COMMON ADMISSION FORM
# =========================================================

@login_required
def admission_application_common(request, slug):
    college = get_object_or_404(College, slug=slug)

    field_names = [
        "full_name", "father_name", "gender", "date_of_birth",
        "relationship", "student_cnic", "guardian_cnic",
        "student_contact", "guardian_contact", "email", "address",
        "location", "heard_about_us", "course", "degree",
        "passing_year", "board", "group", "board_roll_no",
        "obtained_marks", "total_marks", "previous_school",
    ]

    data = {field: "" for field in field_names}
    data["gender"] = ""
    data["heard_about_us"] = ""

    if request.method == "POST":
        data = {
            field: request.POST.get(field, "").strip()
            for field in field_names
        }

        errors = []

        required_fields = {
            "full_name": "Student name",
            "father_name": "Father's name",
            "gender": "Gender",
            "date_of_birth": "Date of birth",
            "guardian_contact": "Guardian contact",
            "email": "Email",
            "address": "Address",
            "course": "Course",
        }

        for field, label in required_fields.items():
            if not data[field]:
                errors.append(f"{label} is required.")

        dob = None
        if data["date_of_birth"]:
            try:
                dob = parse_date(data["date_of_birth"])
            except (ValueError, TypeError):
                dob = None

            if dob is None:
                errors.append("Enter a valid date of birth.")
            elif dob > timezone.localdate():
                errors.append("Date of birth cannot be in the future.")

        if data["gender"] and data["gender"] not in ("Male", "Female"):
            errors.append("Please select a valid gender.")

        if data["email"]:
            try:
                validate_email(data["email"])
            except ValidationError:
                errors.append("Enter a valid email address.")

        for field, label in (
            ("student_cnic", "Student CNIC"),
            ("guardian_cnic", "Guardian CNIC"),
        ):
            value = data[field]
            if value and not re.fullmatch(r"[0-9]{13}", value):
                errors.append(f"{label} must contain exactly 13 digits.")

        for field, label in (
            ("student_contact", "Student contact"),
            ("guardian_contact", "Guardian contact"),
        ):
            value = data[field]
            if value and not re.fullmatch(r"[0-9]{11}", value):
                errors.append(f"{label} must contain exactly 11 digits.")

        if request.POST.get("confirm_terms") != "on":
            errors.append("Please accept the terms before submitting.")

        if errors:
            for error in errors:
                messages.error(request, error)

        else:
            AdmissionApplication.objects.create(
                student=request.user,
                college=college,
                full_name=data["full_name"],
                father_name=data["father_name"],
                gender=data["gender"],
                date_of_birth=dob,
                relationship=data["relationship"],
                student_cnic=data["student_cnic"],
                guardian_cnic=data["guardian_cnic"],
                student_contact=data["student_contact"],
                guardian_contact=data["guardian_contact"],
                email=data["email"],
                address=data["address"],
                location=data["location"],
                heard_about_us=data["heard_about_us"],
                course=data["course"],
                degree=data["degree"],
                passing_year=data["passing_year"],
                board=data["board"],
                group=data["group"],
                board_roll_no=data["board_roll_no"],
                obtained_marks=data["obtained_marks"],
                total_marks=data["total_marks"],
                previous_school=data["previous_school"],
                status="Pending",
            )

            messages.success(
                request,
                f"Your admission application for {college.name} "
                "was submitted successfully.",
            )
            return redirect("dashboard")

    return render(
        request,
        "admission-form.html",
        {
            "college": college,
            "form_data": data,
            "terms_checked": (
                request.method == "POST"
                and request.POST.get("confirm_terms") == "on"
            ),
        },
    )

# =========================================================
# LEGACY APPLY URLS
# Keep existing URL names, but use the common form
# =========================================================

def _redirect_to_common_admission(college_name):
    college = get_object_or_404(College, name=college_name)
    return redirect("admission-form", slug=college.slug)


@login_required
def admission_application(request):
    return _redirect_to_common_admission(
        "Punjab College Chishtian"
    )


@login_required
def admission_application_csc(request):
    return _redirect_to_common_admission(
        "Chishtian Science College"
    )


@login_required
def admission_application_ripah(request):
    return _redirect_to_common_admission(
        "Riphah International College"
    )


@login_required
def admission_application_superior(request):
    return _redirect_to_common_admission(
        "Superior College Chishtian"
    )


# =========================================================
# SINGLE-COLLEGE SELECTION SUBMISSION
# The template sends college_slug, not college_slugs
# =========================================================

@login_required
def admission_application_multiple(request):
    if request.method != "POST":
        return redirect("choose-college")

    selected_slug = request.POST.get("college_slug", "").strip()

    if not selected_slug:
        messages.error(request, "Please select one college.")
        return redirect("choose-college")

    college = get_object_or_404(College, slug=selected_slug)

    return redirect("admission-form", slug=college.slug)


# =========================================================
# SIGN UP / LOGIN
# =========================================================


def application_form(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    show_login = request.GET.get("mode") == "login"

    if request.method == "POST":
        form_type = request.POST.get("form_type", "signup")
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if form_type == "login":
            show_login = True

            if not email or not password:
                messages.error(
                    request,
                    "Please enter your email and password.",
                )
            else:
                users = User.objects.filter(email__iexact=email)

                if users.count() != 1:
                    messages.error(
                        request,
                        "Invalid email or password.",
                    )
                else:
                    user_record = users.first()
                    user = authenticate(
                        request,
                        username=user_record.username,
                        password=password,
                    )

                    if user is None:
                        messages.error(
                            request,
                            "Invalid email or password.",
                        )
                    else:
                        login(request, user)
                        return redirect("choose-college")

        elif form_type == "signup":
            full_name = request.POST.get(
                "full_name", ""
            ).strip()
            mobile = request.POST.get(
                "mobile", ""
            ).strip()
            confirm_password = request.POST.get(
                "confirm_password", ""
            )

            if not all([
                full_name,
                email,
                mobile,
                password,
                confirm_password,
            ]):
                messages.error(
                    request,
                    "Please complete all required fields.",
                )

            elif not re.fullmatch(r"\d{11}", mobile):
                messages.error(
                    request,
                    "Mobile number must contain exactly 11 digits.",
                )

            elif password != confirm_password:
                messages.error(
                    request,
                    "Passwords do not match.",
                )

            else:
                try:
                    validate_email(email)
                    validate_password(password)
                except ValidationError as error:
                    for message in error.messages:
                        messages.error(request, message)
                else:
                    existing_user = User.objects.filter(
                        email__iexact=email
                    ).first()

                    if existing_user is not None:
                        messages.error(
                            request,
                            "This email already has an account. Please log in.",
                        )
                    else:
                        try:
                            with transaction.atomic():
                                user = User.objects.create_user(
                                    username=email,
                                    email=email,
                                    first_name=full_name,
                                    password=password,
                                    is_active=True,
                                )

                                profile, created = (
                                    StudentProfile.objects.get_or_create(
                                        user=user
                                    )
                                )
                                profile.mobile = mobile
                                profile.save(
                                    update_fields=["mobile"]
                                )

                            messages.success(
                                request,
                                "Your account was created successfully. "
                                "You can now log in.",
                            )
                            return redirect("/accounts/login/?mode=login")

                        except Exception:
                            messages.error(
                                request,
                                "We could not create your account. "
                                "Please try again.",
                            )

        else:
            messages.error(
                request,
                "Invalid form submission.",
            )

    return render(
        request,
        "application-form.html",
        {"show_login": show_login},
    )

# =========================================================
# EMAIL OTP VERIFICATION
# =========================================================

def verify_email(request):
    email = request.session.get("pending_verification_email")
    mobile = request.session.get("pending_verification_mobile")

    if not email:
        messages.error(
            request,
            "Please sign up first to verify your email.",
        )
        return redirect("login")

    if request.method == "POST":
        code = request.POST.get("otp", "").strip()

        otp_record = EmailOTP.objects.filter(
            email__iexact=email,
            is_verified=False,
        ).order_by("-created_at").first()

        if otp_record is None:
            messages.error(
                request,
                "No active verification code found. Please sign up again.",
            )

        elif timezone.now() >= otp_record.expires_at:
            messages.error(
                request,
                "Your verification code has expired. Please request a new one.",
            )

        elif otp_record.attempts >= 5:
            messages.error(
                request,
                "Too many incorrect attempts. Please request a new code.",
            )

        elif not check_password(code, otp_record.code_hash):
            otp_record.attempts += 1
            otp_record.save(update_fields=["attempts"])
            messages.error(request, "Incorrect verification code.")

        else:
            with transaction.atomic():
                user = User.objects.select_for_update().filter(
                    email__iexact=email,
                    is_active=False,
                ).first()

                if user is None:
                    messages.error(
                        request,
                        "Account not found or already verified. Please log in.",
                    )
                    return redirect("login")

                profile, created = StudentProfile.objects.get_or_create(
                    user=user
                )

                if mobile and re.fullmatch(r"\d{11}", mobile):
                    profile.mobile = mobile
                    profile.save(update_fields=["mobile"])

                user.is_active = True
                user.save(update_fields=["is_active"])

                otp_record.is_verified = True
                otp_record.save(update_fields=["is_verified"])

            request.session.pop(
                "pending_verification_email", None
            )
            request.session.pop(
                "pending_verification_mobile", None
            )

            login(request, user)
            messages.success(request, "Email verified successfully!")
            return redirect("choose-college")

    return render(
        request,
        "verify-email.html",
        {"email": email},
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):
    applications = AdmissionApplication.objects.filter(
        student=request.user
    ).order_by("-created_at")

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
    )

    return render(
        request,
        "dashboard.html",
        {
            "applications": applications,
            "total_applications": applications.count(),
            "pending_applications": applications.filter(
                status="Pending"
            ).count(),
            "approved_applications": applications.filter(
                status="Approved"
            ).count(),
            "rejected_applications": applications.filter(
                status="Rejected"
            ).count(),
            "unread_notifications_count": unread_notifications.count(),
            "latest_notification": unread_notifications.first(),
        },
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@login_required
def notifications(request):
    notifications_list = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications.html",
        {"notifications": notifications_list},
    )


@login_required
def mark_notification_read(request, id):
    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user,
    )

    notification.is_read = True
    notification.save(update_fields=["is_read"])

    if notification.application:
        return redirect(
            "application-detail",
            id=notification.application.id,
        )

    return redirect("notifications")


@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(is_read=True)

    return redirect("notifications")


# =========================================================
# STUDENT PROFILE
# =========================================================

@login_required
def profile(request):
    student_profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "upload_picture":
            picture = request.FILES.get("profile_picture")

            if picture:
                student_profile.profile_picture = picture
                student_profile.save()
                messages.success(
                    request,
                    "Profile picture updated successfully.",
                )
            else:
                messages.error(
                    request,
                    "Please select a picture first.",
                )

            return redirect("profile")

        if action == "remove_picture":
            if student_profile.profile_picture:
                student_profile.profile_picture.delete(save=False)
                student_profile.profile_picture = None
                student_profile.save()
                messages.success(
                    request,
                    "Profile picture removed successfully.",
                )
            else:
                messages.info(
                    request,
                    "You do not have a profile picture.",
                )

            return redirect("profile")

    applications_count = AdmissionApplication.objects.filter(
        student=request.user
    ).count()

    return render(
        request,
        "profile.html",
        {
            "applications_count": applications_count,
            "student_profile": student_profile,
        },
    )


# =========================================================
# APPLICATION DETAILS
# =========================================================

@login_required
def application_detail(request, id):
    application = get_object_or_404(
        AdmissionApplication,
        id=id,
        student=request.user,
    )

    return render(
        request,
        "application-detail.html",
        {"application": application},
    )

# =========================================================
# FORGOT PASSWORD
# =========================================================

@require_http_methods(["GET", "POST"])
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, "forgot-password.html")

        # Same response prevents revealing whether an account exists.
        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user:
            try:
                otp = f"{secrets.randbelow(1_000_000):06d}"
                now = timezone.now()

                # Send first; keep the old record if delivery fails.
                sent = send_mail(
                    "College Portal Password Reset Code",
                    (
                        f"Your password reset code is: {otp}\n\n"
                        "It expires in 10 minutes. "
                        "If you did not request this, ignore this email."
                    ),
                    None,
                    [user.email],
                    fail_silently=False,
                )

                if sent == 1:
                    EmailOTP.objects.filter(
                        email__iexact=email,
                        is_verified=False,
                    ).delete()

                    EmailOTP.objects.create(
                        email=email,
                        code_hash=make_password(otp),
                        expires_at=now + timedelta(minutes=10),
                    )

                    request.session["password_reset_email"] = email
                    request.session["password_reset_user_id"] = user.id
                else:
                    # Do not disclose whether the email exists.
                    pass

            except Exception:
                # Keep the public response generic.
                pass

        messages.success(
            request,
            "If an active account exists for that email, a reset code "
            "will be sent. Check your inbox and spam folder."
        )
        return redirect("reset-password")

    return render(request, "forgot-password.html")


@require_http_methods(["GET", "POST"])
def reset_password(request):
    email = request.session.get("password_reset_email")
    user_id = request.session.get("password_reset_user_id")

    if not email or not user_id:
        messages.error(
            request,
            "Please request a password reset code first."
        )
        return redirect("forgot-password")

    if request.method == "POST":
        code = request.POST.get("otp", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        record = EmailOTP.objects.filter(
            email__iexact=email,
            is_verified=False,
        ).order_by("-created_at").first()

        if not record:
            messages.error(request, "Please request a new reset code.")
        elif timezone.now() >= record.expires_at:
            messages.error(request, "The reset code has expired. Request a new one.")
        elif record.attempts >= 5:
            messages.error(request, "Too many attempts. Request a new code.")
        elif not check_password(code, record.code_hash):
            record.attempts += 1
            record.save(update_fields=["attempts"])
            messages.error(request, "Invalid reset code.")
        elif not password or password != confirm_password:
            messages.error(request, "Passwords are empty or do not match.")
        else:
            try:
                validate_password(password)
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
            else:
                with transaction.atomic():
                    user = User.objects.select_for_update().filter(
                        id=user_id,
                        email__iexact=email,
                        is_active=True,
                    ).first()

                    if not user:
                        messages.error(request, "Please request a new reset code.")
                        return redirect("forgot-password")

                    # Mark the code used and change password atomically.
                    record.is_verified = True
                    record.save(update_fields=["is_verified"])
                    user.set_password(password)
                    user.save(update_fields=["password"])

                request.session.pop("password_reset_email", None)
                request.session.pop("password_reset_user_id", None)

                messages.success(
                    request,
                    "Password changed successfully. Please log in."
                )
                return redirect("login")

    return render(request, "reset-password.html")


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):
    logout(request)
    return redirect("login")


# =========================================================
# EMAIL OTP GENERATION
# =========================================================

def generate_email_otp(email):
    email = email.strip().lower()
    otp = f"{secrets.randbelow(1_000_000):06d}"
    expires_at = timezone.now() + timedelta(minutes=5)

    sent = send_mail(
        subject="Your College Portal Verification Code",
        message=(
            f"Your email verification code is {otp}.\n\n"
            "This code expires in 5 minutes. "
            "If you did not request it, ignore this email."
        ),
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

    if sent != 1:
        raise RuntimeError("Verification email could not be sent.")

    EmailOTP.objects.filter(
        email__iexact=email,
        is_verified=False,
    ).delete()

    EmailOTP.objects.create(
        email=email,
        code_hash=make_password(otp),
        expires_at=expires_at,
    )


# =========================================================
# RESEND EMAIL OTP
# =========================================================

def resend_email_otp(request):
    if request.method != "POST":
        return redirect("verify-email")

    email = request.session.get("pending_verification_email")

    if not email:
        messages.error(
            request,
            "Please sign up first to verify your email.",
        )
        return redirect("login")

    latest_otp = EmailOTP.objects.filter(
        email__iexact=email,
        is_verified=False,
    ).order_by("-created_at").first()

    if latest_otp is not None:
        seconds_since_sent = (
            timezone.now() - latest_otp.created_at
        ).total_seconds()

        if seconds_since_sent < 60:
            wait_seconds = max(
                1, int(60 - seconds_since_sent)
            )
            messages.error(
                request,
                f"Please wait {wait_seconds} seconds before requesting another code.",
            )
            return redirect("verify-email")

    try:
        generate_email_otp(email)
    except Exception:
        messages.error(
            request,
            "We could not send a new code. Please try again later.",
        )
    else:
        messages.success(
            request,
            "A new verification code has been sent to your email.",
        )

    return redirect("verify-email")


# =========================================================
# CUSTOM ERROR PAGES
# =========================================================

def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_403(request, exception):
    return render(request, "403.html", status=403)


def error_500(request):
    return render(request, "500.html", status=500)

def formteachpgc(request):
    if request.method == "POST":
        data = request.POST
        errors = []

        required_fields = [
            "name", "father_name", "date_of_birth", "nationality",
            "cnic", "domicile", "email", "phone", "department",
            "last_degree", "degree_title", "passing_year",
            "university", "institution", "marks_cgpa", "specialization",
        ]

        for field in required_fields:
            if not data.get(field, "").strip():
                errors.append(f"{field.replace('_', ' ').title()} is required.")

        email = data.get("email", "").strip()
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Please enter a valid email address.")

        cnic = data.get("cnic", "").strip()
        if not cnic.isdigit() or len(cnic) != 13:
            errors.append("CNIC must contain exactly 13 digits.")

        try:
            dob = date.fromisoformat(data.get("date_of_birth", ""))
            if dob >= date.today():
                errors.append("Date of birth must be in the past.")
        except (ValueError, TypeError):
            dob = None
            errors.append("Please enter a valid date of birth.")

        try:
            passing_year = int(data.get("passing_year", ""))
            if not 1950 <= passing_year <= date.today().year:
                errors.append("Please enter a valid passing year.")
        except (ValueError, TypeError):
            passing_year = None
            errors.append("Passing year must be a number.")

        department = data.get("department", "")
        if department not in dict(TeachingApplication.DEPARTMENT_CHOICES):
            errors.append("Please select a valid department.")

        degree = data.get("last_degree", "")
        if degree not in dict(TeachingApplication.DEGREE_CHOICES):
            errors.append("Please select a valid degree.")

        experience = data.get("experience", "")
        if experience and experience not in dict(TeachingApplication.EXPERIENCE_CHOICES):
            errors.append("Please select a valid experience range.")

        cv = request.FILES.get("cv")
        other_documents = request.FILES.get("other_documents")

        if not cv:
            errors.append("Please upload your CV.")

        allowed_extensions = {".pdf", ".doc", ".docx"}
        max_size = 5 * 1024 * 1024

        for uploaded_file, label in [
            (cv, "CV"),
            (other_documents, "Other document"),
        ]:
            if uploaded_file:
                filename = uploaded_file.name.lower()
                extension = "." + filename.rsplit(".", 1)[-1] if "." in filename else ""
                if extension not in allowed_extensions:
                    errors.append(f"{label} must be a PDF, DOC, or DOCX file.")
                if uploaded_file.size > max_size:
                    errors.append(f"{label} must be 5 MB or smaller.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "formteachpgc.html")

        TeachingApplication.objects.create(
            name=data["name"].strip(),
            father_name=data["father_name"].strip(),
            date_of_birth=dob,
            nationality=data["nationality"].strip(),
            cnic=cnic,
            domicile=data["domicile"].strip(),
            present_address=data.get("present_address", "").strip(),
            permanent_address=data.get("permanent_address", "").strip(),
            email=email,
            phone=data["phone"].strip(),
            department=department,
            campus=data.get("campus", "").strip(),
            last_degree=degree,
            degree_title=data["degree_title"].strip(),
            passing_year=passing_year,
            university=data["university"].strip(),
            institution=data["institution"].strip(),
            marks_cgpa=data["marks_cgpa"].strip(),
            specialization=data["specialization"].strip(),
            experience=experience,
            last_organization=data.get("last_organization", "").strip(),
            reference_1=data.get("reference_1", "").strip(),
            reference_2=data.get("reference_2", "").strip(),
            cv=cv,
            other_documents=other_documents,
        )

        messages.success(
            request,
            "Your teaching application has been submitted successfully."
        )
        return redirect("formteachpgc")

    return render(request, "formteachpgc.html")
def formteachcsc(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        errors = []

        required_fields = [
            "name", "father_name", "date_of_birth",
            "nationality", "cnic", "domicile",
            "present_address", "permanent_address",
            "email", "phone", "department",
            "last_degree", "degree_title", "passing_year",
            "university", "institution", "marks_cgpa",
            "specialization",
        ]

        for field in required_fields:
            if not data.get(field, "").strip():
                errors.append(
                    f"{field.replace('_', ' ').title()} is required."
                )

        dob = None
        try:
            dob = date.fromisoformat(data.get("date_of_birth", ""))
            if dob > date.today():
                errors.append("Date of birth cannot be in the future.")
        except (ValueError, TypeError):
            errors.append("Please enter a valid date of birth.")

        cnic = re.sub(r"\D", "", data.get("cnic", ""))
        if len(cnic) != 13:
            errors.append("CNIC must contain 13 digits.")

        year_text = data.get("passing_year", "").strip()
        year = None
        if not year_text.isdigit() or len(year_text) != 4:
            errors.append("Enter a valid four-digit passing year.")
        else:
            year = int(year_text)
            if year < 1950 or year > date.today().year + 1:
                errors.append("Please enter a valid passing year.")

        allowed_extensions = {".pdf", ".doc", ".docx"}

        def valid_file(upload, max_size):
            if not upload:
                return False
            extension = (
                "." + upload.name.rsplit(".", 1)[-1].lower()
                if "." in upload.name else ""
            )
            return (
                extension in allowed_extensions
                and upload.size <= max_size
            )

        cv = files.get("cv")
        other_documents = files.get("other_documents")

        if not cv:
            errors.append("Please upload your CV.")
        elif not valid_file(cv, 5 * 1024 * 1024):
            errors.append("CV must be PDF, DOC, or DOCX and no larger than 5 MB.")

        if other_documents and not valid_file(
            other_documents, 10 * 1024 * 1024
        ):
            errors.append(
                "Other documents must be PDF, DOC, or DOCX and no larger than 10 MB."
            )

        department = data.get("department", "")
        if department not in dict(TeachingApplication.DEPARTMENT_CHOICES):
            errors.append("Please select a valid department.")

        degree = data.get("last_degree", "")
        if degree not in dict(TeachingApplication.DEGREE_CHOICES):
            errors.append("Please select a valid degree.")

        experience = data.get("experience", "")
        if experience and experience not in dict(
            TeachingApplication.EXPERIENCE_CHOICES
        ):
            errors.append("Please select a valid experience option.")

        if errors:
            for error in errors:
                messages.error(request, error)

            return render(
                request,
                "formteachcsc.html",
                {"form_data": data},
            )

        TeachingApplication.objects.create(
            name=data["name"].strip(),
            father_name=data["father_name"].strip(),
            date_of_birth=dob,
            nationality=data["nationality"].strip(),
            cnic=cnic,
            domicile=data["domicile"].strip(),
            present_address=data["present_address"].strip(),
            permanent_address=data["permanent_address"].strip(),
            email=data["email"].strip(),
            phone=data["phone"].strip(),
            department=department,
            campus="CSC",
            last_degree=degree,
            degree_title=data["degree_title"].strip(),
            passing_year=year,
            university=data["university"].strip(),
            institution=data["institution"].strip(),
            marks_cgpa=data["marks_cgpa"].strip(),
            specialization=data["specialization"].strip(),
            experience=experience,
            last_organization=data.get("last_organization", "").strip(),
            reference_1=data.get("reference_1", "").strip(),
            reference_2=data.get("reference_2", "").strip(),
            cv=cv,
            other_documents=other_documents,
        )

        messages.success(
            request,
            "Your Chishtian Science College application was submitted successfully!"
        )
        return redirect("formteachcsc")

    return render(request, "formteachcsc.html", {"form_data": {}})
