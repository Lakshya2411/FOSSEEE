from rest_framework import serializers
from .models import Upload, Equipment

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class UploadSerializer(serializers.ModelSerializer):
    # We might not want to return all equipments in the list view for performance, 
    # but for detail view it is fine.
    equipments = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Upload
        fields = ['id', 'file', 'uploaded_at', 'equipments']
