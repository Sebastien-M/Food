from django.urls import path
from graphene_django.views import GraphQLView
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graphql', GraphQLView.as_view(graphiql=True)),
]
