from dcim.models import Manufacturer, ModuleType

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["manufacturer", "model"]
REQUIRED_ASSOCS = {"manufacturer": (Manufacturer, "name")}


class ModuleTypeInitializer(BaseInitializer):
    data_file_name = "module_types.yml"

    def load_data(self):
        module_types = self.load_yaml()
        if module_types is None:
            return
        for params in module_types:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            module_type, created = ModuleType.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🔡 Created module type", module_type.manufacturer, module_type.model)

            self.set_custom_fields_values(module_type, custom_field_data)


register_initializer("module_types", ModuleTypeInitializer)
