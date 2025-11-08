from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User, Author, Book, BookLoan


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone', 'address', 'user_type')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Проверяем уникальность username
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})

        # Проверяем уникальность email
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})

        return attrs

    def create(self, validated_data):
        # Удаляем password2 из validated_data перед созданием пользователя
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'user_type')
        read_only_fields = ('id', 'username')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all(),
        source='authors',
        write_only=True
    )

    class Meta:
        model = Book
        fields = '__all__'


class BookLoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = BookLoan
        fields = '__all__'
        # Убираем status из read_only_fields, чтобы можно было обновлять
        read_only_fields = ('borrowed_date',)

    def get_is_overdue(self, obj):
        return obj.is_overdue()


class BookLoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = ('book', 'due_date')

    def validate(self, attrs):
        book = attrs['book']
        if book.available_copies < 1:
            raise serializers.ValidationError("No available copies of this book")
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        book = validated_data['book']
        book.available_copies -= 1
        book.save()
        return super().create(validated_data)
