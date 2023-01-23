from wireless.models import WirelessLAN, WirelessLANGroup
from ipam.models import VLAN
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["ssid"]
OPTIONAL_ASSOCS = {
    "vlan": (VLAN, "name"),
    "tenant": (Tenant, "name"),
    "group": (WirelessLANGroup, "name"),
}


class WirelessLANInitializer(BaseInitializer):
    data_file_name = "wireless_lans.yml"

    def load_data(self):
        wireless_lans = self.load_yaml()
        if wireless_lans is None:
            return
        for params in wireless_lans:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            wireless_lan, created = WirelessLAN.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("📶 Created wireless LAN", wireless_lan.ssid)

            self.set_custom_fields_values(wireless_lan, custom_field_data)


register_initializer("wireless_lans", WirelessLANInitializer)
