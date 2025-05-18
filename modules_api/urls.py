from django.urls import path
from .views import HomeView, ListModules, ModuleView, RunModule, RunStatus


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/modules', ListModules.as_view(), name='list_modules'),
    path('api/module/<str:backend>', ModuleView.as_view(), name='module_view'),
    path('api/run-module', RunModule.as_view(), name='run_module'),
    path('api/status/<str:task_id>', RunStatus.as_view(), name='run_status'),
]