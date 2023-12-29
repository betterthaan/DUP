from django.db import models
import datetime
from rest_framework.response import Response


# Create your models here.
class Machine(models.Model):
    name_machine = models.TextField("Машина", max_length=100)
    description = models.TextField("Пояснение")
    id_department = models.PositiveIntegerField("Id Department")

    def __str__(self):
        return self.name_machine

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"


class Job(models.Model):
    # release_dates = models.PositiveIntegerField("Release dates", default = 0, blank="True")
    priority = models.PositiveIntegerField("Приоритет выполнения")
    machine = models.ForeignKey(
        Machine, verbose_name="Машина", on_delete=models.CASCADE, null=False)
    processing_times = models.PositiveIntegerField("Время выполнения процесса")
    # prev_stage = models.ManyToManyField(PrevStage, blank=True)
    # prev_stage = models.ManyToManyField(
    #     'self', verbose_name='Предыдущий этап', blank=True)

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.prev_stage.through.objects.filter(from_job_id=self.id).delete()
    #     for prev_job in self.prev_stage.all():
    #         self.prev_stage.through.objects.create(
    #             from_job_id=prev_job.id,
    #             to_job_id=self.id,
    #         )


class Links(models.Model):
    from_stage = models.PositiveIntegerField("From")
    to_stage = models.PositiveIntegerField("To")


class JobName(models.Model):
    name_job = models.CharField("Работа", max_length=100, blank="True")
    description = models.TextField("Пояснение")
    due_dates = models.DateField("Due dates", blank="True")
    explanation = models.ManyToManyField(Job, related_name='explanation')
    links = models.ManyToManyField(Links, related_name='links')
    # department = models.ManyToManyField(Department, related_name='department')
    # name_department = models.CharField("Цех", max_length=100, blank=True)
    id_department = models.PositiveIntegerField("Id Department")


# class Department(models.Model):
#     name_department = models.CharField("Цех", max_length=100, blank="True")
#     job_name = models.ManyToManyField(JobName, related_name='job_name')

class Department(models.Model):
    name_department = models.CharField("Цех", max_length=100, blank="True")
    # job_name = models.ManyToManyField(JobName, related_name='job_name')


class ObtainedResult(models.Model):
    id = models.IntegerField(primary_key=True)
    job = models.IntegerField()
    name_job = models.CharField(max_length=255)
    description = models.TextField()
    due_dates = models.IntegerField()
    priority = models.IntegerField()
    processing_times = models.IntegerField()
    machine_id = models.IntegerField()
    # machine_id = models.ForeignKey(Machine, verbose_name="Машина", on_delete=models.CASCADE, null=False)
    name_machine = models.CharField(max_length=255)
    description_machine = models.TextField()
    T_i = models.DateField()
    T_c = models.DateField()
    score = models.IntegerField()

    @classmethod
    def create_from_data(cls, data):
        # for item in data:
        #     cls.objects.create(
        #         # job=item["job"],
        #         name_job=item["name_job"],
        #         description=item["description"],
        #         due_dates=item["due_dates"],
        #         priority=item["priority"],
        #         processing_times=item["processing_times"],
        #         machine_id=item["machine_id"],
        #         name_machine=item["name_machine"],
        #         description_machine=item["description_machine"],
        #         T_i=item["T_i"],
        #         T_c=item["T_c"],
        #         score=item["score"]
        #     )
        # Приведем данные к нужному формату(массив массивов) для вывода на диаграмму Ганта
        result = []
        for item in data:
            t_i = datetime.datetime.strptime(
                item["T_i"], "%Y-%m-%d").strftime("%Y-%m-%d")
            t_c = datetime.datetime.strptime(
                item["T_c"], "%Y-%m-%d").strftime("%Y-%m-%d")
            task = [
                item["name_job"],
                item["name_machine"],
                # new Date(2022, 0, 1),
                # new Date(2022, 2, 1),
                item["T_i"],
                item["T_c"],
                # t_i,
                # t_c,
                item["processing_times"],
                item["score"] / 100  # прогресс задачи в процентах
            ]
            result.append(task)
        return result


class ObtainedResultMachine(models.Model):
    # id = models.IntegerField(primary_key=True)
    # id = models.AutoField(primary_key=True)
    # у каждого цеха будет свое расписание
    stage = models.PositiveIntegerField("Id Stage")
    department = models.PositiveIntegerField("Id Department")
    department_name = models.CharField("Department Name", max_length=255)
    machine = models.PositiveIntegerField()
    name_machine = models.CharField(max_length=255)
    description_machine = models.TextField()
    job = models.PositiveIntegerField()
    job_name = models.CharField(max_length=255)
    descripiton_job = models.TextField()
    T_i = models.DateField()  # date start
    T_c = models.DateField()  # date finish
    # obtained_result = models.ManyToManyField(ObtainedResult, related_name='obtained_result')


# class JobnameExplanation(models.Model):
#     id = models.IntegerField(primary_key=True)
#     jobname_id = models.ForeignKey(JobName, models.DO_NOTHING)
#     job_id = models.ForeignKey(Job, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'app_jobname_explanation'
#         unique_together = (('id', 'jobname_id', 'job_id'),)
class JobnameExplanation(models.Model):
    jobname = models.ForeignKey(JobName, models.DO_NOTHING)
    job = models.ForeignKey(Job, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_jobname_explanation'


# модель, которая создалась в бд исходя из связей моделей
class JobnameLinks(models.Model):
    jobname = models.ForeignKey(JobName, models.DO_NOTHING)
    links = models.ForeignKey(Links, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_jobname_links'
