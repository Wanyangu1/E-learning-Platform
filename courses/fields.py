from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields  # Fields to filter by when calculating order
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # If the field has no value yet (None)
            try:
                qs = self.model.objects.all()  # Get all instances of the model
                if self.for_fields:
                    # If for_fields is set, filter by these fields
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)

                # Get the last item in the queryset based on the ordering field
                last_item = qs.latest(self.attname)
                value = last_item.order + 1  # Increment the order by 1
            except ObjectDoesNotExist:
                # If no items exist, start ordering from 0
                value = 0

            # Set the calculated order value
            setattr(model_instance, self.attname, value)
            return value
        else:
            # If the value is already set, return the current value
            return super().pre_save(model_instance, add)
