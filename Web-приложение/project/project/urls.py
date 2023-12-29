from django.contrib import admin
from django.urls import path, include
from app import views
from app.views import *
from rest_framework import routers
from app.serializers import *

routerJobName = routers.DefaultRouter()
routerMachines = routers.DefaultRouter()
routerObtainedResult = routers.DefaultRouter()
routerObtainedResultMachine = routers.DefaultRouter()
routerJob = routers.DefaultRouter()
routerJobnameExplanation = routers.DefaultRouter()
routerDepartment = routers.DefaultRouter()
routerLinks = routers.DefaultRouter()
routerJobnameLinks = routers.DefaultRouter()

routerJobName.register("", JobNameView, basename='jobnameview')
routerMachines.register("", MachineView, basename='machineview')
routerObtainedResult.register(
    "", ObtainedResultAPIView, basename='obtainedresult')
routerObtainedResultMachine.register(
    "", ObtainedResultMachineAPIView, basename='obtainedresulmachine')
routerJob.register("", JobView, basename='jobview')
routerJobnameExplanation.register(
    "", JobnameExplanationView, basename='jobnameexplanationview')
routerDepartment.register("", DepartmentView, basename='departmentview')
routerLinks.register("", LinksView, basename='linksview')
routerJobnameLinks.register("", JobnameLinksView, basename='jobnamelinksview')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobname/', include((routerJobName.urls, 'jobnameview'))),
    path('machines/', include((routerMachines.urls, 'machineview'))),
    # path('result/', include((routerObtainedResult.urls, 'obtainedresult'))),
    path('result/', include((routerObtainedResultMachine.urls, 'obtainedresultmachine'))),
    path('job/', include((routerJob.urls, 'jobview'))),
    path('explanation/',
         include((routerJobnameExplanation.urls, 'jobnameexplanationview'))),
    path('department/', include((routerDepartment.urls, 'departmentview'))),
    path('links/', include((routerLinks.urls, 'linksview'))),
    path('jobnamelinks/', include((routerJobnameLinks.urls, 'jobnamelinksview'))),
]
