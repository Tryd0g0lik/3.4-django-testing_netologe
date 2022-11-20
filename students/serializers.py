from rest_framework import serializers

from students.models import Course, Student


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    class Meta:
        model = Student
        fields = ('id', 'name',)


class CourseSerializer(serializers.ModelSerializer):
    persons = StudentSerializer(many=True,
                                read_only=True)


    class Meta:
        model = Course
        fields = ("id", "name", "persons")
