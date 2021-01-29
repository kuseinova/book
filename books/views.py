from datetime import timedelta

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import generics, serializers, status, permissions
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from books.filters import BookFilter
from books.models import Book, Favorites, Ratings, Comment
from books.serializers import BookAPISerializer, FavoritesAPISerializer, RatingSerializer, CommentSerializer, \
    BookSerializer
from books.utils import send_activation_email
from order.models import Ordered
from books.permissions import IsAuthorOrReadOnly



# class MyPagination(PageNumberPagination):
#     page_size = 1


class BookListApiView(ListCreateAPIView):
    queryset = Book.objects.filter(active=True)
    serializer_class = BookAPISerializer
    # pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        time = self.request.query_params.get('time')
        search = self.request.query_params.get('search')
        if time:
            if time == 'hour':
                start_time = timezone.now() - timedelta(hours=1)
            elif time == 'day':
                start_time = timezone.now() - timedelta(days=1)
            elif time == 'week':
                start_time = timezone.now() - timedelta(weeks=1)
            elif time == 'minutes':
                start_time = timezone.now() - timedelta(minutes=1)
            else:
                queryset = Book.objects.filter(active=True)
                return queryset
            queryset = Book.objects.filter(created_at__gte=start_time,
                                           active=True)
        if search and time:
            queryset = Book.objects.filter(Q(title__icontains=search) |
                                           Q(description__icontains=search) |
                                           Q(author__icontains=search),
                                           created_at__gte=start_time,
                                           active=True)
        elif search:
            queryset = Book.objects.filter(Q(title__icontains=search) |
                                           Q(description__icontains=search) |
                                           Q(author__icontains=search),
                                           active=True)
        else:
            queryset = Book.objects.filter(active=True)
        return queryset

    def post(self, request, *args, **kwargs):
        request.data['publisher'] = request.user.pk
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        id = serializer.data['id']
        user = serializer.data['publisher']
        title = serializer.data['title']
        send_activation_email(id, title)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) |
                                       Q(description__icontains=q))
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class BookDetailApiView(RetrieveUpdateDestroyAPIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Book.objects.all()
    serializer_class = BookAPISerializer


class ActivationView(View):

    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
            book.active = True
            book.save()
            return render(request, 'activation_complete.html', {})

        except Book.DoesNotExist:
            return render(request, 'activation_error.html', {})


class FavoritesListApiView(generics.ListCreateAPIView):

    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = FavoritesAPISerializer

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if len(request.data.keys()) == 1 and request.data.get('book'):
            user = request.user.pk
            book = request.data['book']
            favorites = Favorites.objects.filter(book=book, user=user)
            if favorites:
                raise serializers.ValidationError('Книга уже в избранных')
            request.data['user'] = request.user.pk

        else:
            raise serializers.ValidationError('Неправильно переданы данные')
            pass
        return self.create(request, *args, **kwargs)


class FavoriteAdd(APIView):

    permission_classes = (IsAuthorOrReadOnly,)

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        user = request.user
        url = request.build_absolute_uri()
        if Favorites.objects.filter(user=user.pk, book=pk):
            raise serializers.ValidationError('Книга уже добавлена в '
                                              'избранные')
        new_favorite = Favorites.objects.create(user=user, book=book)
        return HttpResponseRedirect(redirect_to=url)


class FavoriteDelete(APIView):
    permission_classes = (IsAuthorOrReadOnly,)
    def get(self, request, pk):
        user = request.user
        favor = Favorites.objects.filter(user=user.pk, book=pk)
        if favor:
            favor.delete()
            raise serializers.ValidationError('Книга удалена из избранных')
        raise serializers.ValidationError('Книги нету в избранных')


class RatingCreate(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = RatingSerializer

    def post(self, request, *args, **kwargs):
        ordered = Ordered.objects.filter(user=request.user.pk,
                                         book=request.data['book'])
        if not ordered:
            raise serializers.ValidationError('Вы не купили эту книгу')
        rating = Ratings.objects.filter(book=request.data['book'],
                                        user=request.user.pk)
        if rating:
            rating = rating.first()
            rating.delete()
        request.data._mutable = True
        request.data['user'] = request.user.pk
        request.data._mutable = False
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        book = serializer.data['book']
        book = Book.objects.get(pk=book)
        all_ratings = []
        all_sum = 0
        ratings = Ratings.objects.filter(book=book.pk)
        for i in ratings:
            all_ratings.append(i.rating)
            all_sum += i.rating
        rat = all_sum / len(all_ratings)
        print(rat)
        book.rating = rat
        book.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)



class CommentCreate(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

