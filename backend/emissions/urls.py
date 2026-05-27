from django.urls import path

from .views import (
    health_check,
    emission_records,
    ingest_sap_data,
    update_record_status
)

urlpatterns = [
    path('health/', health_check),
    path('records/', emission_records),
    path('ingest-sap/', ingest_sap_data),

    path(
        'records/<int:record_id>/status/',
        update_record_status
    ),
]