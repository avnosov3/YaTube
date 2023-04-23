from rest_framework import mixins, viewsets


class CreateListtViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass
