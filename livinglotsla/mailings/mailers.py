from django.contrib.sites.models import Site

from livinglots_mailings.mailers import DaysAfterAddedMailer


class DaysAfterParticipantAddedMailer(DaysAfterAddedMailer):
    """
    DaysAfterAddedMailer customized for participants.
    """

    def get_context(self, recipients):
        context = super(DaysAfterParticipantAddedMailer, self).get_context(recipients)

        # Add BASE_URL for full-path links back to the site
        context['BASE_URL'] = Site.objects.get_current().domain

        # Consolidate participant objects (handy when merging mailings)
        context['lots'] = [r.content_object for r in recipients]

        # Url for changing what one's organizing/watching
        context['edit_url'] = recipients[0].get_edit_url()
        return context
