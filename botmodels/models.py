from django.db import models
from django.utils import timezone

class CreatedUpdatedMixin(models.Model):

    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Дата и время создания записи")
    updated_at = models.DateTimeField(auto_now=True,  blank=True, null=True, verbose_name="Дата и время обновления записи")

    class Meta:
        abstract = True



class QuestionType(CreatedUpdatedMixin):

    title = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Тип вопроса'

    def __str__(self):
        return str(self.title)


class QuestionContent(CreatedUpdatedMixin):

    value = models.CharField(max_length=4096)

    class Meta:
        verbose_name = 'Содержимое вопроса'

    def __str__(self):
        return str(self.value[:100]+'...')


class Workflow(CreatedUpdatedMixin):

    title = models.CharField(max_length=64)

    def __str__(self):
        return str(self.title)


class Question(CreatedUpdatedMixin):

    #slug = models.SlugField(unique=True)
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, verbose_name='Тип вопроса', related_name='questions')
    content = models.ForeignKey(QuestionContent, on_delete=models.CASCADE, verbose_name='Содержание вопроса')
    workflow_id = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='Workflow')
    explanation = models.CharField(max_length=2048, verbose_name='Поянение ответа')

    class Meta:
        verbose_name = 'Вопрос'


class User(CreatedUpdatedMixin):

    telegram_id = models.CharField(max_length=256, verbose_name='Id пользователя в телеграмме')
    nick = models.CharField(max_length=128, verbose_name='Ник пользователя')

    def __str__(self):
        return 'Пользователь: '+str(self.nick) + ', Токен: ' + str(self.telegram_id)

    class Meta:
        verbose_name = 'Юзер'


class Answer(CreatedUpdatedMixin):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос, которому принадлежит ответ', related_name='answers')
    text = models.CharField(max_length=2048, verbose_name='Текст ответа')
    is_correct = models.BooleanField(verbose_name='Корректен ли ответ')

    class Meta:
        verbose_name = 'Ответ'


class UserAnswer(CreatedUpdatedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='his_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ пользователя'