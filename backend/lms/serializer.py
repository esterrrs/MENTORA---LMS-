from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import Pengguna, LMS, Pengajar, PesertaDidik, Course, Tugas, Quiz, Modul

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError("Username hanya boleh berisi huruf dan angka")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Username atau password salah")

        refresh = RefreshToken.for_user(user)
        return {
            'user': user.username,
            'tokens': {
                'refreshToken': str(refresh),
                'accessToken': str(refresh.access_token),
            }
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('Error')


class PenggunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengguna
        fields = '_all_'

class LMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = LMS
        fields = '_all_'

class PengajarSerializer(serializers.ModelSerializer):
    id_pengguna = serializers.PrimaryKeyRelatedField(queryset=Pengguna.objects.all())   
    class Meta:
        model = Pengajar
        fields = '_all_'

class PesertaDidikSerializer(serializers.ModelSerializer):
    id_pengguna = serializers.PrimaryKeyRelatedField(queryset=Pengguna.objects.all())  
    class Meta:
        model = PesertaDidik
        fields = '_all_'

class CourseSerializer(serializers.ModelSerializer):
    id_pengajar = serializers.PrimaryKeyRelatedField(queryset=Pengajar.objects.all())  
    id_peserta_didik = serializers.PrimaryKeyRelatedField(queryset=PesertaDidik.objects.all(), many=True)
    class Meta:
        model = Course
        fields = '_all_'

class TugasSerializer(serializers.ModelSerializer):
    id_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Tugas
        fields = '_all_'

class QuizSerializer(serializers.ModelSerializer):
    id_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all()) 
    class Meta:
        model = Quiz
        fields = '_all_'

class ModulSerializer(serializers.ModelSerializer):
    id_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())  
    class Meta:
        model = Modul
        fields = '_all_'