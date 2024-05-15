from django.db import models
#from django.contrib.contenttypes.fields import GenericForeignKey


class ExtraFile(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name='File name'
    )

    circuit = models.ForeignKey(
        to='circuits.Circuit',
        on_delete=models.PROTECT,
        related_name='circuits'
    )

    file = models.FileField(upload_to='extra-files/')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
