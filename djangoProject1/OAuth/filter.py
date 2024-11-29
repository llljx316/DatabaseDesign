from django_filters import rest_framework as filters
from OAuth.models import (newuser, Ship, ShipCrew, ShipRoutePoint, EditShipView, EditShipPointView)

class EditShipFilter(filters.FilterSet):
    ship__name = filters.CharFilter(field_name='ship__name', lookup_expr='icontains')  # 对标题进行模糊匹配
    user__username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')  # 对作者名字进行模糊匹配

    class Meta:
        model = EditShipView
        fields = ['ship', 'user']

