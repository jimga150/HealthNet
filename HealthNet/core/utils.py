from django.forms import ModelChoiceField


class UserChoiceField(ModelChoiceField):
    """
    Custom ModelChoiceField written to display User's last name in the field.
    """
    def label_from_instance(self, obj):
        # return obj.get_profile().full_name()
        return obj.last_name
