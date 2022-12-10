from random import randrange
from typing import List

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Appr, Brief, Group
from .serializers import (
    ApprSerializer,
    BriefSerializer,
    BriefCUSerializer,
    GroupSerializer,
)


def generate_nomes(brief: Brief, apprenants: List[Appr], force=False):
    nb_appr_nome = brief.brief_nb_apprs
    if len(apprenants) <= nb_appr_nome:
        n_ome = Group(
            grp_nom=f"Groupe 1 du brief '{brief.brief_title}'", grp_brief=brief
        )
        n_ome.save()
        for a in apprenants:
            n_ome.grp_apprs.add(a)

        return [n_ome]

    lasts = []
    while len(apprenants) % nb_appr_nome != 0:
        lasts.append(apprenants.pop(randrange(len(apprenants))))

    n_omes: List[Group] = []
    i_nome = 1
    while len(apprenants) > 0:
        n_ome = Group(
            grp_nom=f"Groupe {i_nome} du brief '{brief.brief_title}'", grp_brief=brief
        )
        n_ome.save()
        for _ in range(nb_appr_nome):
            i = randrange(len(apprenants))
            n_ome.grp_apprs.add(apprenants.pop(i))

        n_omes.append(n_ome)
        i_nome += 1

    already_added_indexes = []
    for a in lasts:
        i = randrange(len(n_omes))
        if i not in already_added_indexes:
            n_omes[i].grp_apprs.add(a)
            n_omes[i].save()

        already_added_indexes.append(i)
        if len(n_omes) == len(already_added_indexes):
            already_added_indexes = []

    return n_omes


class ApprViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage apprenants.
    """

    queryset = Appr.objects.all()
    serializer_class = ApprSerializer


class BriefViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage briefs.
    """

    queryset = Brief.objects.all()
    serializer_class = BriefSerializer

    def list(self, request, *args, **kwargs):
        """API endpoint to list all briefs."""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        serializers = {
            "create": BriefCUSerializer,
            "update": BriefCUSerializer,
            "partial_update": BriefCUSerializer,
            "list": BriefSerializer,
            "retrieve": BriefSerializer,
        }
        return serializers.get(self.action)


class GenGoupsView(APIView):
    """
    API endpoint to create nomes associated with a brief
    You can add the following in request body to overwrite groups:

    `{"force": 1}`
    """

    def post(self, request: Request, pk, format=None):
        brief = get_object_or_404(Brief, pk=pk)

        n_omes = Group.objects.filter(grp_brief=brief)
        # print(f"{n_omes.count()} nomes: {n_omes}")

        # print("#############")
        # print(request.data)
        try:
            force = bool(request.data.get("force", False))
            # print(f"force value in request: {request.data.get('force', None)}")
        except AttributeError:
            force = False

        # print(f"force? {force}")
        # print("#############")

        if force:
            nome: Group
            for nome in brief.groups.all():
                nome.delete()

        if n_omes.count() > 0:
            return Response({"error": "This brief already has groups defined!"})

        apprenants = list(Appr.objects.all())

        groups = GroupSerializer(generate_nomes(brief, apprenants), many=True)

        # print(groups.data)

        return Response(groups.data)
