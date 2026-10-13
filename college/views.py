
import re
import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    AdmissionApplication,
    College,
    EmailOTP,
    Notification,
    StudentProfile,
)


# =========================================================
# HELPER: RENDER ADMISSION FORM WITH CONTEXT
# =========================================================

def render_admission_form(
    request,
    colleges=None,
    college=None,
    selected_slugs=None,
    multiple_colleges=False,
):
    """
    Shared context for the common admission form.
    Supports either one college or multiple selected colleges.
    """
    context = {
        "college": college,
        "colleges": colleges or ([college] if college else []),
        "selected_slugs": selected_slugs or [],
        "multiple_colleges": multiple_colleges,
    }

    return render(request, "admission-form.html", context)


# =========================================================
# HELPER: VALIDATE ADMISSION FIELDS
# =========================================================

def validate_admission_form(request):
    guardian_cnic = request.POST.get("guardian_cnic", "").strip()
    student_cnic = request.POST.get("student_cnic", "").strip()
    guardian_contact = request.POST.get("guardian_contact", "").strip()
    student_contact = request.POST.get("student_contact", "").strip()

    if guardian_cnic and not re.fullmatch(r"\d{13}", guardian_cnic):
        return "Guardian CNIC must contain exactly 13 digits."

    if student_cnic and not re.fullmatch(r"\d{13}", student_cnic):
        return "Student CNIC must contain exactly 13 digits."

    if guardian_contact and not re.fullmatch(r"\d{11}", guardian_contact):
        return "Guardian contact number must contain exactly 11 digits."

    if student_contact and not re.fullmatch(r"\d{11}", student_contact):
        return "Student contact number must contain exactly 11 digits."

    return None


# =========================================================
# HELPER: GET ADMISSION DATA FROM FORM
# =========================================================

def get_admission_data(request):
    """
    Prepare the common fields shared by admission applications.
    """
    return {
        "gender": request.POST.get("gender", "").strip(),
        "location": request.POST.get("location", "").strip(),
        "course": request.POST.get("course", "").strip(),
        "full_name": request.POST.get("full_name", "").strip(),
        "father_name": request.POST.get("father_name", "").strip(),
        "relationship": request.POST.get("relationship", "").strip(),
        "guardian_cnic": request.POST.get("guardian_cnic", "").strip(),
        "student_cnic": request.POST.get("student_cnic", "").strip(),
        "date_of_birth": request.POST.get("date_of_birth") or None,
        "guardian_contact": request.POST.get("guardian_contact", "").strip(),
        "student_contact": request.POST.get("student_contact", "").strip(),
        "email": request.POST.get("email", "").strip(),
        "address": request.POST.get("address", "").strip(),
        "degree": request.POST.get("degree", "").strip(),
        "passing_year": request.POST.get("passing_year", "").strip(),
        "board": request.POST.get("board", "").strip(),
        "group": request.POST.get("group", "").strip(),
        "obtained_marks": request.POST.get("obtained_marks", "").strip(),
        "total_marks": request.POST.get("total_marks", "").strip(),
        "board_roll_no": request.POST.get("board_roll_no", "").strip(),
        "previous_school": request.POST.get("previous_school", "").strip(),
        "heard_about_us": request.POST.get("heard_about_us", "").strip(),
    }


# =========================================================
# HELPER: CREATE APPLICATIONS FOR SELECTED COLLEGES
# =========================================================

def create_applications_for_colleges(request, colleges, application_data):
    """
    Create applications using the same fields for one or more colleges.
    Atomic transaction prevents a partial set of applications.
    """
    with transaction.atomic():
        for college in colleges:
            AdmissionApplication.objects.create(
                student=request.user,
                college=college,
                **application_data,
            )


# =========================================================
# MAIN WEBSITE
# =========================================================

def home(request):
    colleges = College.objects.all().order_by("name")

    return render(
        request,
        "index.html",
        {"colleges": colleges},
    )


def college_detail(request, slug):
    """
    Display college details using its readable URL slug.
    Example: /college/superior-college-chishtian/
    """
    college = get_object_or_404(College, slug=slug)

    return render(
        request,
        "college_detail.html",
        {"college": college},
    )


