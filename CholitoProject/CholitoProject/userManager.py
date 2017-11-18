from naturalUser.models import NaturalUser
from municipality.models import MunicipalityUser
from ong.models import ONGUser


def get_user_or_none(model, user):
    try:
        the_user = model.objects.get(user=user)
    except Exception:
        the_user = None
    return the_user


def get_user_index(user):
    original_user = get_user_or_none(NaturalUser, user)
    if original_user is not None:
        return original_user
    original_user = get_user_or_none(MunicipalityUser, user)
    if original_user is not None:
        return original_user
    original_user = get_user_or_none(ONGUser, user)
    if original_user is not None:
        return original_user
    else:
        return None
