from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response 
from .models import Pengguna, LMS, Pengajar, PesertaDidik, Course, Tugas, Quiz, Modul, Assignment
from .serializer import PenggunaSerializer, LMSSerializer, PengajarSerializer, PesertaDidikSerializer, CourseSerializer, TugasSerializer, QuizSerializer, ModulSerializer

from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import LoginSerializer, LogoutSerializer, RegisterSerializer


class LoginAPIView(generics.GenericAPIView):  
    serializer_class = LoginSerializer  

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        
        return Response({
            'user': serializer.validated_data['user'],
            'tokens': serializer.validated_data['tokens']
        }, status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            request.user.auth_token.delete()  
            return Response({"message": "Logout berhasil"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Logout gagal", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer 
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class PenggunaViewSet(viewsets.ModelViewSet):
    queryset = Pengguna.objects.all()
    serializer_class = PenggunaSerializer

class LMSViewSet(viewsets.ModelViewSet):
    queryset = LMS.objects.all()
    serializer_class = LMSSerializer

class PengajarViewSet(viewsets.ModelViewSet):
    queryset = Pengajar.objects.all()
    serializer_class = PengajarSerializer

class PesertaDidikViewSet(viewsets.ModelViewSet):
    queryset = PesertaDidik.objects.all()
    serializer_class = PesertaDidikSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TugasViewSet(viewsets.ModelViewSet):
    queryset = Tugas.objects.all()
    serializer_class = TugasSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class ModulViewSet(viewsets.ModelViewSet):
    queryset = Modul.objects.all()
    serializer_class = ModulSerializer

class AssignmentViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):  
        course_id = pk
        tugas = Tugas.objects.filter(id_course=course_id)
        quiz = Quiz.objects.filter(id_course=course_id)
        tugas_data = TugasSerializer(tugas, many=True).data
        quiz_data = QuizSerializer(quiz, many=True).data
        return Response({'tugas': tugas_data, 'quiz': quiz_data})


def list_assignment(request, course_id):
    # Filter data tugas
    tugas_list = Assignment.objects.filter(id_course=course_id, tipe='TUGAS')
    
    # Filter data quiz
    quiz_list = Assignment.objects.filter(id_course=course_id, tipe='QUIZ')

    context = {
        'tugas_list': tugas_list,
        'quiz_list': quiz_list,
    }
    return render(request, 'assignment/list.html', context)