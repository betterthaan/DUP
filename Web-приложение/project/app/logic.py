# from .serializers import StageSerializer
from datetime import datetime, timedelta
# import datetime
from . models import *
from itertools import groupby
from django.db import models


def JobWithMinDueDates(machines_group):

    # for item in group:
    #     machines_group.append(group)
    #     if item.d_j < min_due_dates:
    #         min_due_dates = item.d_j

    # print('machines_group', machines_group)
    # return min_due_dates
    # for group in machines_group.values():
    #     min_due_dates = float('inf')
    #     for element in group:
    #         # print(element.name_machine)
    #         if element.d_j < min_due_dates:
    #             min_due_dates = element.d_j

    #     print(element.name_machine, min_due_dates)
    # for group in machines_group.values():
    #     for element in sorted(group, key=lambda x: x.processing_times):
    for group_id, group in machines_group.items():
        sorted_group = sorted(group, key=lambda x: x.d_j)
        # group_string = ", ".join(str(element.d_j) for element in sorted_group)
        # group_string = ",".join(f"({element.machine_id}, {element.name_machine}, {element.d_j})" for element in sorted_group)
        # print(f"Group {group_id}: {group_string}")
        for element in sorted_group:
            print(element.d_j)
        print()


def SamePriorityJob(job, jobs_name):
    amount = 0
    proc_time_same_priority_jobs = 0
    for job_name in jobs_name:
        if job_name.pk != job.pk and job_name.id == job.id and job_name.priority == job.priority:
            amount += 1
            if job_name.processing_times > proc_time_same_priority_jobs:
                proc_time_same_priority_jobs = job_name.processing_times

    if amount > 0:
        return proc_time_same_priority_jobs, job.id
    else:
        return job.processing_times, 0


def processTimeSubsOperations(job, jobs_name):
    processing_times_subs_jobs = 0
    job_id = 0

    for job_name in jobs_name:
        if job_name.priority > job.priority and job_name.id == job.id and job_name.pk != job.pk and job_name.id != job_id:
            same_processing_times, job_id = SamePriorityJob(
                job_name, jobs_name)
            processing_times_subs_jobs += same_processing_times
            # print(processing_times_subs_jobs)

    # if processing_times_subs_jobs == 0:
    #     # print(job.due_dates)
    #     return job.due_dates
    # else:
    #     # print(processing_times_subs_jobs)
    #     return processing_times_subs_jobs
    return job.due_dates - processing_times_subs_jobs


def processTimePrevOperations(job, jobs_name):
    processing_times_prev_jobs = 0
    job_id = 0

    for job_name in jobs_name:
        # print(job.id)
        if job_name.pk != job.pk and job_name.id == job.id and job_name.id != job_id and job_name.priority < job.priority:
            same_processing_times, job_id = SamePriorityJob(
                job_name, jobs_name)
            processing_times_prev_jobs += same_processing_times

    return processing_times_prev_jobs


