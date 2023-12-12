from django.utils.translation import gettext as _
from django.contrib.gis.db import models
from parler.models import TranslatableModel, TranslatedFields


class Region(TranslatableModel, models.Model,):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200)

    )

    class Meta:
        verbose_name = _("регион")
        verbose_name_plural = _("регионы")

    def __str__(self):
        return self.name


class District(TranslatableModel, models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200)

    )

    class Meta:
        verbose_name = _("район")
        verbose_name_plural = _("районы")
