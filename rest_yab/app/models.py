from django.db import models
from django.urls import reverse

class Brief(models.Model):
    brief_title = models.CharField(max_length=255, null=True)
    brief_url = models.CharField(max_length=255, null=True)
    brief_nb_apprs = models.PositiveIntegerField(default=2)

    def __str__(self) -> str:
        return self.brief_title

    def get_absolute_url(self):
        return reverse('app:brief_detail', kwargs={'brief_id': self.pk})

class Appr(models.Model):
    appr_nom = models.CharField(max_length=255)
    appr_prenom = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.appr_prenom} {self.appr_nom}"

class Group(models.Model):
    grp_nom = models.CharField(max_length=255, null=True)
    grp_brief = models.ForeignKey(Brief, on_delete=models.CASCADE, related_name="groups")
    grp_apprs = models.ManyToManyField(Appr)

    def __str__(self) -> str:
        return self.grp_nom
