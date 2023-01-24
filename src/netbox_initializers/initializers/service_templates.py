from ipam.models import ServiceTemplate

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name"]


class ServiceTemplateInitializer(BaseInitializer):
    data_file_name = "service_templates.yml"

    def load_data(self):
        service_templates = self.load_yaml()
        if service_templates is None:
            return
        for params in service_templates:
            custom_field_data = self.pop_custom_fields(params)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            service_template, created = ServiceTemplate.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🧰 Created Service Template", service_template.name)

            self.set_custom_fields_values(service_template, custom_field_data)


register_initializer("service_templates", ServiceTemplateInitializer)
