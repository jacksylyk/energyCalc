from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    bin_number = models.CharField(max_length=12, verbose_name="БИН номер")
    information = models.CharField(max_length=256, verbose_name="Информация ПКУ", blank=True)
    contract_number = models.CharField(max_length=50, verbose_name="Номер договора")
    contract_date = models.DateField(verbose_name="Дата акта")
    location = models.CharField(max_length=128, verbose_name="Местоположение ПКУ", blank=True)
    notes = models.CharField(max_length=256, verbose_name="Примечания", blank=True)

    class Meta:
        verbose_name_plural = 'Клиенты'


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts', verbose_name="Клиент")
    contact = models.CharField(max_length=100, verbose_name="Контакт")

    def __str__(self):
        return self.contact
