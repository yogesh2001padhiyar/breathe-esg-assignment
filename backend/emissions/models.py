from django.db import models

# Create your models here.
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class DataSource(models.Model):
    SOURCE_TYPES = [
        ('sap', 'SAP'),
        ('utility', 'Utility'),
        ('travel', 'Travel'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_file_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company.name} - {self.source_type}"


class EmissionRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)

    scope = models.CharField(max_length=50)
    activity_type = models.CharField(max_length=255)

    quantity = models.FloatField()
    unit = models.CharField(max_length=50)

    normalized_value = models.FloatField(null=True, blank=True)

    record_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_flagged = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity_type
