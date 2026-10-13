
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# =========================================================
# COLLEGE
# =========================================================

class College(models.Model):

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
    )

    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    image = models.ImageField(
        upload_to="colleges/",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        # Generate a slug automatically when it is missing.
        if not self.slug:
            base_slug = slugify(self.name) or "college"
            candidate = base_slug
            counter = 2

            while College.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                suffix = f"-{counter}"
                candidate = f"{base_slug[:220 - len(suffix)]}{suffix}"
                counter += 1

            self.slug = candidate

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# STUDENT PROFILE
# =========================================================

class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    mobile = models.CharField(
        max_length=11,
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.user.username} Profile"


# =========================================================
# APPLICATION
# =========================================================

class Application(models.Model):

    user_id = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(max_length=11)
    full_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# =========================================================
# ADMISSION APPLICATION
# =========================================================

class AdmissionApplication(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    gender = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=150, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    father_name = models.CharField(max_length=150, blank=True)
    relationship = models.CharField(max_length=50, blank=True)

    guardian_cnic = models.CharField(max_length=13, blank=True)
    student_cnic = models.CharField(max_length=13, blank=True)

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    guardian_contact = models.CharField(max_length=11, blank=True)
    student_contact = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    degree = models.CharField(max_length=100, blank=True)
    passing_year = models.CharField(max_length=10, blank=True)
    board = models.CharField(max_length=100, blank=True)
    group = models.CharField(max_length=100, blank=True)
    obtained_marks = models.CharField(max_length=20, blank=True)
    total_marks = models.CharField(max_length=20, blank=True)
    board_roll_no = models.CharField(max_length=50, blank=True)
    previous_school = models.CharField(max_length=200, blank=True)
    heard_about_us = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.college.name}"


# =========================================================
# NOTIFICATION
# =========================================================

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    application = models.ForeignKey(
        AdmissionApplication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# =========================================================
# EMAIL OTP VERIFICATION
# =========================================================

class EmailOTP(models.Model):

    email = models.EmailField(db_index=True)
    code_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP verification for {self.email}"


# =========================================================
# TEACHING APPLICATION
# =========================================================

class TeachingApplication(models.Model):

    DEPARTMENT_CHOICES = [
        ("Mathematics", "Mathematics"),
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("Computer Science", "Computer Science"),
        ("English", "English"),
    ]

    DEGREE_CHOICES = [
        ("BS", "BS"),
        ("MS", "MS"),
        ("MPhil", "MPhil"),
    ]

    EXPERIENCE_CHOICES = [
        ("0-1 Years", "0-1 Years"),
        ("2-5 Years", "2-5 Years"),
        ("5+ Years", "5+ Years"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Reviewed", "Reviewed"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
    ]

    name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=80)
    cnic = models.CharField(max_length=15)
    domicile = models.CharField(max_length=100)

    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
    )

    campus = models.CharField(max_length=100, blank=True)

    last_degree = models.CharField(
        max_length=10,
        choices=DEGREE_CHOICES,
    )

    degree_title = models.CharField(max_length=150)
    passing_year = models.PositiveSmallIntegerField()
    university = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    marks_cgpa = models.CharField(max_length=30)
    specialization = models.CharField(max_length=150)

    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        blank=True,
    )

    last_organization = models.CharField(max_length=150, blank=True)
    reference_1 = models.CharField(max_length=200, blank=True)
    reference_2 = models.CharField(max_length=200, blank=True)

    cv = models.FileField(
        upload_to="teaching_applications/cvs/",
    )

    other_documents = models.FileField(
        upload_to="teaching_applications/documents/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} - {self.department} ({self.status})"
