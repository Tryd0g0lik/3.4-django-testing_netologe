from django.db import models


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )

    def __str__(self):
        return self.name

class Course(models.Model):

    name = models.TextField()

    student = models.ManyToManyField(
        Student,
        blank=True,
        related_name="persons",
        through='Faculty'
    )

    def __str__(self):
        return self.name

class Faculty(models.Model):
    student =  models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
