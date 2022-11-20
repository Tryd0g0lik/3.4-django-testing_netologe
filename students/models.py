from django.db import models



class Student(models.Model):

    name = models.CharField(
        max_length= 100,
        help_text= """Имя студента""",
        db_index=True
    )

    birth_date = models.DateField(
        null=True,
        help_text = """Дата регистрации""",
        auto_now_add=True,
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
        verbose_name="Title course",
        db_index=True
        )

    student = models.ManyToManyField(
        Student,
        blank=True,

        through="Faculty",
        through_fields= ("courses", "students"),
        help_text = """ Привязанная таблица студентов"""
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


    def __str__(self):
        return self.name


class Faculty(models.Model):
    # students = models.ForeignKey(Student, on_delete=models.CASCADE,
    #                              )
    courses = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="faculty_stude",
        )
    students = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name= "faculty_stude",
    )
    datestude = models.DateField(
        null=True,
        help_text ="Дата занятий"
    )
