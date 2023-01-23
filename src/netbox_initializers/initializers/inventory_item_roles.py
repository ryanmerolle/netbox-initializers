from dcim.models import InventoryItemRole
from utilities.choices import ColorChoices

from . import BaseInitializer, register_initializer


class InventoryItemRoleInitializer(BaseInitializer):
    data_file_name = "inventory_item_roles.yml"

    def load_data(self):
        inventory_item_roles = self.load_yaml()
        if inventory_item_roles is None:
            return
        for params in inventory_item_roles:

            if "color" in params:
                color = params.pop("color")

                for color_tpl in ColorChoices:
                    if color in color_tpl:
                        params["color"] = color_tpl[0]

            matching_params, defaults = self.split_params(params)
            inventory_item_role, created = InventoryItemRole.objects.get_or_create(
                **matching_params, defaults=defaults
            )

            if created:
                print("🎨 Created inventory item role", inventory_item_role.name)


register_initializer("inventory_item_roles", InventoryItemRoleInitializer)
