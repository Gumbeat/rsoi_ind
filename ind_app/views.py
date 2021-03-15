import os

from rest_framework.response import Response

from .models import Document
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from .serializers import DocumentListSerializer
from .index import index


def detail(request: HttpRequest, question_id):
    return HttpResponse(f"You're looking at question {question_id}.")


def create_index(request: HttpRequest):
    pass


class DocumentListView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentListSerializer


class DocumentView(APIView):
    queryset = Document.objects.all()
    serializer_class = DocumentListSerializer

    def get(self, request, *args, **kwargs):
        text = kwargs.get('doc')

        documents = index.get_word_dict().get(text)
        return Response({'word': text, 'documents': documents})
