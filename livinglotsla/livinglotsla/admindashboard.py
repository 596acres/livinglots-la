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

        self.children.append(modules.Group(
            title=_('Lot Content'),
            display='accordion',
            children=[
                modules.ModelList(
                    title='Lot info',
                    models=(
                        'livinglots_lots.*',
                    )
                ),
                modules.ModelList(
                    title='User-generated',
                    models=(
                        'livinglots_usercontent.*',
                    )
                ),
                modules.ModelList(
                    title='Organizing',
                    models=(
                        'organize.*',
                        'livinglots_organize.*',
                    )
                ),
                modules.ModelList(
                    title='Owners',
                    models=(
                        'owners.*',
                        'friendlyowners.*',
                    )
                ),
                modules.ModelList(
                    title='Corrections and projects',
                    models=(
                        'groundtruth.*',
                        'steward.*',
                    )
                ),
            ]
        ))

        self.children.append(modules.Group(
            title=_('Advanced'),
            display='accordion',
            children=[
                modules.ModelList(
                    title='Activities',
                    models=(
                        'actstream.*',
                    )
                ),
                modules.ModelList(
                    title='Data',
                    models=(
                        'datasync.*',
                    )
                ),
                modules.ModelList(
                    title='Mailings',
                    models=(
                        'livinglots_mailings.*',
                        'mailings.*',
                    )
                ),
                modules.ModelList(
                    title='RSS',
                    models=(
                        'rsssync.*',
                    )
                ),
            ]
        ))

        self.children.append(modules.AppList(
            title=_('Everything else'),
            exclude=(
                'actstream.*',
                'datasync.*',
                'django.contrib.*',
                'django_monitor.*',
                'elephantblog.*',
                'feincms.module.page.*',
                'flatblocks.*',
                'friendlyowners.*',
                'groundtruth.*',
                'livinglots_lots.*',
                'livinglots_mailings.*',
                'livinglots_organize.*',
                'livinglots_usercontent.*',
                'mailings.*',
                'lots.*',
                'organize.*',
                'owners.*',
                'pathways.*',
                'rsssync.*',
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
