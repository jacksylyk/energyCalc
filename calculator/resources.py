from import_export import resources, fields

from calculator.models import Invoice


class ClientResource(resources.ModelResource):
    consumption = fields.Field(column_name="Consumption", attribute="consumption")
    without_vat = fields.Field(column_name="Without VAT", attribute="without_vat")
    client = fields.Field(column_name="Клиент", attribute="client")
    client__location = fields.Field(column_name="Местоположение ПКУ", attribute="client__location")
    client__information = fields.Field(column_name="Информация о ПКУ", attribute="client__information")
    client__contract_date = fields.Field(column_name="Дата акта", attribute="client__contract_date")
    voltage = fields.Field(column_name="U \n кВт", attribute="voltage")
    client__bin_number = fields.Field(column_name="БИН", attribute="client__bin_number")
    start = fields.Field(column_name="Начало показании", attribute="start")
    end = fields.Field(column_name="Конец показании", attribute="end")
    consumption = fields.Field(column_name="Потребление", attribute="consumption")
    without_vat = fields.Field(column_name="Без НДС", attribute="without_vat")

    class Meta:
        model = Invoice
        fields = ('client', 'client__location', 'client__information', 'client__contract_date', 'voltage',
                  'client__bin_number', 'start', 'end', 'consumption', 'without_vat')