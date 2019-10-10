import graphene
from django.contrib.auth import authenticate
from graphene_django import DjangoObjectType
from graphql_jwt.utils import jwt_encode, jwt_payload
from SendgridDjangoDemo.authentication.models import User
from SendgridDjangoDemo.authentication.send_email import send_confirmation_email


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CreateUser(graphene.Mutation):
    message = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = User.objects.create_user(
            email=kwargs.get('email'),
            username=kwargs.get('username'),
        )
        user.set_password(kwargs.get('password'))
        user.save()
        send_confirmation_email(email=user.email, username=user.username)
        return CreateUser(user=user, message="Successfully created user, {}".format(user.username))


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    message = graphene.String()
    token = graphene.String()
    verification_prompt = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = authenticate(username=email, password=password)
        error_message = 'Invalid login credentials'
        success_message = "You logged in successfully."
        verification_error = 'Your email is not verified'
        if user:
            if user.is_verified:
                payload = jwt_payload(user)
                token = jwt_encode(payload)
                return LoginUser(token=token, message=success_message)
            return LoginUser(message=verification_error)
        return LoginUser(message=error_message)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
