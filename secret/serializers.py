from rest_framework import serializers

from .models import Secret


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = '__all__'

    def validate(self, attrs):
        passphrase = attrs.get('passphrase')
        time_to_live = attrs.get('time_to_live')
        if (time_to_live) and (time_to_live > 100000 or time_to_live <= 1):
            raise serializers.ValidationError("Время для существования "
                                              "секретов не "
                                              "может быть меньше 1 "
                                              "и превышать 100000 минут")
        if len(passphrase) < 16:
            raise serializers.ValidationError("Длина кодовой фразы должна "
                                              "быть не меньше 15 символов")
        return attrs
