from wireless.models import WirelessLANGroup

from . import BaseInitializer, register_initializer

OPTIONAL_ASSOCS = {"parent": (WirelessLANGroup, "name")}


class WirelessLANGroupInitializer(BaseInitializer):
    data_file_name = "wireless_lan_groups.yml"

    def load_data(self):
        wireless_lan_groups = self.load_yaml()
        if wireless_lan_groups is None:
            return
        for params in wireless_lan_groups:

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params)
            wireless_lan_group, created = WirelessLANGroup.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("📶 Created wireless LAN group", wireless_lan_group.name)


register_initializer("wireless_lan_groups", WirelessLANGroupInitializer)
