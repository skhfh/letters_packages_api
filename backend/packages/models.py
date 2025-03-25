from django.db import models
from django.core.validators import RegexValidator


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
            regex='^\+7\d{10}$',
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
            regex='^\d{6}$',
            message='Введите почтовый индекс из шести цифр',
            code='invalid_postal_index')],
    )

    class Meta:
        verbose_name = 'Почтовое отделение'
        verbose_name_plural = 'Почтовые отделения'

    def __str__(self):
        return self.address


class PackageAbstractModel(models.Model):
    """АБСТРАКТНАЯ модель для писем и посылок"""
    sender = models.ForeignKey(Client,
                               related_name='package_sender',
                               on_delete=models.CASCADE,
                               verbose_name='Отправитель',)
    recipient  = models.ForeignKey(Client,
                                   related_name='package_recipient',
                                   on_delete=models.CASCADE,
                                   verbose_name='Получатель',)
    departure_office = models.ForeignKey(PostOffice,
                                         related_name='sent_from',
                                         on_delete=models.CASCADE,
                                         verbose_name='Пункт отправки',)
    arrival_office = models.ForeignKey(PostOffice,
                                       related_name='sent_to',
                                       on_delete=models.CASCADE,
                                       verbose_name='Пункт получения',)

    class Meta:
        abstract = True


class Letter(PackageAbstractModel):

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Package(PackageAbstractModel):

    class Meta:
        verbose_name = 'Посылка'
        verbose_name_plural = 'Посылки'
