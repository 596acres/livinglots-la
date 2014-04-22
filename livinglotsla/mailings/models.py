from livinglots_mailings.models import DaysAfterAddedMixin, Mailing

from .mailers import DaysAfterParticipantAddedMailer


class DaysAfterAddedMailing(DaysAfterAddedMixin, Mailing):

    def get_mailer(self):
        return DaysAfterParticipantAddedMailer(self)
