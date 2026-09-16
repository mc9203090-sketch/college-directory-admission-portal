from django.db import models
from django.contrib.auth.models import User


# =========================
# COLLEGE
# =========================

class College(models.Model):

    name = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    image = models.ImageField(
        upload_to='colleges/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# =========================
# STUDENT PROFILE
# =========================

class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"


# =========================
# APPLICATION
# =========================

class Application(models.Model):

    user_id = models.CharField(
        max_length=30
    )

    email = models.EmailField()

    mobile = models.CharField(
        max_length=11
    )

    full_name = models.CharField(
        max_length=150
    )

    password = models.CharField(
        max_length=128
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


# =========================
# ADMISSION APPLICATION
# =========================

class AdmissionApplication(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # =========================
    # STUDENT & COLLEGE
    # =========================

    student = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE
    )

    # =========================
    # APPLICATION STATUS
    # =========================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # =========================
    # STUDENT INFORMATION
    # =========================

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    course = models.CharField(
        max_length=150,
        blank=True
    )

    full_name = models.CharField(
        max_length=150,
        blank=True
    )

    father_name = models.CharField(
        max_length=150,
        blank=True
    )

    relationship = models.CharField(
        max_length=50,
        blank=True
    )

    # =========================
    # CNIC
    # =========================

    guardian_cnic = models.CharField(
        max_length=13,
        blank=True
    )

    student_cnic = models.CharField(
        max_length=13,
        blank=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    # =========================
    # CONTACT INFORMATION
    # =========================

    guardian_contact = models.CharField(
        max_length=11,
        blank=True
    )

    student_contact = models.CharField(
        max_length=11,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    # =========================
    # ACADEMIC INFORMATION
    # =========================

    degree = models.CharField(
        max_length=100,
        blank=True
    )

    passing_year = models.CharField(
        max_length=10,
        blank=True
    )

    board = models.CharField(
        max_length=100,
        blank=True
    )

    group = models.CharField(
        max_length=100,
        blank=True
    )

    obtained_marks = models.CharField(
        max_length=20,
        blank=True
    )

    total_marks = models.CharField(
        max_length=20,
        blank=True
    )

    board_roll_no = models.CharField(
        max_length=50,
        blank=True
    )

    previous_school = models.CharField(
        max_length=200,
        blank=True
    )

    heard_about_us = models.CharField(
        max_length=100,
        blank=True
    )

    # =========================
    # CREATED DATE
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.full_name} - {self.college.name}"