from django.db import models
import uuid
from ticket.models import Ticket
from django.core.validators import MinValueValidator, MaxValueValidator

class Survey(models.Model):
    four_choices = (
        ('Very Good' , 'Very Good'),
        ('Good', 'Good'),
        ('Bad' , 'Bad'),
        ('Very Bad' , 'Very Bad'),
    )
    subject_choices = (
        ('Algorithms' , 'Algorithms'),
        ('Graph' , 'Graph')
    )
    subject = models.CharField(max_length=15 , choices=subject_choices)
    student_code = models.CharField(unique=True , max_length=50)
    student_name = models.CharField(max_length=150)
    
    teachers_teaching = models.CharField(max_length=15 , choices=four_choices)
    teachers_availability = models.CharField(max_length=15 , choices=four_choices)
    description1 = models.TextField()
    description2 = models.TextField()
    description3 = models.TextField()
    description4 = models.TextField()

    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.student_name
    
class TicketFeedback(models.Model) :
    satisfy = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    opinion = models.TextField()
    ticket = models.ForeignKey(Ticket , on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

