from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from log_api.models import User, UserProfile, Machine, Application, Execution, Event
import datetime


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["nickname", "last_login", "active"]


class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileModelSerializer(required=True)

    included_serializers = {
        'machines': "log_api.serializers.MachineModelSerializer"
    }

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


class ApplicationModelSerializer(serializers.HyperlinkedModelSerializer):

    included_serializers = {
        'machines': 'log_api.serializers.MachineModelSerializer'
    }

    class JSONAPIMeta:
        included_resources = ['machines']

    class Meta:
        model = Application
        fields = ["id", "name", "active", "description", "version","url"]

class MachineModelSerializer(serializers.HyperlinkedModelSerializer):

    included_serializers = {
        'applications': ApplicationModelSerializer
    }

    applications = serializers.ResourceRelatedField(
        queryset=Application.objects, 
        many=True,
        related_link_view_name='machine-related',
        related_link_url_kwarg='pk',
        self_link_view_name='machine-relationships'
    )

    class Meta:
        model = Machine
        fields = ["id", "name", "active", "environment", "address", "applications", 'url']

    class JSONAPIMeta:
        included_resources = ['applications']

class ExecutionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = ["id", "machine_id", "application_id", "dateref", "success"]


class EventModelSerializer(serializers.ModelSerializer):
    execution_id = serializers.ResourceRelatedField(queryset=Execution.objects.all())

    class Meta:
        model = Event
        fields = ["id", "level", "dateref", "archived", "description", "execution_id"]
