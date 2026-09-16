from django.contrib import admin
from django.core.mail import send_mail

from .models import College, AdmissionApplication


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'location',
        'website',
    )

    search_fields = (
        'name',
        'location',
        'description',
    )

    list_per_page = 20

    ordering = (
        'name',
    )


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'college',
        'course',
        'gender',
        'status',
        'email',
        'student_contact',
        'created_at',
    )

    list_filter = (
        'status',
        'college',
        'gender',
        'course',
        'created_at',
    )

    search_fields = (
        'full_name',
        'email',
        'guardian_cnic',
        'student_cnic',
        'course',
        'student_contact',
        'guardian_contact',
        'board_roll_no',
    )

    list_editable = (
        'status',
    )

    readonly_fields = (
        'student',
        'college',
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 20

    fieldsets = (
        (
            'Application Status',
            {
                'fields': (
                    'status',
                )
            }
        ),

        (
            'Student Information',
            {
                'fields': (
                    'student',
                    'college',
                    'full_name',
                    'gender',
                    'date_of_birth',
                    'student_cnic',
                    'location',
                    'address',
                )
            }
        ),

        (
            'Guardian Information',
            {
                'fields': (
                    'father_name',
                    'relationship',
                    'guardian_cnic',
                    'guardian_contact',
                )
            }
        ),

        (
            'Contact Information',
            {
                'fields': (
                    'student_contact',
                    'email',
                )
            }
        ),

        (
            'Academic Information',
            {
                'fields': (
                    'course',
                    'degree',
                    'passing_year',
                    'board',
                    'group',
                    'obtained_marks',
                    'total_marks',
                    'board_roll_no',
                    'previous_school',
                )
            }
        ),

        (
            'Additional Information',
            {
                'fields': (
                    'heard_about_us',
                    'created_at',
                )
            }
        ),
    )

    def save_model(self, request, obj, form, change):

        old_status = None

        if change:
            old_application = AdmissionApplication.objects.get(
                pk=obj.pk
            )
            old_status = old_application.status

        super().save_model(request, obj, form, change)

        if (
            change
            and old_status != obj.status
            and obj.status in ['Approved', 'Rejected']
            and obj.email
        ):

            if obj.status == 'Approved':

                subject = 'Admission Application Approved'

                message = (
                    f'Dear {obj.full_name},\n\n'
                    f'Congratulations! Your admission application '
                    f'for {obj.college.name} has been approved.\n\n'
                    f'Course: {obj.course}\n'
                    f'Application ID: {obj.id}\n\n'
                    f'Please contact the college administration '
                    f'for further admission instructions.\n\n'
                    f'Regards,\n'
                    f'College Directory'
                )

            else:

                subject = 'Admission Application Status'

                message = (
                    f'Dear {obj.full_name},\n\n'
                    f'Your admission application for '
                    f'{obj.college.name} has been rejected.\n\n'
                    f'Course: {obj.course}\n'
                    f'Application ID: {obj.id}\n\n'
                    f'Please contact the college administration '
                    f'for further information.\n\n'
                    f'Regards,\n'
                    f'College Directory'
                )

            send_mail(
                subject,
                message,
                None,
                [obj.email],
                fail_silently=True,
            )