from cartodbsync.synchronizers import BaseSynchronizer


class LotSynchronizer(BaseSynchronizer):

    def get_column_names(self):
        return ['id', 'layer', 'size', 'the_geom']

    def get_cartodb_mapping(self, instance):
        return {
            'id': instance.pk,
            'layer': instance.layer,
            'size': instance.area_acres,
            'the_geom': instance.centroid,
        }
