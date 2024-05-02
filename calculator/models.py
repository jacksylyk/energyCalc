from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Client(models.Model):
    LOCAL_BUDGET = 'Местный бюджет'
    STATE_BUDGET = 'Республиканский бюджет'
    LEGAL_ENTITY = 'Юридическое лицо'

    CONSUMER_GROUP_CHOICES = [
        (LOCAL_BUDGET, 'Местный бюджет'),
        (STATE_BUDGET, 'Республиканский бюджет'),
        (LEGAL_ENTITY, 'Юридическое лицо'),
    ]

    name = models.CharField(max_length=100, verbose_name="Наименование")
    bin_number = models.CharField(max_length=12, verbose_name="БИН номер")
    information = models.CharField(max_length=256, verbose_name="Информация ПКУ", blank=True)
    contract_number = models.CharField(max_length=50, verbose_name="Номер договора")
    contract_date = models.DateField(verbose_name="Дата акта")
    location = models.CharField(max_length=128, verbose_name="Местоположение ПКУ", blank=True)
    notes = models.CharField(max_length=256, verbose_name="Примечания", blank=True)
    address = models.CharField(max_length=256, verbose_name="Юридический адрес", blank=True)
    consumer_group = models.CharField(max_length=50, choices=CONSUMER_GROUP_CHOICES, verbose_name="Группа потребителей",
                                      default=LOCAL_BUDGET)

    class Meta:
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts', verbose_name="Клиент")
    contact = models.CharField(max_length=100, verbose_name="Контакт")

    def __str__(self):
        return self.contact


# Модель для счета
class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices', verbose_name="Клиент")
    ktt = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)], verbose_name="KTT")
    voltage = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)],
                                  verbose_name="Напряжение")
    start = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)],
                                verbose_name="Начало")
    end = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)], verbose_name="Конец")
    xx = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)], verbose_name="XX")
    tariff = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)],
                                 verbose_name="Тариф")
    loss_xx = models.IntegerField(verbose_name="Потери XX", default=0)
    recalculation = models.IntegerField(verbose_name="Перерасчет")

    @property
    def consumption(self):
        result = ((self.end - self.start) * self.ktt) * ((self.xx + 100) / 100)
        result = (100 + self.loss_xx) * result

        result = (100 + self.recalculation) * result

        return result

    @property
    def without_vat(self):
        return self.consumption * self.tariff

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f"Cчет №{self.pk} - {self.client} "
