from external_data_sync import register, synchronizers

from ladata.zoning.models import ZoningDistrict

from .models import Lot


class LotZoningSynchronizer(synchronizers.Synchronizer):

    def find_lots(self, batch_size=1000):
        return Lot.objects.filter(zoning_district=None)[:batch_size]

    def sync(self, data_source):
        lots = self.find_lots(batch_size=data_source.batch_size)
        for lot in lots:
            try:
                lot.zoning_district = ZoningDistrict.objects.get(
                    geometry__contains=lot.centroid,
                )
                lot.save()
            except ZoningDistrict.DoesNotExist:
                print 'No ZoningDistrict found for lot %d' % lot.pk
            except ZoningDistrict.MultipleObjectsReturned:
                print 'Multiple ZoningDistricts found for lot %d' % lot.pk


register(LotZoningSynchronizer)
