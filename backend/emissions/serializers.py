from rest_framework import serializers
from .models import Department, EmissionLog


class DepartmentSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string

    class Meta:
        model = Department
        fields = ['_id', 'name']


class EmissionLogSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    department_name = serializers.CharField(source='department.name', read_only=True)
    department = DepartmentSerializer()  # writeable nested input

    class Meta:
        model = EmissionLog
        fields = ['_id', 'department', 'department_name', 'source', 'amount', 'unit', 'timestamp']

    def create(self, validated_data):
        dept_data = validated_data.pop('department')
        dept, _ = Department.objects.get_or_create(name=dept_data['name'])
        emission_log = EmissionLog.objects.create(department=dept, **validated_data)
        return emission_log
