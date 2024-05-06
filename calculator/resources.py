from import_export import resources, fields

from calculator.models import Invoice


class ClientResource(resources.ModelResource):
    consumption = fields.Field(column_name="Consumption", attribute="consumption")
    without_vat = fields.Field(column_name="Without VAT", attribute="without_vat")
    meter_readings = fields.Field(column_name="Meter Readings")

    class Meta:
        model = Invoice
        fields = ('client', 'client__location', 'client__information', 'client__contract_date', 'voltage',
                  'client__bin_number', 'start', 'end', 'consumption', 'without_vat', 'meter_readings')

    def get_meter_readings(self, obj):
        return [obj.start, obj.end]
