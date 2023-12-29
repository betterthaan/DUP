from rest_framework import serializers
from .models import *
from django.db import transaction


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'priority', 'machine', 'processing_times')


class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = '__all__'


# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = '__all__'


class JobnameExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobnameExplanation
        fields = '__all__'


class JobnameLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobnameLinks
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class JobNameSerializer(serializers.ModelSerializer):
    explanation = JobSerializer(many=True)
    links = LinksSerializer(many=True)  # добавляем сериализатор для поля links
    # department = DepartmentSerializer(many=True)

    class Meta:
        model = JobName
        fields = ('id', 'name_job', 'description',
                  'due_dates', 'explanation', 'links', 'id_department')

    def create(self, validated_data):
        explanations_data = validated_data.pop('explanation')
        # получаем данные для поля links
        links_data = validated_data.pop('links')
        # departments_data = validated_data.pop('department')
        with transaction.atomic():
            job_name = JobName.objects.create(**validated_data)
            explanation = []
            for explanation_data in explanations_data:
                job = Job.objects.create(**explanation_data)
                explanation.append(job)
            links = []
            for link_data in links_data:  # создаем объекты Links и добавляем их в список
                link = Links.objects.create(**link_data)
                links.append(link)
            # departments = []
            # for department_data in departments_data:
            #     department = Department.objects.create(**department_data)
            #     departments.append(department)
            # Замена связей в таблице-связи
            job_name.explanation.set(explanation)
            job_name.links.set(links)  # устанавливаем связь для поля links
            # job_name.department.set(departments)
            job_name.save()
        return job_name


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = (
            'id',
            'name_machine',
            'description',
            'id_department'
        )


class ObtainedResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObtainedResult
        fields = '__all__'


class ObtainedResultMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObtainedResultMachine
        fields = (
            # 'id'
            'stage',
            'department',
            'department_name',
            'machine',
            'name_machine',
            'description_machine',
            'job',
            'job_name',
            'descripiton_job',
            'T_i',
            'T_c'
        )
