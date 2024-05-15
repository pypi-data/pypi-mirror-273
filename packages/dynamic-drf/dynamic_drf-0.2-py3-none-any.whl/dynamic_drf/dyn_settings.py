from django.urls import path
from drf_spectacular.views import (SpectacularAPIView,
                                    SpectacularRedocView,
                                    SpectacularSwaggerView)
from django.conf import settings
# from dynamic_drf.auth import LoginView



swagger_ui_url= settings.SWAGGER_URL
redoc_url = settings.REDOC_URL 



class InstalledAppsDescriptor:

    def __get__(self, obj, objtype=None):
        value = obj._installed_apps
        return value

    def __set__(self, obj, value):
        obj._installed_apps = value

class ProjectUrlDescriptor:

    def __get__(self,obj,objtype=None):
        value = obj._urlpatterns
        return value 

    def __set__(self,obj,value):
        value.extend([
            path('schema/', SpectacularAPIView.as_view(), name='schema'),
            path(swagger_ui_url, SpectacularSwaggerView.as_view(url_name='schema'), name=swagger_ui_url),
            path(redoc_url,SpectacularRedocView.as_view(url_name='schema'), name=redoc_url),           
            ]
        )
        obj._urlpatterns = value
 
        
class DynamicDRFSpectacular:

    installed_apps = InstalledAppsDescriptor()
    urlpatterns = ProjectUrlDescriptor()

    def __init__(self,installed_apps):
        self.installed_apps:list = installed_apps

    def override_apps(self) -> list:
        self.installed_apps.append("drf_spectacular")
        return self.installed_apps
    
    def append_urls(self) -> list:
        self.urlpatterns = []
        return self.urlpatterns

        

spectacular= DynamicDRFSpectacular(settings.INSTALLED_APPS)
installed_apps = spectacular.override_apps()
urlpatterns = spectacular.append_urls()

    