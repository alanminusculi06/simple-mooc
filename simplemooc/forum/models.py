from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings

class Thread(models.Model):
    title = models.CharField('Título', max_length=100)
    body = models.TextField('Mensagem')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads', on_delete=models.CASCADE)
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-updated_at']


class Reply(models.Model):
    thread = models.ForeignKey(Thread, verbose_name='Tópico', related_name='replies', on_delete=models.CASCADE)
    message = models.TextField('Mensagem')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='replies', on_delete=models.CASCADE)
    correct = models.BooleanField('Melhor resposta', blank=True, default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.message[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created_at']

    