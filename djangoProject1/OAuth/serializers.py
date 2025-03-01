from django.urls import path, include
from OAuth.models import (newuser, Ship, ShipCrew, ShipRoutePoint, EditShipView, EditShipPointView, Event)
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = newuser
        fields = ['url', 'username', 'email', 'is_staff', 'id', 'typevalue', 'roles']

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = '__all__'

class ShipCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipCrew
        # fields = ['ShipID', 'user']
        fields = '__all__'

class ShipCrewSerializer2(serializers.ModelSerializer):
    class Meta:
        model = newuser
        # fields = ['ShipID', 'user']
        fields = '__all__'
    def create(self, validated_data):
        user_info_data = validated_data.pop('ShipID')
        user = newuser.objects.create(**validated_data)
        ShipCrew.objects.create(user=user, **user_info_data)
        return user

class ShipRoutePointSerializer(serializers.ModelSerializer):
    # ship = serializers.IntegerField(source='ship.shipid')
    class Meta:
        model = ShipRoutePoint
        fields = '__all__'
        # fields = ['id', 'longtitude', 'latitude', 'ship', 'next_node']

class EditShipSerializer(serializers.ModelSerializer):
    ship = ShipSerializer()
    user = UserSerializer()

    class Meta:
        model = EditShipView
        fields = '__all__'

class ShipRoutePointFullSerializer(serializers.ModelSerializer):
    ship = ShipSerializer()
    class Meta:
        model = ShipRoutePoint
        fields = '__all__'
        # fields = ['id', 'longtitude', 'latitude', 'ship', 'next_node']

class EditShipPointSerializer(serializers.ModelSerializer):
    point = ShipRoutePointFullSerializer()
    user = UserSerializer()
    class Meta:
        model = EditShipPointView
        fields = '__all__'

class EventCreateSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Event
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Event
        fields = '__all__'