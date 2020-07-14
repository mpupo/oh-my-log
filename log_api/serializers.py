from rest_framework import serializers
from log_api.models import User, Machine, OperationSystem, Application, Execution, Event


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]


class ApplicationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "name", "active", "description", "version"]


class OperationSystemModelSerializer(serializers.ModelSerializer):
    installed_apps = ApplicationModelSerializer(many=True, required=False)

    class Meta:
        model = OperationSystem
        fields = ["id", "name", "version", "installed_apps"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.version = validated_data.get("version", instance.version)
        instance.save()

        if validated_data.get("installed_apps"):
            apps_data = validated_data.pop("installed_apps")

            for app in apps_data:
                name = app.get("name")
                app_model = Application.objects.get(name=name)
                instance.installed_apps.add(app_model)

        return instance


class MachineModelSerializer(serializers.ModelSerializer):
    operation_systems = OperationSystemModelSerializer(many=True, required=False)

    class Meta:
        model = Machine
        fields = ["id", "name", "active", "environment", "address", "operation_systems"]

    def create(self, validated_data):
        machine_os = validated_data.pop("operation_systems")
        machine = Machine.objects.create(**validated_data)
        for os in machine_os:
            operation_serializer = OperationSystemModelSerializer(data=os)
            operation_serializer.is_valid(raise_exception=True)
            machine.operation_systems.add(operation_serializer.save())
        return machine


class ExecutionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = ['id', 'machine_id', 'application_id', 'dateref', 'success']


class EventModelSerializer(serializers.ModelSerializer):
    execution = ExecutionModelSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "level", "dateref", "archived", "description", "execution"]

