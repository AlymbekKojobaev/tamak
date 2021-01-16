from .models import Cook
from django.views.generic import CreateView


class CookCreateView(CreateView):
    model = Cook
    fields = ('user', 'position', 'education', 'experience', 'work_history')
    template_name='teams/team.html'

    def get_context_data(self, **kwargs):
        kwargs['cooks']=Cook.objects.all()
        return super().get_context_data(**kwargs)

#################################################
#################################################
#################################################
#################################################


from rest_framework import generics, status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, User, CookSerializer


class CookCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CookSerializer

    def get(self, request):
        cook=Cook.objects.all()
        serializer=self.serializer_class(cook, many=True)

        return Response(
            {
            "success": True,
            "result": serializer.data
        },
            status=status.HTTP_200_OK
        )




    def post(self, request):
        try:
            if request.data.get('user_id'):
                user = User.objects.get(pk=request.data.get('user_id'))
                user_id = user.pk
            else:
                user_id = None
        except User.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такого пользователя нет"
            },
            status=status.HTTP_201_CREATED
        )



        serializer=CookSerializer(data=request.data, context={"user_id":user_id, "request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "result": "Повар был добавлен"
            },
            status=status.HTTP_201_CREATED
        )


class CookUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CookSerializer

    def put(self, request):

        try:
            cook_id=Cook.objects.get(pk=request.data.get('cook_id'))
            print(cook_id)
            serializer=CookSerializer(instance=cook_id, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                "success": True,
                "result": "Повар был обнавлен"
                },
                status=status.HTTP_201_CREATED
                )

        except Cook.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такой повар не был найден"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )



class CookDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CookSerializer

    def delete(self, request):
        try:
            cook_id=Cook.objects.get(pk=request.data.get('cook_id'))
            cook_id.delete()

            return Response(
                {
                "success": True,
                "result": "Повар был удален"
                },
                status=status.HTTP_202_ACCEPTED
                )

        except Cook.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такой повар не был найден"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )




