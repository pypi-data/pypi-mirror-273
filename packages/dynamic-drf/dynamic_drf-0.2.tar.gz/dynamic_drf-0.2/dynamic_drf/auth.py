from rest_framework.views import APIView
from rest_framework.response import Response
from dynamic_drf.views import LoginSerializer
# from drf_spectacular


class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success":"True","data":serializer.validated_data})



from dynamic_drf import urlpatterns
from django.urls import path

# urlpatterns+=[
#     path("login/",LoginView.as_view(),name="login")
# ]