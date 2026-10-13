
from django.urls import path, reverse
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.shortcuts import redirect
from . import views


# Redirect old URLs to the new readable URLs.
def redirect_to_named_url(request, url_name, *args, **kwargs):
    return redirect(reverse(url_name, args=args, kwargs=kwargs))


urlpatterns = [
    # ==================================================
    # HOME AND COLLEGE DETAILS
    # ==================================================
    path("", views.home, name="index"),

    # New readable college detail URL
    path(
        "college/<slug:slug>/",
        views.college_detail,
        name="college_detail",
    ),

    # ==================================================
    # CHOOSE COLLEGE
    # ==================================================
    path(
        "admissions/choose-college/",
        views.choose_college,
        name="choose-college",
    ),
    path(
        "choose-college/",
        RedirectView.as_view(
            pattern_name="choose-college",
            permanent=True,
        ),
    ),

    # ==================================================
    # EMAIL VERIFICATION
    # ==================================================
    path("verify-email/", views.verify_email, name="verify-email"),
    path(
        "resend-email-otp/",
        views.resend_email_otp,
        name="resend-email-otp",
    ),

    # ==================================================
    # COLLEGE HOME PAGES
    # ==================================================
    path(
        "superior-college-chishtian/",
        views.superior,
        name="superior",
    ),
    path(
        "punjab-college-chishtian/",
        views.pgc,
        name="pgc",
    ),
    path(
        "chishtian-science-college/",
        views.chishtian_science,
        name="chishtian_science",
    ),
    path(
        "riphah-international-college/",
        views.ripah,
        name="ripah",
    ),

    # Old college home URLs
    path(
        "superior/",
        RedirectView.as_view(
            pattern_name="superior",
            permanent=True,
        ),
    ),
    path(
        "pgc/",
        RedirectView.as_view(
            pattern_name="pgc",
            permanent=True,
        ),
    ),
    path(
        "chishtian-science/",
        RedirectView.as_view(
            pattern_name="chishtian_science",
            permanent=True,
        ),
    ),
    path(
        "ripah/",
        RedirectView.as_view(
            pattern_name="ripah",
            permanent=True,
        ),
    ),

    # ==================================================
    # SUPERIOR COLLEGE
    # ==================================================
    path(
        "superior-college-chishtian/apply/",
        TemplateView.as_view(template_name="apply.html"),
        name="apply",
    ),
    path(
        "superior-college-chishtian/about/",
        TemplateView.as_view(template_name="aboutsup.html"),
        name="aboutsup",
    ),
    path(
        "superior-college-chishtian/history/",
        TemplateView.as_view(template_name="historysup.html"),
        name="historysup",
    ),
    path(
        "superior-college-chishtian/mission/",
        TemplateView.as_view(template_name="missionsup.html"),
        name="missionsup",
    ),
    path(
        "superior-college-chishtian/results/",
        TemplateView.as_view(template_name="results.html"),
        name="results",
    ),
    path(
        "superior-college-chishtian/admissions/",
        TemplateView.as_view(template_name="addmission.html"),
        name="addmission",
    ),
    path(
        "superior-college-chishtian/application-form/",
        views.application_form,
        name="application-form",
    ),
    path(
        "superior-college-chishtian/classrooms/",
        TemplateView.as_view(template_name="class.html"),
        name="class",
    ),
    path(
        "superior-college-chishtian/spaces/",
        TemplateView.as_view(template_name="spaces.html"),
        name="spaces",
    ),
    path(
        "superior-college-chishtian/affiliate/",
        TemplateView.as_view(template_name="affiliate.html"),
        name="affiliate",
    ),
    path(
        "superior-college-chishtian/contact/",
        TemplateView.as_view(template_name="contact.html"),
        name="contact",
    ),
    path(
        "superior-college-chishtian/fees/",
        TemplateView.as_view(template_name="fee.html"),
        name="fee",
    ),

    # ==================================================
    # PUNJAB COLLEGE (PGC)
    # ==================================================
    path(
        "punjab-college-chishtian/history/",
        TemplateView.as_view(template_name="historypgc.html"),
        name="historypgc",
    ),
    path(
        "punjab-college-chishtian/uniquely/",
        TemplateView.as_view(template_name="uniquelypgc.html"),
        name="uniquelypgc",
    ),
    path(
        "punjab-college-chishtian/mission/",
        TemplateView.as_view(template_name="missionpgc.html"),
        name="missionpgc",
    ),
    path(
        "punjab-college-chishtian/undergraduate/",
        TemplateView.as_view(template_name="undergraduatepgc.html"),
        name="undergraduatepgc",
    ),
    path(
        "punjab-college-chishtian/fees/",
        TemplateView.as_view(template_name="feepgc.html"),
        name="feepgc",
    ),
    path(
        "punjab-college-chishtian/apply/",
        views.choose_college,
        name="applypgc",
    ),
    path(
        "punjab-college-chishtian/activities/",
        TemplateView.as_view(template_name="activities.html"),
        name="activities",
    ),
    path(
        "punjab-college-chishtian/blog/",
        TemplateView.as_view(template_name="blog.html"),
        name="blog",
    ),
    path(
        "punjab-college-chishtian/careers/",
        TemplateView.as_view(template_name="careers.html"),
        name="careers",
    ),
    path(
        "punjab-college-chishtian/careers/teaching-form/",
        TemplateView.as_view(template_name="teachingform.html"),
        name="teaching-form",
    ),
    path(
        "punjab-college-chishtian/affiliate/",
        TemplateView.as_view(template_name="affiliatepgc.html"),
        name="affiliatepgc",
    ),
    path(
        "punjab-college-chishtian/contact/",
        TemplateView.as_view(template_name="contactpgc.html"),
        name="contactpgc",
    ),
    path(
        "punjab-college-chishtian/signup/",
        TemplateView.as_view(template_name="signup pgc.html"),
        name="signup-pgc",
    ),

    # ==================================================
    # RIPHAH COLLEGE
    # ==================================================
    path(
        "riphah-international-college/history/",
        TemplateView.as_view(template_name="historyrip.html"),
        name="historyrip",
    ),
    path(
        "riphah-international-college/mission/",
        TemplateView.as_view(template_name="missionrip.html"),
        name="missionrip",
    ),
    path(
        "riphah-international-college/fees/",
        TemplateView.as_view(template_name="feestructurerip.html"),
        name="feestructurerip",
    ),
    path(
        "riphah-international-college/apply/",
        views.choose_college,
        name="applyrip",
    ),
    path(
        "riphah-international-college/classrooms/",
        TemplateView.as_view(template_name="classrip.html"),
        name="classrip",
    ),
    path(
        "riphah-international-college/spaces/",
        TemplateView.as_view(template_name="spacerip.html"),
        name="spacerip",
    ),
    path(
        "riphah-international-college/affiliate/",
        TemplateView.as_view(template_name="affiliaterip.html"),
        name="affiliaterip",
    ),
    path(
        "riphah-international-college/contact/",
        TemplateView.as_view(template_name="contactrip.html"),
        name="contactrip",
    ),

    # ==================================================
    # CHISHTIAN SCIENCE COLLEGE
    # ==================================================
    path(
        "chishtian-science-college/history/",
        TemplateView.as_view(template_name="historycsc.html"),
        name="historycsc",
    ),
    path(
        "chishtian-science-college/uniquely/",
        TemplateView.as_view(template_name="uniquelycsc.html"),
        name="uniquelycsc",
    ),
    path(
        "chishtian-science-college/mission/",
        TemplateView.as_view(template_name="missioncsc.html"),
        name="missioncsc",
    ),
    path(
        "chishtian-science-college/undergraduate/",
        TemplateView.as_view(template_name="undergraduatecsc.html"),
        name="undergraduatecsc",
    ),
    path(
        "chishtian-science-college/fees/",
        TemplateView.as_view(template_name="feecsc.html"),
        name="feecsc",
    ),
    path(
        "chishtian-science-college/apply/",
        views.choose_college,
        name="applycsc",
    ),
    path(
        "chishtian-science-college/activities/",
        TemplateView.as_view(template_name="activitycsc.html"),
        name="activitycsc",
    ),
    path(
        "chishtian-science-college/careers/",
        TemplateView.as_view(template_name="careercsc.html"),
        name="careercsc",
    ),
    path(
        "chishtian-science-college/careers/teaching-form/",
        TemplateView.as_view(template_name="formteachcsc.html"),
        name="formteachcsc",
    ),
    path(
        "chishtian-science-college/affiliate/",
        TemplateView.as_view(template_name="affiliatecsc.html"),
        name="affiliatecsc",
    ),
    path(
        "chishtian-science-college/contact/",
        TemplateView.as_view(template_name="contactcsc.html"),
        name="contactcsc",
    ),

    # ==================================================
    # LOGIN / SIGNUP
    # ==================================================
    path(
        "accounts/login/",
        views.application_form,
        name="login",
    ),

    # ==================================================
    # DASHBOARD AND PROFILE
    # ==================================================
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path(
        "application/<int:id>/",
        views.application_detail,
        name="application-detail",
    ),

    # ==================================================
    # ADMISSION APPLICATIONS
    # ==================================================
    path(
        "admission-application/",
        views.admission_application,
        name="admission-application",
    ),
    path(
        "admissions/<slug:slug>/",
        views.admission_application_common,
        name="admission-form",
    ),
    path(
        "admission/<slug:slug>/",
        RedirectView.as_view(
            pattern_name="admission-form",
            permanent=True,
        ),
    ),
    path(
        "admissions/multiple/",
        views.admission_application_multiple,
        name="admission-form-multiple",
    ),
    path(
        "admission/multiple/",
        RedirectView.as_view(
            pattern_name="admission-form-multiple",
            permanent=True,
        ),
    ),

    # ==================================================
    # LOGOUT
    # ==================================================
    path("logout/", views.user_logout, name="logout"),

    # ==================================================
    # NOTIFICATIONS
    # ==================================================
    path("notifications/", views.notifications, name="notifications"),
    path(
        "notifications/read/<int:id>/",
        views.mark_notification_read,
        name="mark-notification-read",
    ),
    path(
        "notifications/read-all/",
        views.mark_all_notifications_read,
        name="mark-all-notifications-read",
    ),
]


# ======================================================
# CUSTOM ERROR HANDLERS
# ======================================================
handler404 = "college.views.error_404"
handler403 = "college.views.error_403"
handler500 = "college.views.error_500"
