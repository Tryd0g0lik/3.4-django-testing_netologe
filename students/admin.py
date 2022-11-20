from django.contrib import admin

# Register your models here.
from students.models import Student, Course, Faculty

#
class FaciltyInline(admin.TabularInline):
	model = Faculty
	extra = 0

class StudentModelAdmin(admin.ModelAdmin):


	list_display = ['id', 'name']
	list_filter = ['id', 'name']
	ordering = ['-id', 'name']
	search_fields = ('name', )
	nlines = [FaciltyInline, ]


class CoursModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'name',]
	list_filter = ['id', 'name']
	ordering = ['-id',]
	search_fields = ('name',)

	inlines = [FaciltyInline, ]

admin.site.register(Student, StudentModelAdmin)
admin.site.register(Course, CoursModelAdmin)



