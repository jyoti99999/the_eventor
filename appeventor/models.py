from django.db import models
# from django.contrib.auth.models import User 
# Create your models here.
class datadesire(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phone=models.CharField(max_length=15,null=True)
    password=models.CharField(max_length=16)
    
class user_query(models.Model):
    # user=models.ForeignKey(userclient,on_delete=models.CASCADE)
    Q_email=models.EmailField()
    query=models.CharField(max_length=200)

class adminuser(models.Model):
    name=models.CharField(max_length=20)
    is_read = models.BooleanField(default=False)
    username=models.EmailField()
    password=models.CharField(max_length=16)
    suggestion=models.TextField(null=True)
    
    def __str__(self):
        return self.username


class FakePayment(models.Model):
    # user = models.ForeignKey(datadesire, on_delete=models.CASCADE, related_name="payments") 
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')], default='Success')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.transaction_id}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone=models.CharField(max_length=12)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserDocument(models.Model):
    DOCUMENT_TYPES = [
        ('Pan card', 'Pan card'),
        ('National ID', 'National ID'),
    ]
    user = models.ForeignKey(datadesire, on_delete=models.CASCADE, related_name="documents")  
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)  
    document_file = models.FileField(upload_to="documents/")  
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.email} - {self.document_type}"

class reservation(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=50)
    company=models.CharField(max_length=50)
    venue=models.CharField(max_length=50)
    event=models.CharField(max_length=50)
    date1=models.DateField(null=True)
    date2=models.DateField(null=True)
    about=models.TextField()


# --- features for chatbot, seat map, and smart recommendations ---

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    venue = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Seat(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    class Meta:
        unique_together = ('event', 'row', 'number')

    def __str__(self):
        return f"{self.event.name} - {self.row}{self.number} ({self.status})"


class ChatMessage(models.Model):
    user = models.ForeignKey(datadesire, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        role = 'Bot' if self.is_bot else 'User'
        return f"[{self.timestamp}] {role}: {self.message[:30]}"