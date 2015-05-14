# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class MailMail(models.Model):
    """ Overwrites mail.mail model to capture all sended mail
    """

    _name = 'mail.mail'
    _inherit = ['mail.mail']

    _capture_msg = _('Email to {} has been captured and sent to {}')

    # ------------------------- OVERWRITTEN METHODS ---------------------------

    @api.model
    def send_get_mail_to(self, mail, partner=None):
        """ Returns an overwritten `mail_to` and outputs the real value
            to the log
        """

        _super = super(MailMail, self)
        real_mail_to = _super.send_get_mail_to(mail, partner)

        capture, fake_mail_to = self._get_email_config_settings()

        if capture:
            _logger.info(
                self._capture_msg.format(real_mail_to, fake_mail_to))

        return fake_mail_to or real_mail_to

    # -------------------------- AUXILIARY METHODS ----------------------------

    @api.model
    def _get_email_config_settings(self):
        """ Overwrites parent method to return the alternative email to collect
            the outgoing mails
        """

        config = self.env['development_tools.config.settings']

        email_to = False

        email_capture = config.get_email_capture()
        if email_capture:
            email_to = config.get_email_to()
            if not email_to:
                admin = self.env.ref('base.user_root')
                if admin.email:
                    email_to = admin.email

        return (
            email_capture and email_to,
            [unicode(email_to)] if email_to else False
        )
