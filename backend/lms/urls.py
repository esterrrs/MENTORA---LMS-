from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView)
from .views import (
    PenggunaViewSet,
    LMSViewSet,
    PengajarViewSet,
    PesertaDidikViewSet,
    CourseViewSet,
    TugasViewSet,
    QuizViewSet,
    ModulViewSet,
    AssignmentViewSet, 
    LoginAPIView,
    LogoutAPIView,
    RegisterView
)
from . import views

router = DefaultRouter()

router.register(r'pengguna', PenggunaViewSet)
router.register(r'lms', LMSViewSet)
router.register(r'pengajar', PengajarViewSet)
router.register(r'pesertadidik', PesertaDidikViewSet)
router.register(r'course', CourseViewSet)
router.register(r'tugas', TugasViewSet)
router.register(r'quiz', QuizViewSet)
router.register(r'modul', ModulViewSet)
router.register(r'assignment', AssignmentViewSet, basename='assignment')


urlpatterns = [
    path('', include(router.urls)),  
    path('api-auth/', include('rest_framework.urls')),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('api/token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
]