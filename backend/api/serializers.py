from rest_framework import serializers

from packages.models import Letter, Package


class LetterSerializer(serializers.ModelSerializer):
    """Сериализатор для писем CRUD"""
    departure_index = serializers.CharField(
        source='departure_office.postal_index',
        read_only=True,
    )
    arrival_index = serializers.CharField(
        source='arrival_office.postal_index',
        read_only=True,
    )

    class Meta:
        model = Letter
        fields = ('id',
                  'sender',
                  'recipient',
                  'departure_office',
                  'arrival_office',
                  'departure_index',
                  'arrival_index',
                  'category',
                  'weight',)

    def to_representation(self, instance):
        """Отображение текстовых данных из связанных моделей."""
        ret = super().to_representation(instance)
        ret['sender'] = instance.sender.full_name
        ret['recipient'] = instance.recipient.full_name
        ret['departure_office'] = instance.departure_office.address
        ret['arrival_office'] = instance.arrival_office.address
        ret['category'] = instance.get_category_display()
        return ret

    def validate(self, data):
        """Валидация условия разных данных в парах:
        Отправитель/Получатель и пункт отправки/пункт получения.
        Предусмотрено использование метода PATCH.
        """
        instance = getattr(self, 'instance', None)

        sender = data.get('sender', instance.sender if instance else None)
        recipient = data.get('recipient',
                             instance.recipient if instance else None)
        if sender == recipient:
            raise serializers.ValidationError(
                'Отправитель и получатель должны быть разные')

        departure_office = data.get(
            'departure_office',
            instance.departure_office if instance else None
        )
        arrival_office = data.get(
            'arrival_office',
            instance.arrival_office if instance else None
        )
        if departure_office == arrival_office:
            raise serializers.ValidationError(
                'Пункты отправления и получения должны быть разные')
        return data


class PackageSerializer(LetterSerializer):
    """Сериализатор для посылок CRUD.
    Наследование от сериализатора Писем."""
    phone_number = serializers.CharField(
        source='recipient.phone_number',
        read_only=True,
    )

    class Meta:
        model = Package
        fields = ('id',
                  'sender',
                  'recipient',
                  'departure_office',
                  'arrival_office',
                  'departure_index',
                  'arrival_index',
                  'phone_number',
                  'category',
                  'cost',)
