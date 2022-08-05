from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Partner(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Contract(models.Model):
    name = models.TextField(
        'Название договра',
        help_text='Введите название договра'
    )
    number = models.TextField(
        'Номер договра',
        help_text='Введите номер договра'
    )
    start_date = models.DateField(
        'Дата начала',
        help_text='Введите дату начала договра'
    )
    end_date = models.DateField(
        'Дата окончания',
        help_text='Введите дату окончания договра'
    )
    curator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='contracts',
        verbose_name='Куратор договора'
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='partner',
        blank=False,
        null=False,
        verbose_name='Контрагент',
        help_text='Вторая сторона по договору'
    )
    file = models.FileField(
        'Файл договора',
        upload_to='files/',
        blank=True
    )

    class Meta:
        ordering = ['-start_date']

    def __str__(self) -> str:
        return self.name


class UserContraсts(models.Model):
    
    collaborator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='Collaborator',
        verbose_name='Пользователь договора'
    )
    deal = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        null=True,
        related_name='Contract',
        verbose_name='Договор'
    )

    def __str__(self) -> str:
        return 'Договоры пользователей'
