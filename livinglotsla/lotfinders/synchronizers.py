from external_data_sync import register, synchronizers

from .finders import VacantParcelFinder


class VacantParcelSynchronizer(synchronizers.Synchronizer):

    def sync(self, data_source):
        finder = VacantParcelFinder()
        finder.find_lots(batch_size=data_source.batch_size)


register(VacantParcelSynchronizer)
