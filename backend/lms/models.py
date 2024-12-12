from django.db import models

class Pengguna(models.Model):
    id_pengguna = models.CharField(max_length=20, unique=True)
    foto_profil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    nama = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def _str_(self):
        return self.nama


class LMS(models.Model):
    id_lms = models.CharField(max_length=20, unique=True)
    id_pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE, related_name="lms") 
    role = models.CharField(
        max_length=20,
        choices=[('Pengajar', 'Pengajar'), ('Peserta Didik', 'Peserta Didik')],
        default='Peserta Didik'
    )
    waktu_akses = models.DateTimeField()

    def _str_(self):
        return self.id_lsm_spada


class Pengajar(models.Model):
    id_pengajar = models.CharField(max_length=20, unique=True)
    id_pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, related_name="pengajar")  
    tahun_ajaran = models.CharField(max_length=20)
    status_pengajar = models.CharField(max_length=20)

    def _str_(self):
        return f"{self.id_pengajar} ({self.tahun_ajaran})"

class PesertaDidik(models.Model):
    id_peserta_didik = models.CharField(max_length=20, unique=True)  
    id_pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, related_name="peserta_didik")  
    status_pendaftaran = models.CharField(max_length=20)
    tanggal_pendaftaran = models.DateField()

    def _str_(self):
        return f"{self.id_peserta_didik} ({self.status_pendaftaran})"


class Course(models.Model):
    nama_course = models.CharField(max_length=100)
    id_course = models.CharField(max_length=20, unique=True)
    id_pengajar = models.ForeignKey(Pengajar, on_delete=models.CASCADE, related_name="courses")  
    id_peserta_didik = models.ManyToManyField(PesertaDidik, related_name="courses") 

    def _str_(self):
        return self.nama_course


class Tugas(models.Model):
    id_tugas = models.CharField(max_length=100, unique=True)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tugas")  
    nilai_tugas = models.IntegerField()
    tanggal_pengumpulan = models.DateField()

    def _str_(self):
        return f"Tugas {self.id_tugas} - {self.id_course.nama_course}"


class Quiz(models.Model):
    id_quiz = models.CharField(max_length=100, unique=True)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quiz")  
    jumlah_soal = models.IntegerField()
    durasi_waktu = models.DurationField()  
    tanggal_pengumpulan = models.DateField()

    def _str_(self):
        return self.id_quiz


class Modul(models.Model):
    id_modul = models.CharField(max_length=100, unique=True)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modul")  
    judul_modul = models.CharField(max_length=100)
    jenis_file = models.CharField(max_length=50)
    ukuran_file = models.FloatField(help_text="Ukuran file dalam MB")

    def _str_(self):
        return self.judul_modul
    
class Assignment(models.Model):
    ASSIGNMENT_TYPE_CHOICES = [
        ('TUGAS', 'Tugas'),
        ('QUIZ', 'Quiz'),
    ]
    id_assignment = models.CharField(max_length=100, unique=True)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")  
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    tipe = models.CharField(max_length=5, choices=ASSIGNMENT_TYPE_CHOICES)
    nilai_tugas = models.IntegerField(blank=True, null=True)  
    jumlah_soal = models.IntegerField(blank=True, null=True)  
    durasi_waktu = models.DurationField(blank=True, null=True)  
    tanggal_pengumpulan = models.DateField()

    def _str_(self):
        return f"{self.tipe}: {self.judul}"