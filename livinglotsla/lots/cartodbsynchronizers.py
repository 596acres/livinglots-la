from cartodbsync.synchronizers import BaseSynchronizer


class LotSynchronizer(BaseSynchronizer):

    def get_column_names(self):
        return ['id', 'layer', 'organizing', 'size', 'the_geom', 'zone_class',]

    def get_cartodb_mapping(self, instance):
        return {
            'id': instance.pk,
            'friendly_owner': instance.friendly_owner,
            'layer': instance.layer,
            'organizing': instance.actively_organizing,
            'size': round(instance.area_acres, 2),
            'the_geom': instance.centroid,
            'zone_class': self.get_zone_class(instance),
        }

    def get_zone_class(self, instance):
        if instance.zoning_district:
            return instance.zoning_district.zone_class
        return None
