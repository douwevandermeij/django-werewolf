from cms import models as cms_models
from django.db import models

from werewolf.models import WerewolfBaseModel


class Page(WerewolfBaseModel):
    page = models.ForeignKey(cms_models.Page)

    def __unicode__(self):
        return self.page.__str__()
