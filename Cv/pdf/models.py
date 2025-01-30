from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    THEME_CHOICES = [
        ('classic', 'Classique - Bleu'),
        ('modern', 'Moderne - Violet'),
        ('elegant', 'Élégant - Vert'),
        ('creative', 'Créatif - Orange'),
        ('professional', 'Professionnel - Gris'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    proffession = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    birthday = models.DateField()
    language = models.CharField(max_length=100)
    hobbie = models.CharField(max_length=200)
    skill = models.CharField(max_length=300)
    experience = models.TextField(max_length=500)
    formation = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='classic')

    def __str__(self):
        return f"{self.user.username if self.user else 'No User'} - {self.name}"
    
    class Meta:
        ordering = ['-date_added']

class CVStatistics(models.Model):
    date = models.DateField(auto_now_add=True)
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    profession_category = models.CharField(max_length=100)
    language_used = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "CV Statistics"
