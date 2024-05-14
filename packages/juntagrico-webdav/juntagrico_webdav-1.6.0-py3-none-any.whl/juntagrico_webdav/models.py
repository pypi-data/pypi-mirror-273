from django.db import models
from django.utils.translation import gettext as _


class WebdavServer(models.Model):
    '''
    Webdav Server configuration
    '''

    class SortOrder:
        BY_NAME_ASC = 1
        BY_NAME_DESC = 2
        BY_DATE_ASC = 3
        BY_DATE_DESC = 4
        choices = [
            (BY_NAME_ASC, _('Dateiname aufsteigend')),
            (BY_NAME_DESC, _('Dateiname absteigend')),
            (BY_DATE_ASC, _('Änderungsdatum aufsteigend')),
            (BY_DATE_DESC, _('Änderungsdatum absteigend'))
        ]

    USER_SERVER = 1
    ADMIN_SERVER = 2
    type_choices = [
        (USER_SERVER, _('User')),
        (ADMIN_SERVER, _('Admin'))
    ]

    name = models.CharField(_('Name'), max_length=100, default='')
    url = models.CharField(_('Server URL'), max_length=100, default='')
    path = models.CharField(_('Ordner Pfad'), max_length=100, default='')
    username = models.CharField(_('Benutzername'), max_length=100, default='')
    password = models.CharField(_('Passwort'), max_length=100, default='')
    menu_title = models.CharField(_('Menu Titel'), max_length=100, default='')
    sortby = models.PositiveIntegerField(_('Sortieren nach'),
                                         choices=SortOrder.choices)
    active = models.BooleanField(_('aktiv'), default=True)
    type = models.PositiveIntegerField(_('Typ'), choices=type_choices)

    @property
    def sorted_by_name(self):
        return self.sortby in [self.SortOrder.BY_NAME_DESC, self.SortOrder.BY_NAME_ASC]

    @property
    def sorted_desc(self):
        return self.sortby in [self.SortOrder.BY_NAME_DESC, self.SortOrder.BY_DATE_DESC]
