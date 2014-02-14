from ladata.councildistricts.models import CouncilDistrict
from ladata.parcels.models import Parcel
from ladata.protectedareas.models import ProtectedArea

from lots.models import Lot


class VacantParcelFinder(object):
    """
    Find lots by looking for parcels in LA city with vacant use codes.
    """

    private_vacant_use_codes = ('100V', '010V', '300V', '200V',)
    public_vacant_use_codes = ('880V',)

    def find_parcels(self, count=None):
        vacant_use_codes = (self.private_vacant_use_codes +
                            self.public_vacant_use_codes)
        # TODO rather than select any, shuffled, make a record of parcels
        # attempted, and when
        parcels = Parcel.objects.filter(
            local_roll__use_cde__in=(vacant_use_codes),
            lot_model=None,
        ).order_by('?')
        if count:
            parcels = parcels[:count]
        return parcels

    def find_lots(self, batch_size=1000):
        for parcel in self.find_parcels(count=batch_size):
            # Ensure parcel is not in a protected area
            if ProtectedArea.objects.filter(geom__overlaps=parcel.geom).exists():
                continue

            # Ensure parcel is in a council district
            if not CouncilDistrict.objects.filter(geom__overlaps=parcel.geom).exists():
                continue

            Lot.objects.create_lot_for_parcels([parcel])
