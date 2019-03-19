from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Client(models.Model):
    name = models.CharField(max_length=100)

    sftp_host = models.CharField(max_length=100, verbose_name='hostname')
    sftp_port = models.IntegerField(default=22, validators=[MinValueValidator(0), MaxValueValidator(65535)], verbose_name='port')
    sftp_path = models.CharField(max_length=100, default='/', verbose_name='directory path')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clients-detail', kwargs={'pk': self.pk})
