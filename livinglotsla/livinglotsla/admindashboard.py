from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard


class LivingLotsDashboard(Dashboard):
    columns = 3

    def __init__(self, **kwargs):

        self.children = self.children or []

        self.children.append(modules.ModelList(
            title=_('Site Content'),
            models=(
                'feincms.module.page.*',
                'flatblocks.*',
                'pathways.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Moderation'),
            models=(
                'django_monitor.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Lots'),
            models=(
                'lots.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Lot Content'),
            models=(
                'livinglots_usercontent.*',
                'organize.*',
                'livinglots_organize.*',
                'owners.*',
                'groundtruth.*',
                'steward.*',
                'friendlyowners.*',
                'livinglots_lots.*',
            ),
        ))

        self.children.append(modules.AppList(
            title=_('Other Applications'),
            exclude=(
                'django.contrib.*',
                'django_monitor.*',
                'elephantblog.*',
                'feincms.module.page.*',
                'flatblocks.*',
                'friendlyowners.*',
                'groundtruth.*',
                'livinglots_lots.*',
                'livinglots_organize.*',
                'livinglots_usercontent.*',
                'lots.*',
                'organize.*',
                'owners.*',
                'pathways.*',
                'steward.*',
            ),
        ))

        self.children.append(modules.AppList(
            title=_('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=5
        ))
