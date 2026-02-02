from django.db import models

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload {self.id} at {self.uploaded_at}"

class Equipment(models.Model):
    upload = models.ForeignKey(Upload, related_name='equipments', on_delete=models.CASCADE)
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()

    def __str__(self):
        return self.equipment_name
