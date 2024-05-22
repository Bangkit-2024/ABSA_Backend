from rest_framework import permissions

class IsNotEditable(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Method PATCH dan PUT dilarang

        if request.method in ["GET","HEAD","POST"]:
            return True
        
        return False