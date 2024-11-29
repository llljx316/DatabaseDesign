import math

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from OAuth.models import (newuser, Ship, ShipCrew, ShipRoutePoint, EditShipView, EditShipPointView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
# Create your views here.
from OAuth.serializers import *
from django.db.models import Q
from rest_framework import filters
# import folium
from django.db.models import OuterRef, Subquery, Q, Exists
import django_filters
from OAuth.filter import EditShipFilter



def get_start_nodes():
    subquery = ShipRoutePoint.objects.filter(next_node=OuterRef('id'))
    start_nodes = ShipRoutePoint.objects.annotate(
        ids=~Exists(subquery)
    ).filter(ids=True)
    return start_nodes

# class StartRouteView(APIView):
#     def get(self, request):
#         start_nodes = get_start_nodes()
#         serializer = ShipRoutePointSerializer(start_nodes, many=True)
#         return Response(serializer.data)

class StartRouteView(viewsets.ModelViewSet):
    queryset = get_start_nodes()
    serializer_class = ShipRoutePointSerializer

    # def get(self, request):
    #     start_nodes = get_start_nodes()
    #     serializer = ShipRoutePointSerializer(start_nodes, many=True)
    #     return Response(serializer.data)
    # def list(self, request, *args, **kwargs):


class RouteFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='ship', lookup_expr='exact')

    class Meta:
        model = ShipRoutePoint
        fields = ['ship']

class EndRouteView(viewsets.ModelViewSet):
    queryset = ShipRoutePoint.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RouteFilter
    serializer_class = ShipRoutePointSerializer

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.query_params.get('search', None)
        if query:
            queryset = queryset.filter(
                Q(ship__name__icontains=query)
                # 其他需要搜索的字段
            )
        return queryset



    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(next_node_id__isnull=True))
        #找到ship为NULL的所有键


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ShipRoutePathsViewSet(viewsets.ModelViewSet):
    queryset = ShipRoutePoint.objects.all()
    serializer_class = ShipRoutePointSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        subquery = ShipRoutePoint.objects.filter(next_node=OuterRef('id'))
        start_nodes = ShipRoutePoint.objects.annotate(ids=~Exists(subquery)).filter(ids=True)

        paths = []
        for start_node in start_nodes:
            path = []
            node = start_node
            while node:
                path.append(self.get_serializer(node).data)
                node = node.next_node
            if len(path) <=1 : #如果只有一个节点会导致画不出来
                continue
            paths.append(path)

        # 构建二维数组
        paths_2d = [[point for point in path] for path in paths]

        return Response(paths_2d)

# def map(request):
#     ship_points = ShipRoutePoint.objects.all()
#     m = folium.Map(location=[41,-72], zoom_start=11, tiles='Stamen Terrain')
#
#     #add marker
#     for point in ship_points:
#         coorodinates = { point.latitude, point.longitude}
#         folium.Marker(coorodinates).add_to(m)
#     context = {'map': m._repr_html_()}
#     return render(request, 'map.html', context)


def calculate_direction_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    # 使用 atan2 计算角度（弧度）
    angle_rad = math.atan2(dy, dx)

    # 将弧度转换为度
    angle_deg = math.degrees(angle_rad)

    # 将角度转换为0到360度范围内
    if angle_deg < 0:
        angle_deg += 360

    return angle_deg

class ShipPointViewSet(viewsets.ModelViewSet):
    queryset = ShipRoutePoint.objects.all().order_by('ship')
    serializer_class = ShipRoutePointSerializer
    http_method_names = ['get', 'post', 'delete']
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def detect_anomaly(self,now_node, pre_node, user):
        distance = math.sqrt((now_node.longtitude - pre_node.longtitude) * (now_node.longtitude - pre_node.longtitude)
                             + (now_node.latitude - pre_node.latitude) * (now_node.latitude - pre_node.latitude))
        is_anomaly = False
        content = f'Ship {now_node.ship.name} alert!!! '
        if distance > 20:
            is_anomaly = True
            content += f'Delta Distance: {distance:.1f}! '
            # Event.objects.create(content=f'Ship {now_node.ship.name} alert!!! Distance: {distance}',
            #                      user=newuser.objects.get(id=user['user_id']))
        #航向上
        if pre_node.direction is not None:
            dd = math.fabs(now_node.direction - pre_node.direction)
            if dd > 180:
                dd = 360 - dd
            if dd > 60:
                is_anomaly = True
                content += f'Direction changed is {dd:.1f} degree! '
                # Event.objects.create(content=f'Ship {now_node.ship.name} alert!!! Direction changed is {dd} degree',
                #                  user=newuser.objects.get(id=user['user_id']))

        if now_node.speed > 20:
            is_anomaly = True
            content += f'Speed is {now_node.speed:.1f}, too fast! '
            # Event.objects.create(content=f'Ship {now_node.ship.name} alert!!! Speed is {now_node.speed}, too fast!!!',
            #                      user=newuser.objects.get(id=user['user_id']))

        if is_anomaly:
            Event.objects.create(content=content, user=newuser.objects.get(id=user['user_id']))

    def calculate_direction(self, now_node, pre_node):
        angle = calculate_direction_angle(now_node.longtitude,now_node.latitude,pre_node.longtitude,pre_node.latitude)
        angle = (360 - angle) - 90
        if angle < 0:
            angle += 360
        return angle


    def create(self, request, *args, **kwargs):
        try:
            old_node_id = request.data['next_node']
        except:
            old_node_id = ''
        if old_node_id != '':
            pre_node = ShipRoutePoint.objects.get(id=old_node_id)
            #检查是否已经有节点
            if pre_node.next_node is not None:
                return Response({'detail': 'try add to a middle point!'},status=status.HTTP_403_FORBIDDEN)
        reqdata = request.data.copy()
        reqdata.pop('next_node',None)
        serializer = self.get_serializer(data=reqdata)
        serializer.is_valid(raise_exception=True)
        now_node = self.perform_create(serializer)
        if old_node_id != '':
            pre_node.next_node = now_node
            # 计算航向
            angle = self.calculate_direction(now_node, pre_node)
            now_node.direction = angle

            pre_node.save()
            now_node.save()
            # 检测异常
            # 根据距离
            self.detect_anomaly(now_node,pre_node,request.auth)
            # distance = math.sqrt((now_node.longtitude - pre_node.longtitude)* (now_node.longtitude - pre_node.longtitude)
            #                      + (now_node.latitude - pre_node.latitude)* (now_node.latitude - pre_node.latitude))
            # if distance > 10:
            #     Event.objects.create(content=f'Ship {now_node.ship.name} alert!!!', user=newuser.objects.get(id=request.auth['user_id']))
        else:
            now_node.direction = None
            now_node.save()
        #add edit node subject
        EditShipPointView.objects.create(point = now_node, user = newuser.objects.get(id=request.auth['user_id']))



        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        #检查是否中间
        instance = self.get_object()
        #检查
        if instance.next_node is not None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

