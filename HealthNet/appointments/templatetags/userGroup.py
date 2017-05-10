from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='in_group')
def has_group(user, group_name):
    """
    A helper filter that determines if a user is in a given group
    :param user: The user that will have their group checked
    :param group_name: The name of the group to check for
    :return: True if the user is in the group
    """
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()
