from rest_framework import serializers
from .models import Brief, Appr, Group

class ApprSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appr
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    grp_apprs = ApprSerializer(many=True)
    class Meta:
        model = Group
        fields = ["grp_nom", "grp_apprs"]

class BriefSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = Brief
        fields = ["brief_title", "brief_url", "brief_nb_apprs", "groups"]