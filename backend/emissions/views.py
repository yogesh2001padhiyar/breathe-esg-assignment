from django.shortcuts import render

import csv
from datetime import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import (
    EmissionRecord,
    Company,
    DataSource
)

from .serializers import EmissionRecordSerializer


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "Backend working"
    })


@api_view(['GET'])
def emission_records(request):
    records = EmissionRecord.objects.all()
    serializer = EmissionRecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def ingest_sap_data(request):

    company = Company.objects.first()

    source = DataSource.objects.create(
        company=company,
        source_type='sap',
        original_file_name='sap_fuel_data.csv'
    )

    file_path = './sample_data/sap_fuel_data.csv'

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            quantity = float(row['quantity'])

            EmissionRecord.objects.create(
                company=company,
                source=source,
                scope='Scope 1',
                activity_type=row['fuel_type'],
                quantity=quantity,
                unit=row['unit'],
                normalized_value=quantity * 2.5,
                record_date=datetime.strptime(
                    row['date'],
                    '%Y-%m-%d'
                ).date(),
                status='pending',
                is_flagged=quantity > 10000
            )

    return Response({
        "message": "SAP data ingested successfully"
    })
@api_view(['POST'])
def update_record_status(request, record_id):

    try:
        record = EmissionRecord.objects.get(id=record_id)

        status_value = request.data.get('status')

        if status_value in ['approved', 'rejected']:
            record.status = status_value
            record.save()

            return Response({
                "message": f"Record marked as {status_value}"
            })

        return Response({
            "error": "Invalid status"
        }, status=400)

    except EmissionRecord.DoesNotExist:
        return Response({
            "error": "Record not found"
        }, status=404)