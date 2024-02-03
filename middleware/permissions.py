from rest_framework import permissions
from rest_framework import exceptions
from users.models.sellers import *
from users.models.buyers import *

class SellerPermission(permissions.BasePermission):

    edit_methods = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')

    def has_permission(self, request, view):
        if Seller.objects.filter(user=request.user).exists():
            return True
        else:
            raise exceptions.PermissionDenied('Not a Seller')
        
class BuyerPermission(permissions.BasePermission):

    edit_methods = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')

    def has_permission(self, request, view):
        if Buyer.objects.filter(user=request.user).exists():
            return True
        else:
            raise exceptions.PermissionDenied('Not a Buyer')


