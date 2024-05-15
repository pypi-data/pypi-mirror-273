from rest_framework.views import APIView
from rest_framework.response import Response
from dynamic_drf.serializers import LoginSerializer
from drf_spectacular.utils import extend_schema



class LoginView(APIView):

    @extend_schema(
        request=LoginSerializer,
        responses={201: LoginSerializer},
    )
    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success":"True","data":serializer.validated_data})



