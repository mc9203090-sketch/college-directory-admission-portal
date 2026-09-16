from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [

# =========================
# MAIN WEBSITE
# =========================

path(
    '',
    views.home,
    name='index'
),

path(
    'college/<int:id>/',
    views.college_detail,
    name='college_detail'
),

path(
    'choose-college/',
    views.choose_college,
    name='choose-college'
),


# =========================
# COLLEGES
# =========================

path(
    'superior/',
    views.superior,
    name='superior'
),

path(
    'pgc/',
    views.pgc,
    name='pgc'
),

path(
    'chishtian-science/',
    views.chishtian_science,
    name='chishtian_science'
),

path(
    'ripah/',
    views.ripah,
    name='ripah'
),


# =========================
# SUPERIOR COLLEGE
# ABOUT US
# =========================

path(
    'superior/about/',
    TemplateView.as_view(
        template_name='aboutsup.html'
    ),
    name='aboutsup'
),

path(
    'superior/history/',
    TemplateView.as_view(
        template_name='historysup.html'
    ),
    name='historysup'
),

path(
    'superior/mission/',
    TemplateView.as_view(
        template_name='missionsup.html'
    ),
    name='missionsup'
),

path(
    'superior/results/',
    TemplateView.as_view(
        template_name='results.html'
    ),
    name='results'
),


# =========================
# SUPERIOR
# ADMISSIONS
# =========================

path(
    'superior/admissions/',
    TemplateView.as_view(
        template_name='addmission.html'
    ),
    name='addmission'
),

path(
    'superior/fees/',
    TemplateView.as_view(
        template_name='fee.html'
    ),
    name='fee'
),

path(
    'superior/apply/',
    TemplateView.as_view(
        template_name='apply.html'
    ),
    name='apply'
),

path(
    'superior/admission-application/',
    views.admission_application_superior,
    name='applysuperior'
),

path(
    'superior/application-form/',
    views.application_form,
    name='application-form'
),


# =========================
# SUPERIOR
# FACILITIES
# =========================

path(
    'superior/classrooms/',
    TemplateView.as_view(
        template_name='class.html'
    ),
    name='class'
),

path(
    'superior/spaces/',
    TemplateView.as_view(
        template_name='spaces.html'
    ),
    name='spaces'
),


# =========================
# SUPERIOR
# OTHER
# =========================

path(
    'superior/affiliate/',
    TemplateView.as_view(
        template_name='affiliate.html'
    ),
    name='affiliate'
),

path(
    'superior/contact/',
    TemplateView.as_view(
        template_name='contact.html'
    ),
    name='contact'
),


# =========================
# PGC - ABOUT US
# =========================

path(
    'pgc/history/',
    TemplateView.as_view(
        template_name='historypgc.html'
    ),
    name='historypgc'
),

path(
    'pgc/uniquely/',
    TemplateView.as_view(
        template_name='uniquelypgc.html'
    ),
    name='uniquelypgc'
),

path(
    'pgc/mission/',
    TemplateView.as_view(
        template_name='missionpgc.html'
    ),
    name='missionpgc'
),


# =========================
# PGC - ADMISSIONS
# =========================

path(
    'pgc/undergraduate/',
    TemplateView.as_view(
        template_name='undergraduatepgc.html'
    ),
    name='undergraduatepgc'
),

path(
    'pgc/fees/',
    TemplateView.as_view(
        template_name='feepgc.html'
    ),
    name='feepgc'
),

path(
    'pgc/apply/',
    views.admission_application,
    name='applypgc'
),


# =========================
# PGC - OTHER
# =========================

path(
    'pgc/activities/',
    TemplateView.as_view(
        template_name='activitypgc.html'
    ),
    name='activitypgc'
),

path(
    'pgc/blog/',
    TemplateView.as_view(
        template_name='blogpgc.html'
    ),
    name='blogpgc'
),

path(
    'pgc/careers/',
    TemplateView.as_view(
        template_name='careerpgc.html'
    ),
    name='careerpgc'
),

path(
    'pgc/careers/teaching-form/',
    TemplateView.as_view(
        template_name='formteachpgc.html'
    ),
    name='formteachpgc'
),

path(
    'pgc/affiliate/',
    TemplateView.as_view(
        template_name='affiliatepgc.html'
    ),
    name='affiliatepgc'
),

path(
    'pgc/contact/',
    TemplateView.as_view(
        template_name='contactpgc.html'
    ),
    name='contactpgc'
),

path(
    'pgc/signup/',
    TemplateView.as_view(
        template_name='signup pgc.html'
    ),
    name='signup pgc'
),


# =========================
# RIPHAH COLLEGE
# ABOUT US
# =========================

path(
    'ripah/history/',
    TemplateView.as_view(
        template_name='historyrip.html'
    ),
    name='historyrip'
),

path(
    'ripah/mission/',
    TemplateView.as_view(
        template_name='missionrip.html'
    ),
    name='missionrip'
),


# =========================
# RIPHAH
# ADMISSIONS
# =========================

path(
    'ripah/fees/',
    TemplateView.as_view(
        template_name='feestructurerip.html'
    ),
    name='feestructurerip'
),

path(
    'ripah/apply/',
    views.admission_application_ripah,
    name='applyrip'
),


# =========================
# RIPHAH
# FACILITIES
# =========================

path(
    'ripah/classrooms/',
    TemplateView.as_view(
        template_name='classrip.html'
    ),
    name='classrip'
),

path(
    'ripah/spaces/',
    TemplateView.as_view(
        template_name='spacerip.html'
    ),
    name='spacerip'
),


# =========================
# RIPHAH
# OTHER
# =========================

path(
    'ripah/affiliate/',
    TemplateView.as_view(
        template_name='affiliaterip.html'
    ),
    name='affiliaterip'
),

path(
    'ripah/contact/',
    TemplateView.as_view(
        template_name='contactrip.html'
    ),
    name='contactrip'
),


# =========================
# CHISHTIAN SCIENCE COLLEGE
# =========================

path(
    'chishtian-science/history/',
    TemplateView.as_view(
        template_name='historycsc.html'
    ),
    name='historycsc'
),

path(
    'chishtian-science/uniquely/',
    TemplateView.as_view(
        template_name='uniquelycsc.html'
    ),
    name='uniquelycsc'
),

path(
    'chishtian-science/mission/',
    TemplateView.as_view(
        template_name='missioncsc.html'
    ),
    name='missioncsc'
),

path(
    'chishtian-science/undergraduate/',
    TemplateView.as_view(
        template_name='undergraduatecsc.html'
    ),
    name='undergraduatecsc'
),

path(
    'chishtian-science/fees/',
    TemplateView.as_view(
        template_name='feecsc.html'
    ),
    name='feecsc'
),

path(
    'chishtian-science/apply/',
    views.admission_application_csc,
    name='applycsc'
),

path(
    'chishtian-science/activities/',
    TemplateView.as_view(
        template_name='activitycsc.html'
    ),
    name='activitycsc'
),

path(
    'chishtian-science/careers/',
    TemplateView.as_view(
        template_name='careercsc.html'
    ),
    name='careercsc'
),

path(
    'chishtian-science/careers/teaching-form/',
    TemplateView.as_view(
        template_name='formteachcsc.html'
    ),
    name='formteachcsc'
),

path(
    'chishtian-science/affiliate/',
    TemplateView.as_view(
        template_name='affiliatecsc.html'
    ),
    name='affiliatecsc'
),

path(
    'chishtian-science/contact/',
    TemplateView.as_view(
        template_name='contactcsc.html'
    ),
    name='contactcsc'
),


# =========================
# STUDENT ACCOUNT
# =========================

path(
    'dashboard/',
    views.dashboard,
    name='dashboard'
),

path(
    'profile/',
    views.profile,
    name='profile'
),

path(
    'application/<int:id>/',
    views.application_detail,
    name='application-detail'
),

path(
    'admission-application/',
    views.admission_application,
    name='admission-application'
),

path(
    'logout/',
    views.user_logout,
    name='logout'
),


]

# =========================

# CUSTOM ERROR HANDLERS

# =========================

handler404 = 'college.views.error_404'
handler403 = 'college.views.error_403'
handler500 = 'college.views.error_500'
