from dcim.models import Rack, RackReservation
from django.contrib.auth.models import User
from tenancy.models import Tenant

from . import BaseInitializer, register_initializer

MATCH_PARAMS = ["rack", "units", "user", "description"]
REQUIRED_ASSOCS = {
    "rack": (Rack, "name"),
    "user": (User, "username"),
}

OPTIONAL_ASSOCS = {
    "tenant": (Tenant, "name"),
}

class RackReservationInitializer(BaseInitializer):
    data_file_name = "rack_reservations.yml"

    def load_data(self):
        rack_reservations = self.load_yaml()
        if rack_reservations is None:
            return
        for params in rack_reservations:
            custom_field_data = self.pop_custom_fields(params)

            for assoc, details in REQUIRED_ASSOCS.items():
                model, field = details
                query = {field: params.pop(assoc)}

                params[assoc] = model.objects.get(**query)

            for assoc, details in OPTIONAL_ASSOCS.items():
                if assoc in params:
                    model, field = details
                    query = {field: params.pop(assoc)}

                    params[assoc] = model.objects.get(**query)

            matching_params, defaults = self.split_params(params, MATCH_PARAMS)
            rack_reservation, created = RackReservation.objects.get_or_create(**matching_params, defaults=defaults)

            if created:
                print("🔳  Created rack reservation", rack_reservation.description)

            self.set_custom_fields_values(rack_reservation, custom_field_data)


register_initializer("rack_reservations", RackReservationInitializer)
