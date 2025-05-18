from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Module
from .serializers import GetModuleSerializer, ListModulesSerializer
from celery.result import AsyncResult
from modules_api.tasks import run_scraper_task
from celery_app import celery



class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})
    

class ListModules(APIView):
    serializer_class = ListModulesSerializer
    def get(self, request):
        modules = Module.objects.all()
        serializer = self.serializer_class(modules, many=True)
        print(serializer.data)
        return Response(serializer.data)
    

class ModuleView(APIView):
    serializer_class = GetModuleSerializer
    def get(self, request, backend):
        module = Module.objects.filter(backend=backend).first()
        if module:
            serializer = self.serializer_class(module)
            print(serializer.data)
            return Response(serializer.data)
        else:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

class RunModule(APIView):
    def post(self, request):
        backend = request.data.get('module')
        data = request.data.get('data')
        print(backend, data)
        module = Module.objects.filter(backend=backend).first()
        if module:
            task = run_scraper_task.delay(module.backend, dict(data))
            return Response({"task_id": task.id})
        else:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)


class RunStatus(APIView):
    def get(self, request, task_id):
        task = AsyncResult(task_id, app=celery)
        if task.state == "PENDING":
            return Response({"status": "running"})
        elif task.state == "FAILURE":
            return Response({"status": "error", "error": str(task.result)})
        elif task.state == "SUCCESS":
            return Response({"status": "done", "data": task.result})
        return Response({"status": task.state})
    
