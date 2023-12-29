from django.shortcuts import render
from rest_framework import viewsets
from . models import *
from .serializers import *
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .logic import logic_schedule
from rest_framework.views import APIView
from datetime import datetime
# from .logic import ObtainedResult
import json



# Create your views here.
class JobNameView(viewsets.ModelViewSet):
    serializer_class = JobNameSerializer

    queryset = JobName.objects.all()
    logic_schedule()
    # def get(request):
    #     queryset = WorkSuper.objects.all()
    #     logic_schedule(queryset)

    def get_queryset(self):
        # queryset = WorkSuper.objects.all()
        queryset = JobName.objects.prefetch_related('explanation')
        # logic_schedule(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        # return JsonResponse({'data': data})
        # logic_schedule(data)
        return Response(serializer.data)


class MachineView(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class DepartmentView(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ObtainedResultAPIView(viewsets.ModelViewSet):
    serializer_class = ObtainedResultSerializer

    def get_queryset(self):
        return ObtainedResult.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'job': item.job,
                'name_job': item.name_job,
                'description': item.description,
                'due_dates': item.due_dates,
                'priority': item.priority,
                'processing_times': item.processing_times,
                'machine_id': item.machine_id,
                'name_machine': item.name_machine,
                'description_machine': item.description_machine,
                'T_i': item.T_i,
                'T_c': item.T_c,
                'score': item.score
            })
        return Response(serializer.data)


class JobView(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = []
        for item in queryset:
            data.append({
                'id': item.id,
                'priority': item.priority,
                'machine': item.machine,
                'processing_times': item.processing_times
            })
        return Response(serializer.data)


class JobnameExplanationView(viewsets.ModelViewSet):
    serializer_class = JobnameExplanationSerializer
    queryset = JobnameExplanation.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class JobnameLinksView(viewsets.ModelViewSet):
    serializer_class = JobnameLinksSerializer
    queryset = JobnameLinks.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class LinksView(viewsets.ModelViewSet):
    serializer_class = LinksSerializer
    queryset = Links.objects.all()


class ObtainedResultMachineAPIView(viewsets.ModelViewSet):
    serializer_class = ObtainedResultMachineSerializer

    def get_queryset(self):
        return ObtainedResultMachine.objects.all()

    def my_view(request):
        data = json.loads(request.body)
        obtainedResultMachineData = data['obtainedResultMachineData']
        # обработка полученных данных

    # @api_view(['PUT'])
    # def update_or_create_result(request):
    #     result_data = request.data
    #     stage = result_data.get('stage')
    #     if stage is not None:
    #         result = get_object_or_404(Result, stage=stage)
    #         serializer = ResultSerializer(result, data=result_data)
    #     else:
    #         serializer = ResultSerializer(data=result_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def save_obtained_result_machine_data(data):
    #     obtained_result_machine_list = []
    #     for item in data:
    #         obtained_result_machine = ObtainedResultMachine(
    #             department=item['department'],
    #             department_name=item['department_name'],
    #             machine=item['machine'],
    #             name_machine=item['name_machine'],
    #             description_machine=item['description_machine'],
    #             job=item['job'],
    #             job_name=item['job_name'],
    #             descripiton_job=item['descripiton_job'],
    #             T_i=datetime.strptime(item['T_i'], '%Y-%m-%d').date(),
    #             T_c=datetime.strptime(item['T_c'], '%Y-%m-%d').date()
    #         )
    #         obtained_result_machine_list.append(obtained_result_machine)
    #     return obtained_result_machine_list

    # def CreateModel_ObtainedResultMachine(self, ObtainedResultMachineModel, stagesGroupCopyArray, jobnameslinksGroupCopyArray, obtainedResultMachineData):
    #     # your code here

    #     obtained_result_machine_list = self.save_obtained_result_machine_data(
    #         obtainedResultMachineData)
    #     ObtainedResultMachine.objects.bulk_create(obtained_result_machine_list)

    # your code here
    # your code here

    # def get(self, request):
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many=True)
    #     data = []
    #     for item in queryset:
    #         data.append({
    #             'id': item.id,
    #             'machine': item.machine,
    #             'name_machine': item.name_machine,
    #             'description_machine': item.description_machine,
    #             'job': item.job
    #         })
    #     return Response(serializer.data)
