from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Author, Book, BookLoan
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    AuthorSerializer, BookSerializer, BookLoanSerializer, BookLoanCreateSerializer
)
from .permissions import IsLibrarianOrAdmin, IsAdmin, IsOwnerOrLibrarian


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Views
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsLibrarianOrAdmin]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']


# Author Views
class AuthorListView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsLibrarianOrAdmin]
        return super().get_permissions()


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarianOrAdmin]
    queryset = Author.objects.all()


# Book Views
class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre', 'authors']
    search_fields = ['title', 'isbn', 'authors__name']

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsLibrarianOrAdmin]
        return super().get_permissions()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsLibrarianOrAdmin]
        return super().get_permissions()


# Book Loan Views
class BookLoanListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookLoanCreateSerializer
        return BookLoanSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['librarian', 'admin']:
            return BookLoan.objects.all()
        return BookLoan.objects.filter(user=user)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'book']
    search_fields = ['book__title', 'user__username']


class BookLoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookLoanSerializer
    permission_classes = [IsOwnerOrLibrarian]
    queryset = BookLoan.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'returned':
            book = instance.book
            book.available_copies += 1
            book.save()
        serializer.save()
