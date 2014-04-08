from livinglots_owners.models import BaseOwner, BaseOwnerContact


class Owner(BaseOwner):

    class Meta(BaseOwner.Meta):
        ordering = ('name',)


class OwnerContact(BaseOwnerContact):
    pass
