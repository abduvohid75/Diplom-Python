from django.shortcuts import render
from rest_framework import viewsets
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.generics import RetrieveAPIView

from .models import Secret
from .serializers import SecretSerializer
from rest_framework import serializers


def index(request):
    context = {}
    return render(request, 'secret/index.html', context)


class SecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action != 'create':
            queryset = queryset.none()

        return queryset


class SecretPassphraseDetailView(RetrieveAPIView):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer

    def get_object(self):
        key = urlsafe_base64_encode(self.kwargs['passphrase'].encode('utf-8'))
        if len(list(Secret.objects.filter(passphrase=key))) > 1:
            raise serializers.ValidationError(
                "В базе данных несколько значений с такой кодовой фразой. "
                "Попробуйте в следующий раз усложнить свою кодовую фразу, "
                "а сейчас для доступа воспользуйтесь "
                "выданным секретным ключом")
        else:
            obj = Secret.objects.get(passphrase=key)
            obj.passphrase = urlsafe_base64_decode(key).decode('utf-8')
        self.check_object_permissions(self.request, obj)
        return obj


class SecretKeyDetailView(RetrieveAPIView):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
    lookup_field = 'generated_key'

    def get_object(self):
        obj = super().get_object()
        if not obj.is_active:
            raise serializers.ValidationError("Ключ уже использован")
        obj.is_active = False
        obj.save()
        obj.passphrase = urlsafe_base64_decode(obj.passphrase).decode('utf-8')
        return obj
