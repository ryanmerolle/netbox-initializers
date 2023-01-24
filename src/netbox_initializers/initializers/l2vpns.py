from ipam.models import L2VPN
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["name"]
OPTIONAL_ASSOCS = {"tenant": (Tenant, "name")}


class L2VPNInitializer(BaseInitializer):
    data_file_name = "l2vpns.yml"

    def load_data(self):
        l2vpns = self.load_yaml()
        if l2vpns is None:
            return
        for params in l2vpns:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            l2vpn, created = L2VPN.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("⚡ Created L2VPN", l2vpn.name)

            self.set_custom_fields_values(l2vpn, custom_field_data)


register_initializer("l2vpns", L2VPNInitializer)
