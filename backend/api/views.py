from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import models, transaction
import pandas as pd
from .models import Upload, Equipment
from .serializers import UploadSerializer, EquipmentSerializer

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by('-uploaded_at')
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    # Basic Auth is enabled
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        upload_instance = serializer.save()

        try:
            file_path = upload_instance.file.path
            # Error handling for bad CSV
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                raise ValueError("Not a valid CSV file")

            equipments = []
            for _, row in df.iterrows():
                # Handle potential missing or malformed values gracefully
                def safe_float(val):
                    try:
                        return float(val)
                    except:
                        return 0.0

                equipments.append(Equipment(
                    upload=upload_instance,
                    equipment_name=str(row.get('Equipment Name', 'Unknown')),
                    equipment_type=str(row.get('Type', 'Unknown')),
                    flowrate=safe_float(row.get('Flowrate')),
                    pressure=safe_float(row.get('Pressure')),
                    temperature=safe_float(row.get('Temperature'))
                ))
            
            with transaction.atomic():
                Equipment.objects.bulk_create(equipments)
                
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            upload_instance.delete()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        upload = self.get_object()
        equips = upload.equipments.all()
        
        total_count = equips.count()
        if total_count == 0:
            return Response({
                "total_count": 0, 
                "averages": {"flowrate": 0, "pressure": 0, "temperature": 0},
                "type_distribution": []
            })

        avg_flow = equips.aggregate(models.Avg('flowrate'))['flowrate__avg']
        avg_press = equips.aggregate(models.Avg('pressure'))['pressure__avg']
        avg_temp = equips.aggregate(models.Avg('temperature'))['temperature__avg']
        
        # Distribution
        dist = list(equips.values('equipment_type').annotate(count=models.Count('equipment_type')))
        
        data = {
            "total_count": total_count,
            "averages": {
                "flowrate": round(avg_flow, 2) if avg_flow else 0,
                "pressure": round(avg_press, 2) if avg_press else 0,
                "temperature": round(avg_temp, 2) if avg_temp else 0
            },
            "type_distribution": dist
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        recent = self.queryset[:5]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        import io
        from django.http import HttpResponse
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        upload = self.get_object()
        equips = upload.equipments.all()
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, f"Equipment Report for Upload #{upload.id}")
        p.drawString(100, 730, f"Uploaded at: {upload.uploaded_at}")
        
        y = 700
        p.drawString(100, y, "Summary Statistics:")
        y -= 20
        
        avg_flow = equips.aggregate(models.Avg('flowrate'))['flowrate__avg']
        avg_press = equips.aggregate(models.Avg('pressure'))['pressure__avg']
        avg_temp = equips.aggregate(models.Avg('temperature'))['temperature__avg']
        
        p.drawString(120, y, f"Total Count: {equips.count()}")
        y -= 15
        p.drawString(120, y, f"Avg Flowrate: {avg_flow:.2f}" if avg_flow else "Avg Flowrate: N/A")
        y -= 15
        p.drawString(120, y, f"Avg Pressure: {avg_press:.2f}" if avg_press else "Avg Pressure: N/A")
        y -= 15
        p.drawString(120, y, f"Avg Temperature: {avg_temp:.2f}" if avg_temp else "Avg Temperature: N/A")
        
        y -= 40
        p.drawString(100, y, "Equipment List (First 20 items):")
        y -= 20
        
        for eq in equips[:20]:
            text = f"{eq.equipment_name} ({eq.equipment_type}) - F:{eq.flowrate}, P:{eq.pressure}, T:{eq.temperature}"
            p.drawString(120, y, text)
            y -= 15
            if y < 50:
                p.showPage()
                y = 750
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
