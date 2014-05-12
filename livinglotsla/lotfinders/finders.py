from django.db.models import Q
from django.utils.timezone import now

from ladata.buildings.models import Building
from ladata.parcels.models import Parcel
from ladata.protectedareas.models import ProtectedArea
from ladata.localroll.utils import vacant_use_codes

from lots.models import Lot

from .models import LotFinderAttempt


class VacantParcelFinder(object):
    """
    Find lots by looking for parcels in LA city with vacant use codes.
    """

    def find_parcels(self, count=None):
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
            if Building.objects.filter(geom__overlaps=parcel.geom).exists():
                # Ensure parcel has no buildings on it
                self.reject_parcel(parcel, 'contains buildings')
            elif ProtectedArea.objects.filter(geom__overlaps=parcel.geom).exists():
                # Ensure parcel is not in a protected area
                self.reject_parcel(parcel, 'in a protected area')
            elif (parcel.local_roll and parcel.local_roll.improvement_value and
                  parcel.local_roll.improvement_value > 0):
                # Ensure parcel doesn't have an improvement value
                self.reject_parcel(parcel, 'non-zero improvement value')
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


class TransmissionLineFinder(object):
    """
    Find lots by looking for parcels with transmission line easements.
    """

    def find_parcels(self, count=None):
        parcels = Parcel.objects.exclude(transmissionline=None)
        parcels = parcels.filter(lot_model=None).order_by('ain')
        if count:
            parcels = parcels[:count]
        return parcels

    def find_lots(self, batch_size=5000):
        for parcel in self.find_parcels(count=batch_size):
            if Building.objects.filter(geom__overlaps=parcel.geom).exists():
                # Ensure parcel has no buildings on it
                continue
            if ProtectedArea.objects.filter(geom__overlaps=parcel.geom).exists():
                # Ensure parcel is not in a protected area
                continue
            else:
                self.accept_parcel(parcel)

    def accept_parcel(self, parcel):
        Lot.objects.create_lot_for_parcels([parcel], known_use=None,
                                           known_use_certainty=7)


class SideLotFinder(object):
    """
    Find lots by looking for parcels that are side lots.
    """

    def find_parcels(self, count=None):
        parcels = Parcel.objects.exclude(sidelot=None)
        parcels = parcels.filter(lot_model=None).order_by('ain')
        if count:
            parcels = parcels[:count]
        return parcels

    def find_lots(self, batch_size=5000):
        for parcel in self.find_parcels(count=batch_size):
            if Building.objects.filter(geom__overlaps=parcel.geom).exists():
                # Ensure parcel has no buildings on it
                continue
            if ProtectedArea.objects.filter(geom__overlaps=parcel.geom).exists():
                # Ensure parcel is not in a protected area
                continue
            else:
                self.accept_parcel(parcel)

    def accept_parcel(self, parcel):
        Lot.objects.create_lot_for_parcels([parcel], known_use=None,
                                           known_use_certainty=7)
