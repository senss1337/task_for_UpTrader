from django.db import models
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class Menu(models.Model):
    name = models.CharField('Название меню', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        verbose_name='Меню',
        related_name='items',
        on_delete=models.CASCADE
    )
    name = models.CharField('Название пункта', max_length=100)
    named_url = models.CharField('Именнованный URL', max_length=100, blank=True, null=True)
    url = models.CharField('URL без имени', max_length=200, blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский пункт',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']
        indexes = [
            models.Index(fields=['parent']),
            models.Index(fields=['menu']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if hasattr(self, '_parent_cache'):
            print("[DEBUG] Parent preloaded for:", self.name)
        else:
            print("[DEBUG] Parent not preloaded for:", self.name)

        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.url or '#'
        return self.url or '#'
