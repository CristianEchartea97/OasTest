from django.db import models
from .tasks import request_presigned_upload_url   # <--- add this line

# Create your models here.


class Sale(models.Model):
    release_id = models.CharField(max_length=255)
    isrc_id = models.CharField(max_length=64)
    quantity = models.IntegerField()
    currency = models.CharField(max_length=3)
    territory = models.CharField(max_length=2)
    date = models.DateTimeField()
    sale_type = models.CharField(max_length=1)
    release_title = models.CharField(max_length=255)
    track_title = models.CharField(max_length=255)
    label_id = models.CharField(max_length=255)
    artists = models.CharField(max_length=255)
    service_id = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    line_number = models.IntegerField()
    accounting_date = models.DateField()
    exchange_rate = models.DecimalField(max_digits=29, decimal_places=20)
    total_foreign = models.DecimalField(max_digits=29, decimal_places=20)
    total_local = models.DecimalField(max_digits=29, decimal_places=20)
    total_gross = models.DecimalField(max_digits=29, decimal_places=20)
    total_net = models.DecimalField(max_digits=29, decimal_places=20)
    # organisation = models.ForeignKey('organisations.Organisation', on_delete=models.CASCADE)
    # salesfile = models.ForeignKey('SalesFile', on_delete=models.CASCADE)


class SalesFile(models.Model):
    status = models.CharField(
        max_length=32,
        choices=(
            ('INITIALIZED', 'Initialized'),
            ('UPLOADING', 'Uploading'),
            ('PENDING', 'Pending'),
            ('PROCESSING', 'Processing'),
            ('PROCESSED', 'Processed'),
            ('FAILED', 'Failed'),
        ),
        default='INITIALIZED',
    )
    status_cause = models.CharField(max_length=512, blank=True, null=True)
    filetype = models.CharField(max_length=12)
    filename = models.CharField(max_length=512)
    filesize = models.IntegerField()
    s3_key = models.CharField(max_length=512, blank=True, null=True)
    mongo_id = models.CharField(max_length=512, blank=True, null=True)
    execution_arn = models.CharField(max_length=512, blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True, editable=False, db_index=True)
    updated = models.DateTimeField(
        auto_now=True, editable=False, db_index=True)

    def save(self, *args, **kwargs):
        if not self.s3_key:
            # self.s3_key = f"{self.organisation.id}/{self.filename}"
            org = 'test'
            self.s3_key = f"{org}/{self.filename}"

        super().save(*args, **kwargs)

    # ...
    def generate_presigned_url(self):
        return request_presigned_upload_url(key=self.s3_key)

    # organisation = models.ForeignKey('organisations.Organisation', on_delete=models.CASCADE)
