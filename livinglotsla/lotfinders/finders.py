from django.db.models import Q
from django.utils.timezone import now

from ladata.parcels.models import Parcel
from ladata.protectedareas.models import ProtectedArea

from lots.models import Lot

from .models import LotFinderAttempt


class VacantParcelFinder(object):
    """
    Find lots by looking for parcels in LA city with vacant use codes.
    """

    private_vacant_use_codes = ('100V', '010V', '300V', '200V',)
    public_vacant_use_codes = ('880V',)

    def find_parcels(self, count=None):
        vacant_use_codes = (self.private_vacant_use_codes +
                            self.public_vacant_use_codes)
        a_year_ago = now().replace(year=now().year - 1)
        parcels = Parcel.objects.filter(
            (Q(lotfinderattempt=None) |
             Q(lotfinderattempt__checked__lt=a_year_ago)),
            local_roll__use_cde__in=(vacant_use_codes),
            lot_model=None,
        ).order_by('ain')
        if count:
            parcels = parcels[:count]
        return parcels

    def find_lots(self, batch_size=1000):
        for parcel in self.find_parcels(count=batch_size):
            # Ensure parcel is not in a protected area
            if ProtectedArea.objects.filter(geom__overlaps=parcel.geom).exists():
                self.reject_parcel(parcel, 'in a protected area')
            else:
                self.accept_parcel(parcel, 'use code vacant')

    def get_or_create_attempt(self, parcel, checked=now(), reason=None,
                              status=None):
        (attempt, created) = LotFinderAttempt.objects.get_or_create(parcel=parcel,
            defaults={ 'checked': checked, 'reason': reason, 'status': status }
        )
        attempt.save()

    def accept_parcel(self, parcel, reason):
        self.get_or_create_attempt(parcel, reason=reason, status='added')
        Lot.objects.create_lot_for_parcels([parcel], known_use=None,
                                           known_use_certainty=7)

    def reject_parcel(self, parcel, reason):
        self.get_or_create_attempt(parcel, reason=reason, status='not added')
