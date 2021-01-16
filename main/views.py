from django.shortcuts import render, redirect
from .forms import UserRegistration
from .models import Feedback, Comment
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

########################################################################
######################## Rest Imports ##################################
from rest_framework import generics, status
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, User, FeedbackSerializer, CommentSerializer
########################################################################

def index(request: str):
    return render(
        request=request,
        template_name='main/index.html'
    )

def about(request: str):
    return render(
        request=request,
        template_name='main/about.html'
    )





def registration(request: str):
    if request.method=="POST":
        context=UserRegistration(request.POST)
        if context.is_valid():
            context.save()
        return redirect('/login/')

    else:
        context=UserRegistration()
        return render(
            request=request,
            template_name='main/registration.html',
            context={'context':context}
    )







class FeedbackCreateView(CreateView):
    model = Feedback
    fields = ('feedback_text',)
    template_name='main/feedback_create.html'


    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)






class FeedbackListView(ListView):
    model = Feedback
    template_name='main/feedback_list.html'







class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'main/feedback_details.html'



    def get_context_data(self, **kwargs):
        feedback = self.get_object()
        kwargs["comments"] = Comment.objects.filter(author=feedback.pk)
        return super().get_context_data(**kwargs)




class FeedbackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Feedback
    fields = ('feedback_text',)
    template_name='main/feedback_update.html'


    def test_func(self):
        feedback = self.get_object()

        if self.request.user==feedback.author:
            return True
        return False



class FeedbackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Feedback
    template_name='main/feedback_delete.html'
    success_url = '/feedbacks/'

    def test_func(self):
        feedback = self.get_object()

        if self.request.user==feedback.author:
            return True
        return False




####################################################################################################
####################################################################################################
####################################################################################################

class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def post(self, request):
        try:
            if request.data.get('author_id'):
                user = User.objects.get(pk=request.data.get('author_id'))
                author_id = user.pk
            else:
                author_id = None

        except:
            return Response(
            {
                "success": False,
                "result": "Что-то не то"
            },
            status=status.HTTP_201_CREATED
        )

        serializer=UserSerializer(data=request.data, context={"author_id":author_id, "request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "result": "Пользователь добавлен"
            },
            status=status.HTTP_201_CREATED
        )






class UserListAPIView(generics.ListAPIView):
    permission_classes=[IsAuthenticatedOrReadOnly,]
    serializer_class=UserSerializer

    queryset=User.objects.all()




class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def put(self,request):
        try:
            user_id = User.objects.get(pk=request.data.get('user_id'))

            serializer = UserSerializer(
                instance=user_id,
                data=request.data,
                partial = True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
            data={
                "success":True,
                "result":"Пользователь был ОБНОВЛЕН успешно"
            },
            status = status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"Пользователь не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )

class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def delete(self,request):
        try:
            user_id = User.objects.get(pk=request.data.get('user_id'))
            user_id.delete()
            return Response(
            data={
                "success":True,
                "result":"ПОЛЬЗОВАТЕЛЬ был DELETED успешно"
            },
            status = status.HTTP_202_ACCEPTED
            )
        except User.DoesNotExist:
            return Response(
                data={
                    "success":False,
                    "result":"ПОЛЬЗОВАТЕЛЬ не найден!"
                },
                status = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )



class FeedbackCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = FeedbackSerializer

    def get(self, request):
        feedback=Feedback.objects.all()
        serializer=self.serializer_class(feedback, many=True)

        return Response(
            {
            "success": True,
            "result": serializer.data
        },
            status=status.HTTP_200_OK
        )




    def post(self, request):
        try:
            if request.data.get('author_id'):
                user = User.objects.get(pk=request.data.get('author_id'))
                author_id = user.pk
            else:
                author_id = None
        except User.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такго пользователя нет"
            },
            status=status.HTTP_201_CREATED
        )



        serializer=FeedbackSerializer(data=request.data, context={"author_id":author_id, "request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "result": "Отзыв был оставлен успешно"
            },
            status=status.HTTP_201_CREATED
        )


class FeedbackUpdateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = FeedbackSerializer

    def put(self, request):
        try:
            feedback_id=Feedback.objects.get(pk=request.data.get('feedback_id'))
            serializer=FeedbackSerializer(instance=feedback_id, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                "success": True,
                "result": "Отзыв был обнавлен"
                },
                status=status.HTTP_201_CREATED
                )

        except Feedback.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такой отзыв не был найден"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )



class FeedbackDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny,]
    serializer_class = FeedbackSerializer

    def delete(self, request):
        try:
            feedback_id=Feedback.objects.get(pk=request.data.get('feedback_id'))
            feedback_id.delete()

            return Response(
                {
                "success": True,
                "result": "Отзыв был удален"
                },
                status=status.HTTP_202_ACCEPTED
                )

        except Feedback.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такой отзыв не был найден"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )













class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CommentSerializer

    def get(self, request):
        comment=Comment.objects.all()
        serializer=self.serializer_class(comment, many=True)

        return Response(
            {
            "success": True,
            "result": serializer.data
        },
            status=status.HTTP_200_OK
        )




    def post(self, request):
        try:
            if request.data.get('author_id'):
                user = User.objects.get(pk=request.data.get('author_id'))
                author_id = user.pk
            else:
                author_id = None

        except User.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такого пользователя нет"
            },
            status=status.HTTP_201_CREATED
        )



        serializer=CommentSerializer(data=request.data, context={"author_id":author_id, "request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "result": "Комент был оставлен успешно"
            },
            status=status.HTTP_201_CREATED
        )




class CommentUpdateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CommentSerializer

    def put(self, request):
        try:
            comment_id=Comment.objects.get(pk=request.data.get('comment_id'))
            serializer=CommentSerializer(instance=comment_id, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                "success": True,
                "result": "Комент был обнавлен"
                },
                status=status.HTTP_201_CREATED
                )

        except Comment.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такой комент не был найден"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )



class CommentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CommentSerializer

    def delete(self, request):
        try:
            comment_id=Comment.objects.get(pk=request.data.get('comment_id'))
            comment_id.delete()

            return Response(
                {
                "success": True,
                "result": "Комент был удален"
                },
                status=status.HTTP_202_ACCEPTED
                )

        except Comment.DoesNotExist:
            return Response(
            {
                "success": False,
                "result": "Такой комент не был найден"
            },
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
        )















# class FeedbackListAPIView(generics.ListAPIView):
#     permission_classes=[IsAuthenticatedOrReadOnly,]
#     serializer_class=FeedbackSerializer
#
#     def get_queryset(self):
#         queryset = Feedback.objects.all()
#         return queryset






    # def get(self, request):
    #     # queryset=Feedback.objects.all()
    #
    #     return Response(
    #         data={
    #             "success": True,
    #             "result": Feedback.objects.all().values()
    #
    #         },
    #         status=status.HTTP_200_OK
    #     )
    #
    #
