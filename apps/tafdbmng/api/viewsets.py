"""taf_car ViewSet Api

"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import FreightSerializer


class FreightsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = FreightSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        pk_freights = self.request.query_params.get('pk_freights')
        return pk_freights

    def list(self, request, *args, **kwargs):
        """
        Returns a list of registers for the queryset
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(FreightsViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Returns a record with filtered by pk_toursspots
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(FreightsViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Insert a register
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(FreightsViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a register
        """
        if not request.auth and not request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(FreightsViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a register
        """
        if not request.auth and request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(FreightsViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a register partialy
        """
        if not request.auth and request.auth.user.is_superuser:
            return Response({'message': 'Restriced Action!'}, 401)
        return super(FreightsViewSet, self).partial_update(request, *args, **kwargs)
