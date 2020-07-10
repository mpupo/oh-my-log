from rest_framework import serializers
from log_api.models import User, Machine, OperationSystem

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']


class OperationSystemModelSerializer(serializers.ModelSerializer):
    #machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all(),many=True)
    class Meta:
        model = OperationSystem
        fields = ['id', 'name', 'version']


class MachineModelSerializer(serializers.ModelSerializer):
    operation_systems = OperationSystemModelSerializer(many=True)

    class Meta:
        model = Machine
        fields = ['id', 'name', 'active', 'environment', 'address', 'operation_systems']


    def create(self, validated_data):
        machine_os = validated_data.pop('operation_systems')
        machine = Machine.objects.create(**validated_data)
        for os in machine_os:
            operation_serializer = OperationSystemModelSerializer(data=os)
            operation_serializer.is_valid(raise_exception=True)
            machine.operation_systems.add(operation_serializer.save())
        return machine

