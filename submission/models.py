from django.conf import settings
from django.db import models
from django.urls import reverse


class Submission(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=5)
    problem = models.ForeignKey('problem.Problem', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    status_id = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=50)
    lang_id = models.PositiveSmallIntegerField()
    memory = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    code = models.TextField()
    err = models.TextField(null=True)

    def __str__(self):
        return f'{self.id} | {self.author}:{self.problem}:{self.status}'

    class Meta:
        ordering = ('-id', )

    def get_absolute_url(self):
        return reverse('attempt:get', kwargs={'pk': self.pk})

    def save(self, **kwargs):
        if self.id:
            return super(Submission, self).save(**kwargs)
        if Submission.objects.count():
            prev_id = Submission.objects.first().id
            self.id = '{:05d}'.format(int(prev_id) + 1)
        else:
            self.id = '{:05d}'.format(1)
        return super(Submission, self).save(**kwargs)
