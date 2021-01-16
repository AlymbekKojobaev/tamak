from .models import Order
from django.views.generic import ListView, CreateView

# @login_required
class OrderCreateView(CreateView):
    '''Данная функция обрабатывает данные с формы бронирование
        Если бронь успешна отправляем пользователя на главную страницу,
        иначе просим перезаполнить'''
    model = Order
    fields = ('phone', 'date', 'time', 'persons', 'message')
    template_name='reservation/reservation.html'

    def form_valid(self, form):
        form.instance.reservator=self.request.user
        return super().form_valid(form)


class OrderListView(ListView):
    '''Функция показывает список заказов пользователя'''
    model = Order
    template_name='reservation/user_orders.html'

    def get_context_data(self, **kwargs):
        kwargs["order"] = Order.objects.filter(reservator=self.request.user)
        return super().get_context_data(**kwargs)



###########################################
###########################################
###########################################
###########################################
from rest_framework import generics, status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, User, OrderSerializer

class OrderCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = OrderSerializer

    def get(self, request):
        order=Order.objects.all()
        serializer=self.serializer_class(order, many=True)

        return Response(
            {
            "success": True,
            "result": serializer.data
        },
            status=status.HTTP_200_OK
        )




    def post(self, request):
        try:
            if request.data.get('reservator_id'):
                user = User.objects.get(pk=request.data.get('reservator_id'))
                reservator_id = user.pk
            else:
                reservator_id = None

        except User.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такого пользователя нет"
            },
            status=status.HTTP_201_CREATED
        )



        serializer=OrderSerializer(data=request.data, context={"reservator_id":reservator_id, "request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "result": "Бронь был оставлен успешно"
            },
            status=status.HTTP_201_CREATED
        )




class OrderUpdateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = OrderSerializer

    def put(self, request):
        try:
            order_id=Order.objects.get(pk=request.data.get('order_id'))
            serializer=OrderSerializer(instance=order_id, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                "success": True,
                "result": "Бронь был обнавлен"
                },
                status=status.HTTP_201_CREATED
                )

        except Order.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такая бронь не была найдена"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )



class OrderDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny,]
    serializer_class = OrderSerializer

    def delete(self, request):
        try:
            order_id=Order.objects.get(pk=request.data.get('order_id'))
            order_id.delete()

            return Response(
                {
                "success": True,
                "result": "Бронь была удалена"
                },
                status=status.HTTP_202_ACCEPTED
                )

        except Order.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такая бронь не была найдена"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

