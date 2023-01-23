from circuits.models import Provider, ProviderNetwork
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["provider", "name"]
REQUIRED_ASSOCS = {"provider": (Provider, "name")}


class ProviderNetworkInitializer(BaseInitializer):
    data_file_name = "provider_networks.yml"

    def load_data(self):
        provider_networks = self.load_yaml()
        if provider_networks is None:
            return
        for params in provider_networks:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            provider_network, created = ProviderNetwork.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("⚡ Created provider network", provider_network.name)

            self.set_custom_fields_values(provider_network, custom_field_data)


register_initializer("provider_networks", ProviderNetworkInitializer)
