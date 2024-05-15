from django.apps import AppConfig
import importlib
from django.conf import settings
from django.urls import path



class DynamicDRF(AppConfig):
    name = 'dynamic_drf'
    
    def ready(self):
        from dynamic_drf.dyn_settings import urlpatterns
        settings_module = importlib.import_module(settings.ROOT_URLCONF)
        existing_url = self.get_url_patterns()
        urlpatterns = existing_url + urlpatterns+ self.append_url()
        setattr(settings_module,"urlpatterns",urlpatterns)
        return urlpatterns

    def get_url_patterns(self):   
        settings_module = importlib.import_module(settings.ROOT_URLCONF)
        urlpatterns = getattr(settings_module, 'urlpatterns')
        return urlpatterns
        

    def append_url(self):
        from dynamic_drf.views import LoginView
        login_url = settings.LOGIN_URL
        urlpatterns = [
            path(login_url,LoginView.as_view(),name="login")
        ]
        return urlpatterns
        