#只返回成功，留出接口
class SuccessView(viewsets.ModelViewSet):
    # queryset = newuser.objects.all().order_by('id')
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = newuser.objects.all().order_by('id')
    http_method_names = ['get']
    # serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        print('list_ok')
        user_info = newuser.objects.filter(id=request.user.id).values()[0]
        roles = request.user.roles
        if roles == 0:
            user_info['roles'] = ['admin']
        else:
            user_info['roles'] = ['user']

        return Response(user_info)

# ViewSets define the view behavior.
class  UserViewSet(viewsets.ModelViewSet):
    queryset = newuser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get','put']
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    """
        List a queryset.
        """

    def list(self, request, *args, **kwargs):
        if request.user.roles == 1:
            self.queryset = self.queryset.filter(~Q(username='admin'))
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.user.roles == 1:
            return Response(status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        old_user = newuser.objects.get(id=request.user.id)
        user_info = self.perform_update(serializer)
        # user_info = self.perform_create(serializer)
        user_info.set_password(request.data['password'])
        headers = self.get_success_headers(serializer.data)
        user_info.save()

        try:
            # 如果船员
            if int(request.data['typevalue']) == 2:
                # 创建ship
                ship = Ship.objects.get(shipid=request.data['ShipID'])  # 获取对应的Ship对象
                ShipCrew.objects.get(user=user_info).ShipID = ship
        except:
            user_info.delete()
            old_user.save()
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

    def perform_update(self, serializer):
        return serializer.save()

class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = newuser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # if  newuser.objects.filter(email=request.data['email']).exists():
        #     return Response({'detail': '邮箱重复'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = self.perform_create(serializer)
        user_info.set_password(request.data['password'])
        headers = self.get_success_headers(serializer.data)
        user_info.save()

        try:
            #如果船员
            if int(request.data['typevalue']) == 2:
                # 创建ship
                    ship = Ship.objects.get(shipid=request.data['ShipID'])  # 获取对应的Ship对象
                    ShipCrew.objects.create(user=user_info, ShipID=ship)
        except:
            user_info.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class UserDeleteViewSet(viewsets.ModelViewSet):
    queryset = newuser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['delete']
    # permission_classes = [] #后面再改

    def destroy(self, request, *args, **kwargs):
        if request.user.roles == 1:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class ShipCrewCreateViewSet(viewsets.ModelViewSet):
    queryset = ShipCrew.objects.all()
    serializer_class = ShipCrewSerializer
    http_method_names = ['post']
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class ShipCrewCreateViewSet2(viewsets.ModelViewSet):
    queryset = newuser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #创建ship
        try:
            ship = Ship.objects.get(shipid=request.data['ShipID'])  # 获取对应的Ship对象
            ShipCrew.objects.create(user=user, ShipID=ship)
        except:
            user.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

class ShipIDandNameViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
    http_method_names = ['get']
    permission_classes = []

class ShipIDandNameAuthorViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    http_method_names = ['post','delete','put', 'patch','get']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nowship = self.perform_create(serializer)

        EditShipView.objects.create(ship=nowship, user = newuser.objects.get(id = request.auth['user_id']), operation = 'create')


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        nowship = self.perform_update(serializer)

        EditShipView.objects.create(ship=nowship, user = newuser.objects.get(id = request.auth['user_id']), operation = 'edit')

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save()

class EditShipViewSet(viewsets.ModelViewSet):
    queryset = EditShipView.objects.all()
    serializer_class = EditShipSerializer
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]
    filterset_class = EditShipFilter

class EditPointViewSet(viewsets.ModelViewSet):
    queryset = EditShipPointView.objects.all()
    serializer_class = EditShipPointSerializer
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

class EventCreateViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    http_method_names = ['post']
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.auth['user_id']# newuser.objects.get(id = request.auth['user_id'])
        # request.data['content'] = "test"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']