# =========================================================
# COLLEGE HOME PAGES
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
    colleges = College.objects.all().order_by("name")

    return render(
        request,
        "choose-college.html",
        {"colleges": colleges},
    )


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

        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------
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
                    matching_user = users.first()

                    user = authenticate(
                        request,
                        username=matching_user.username,
                        password=password,
                    )

                    if user is None:
                        if not matching_user.is_active:
                            messages.error(
                                request,
                                "Please verify your email before logging in.",
                            )
                        else:
                            messages.error(
                                request,
                                "Invalid email or password.",
                            )
                    else:
                        login(request, user)
                        return redirect("choose-college")

        # -------------------------------------------------
        # SIGNUP
        # -------------------------------------------------
        elif form_type == "signup":
            full_name = request.POST.get("full_name", "").strip()
            mobile = request.POST.get("mobile", "").strip()
            confirm_password = request.POST.get("confirm_password", "")

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
                    validate_password(password)
                except ValidationError as error:
                    for message in error.messages:
                        messages.error(request, message)
                else:
                    existing_user = User.objects.filter(
                        email__iexact=email
                    ).first()

                    if existing_user and existing_user.is_active:
                        messages.error(
                            request,
                            "This email already has an account. Please log in.",
                        )
                    else:
                        try:
                            with transaction.atomic():
                                if existing_user is None:
                                    user = User.objects.create_user(
                                        username=email,
                                        email=email,
                                        first_name=full_name,
                                        password=password,
                                        is_active=False,
                                    )
                                else:
                                    user = existing_user
                                    user.email = email
                                    user.first_name = full_name
                                    user.set_password(password)
                                    user.save(
                                        update_fields=[
                                            "email",
                                            "first_name",
                                            "password",
                                        ]
                                    )

                                request.session[
                                    "pending_verification_email"
                                ] = email

                                request.session[
                                    "pending_verification_mobile"
                                ] = mobile

                                generate_email_otp(email)

                            messages.success(
                                request,
                                "A verification code has been sent to your email. "
                                "Please check your inbox.",
                            )
                            return redirect("verify-email")

                        except Exception:
                            request.session.pop(
                                "pending_verification_email", None
                            )
                            request.session.pop(
                                "pending_verification_mobile", None
                            )
                            messages.error(
                                request,
                                "We could not send the verification code. "
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
# EMAIL VERIFICATION
# =========================================================

def verify_email(request):
    email = request.session.get("pending_verification_email")
    mobile = request.session.get("pending_verification_mobile")

    if not email:
        messages.error(
            request,
            "Please sign up first to verify your email.",
        )
        return redirect("application-form")

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

            messages.error(
                request,
                "Incorrect verification code.",
            )

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
                    return redirect("application-form")

                profile, _ = StudentProfile.objects.get_or_create(user=user)

                if mobile and re.fullmatch(r"\d{11}", mobile):
                    profile.mobile = mobile
                    profile.save(update_fields=["mobile"])

                user.is_active = True
                user.save(update_fields=["is_active"])

                otp_record.is_verified = True
                otp_record.save(update_fields=["is_verified"])

            request.session.pop("pending_verification_email", None)
            request.session.pop("pending_verification_mobile", None)

            login(request, user)

            messages.success(
                request,
                "Email verified successfully!",
            )
            return redirect("choose-college")

    return render(
        request,
        "verify-email.html",
        {"email": email},
    )


# =========================================================
# RESEND EMAIL OTP
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


def resend_email_otp(request):
    if request.method != "POST":
        return redirect("verify-email")

    email = request.session.get("pending_verification_email")

    if not email:
        messages.error(
            request,
            "Please sign up first to verify your email.",
        )
        return redirect("application-form")

    latest_otp = EmailOTP.objects.filter(
        email__iexact=email,
        is_verified=False,
    ).order_by("-created_at").first()

    if latest_otp is not None:
        seconds_since_sent = (
            timezone.now() - latest_otp.created_at
        ).total_seconds()

        if seconds_since_sent < 60:
            wait_seconds = max(1, int(60 - seconds_since_sent))
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
            "A new verification code has been sent to your email. "
            "The previous code is no longer valid.",
        )

    return redirect("verify-email")


