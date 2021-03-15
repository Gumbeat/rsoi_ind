import os

from django.db import models

# Create your models here.
from django.db.models import Max
from .index import index


class Document(models.Model):
    text = models.TextField(verbose_name='Документ')
    number = models.IntegerField(verbose_name='Номер', blank=True, null=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    @staticmethod
    def get_max_number():
        max_number = Document.objects.aggregate(Max('number'))['number__max']
        if max_number:
            return max_number + 1
        return 1

    def save(self, *args, **kwargs):
        # toDo: создавать файл и перестраивать индекс
        if not self.number:
            self.number = Document.get_max_number()
        filename = str(self.number) + '.txt'
        folder_name = 'documents\\'
        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, f'{folder_name}{filename}'))
        with open(filepath, 'w', encoding='utf-8') as temp_file:
            temp_file.write(self.text)
        index.rebuild()
        super(Document, self).save(*args, **kwargs)
