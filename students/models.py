from django.db import models



class Student(models.Model):

    name = models.CharField(
        max_length= 100,
        help_text= """Имя стубента""",
        db_index=True
    )

    birth_date = models.DateField(
        null=True,
        help_text = """Дата регистрации"""

    )



    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.name

class Course(models.Model):

    name = models.CharField(
        max_length= 100,
        help_text = """Наименование курс""",
        db_index=True
        )

    student = models.ManyToManyField(
        Student,
        blank=True,
        related_name="persons",

        help_text = """ Привязанная таблица студентов"""
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


    def __str__(self):
        return self.name

# class Faculty(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE,
#                                  related_name='students_faculty')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE,
#                                related_name = 'students_faculty')
