from rest_framework import serializers
from .models import Module



class ListModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["name","description","premium","repository", "backend"]


class GetModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["name","description","premium","repository","inputs","outputs","max_results", "backend"]



