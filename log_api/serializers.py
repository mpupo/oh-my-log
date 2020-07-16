from rest_framework import serializers
from log_api.models import User, UserProfile, Machine, Application, Execution, Event
import datetime


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["nickname", "last_login", "active"]


class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileModelSerializer(required=True)

    class Meta:
        model = User
        fields = ["url", "email", "first_name", "last_name", "password", "profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")

        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        try:
            profile = UserProfile.objects.get(user=instance.pk)
        except Exception:
            UserProfile.objects.create(user=instance, **profile_data)
        else:
            profile = instance.profile
            profile.nickname = profile_data.get("nickname", profile.nickname)
            profile.active = profile_data.get("active", profile.active)
            profile.last_time_modified = datetime.datetime.now()
            profile.save()

        return instance


class ApplicationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "name", "active", "description", "version"]


class MachineModelSerializer(serializers.ModelSerializer):
    applications = ApplicationModelSerializer(many=True, required=False)

    class Meta:
        model = Machine
        fields = ["id", "name", "active", "environment", "address", "applications"]

    def create(self, validated_data):
        if validated_data.get("applications"):
            apps = validated_data.pop("applications")
            machine = Machine.objects.create(**validated_data)
            for app in apps:
                apps_serializer = ApplicationModelSerializer(data=app)
                apps_serializer.is_valid(raise_exception=True)
                machine.applications.add(apps_serializer.save())
        else:
            machine = Machine.objects.create(**validated_data)
        return machine

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.active = validated_data.get("active", instance.active)
        instance.environment = validated_data.get("environment", instance.environment)
        instance.address = validated_data.get("address", instance.address)
        instance.save()

        if validated_data.get("applications"):
            apps_data = validated_data.pop("applications")

            for app in apps_data:
                name = app.get("name")
                app_model = Application.objects.get(name=name)
                instance.applications.add(app_model)

        return instance


class ExecutionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = ["id", "machine_id", "application_id", "dateref", "success"]


class EventModelSerializer(serializers.ModelSerializer):
    execution_id = serializers.PrimaryKeyRelatedField(queryset=Execution.objects.all())

    class Meta:
        model = Event
        fields = ["id", "level", "dateref", "archived", "description", "execution_id"]
