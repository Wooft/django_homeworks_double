from rest_framework.authtoken.admin import User
from rest_framework.permissions import BasePermission



class IsOwnerOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'DELETE':
            #Проверка на то, что пользователь явялется администратором
            if User.objects.get(user=request.user).is_staff:
                return True
            else:
                return request.user == obj.creator
        if request.method == 'PATCH':
            if User.objects.get(user=request.user).is_staff:
                return True
            else:
                return request.user == obj.creator
        return request.user == obj.creator
