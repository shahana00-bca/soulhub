from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models



class Psychologist(models.Model):
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Pending')

class User_table(models.Model):
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.CharField(max_length=100)

class schedule(models.Model):
    PSYCHOLOGIST = models.ForeignKey(Psychologist,on_delete=models.CASCADE)
    from_time = models.CharField(max_length=100)
    to_time = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Pending')


class Appointment(models.Model):
    USER = models.ForeignKey(User_table,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    schedule = models.ForeignKey(schedule, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    status= models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

class Complaint(models.Model):
    USER = models.ForeignKey(User_table, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    date= models.CharField(max_length=100)

class Payment(models.Model):
    APPOINTMENT = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    status= models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

class Feedback(models.Model):
    USER = models.ForeignKey(User_table,on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    feedback = models.CharField(max_length=100)

class Rating(models.Model):
    USER = models.ForeignKey(User_table,on_delete=models.CASCADE)
    rating = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    review= models.CharField(max_length=100)

class Chatss(models.Model):
    FROM = models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_id')
    TO = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_id')
    date = models.CharField(max_length=100)
    message= models.CharField(max_length=100)


class Diary_or_journal(models.Model):
    USER = models.ForeignKey(User_table,on_delete=models.CASCADE)
    date = models.DateField()
    details = models.TextField()
    emotion= models.CharField(max_length=100)
    emotion_percentage = models.FloatField(default=0)


class Google_meet_link(models.Model):
    PSYCHOLOGIST = models.ForeignKey(Psychologist, on_delete=models.CASCADE)
    link = models.CharField(max_length=1000)
    date= models.CharField(max_length=100)


class Expert_Rating(models.Model):
    USER = models.ForeignKey(User_table,on_delete=models.CASCADE)
    EXPERT = models.ForeignKey(Psychologist,on_delete=models.CASCADE)
    rating = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    review= models.CharField(max_length=100)




