from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    address = models.TextField()
    def __str__(self):
        return self.username

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.name}"
    
class Booking(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending", "รอการอนุมัติ"
        CONFIRM = "Confirm", "ยืนยัน"
        COMPLETED = "Completed", "เสร็จสิ้น"
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='cus')
    sitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='sit')
    service = models.ForeignKey(Service, on_delete= models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=15, choices=StatusChoices.choices)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Customer : {self.customer} | Sitter : {self.sitter} | Service : {self.service} | {self.get_status_display()} {self.start_date.strftime('%B %d, %Y')}-{self.end_date.strftime('%B %d, %Y')}"
    
class SitterProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    service = models.ManyToManyField(Service, blank=True)
    cert_image = models.FileField(upload_to='image/', null=True, blank=True)

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete= models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)