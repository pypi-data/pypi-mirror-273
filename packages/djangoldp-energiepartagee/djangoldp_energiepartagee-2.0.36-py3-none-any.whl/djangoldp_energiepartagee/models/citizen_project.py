from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_energiepartagee.models.actor import Actor
from djangoldp_energiepartagee.models.region import Region
from djangoldp_energiepartagee.permissions import EPRegionalAdminPermission

CITIZEN_PROJECT_STATUS_CHOICES = [
    ("draft", "Brouillon"),
    ("validation", "En cours de validation"),
    ("published", "Publié"),
    ("retired", "Dépublié"),
]


class CitizenProject(Model):
    founder = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Fondateur",
        related_name="founded_projects",
    )
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Name")
    short_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="description des installations de production",
    )
    city = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ville")
    postcode = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Code Postal"
    )
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    # region = models.CharField(max_length=50, blank=True, null=True, verbose_name="Région")
    region = models.ForeignKey(
        Region,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Région",
        related_name="projects",
    )
    department = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Département"
    )
    action_territory = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Territoire d'action du projet",
    )
    picture = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Photo"
    )
    video = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Vidéo"
    )
    website = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Site"
    )
    facebook_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Facebook"
    )
    linkedin_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="LinkedIn"
    )
    twitter_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Twitter"
    )
    instagram_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Instragram"
    )
    contact_picture = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Contact: Photo"
    )
    contact_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Nom"
    )
    contact_first_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Prénom"
    )
    contact_email = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Email"
    )
    contact_phone = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Téléphone"
    )
    contact_visibility = models.BooleanField(
        blank=True, null=True, verbose_name="Visibilité du contact", default=False
    )
    status = models.CharField(
        choices=CITIZEN_PROJECT_STATUS_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Etat d'avancement du projet",
    )
    lat = models.DecimalField(
        max_digits=30,
        decimal_places=25,
        blank=True,
        null=True,
        verbose_name="Latitude",
    )
    lng = models.DecimalField(
        max_digits=30,
        decimal_places=25,
        blank=True,
        null=True,
        verbose_name="Longitude",
    )
    production_tracking_url = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="URL monitoring du site de production",
    )
    fundraising_url = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="URL Page Collecte locale",
    )
    wp_project_url = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Lien du projet sur le site principal",
    )
    visible = models.BooleanField(
        blank=True, null=True, verbose_name="Visible sur la carte", default=False
    )

    @property
    def technology_used(self):
        technology = ""
        for production_site in self.production_sites.all():
            if production_site.visible:
                technology = (
                    "multi"
                    if (
                        technology != "" and technology != production_site.technology_used
                    )
                    else production_site.technology_used
                )
        if not technology:
            technology = "unknown"
        return technology

    @property
    def energy_type(self):
        energy = ""
        for production_site in self.production_sites.all():
            if production_site.visible:
                energy = (
                    "multi"
                    if (energy != "" and energy != production_site.energy_type)
                    else production_site.energy_type
                )
        if not energy:
            energy = "unknown"
        return energy

    @property
    def progress_status(self):
        status = set()
        for production_site in self.production_sites.all():
            if production_site.visible:
                status.add(production_site.progress_status)
        return status

    class Meta(Model.Meta):
        ordering = ["pk"]
        permission_classes = [InheritPermissions | EPRegionalAdminPermission]
        inherit_permissions = ["founder"]
        rdf_type = "energiepartagee:citizen_project"
        nested_fields = [
            "communication_profile",
            "partnered_by",
            "earned_distinctions",
            "testimonies",
            "production_sites",
        ]
        serializer_fields = [
            "name",
            "visible",
            "technology_used",
            "energy_type",
            "progress_status",
            "short_description",
            "city",
            "postcode",
            "address",
            "department",
            "action_territory",
            "picture",
            "video",
            "website",
            "facebook_link",
            "linkedin_link",
            "twitter_link",
            "instagram_link",
            "contact_picture",
            "contact_name",
            "contact_first_name",
            "contact_email",
            "contact_phone",
            "contact_visibility",
            "status",
            "lat",
            "lng",
            "production_tracking_url",
            "fundraising_url",
            "wp_project_url",
            "founder",
            "region",
            "communication_profile",
            "partnered_by",
            "earned_distinctions",
            "testimonies",
            "production_sites",
        ]
        verbose_name = _("Projet Citoyen")
        verbose_name_plural = _("Projets Citoyens")
        depth = 0

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.urlid
