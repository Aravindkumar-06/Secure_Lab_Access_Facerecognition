from django.db import models

# Create your models here.
class details(models.Model):
    username = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    img = models.ImageField()

    def __str__(self):
        return self.username


class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20)

    class Meta:
        db_table = "Register"



class Newuser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to='Faces/')  


class Card(models.Model):
    HID = models.CharField(max_length=6)
    stuid = models.CharField(max_length=12)
    name = models.CharField(max_length=30)
    cardnum = models.CharField(max_length=9)