def logic_schedule():
    queryset = JobName.objects.all()

    class StagesOfJobs:
        def __init__(self,
                     pk,
                     id,
                     name_job,
                     description,
                     due_dates,
                     priority,
                     processing_times,
                     machine_id,
                     name_machine,
                     description_machine
                     ):
            self.pk = pk
            self.id = id
            self.name_job = name_job
            self.description = description
            self.due_dates = due_dates
            self.priority = priority
            self.processing_times = processing_times
            self.machine_id = machine_id
            self.name_machine = name_machine
            self.description_machine = description_machine

    jobs_name = []
    e_pk = 0
    # jobs = []
    for q in queryset:
        # print(q.firstname);
        # print("Total score for %(n)s is %(s)s" % {'n': q.name_job, 's': q.due_dates});
        # print(q.name_job, " ", q.due_dates)
        date_str = q.due_dates
        # today = datetime.today().date()
        # today = datetime.now().date()
        today = datetime.date.today()
        # delta = date_str - today
        delta = (date_str - today).days

        # queryset = JobName.objects.get(name_job=q.name_job)
        # explanation = queryset.explanation.all()
        explanation = q.explanation.all()

        for e in explanation:
            e_pk += 1
            # queryset = Job.objects.get(id = e.machine_id)
            # machines = queryset.machine
            machines = Machine.objects.get(id=e.machine_id)

            job = StagesOfJobs(
                e_pk,
                q.id,
                q.name_job,
                q.description,
                delta + 1,
                e.priority,
                e.processing_times,
                machines.id,
                machines.name_machine,
                machines.description
            )
            jobs_name.append(job)

    # for job in jobs_name:
    #     print(
    #           job.pk,
    #           job.id,
    #           job.name_job, ",",
    #           job.description, ",",
    #           job.due_dates, ",",
    #           job.priority, ",",
    #           job.processing_times, " machine_id:",
    #           job.machine_id, ",",
    #           job.name_machine, ",",
    #           job.description_machine
    #           )

    class SMSP:
        def __init__(self,
                     pk,
                     id,
                     name_job,
                     description,
                     due_dates,
                     priority,
                     processing_times,
                     machine_id,
                     name_machine,
                     description_machine,
                     r_i,
                     d_j
                     ):
            self.pk = pk
            self.id = id
            self.name_job = name_job
            self.description = description
            self.due_dates = due_dates
            self.priority = priority
            self.processing_times = processing_times
            self.machine_id = machine_id
            self.name_machine = name_machine
            self.description_machine = description_machine
            self.r_i = r_i
            self.d_j = d_j

    smsps = []
    for job in jobs_name:
        if job.priority == 1:
            r_i = 0
        else:
            r_i = processTimePrevOperations(job, jobs_name)

        d_j = processTimeSubsOperations(job, jobs_name)

        smsp = SMSP(
            job.pk,
            job.id,
            job.name_job,
            job.description,
            job.due_dates,
            job.priority,
            job.processing_times,
            job.machine_id,
            job.name_machine,
            job.description_machine,
            r_i,
            d_j
        )
        smsps.append(smsp)
    print("machine1")
    for smsp in smsps:
        if smsp.machine_id == 1:
            print(
                #   smsp.pk,
                #   smsp.id,
                #   smsp.name_job, ",",
                #   smsp.description, ",",
                smsp.due_dates, ",",
                #   smsp.priority, ",",
                smsp.processing_times,
                #   smsp.machine_id, ",",
                #   smsp.name_machine, ",",
                #   smsp.description_machine,
                smsp.r_i,
                smsp.d_j
            )
    print("machine6")
    for smsp in smsps:
        if smsp.machine_id == 2:
            print(
                #   smsp.pk,
                #   smsp.id,
                #   smsp.name_job, ",",
                #   smsp.description, ",",
                smsp.due_dates, ",",
                #   smsp.priority, ",",
                smsp.processing_times,
                #   smsp.machine_id, ",",
                #   smsp.name_machine, ",",
                #   smsp.description_machine,
                smsp.r_i,
                smsp.d_j
            )
    print("machine5")
    for smsp in smsps:
        if smsp.machine_id == 3:
            print(
                #   smsp.pk,
                #   smsp.id,
                #   smsp.name_job, ",",
                #   smsp.description, ",",
                smsp.due_dates, ",",
                #   smsp.priority, ",",
                smsp.processing_times,
                #   smsp.machine_id, ",",
                #   smsp.name_machine, ",",
                #   smsp.description_machine,
                smsp.r_i,
                smsp.d_j
            )
    print("machine4")
    for smsp in smsps:
        if smsp.machine_id == 4:
            print(
                #   smsp.pk,
                #   smsp.id,
                #   smsp.name_job, ",",
                #   smsp.description, ",",
                smsp.due_dates, ",",
                #   smsp.priority, ",",
                smsp.processing_times,
                #   smsp.machine_id, ",",
                #   smsp.name_machine, ",",
                #   smsp.description_machine,
                smsp.r_i,
                smsp.d_j
            )
    print("machine3")
    for smsp in smsps:
        if smsp.machine_id == 5:
            print(
                #   smsp.pk,
                #   smsp.id,
                #   smsp.name_job, ",",
                #   smsp.description, ",",
                smsp.due_dates, ",",
                #   smsp.priority, ",",
                smsp.processing_times,
                #   smsp.machine_id, ",",
                #   smsp.name_machine, ",",
                #   smsp.description_machine,
                smsp.r_i,
                smsp.d_j
            )
    print("machine2")
    for smsp in smsps:
        if smsp.machine_id == 6:
            print(
                #   smsp.pk,
                #   smsp.id,
                #   smsp.name_job, ",",
                #   smsp.description, ",",
                smsp.due_dates, ",",
                #   smsp.priority, ",",
                smsp.processing_times,
                #   smsp.machine_id, ",",
                #   smsp.name_machine, ",",
                #   smsp.description_machine,
                smsp.r_i,
                smsp.d_j
            )

    machines_group = {}
    smsps.sort(key=lambda x: x.machine_id)
    for key, group in groupby(smsps, lambda x: x.machine_id):
        # values = list(group)
        machines_group[key] = list(group)
        # machines_group.append(values)

        # print(key)
        # print("min due dates", JobWithMinDueDates(group))
        # for item in group:
        # print(item.name_machine, '-', item.processing_times)

    JobWithMinDueDates(machines_group)
    # for smsp in smsps:
    # for group in machines_group.values():
    #     for element in group:
    #         print(element.name_machine)

    class ObtainedResultDecoder:
        def __init__(self,
                     pk,
                     id,
                     name_job,
                     description,
                     due_dates,
                     priority,
                     processing_times,
                     machine_id,
                     name_machine,
                     description_machine,
                     r_i,
                     #  T_i,
                     T_c,
                     score
                     ):
            self.pk = pk
            self.id = id
            self.name_job = name_job
            self.description = description
            self.due_dates = due_dates
            self.priority = priority
            self.processing_times = processing_times
            self.machine_id = machine_id
            self.name_machine = name_machine
            self.description_machine = description_machine
            self.r_i = r_i
            # self.T_i = T_i
            self.T_c = T_c
            self.score = score

    obtained_results_decoder = []
    for group_id, group in machines_group.items():
        sorted_group = sorted(group, key=lambda x: x.d_j)
        score_of_jobs_group = 0
        for element in sorted_group:
            score_of_jobs_group += 1
            obtained_result_decoder = ObtainedResultDecoder(
                element.pk,
                element.id,
                element.name_job,
                element.description,
                element.due_dates,
                element.priority,
                element.processing_times,
                element.machine_id,
                element.name_machine,
                element.description_machine,
                element.r_i,
                element.d_j,
                score_of_jobs_group
            )
            obtained_results_decoder.append(obtained_result_decoder)

    print("Obtained result by the decoder")
    for o in obtained_results_decoder:
        print(
            o.id,
            o.name_machine,
            o.T_c,
            o.score
        )

    class ObtainedResultDecoder2:
        def __init__(self,
                     #  pk,
                     job,  # это Id работы, чтобы в Диаграмме Ганта группировать их по цвету
                     name_job,
                     description,
                     due_dates,
                     priority,
                     processing_times,
                     machine_id,
                     name_machine,
                     description_machine,
                     T_i,
                     T_c,
                     score
                     ):
            # self.pk = pk
            self.job = job
            self.name_job = name_job
            self.description = description
            self.due_dates = due_dates
            self.priority = priority
            self.processing_times = processing_times
            self.machine_id = machine_id
            self.name_machine = name_machine
            self.description_machine = description_machine
            self.T_i = T_i
            self.T_c = T_c
            self.score = score

    obtained_results_decoder2 = []
    for o in obtained_results_decoder:
        if o.score == 1:
            T_i = o.r_i
            T_c = T_i + o.processing_times
            previous_T_c = T_c
        else:
            T_i = previous_T_c
            T_c = T_i + o.processing_times
            previous_T_c = T_c
            # if o.r_i >= previous_T_c:
            #     T_i = previous_T_c
            #     T_c = T_i + o.processing_times
            #     previous_T_c = T_c
            # else:
            #     T_i = o.r_i
            #     T_c = T_i + o.processing_times
            #     previous_T_c = T_c
        # переведм T_i и T_c в дату
        # current_date = datetime.now()
        current_date = datetime.datetime.now()
        result_date_T_i = current_date + timedelta(days=T_i)
        result_date_T_c = current_date + timedelta(days=T_c)
        T_i = result_date_T_i.strftime("%Y-%m-%d")
        T_c = result_date_T_c.strftime("%Y-%m-%d")
        print("T_i:", T_i)
        obtained_result_decoder2 = ObtainedResultDecoder2(
            # o.pk,
            o.id,
            o.name_job,
            o.description,
            o.due_dates,
            o.priority,
            o.processing_times,
            o.machine_id,
            o.name_machine,
            o.description_machine,
            T_i,
            T_c,
            o.score
        )
        obtained_results_decoder2.append(obtained_result_decoder2)

    class ObtainedResultMachineStruct:
        def __init__(self,
                     machine,
                     name_machine,
                     description_machine,
                     job,
                     T_i,
                     T_c
                     ):
            self.machine = machine
            self.name_machine = name_machine
            self.description_machine = description_machine
            self.job = job
            self.T_i = T_i
            self.T_c = T_c

    obtained_results_machine = []
    for o in obtained_results_decoder2:
        obtained_result_machine = ObtainedResultMachineStruct(
            o.machine_id,
            o.name_machine,
            o.description_machine,
            o.job,
            o.T_i,
            o.T_c
        )
        obtained_results_machine.append(obtained_result_machine)

    print("Resuuuuuuuuuuuuuuuuult:")
    for o in obtained_results_decoder2:
        print(
            o.name_machine,
            o.score,
            o.T_i,
            o.T_c
        )

    # class ObtainedResult(models.Model):
    #     id = models.IntegerField(primary_key=True)
    #     # job = models.IntegerField()
    #     name_job = models.CharField(max_length=255)
    #     description = models.TextField()
    #     due_dates = models.IntegerField()
    #     priority = models.IntegerField()
    #     processing_times = models.IntegerField()
    #     machine_id = models.IntegerField()
    #     name_machine = models.CharField(max_length=255)
    #     description_machine = models.TextField()
    #     T_i = models.IntegerField()
    #     T_c = models.IntegerField()
    #     score = models.IntegerField()

    #     @classmethod
    #     def create_from_data(cls, data):
    #         for item in data:
    #             cls.objects.create(

    #                 # job=item["job"],
    #                 name_job=item["name_job"],
    #                 description=item["description"],
    #                 due_dates=item["due_dates"],
    #                 priority=item["priority"],
    #                 processing_times=item["processing_times"],
    #                 machine_id=item["machine_id"],
    #                 name_machine=item["name_machine"],
    #                 description_machine=item["description_machine"],
    #                 T_i=item["T_i"],
    #                 T_c=item["T_c"],
    #                 score=item["score"]
    #             )

    data = []
    for obtained_result in obtained_results_decoder2:
        data.append(
            {
                "job": obtained_result.job,
                "name_job": obtained_result.name_job,
                "description": obtained_result.description,
                "due_dates": obtained_result.due_dates,
                "priority": obtained_result.priority,
                "processing_times": obtained_result.processing_times,
                "machine_id": obtained_result.machine_id,
                "name_machine": obtained_result.name_machine,
                "description_machine": obtained_result.description_machine,
                "T_i": obtained_result.T_i,
                "T_c": obtained_result.T_c,
                "score": obtained_result.score
            }
        )
    data_obtained_result_machine = []
    for obtained_result in obtained_results_machine:
        data_obtained_result_machine.append(
            {
                "machine": obtained_result.machine,
                "name_machine": obtained_result.name_machine,
                "description_machine": obtained_result.description_machine,
                "job": obtained_result.job,
                "T_i": obtained_result.T_i,
                "T_c": obtained_result.T_c
            }
        )
    # ObtainedResult.create_from_data(data)
    # ObtainedResult.objects.all().delete()
    # for item in data:
    #     ObtainedResult.objects.create(**item)
    # for item in data_obtained_result_machine:
    #     ObtainedResultMachine.objects.create(**item)

    print()
    for d in data:
        print(d)
        print()