# =========================================================
# STUDENT DASHBOARD
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

    context = {
        "applications": applications,
        "total_applications": applications.count(),
        "pending_applications": applications.filter(status="Pending").count(),
        "approved_applications": applications.filter(status="Approved").count(),
        "rejected_applications": applications.filter(status="Rejected").count(),
        "unread_notifications_count": unread_notifications.count(),
        "latest_notification": unread_notifications.order_by(
            "-created_at"
        ).first(),
    }

    return render(request, "dashboard.html", context)


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
    student_profile, _ = StudentProfile.objects.get_or_create(
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
# LOGOUT
# =========================================================

def user_logout(request):
    logout(request)
    return redirect("application-form")


# =========================================================
# COMMON ADMISSION APPLICATION — SINGLE COLLEGE
# =========================================================

@login_required
def admission_application_common(request, slug):
    college = get_object_or_404(College, slug=slug)

    if request.method == "POST":
        validation_error = validate_admission_form(request)

        if validation_error:
            messages.error(request, validation_error)
            return render_admission_form(request, college=college)

        application_data = get_admission_data(request)

        try:
            create_applications_for_colleges(
                request,
                [college],
                application_data,
            )
        except (ValidationError, ValueError, TypeError):
            messages.error(
                request,
                "Some application information is invalid. Please review the form.",
            )
            return render_admission_form(request, college=college)

        messages.success(
            request,
            f"Your admission application for {college.name} "
            "has been submitted successfully!",
        )
        return redirect("dashboard")

    return render_admission_form(request, college=college)


# =========================================================
# LEGACY ADMISSION URL — PGC
# =========================================================

@login_required
def admission_application(request):
    """
    Preserve the existing admission-application URL.
    The college is looked up dynamically by its existing database name.
    """
    college = get_object_or_404(
        College,
        name="Punjab College Chishtian",
    )

    if request.method == "POST":
        validation_error = validate_admission_form(request)

        if validation_error:
            messages.error(request, validation_error)
            return render(request, "applypgc.html", {"college": college})

        try:
            create_applications_for_colleges(
                request,
                [college],
                get_admission_data(request),
            )
        except (ValidationError, ValueError, TypeError):
            messages.error(
                request,
                "Some application information is invalid. Please review the form.",
            )
            return render(request, "applypgc.html", {"college": college})

        messages.success(
            request,
            "Your admission application has been submitted successfully!",
        )
        return redirect("dashboard")

    return render(request, "applypgc.html", {"college": college})


# =========================================================
# COMMON ADMISSION APPLICATION — MULTIPLE COLLEGES
# =========================================================

@login_required
def admission_application_multiple(request):
    if request.method != "POST":
        return redirect("choose-college")

    # -----------------------------------------------------
    # STAGE 1: COLLEGE SELECTION
    # -----------------------------------------------------
    if request.POST.get("submission_stage") != "admission_form":
        selected_slugs = list(dict.fromkeys(
            request.POST.getlist("college_slugs")
        ))

        if not selected_slugs:
            messages.error(
                request,
                "Please select at least one college.",
            )
            return redirect("choose-college")

        colleges_by_slug = {
            college.slug: college
            for college in College.objects.filter(
                slug__in=selected_slugs
            )
        }

        if (
            len(colleges_by_slug) != len(selected_slugs)
            or any(not slug for slug in selected_slugs)
        ):
            messages.error(
                request,
                "One or more selected colleges are invalid.",
            )
            return redirect("choose-college")

        colleges = [colleges_by_slug[slug] for slug in selected_slugs]

        return render_admission_form(
            request,
            colleges=colleges,
            selected_slugs=selected_slugs,
            multiple_colleges=True,
        )

    # -----------------------------------------------------
    # STAGE 2: FINAL FORM SUBMISSION
    # -----------------------------------------------------
    selected_slugs = list(dict.fromkeys(
        request.POST.getlist("selected_college_slugs")
    ))

    if not selected_slugs or any(not slug for slug in selected_slugs):
        messages.error(
            request,
            "No valid colleges were selected. Please start again.",
        )
        return redirect("choose-college")

    colleges_by_slug = {
        college.slug: college
        for college in College.objects.filter(
            slug__in=selected_slugs
        )
    }

    if len(colleges_by_slug) != len(selected_slugs):
        messages.error(
            request,
            "One or more selected colleges are invalid.",
        )
        return redirect("choose-college")

    colleges = [colleges_by_slug[slug] for slug in selected_slugs]

    required_fields = [
        "gender",
        "location",
        "course",
        "full_name",
        "father_name",
        "relationship",
        "guardian_cnic",
        "student_cnic",
        "date_of_birth",
        "guardian_contact",
        "email",
        "degree",
        "passing_year",
        "board",
        "group",
        "obtained_marks",
        "total_marks",
        "board_roll_no",
        "previous_school",
        "heard_about_us",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not request.POST.get(field, "").strip()
    ]

    if missing_fields:
        messages.error(
            request,
            "Please complete all required fields.",
        )
        return render_admission_form(
            request,
            colleges=colleges,
            selected_slugs=selected_slugs,
            multiple_colleges=True,
        )

    if request.POST.get("confirm_terms") not in {"on", "yes", "true", "1"}:
        messages.error(
            request,
            "Please accept the terms and conditions.",
        )
        return render_admission_form(
            request,
            colleges=colleges,
            selected_slugs=selected_slugs,
            multiple_colleges=True,
        )

    validation_error = validate_admission_form(request)

    if validation_error:
        messages.error(request, validation_error)
        return render_admission_form(
            request,
            colleges=colleges,
            selected_slugs=selected_slugs,
            multiple_colleges=True,
        )

    application_data = get_admission_data(request)

    try:
        create_applications_for_colleges(
            request,
            colleges,
            application_data,
        )
    except (ValidationError, ValueError, TypeError):
        messages.error(
            request,
            "Some application information is invalid. Please review the form.",
        )
        return render_admission_form(
            request,
            colleges=colleges,
            selected_slugs=selected_slugs,
            multiple_colleges=True,
        )

    messages.success(
        request,
        f"Applications submitted successfully to {len(colleges)} college(s).",
    )
    return redirect("dashboard")


# =========================================================
# CUSTOM ERROR PAGES
# =========================================================

def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_403(request, exception):
    return render(request, "403.html", status=403)


def error_500(request):
    return render(request, "500.html", status=500)
