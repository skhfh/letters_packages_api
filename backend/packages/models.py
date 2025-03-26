from django.db import models
from django.core.validators import MinValueValidator, RegexValidator


class Client(models.Model):
    """Модель клиентов (отправитель/получатель)"""
    name = models.CharField(max_length=50, verbose_name='Имя',)
    lastname = models.CharField(max_length=50, verbose_name='Фамилия',)
    middle_name = models.CharField(max_length=50,
                                   verbose_name='Отчество',
                                   null=True,
                                   blank=True,)
    phone_number = models.CharField(
        max_length=50,
        verbose_name='Номер телефона',
        validators=[RegexValidator(
            regex=r'^\+7\d{10}$',
            message='Введите номер телефона в формате +7XXXXXXXXXX',
            code='invalid_phone_number')],
    )

    @property
    def full_name(self):
        """ФИО полностью"""
        return f'{self.lastname} {self.name} {self.middle_name or ""}'.strip()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.full_name


class PostOffice(models.Model):
    """Модель почтовых отделений (пункт отправки/пункт получения)"""
    address = models.CharField(max_length=150, verbose_name='Адрес ПО',)
    postal_index = models.CharField(
        max_length=6,
        verbose_name='Почтовый индекс',
        validators=[RegexValidator(
            regex=r'^\d{6}$',
            message='Введите почтовый индекс из шести цифр',
            code='invalid_postal_index')],
    )

    class Meta:
        verbose_name = 'Почтовое отделение'
        verbose_name_plural = 'Почтовые отделения'

    def __str__(self):
        return self.address


class Letter(models.Model):
    """Модель писем"""
    sender = models.ForeignKey(Client,
                               related_name='letter_sender',
                               on_delete=models.CASCADE,
                               verbose_name='Отправитель',)
    recipient = models.ForeignKey(Client,
                                  related_name='letter_recipient',
                                  on_delete=models.CASCADE,
                                  verbose_name='Получатель',)
    departure_office = models.ForeignKey(PostOffice,
                                         related_name='sent_letter_from',
                                         on_delete=models.CASCADE,
                                         verbose_name='Пункт отправки',)
    arrival_office = models.ForeignKey(PostOffice,
                                       related_name='sent_letter_to',
                                       on_delete=models.CASCADE,
                                       verbose_name='Пункт получения',)

    class LetterType(models.IntegerChoices):
        """Enum класс: Типы писем на выбор"""
        SIMPLE = 1, 'Письмо'
        REGISTERED = 2, 'Заказное письмо'
        VALUABLE = 3, 'Ценное письмо'
        EXPRESS = 4, 'Экспресс-письмо'

    category = models.IntegerField(choices=LetterType.choices,
                                   verbose_name='Тип письма')
    weight = models.PositiveIntegerField(
        verbose_name='Вес письма',
        validators=[MinValueValidator(
            1, 'Вес письма должно быть более 1 г.')],
    )

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender=models.F('recipient')),
                name='letter_sender_and_recipient_different',
            ),
            models.CheckConstraint(
                check=~models.Q(departure_office=models.F('arrival_office')),
                name='letter_departure_and_arrival_different',
            ),
        ]


class Package(models.Model):
    """Модель посылок"""
    sender = models.ForeignKey(Client,
                               related_name='package_sender',
                               on_delete=models.CASCADE,
                               verbose_name='Отправитель',)
    recipient = models.ForeignKey(Client,
                                  related_name='package_recipient',
                                  on_delete=models.CASCADE,
                                  verbose_name='Получатель',)
    departure_office = models.ForeignKey(PostOffice,
                                         related_name='sent_package_from',
                                         on_delete=models.CASCADE,
                                         verbose_name='Пункт отправки',)
    arrival_office = models.ForeignKey(PostOffice,
                                       related_name='sent_package_to',
                                       on_delete=models.CASCADE,
                                       verbose_name='Пункт получения',)

    class PackageType(models.IntegerChoices):
        """Enum класс: Типы посылок на выбор"""
        SMALL = 1, 'Мелкий пакет'
        SIMPLE = 2, 'Посылка'
        FIRST = 3, 'Посылка 1 класса'
        VALUABLE = 4, 'Ценная посылка'
        INTERNATIONAL = 5, 'Посылка международная'
        EXPRESS = 6, 'Экспресс-посылка'

    category = models.IntegerField(choices=PackageType.choices,
                                   verbose_name='Тип посылки')
    cost = models.PositiveIntegerField(
        verbose_name='Сумма платежа',
        validators=[MinValueValidator(
            1, 'Сумма платежа должна быть более 1 руб.')],
    )

    class Meta:
        verbose_name = 'Посылка'
        verbose_name_plural = 'Посылки'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender=models.F('recipient')),
                name='package_sender_and_recipient_different',
            ),
            models.CheckConstraint(
                check=~models.Q(departure_office=models.F('arrival_office')),
                name='package_and_arrival_different',
            ),
        ]
