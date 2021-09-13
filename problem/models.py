from django.db import models
from django.conf import settings
from django.urls import reverse


class Problem(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=5)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    desc = models.TextField()
    input_info = models.CharField(max_length=200)
    output_info = models.CharField(max_length=200)

    data = models.JSONField()
    level = models.CharField(max_length=25, choices=(
        ('Oson', 'Oson'),
        ("O'rtacha", "O'rtacha"),
        ('Murakkab', 'Murakkab'),
    ))

    def __str__(self):
        return f'{self.title}'

    @property
    def url(self):
        return 'http://127.0.0.1:8000' + reverse('api:problem_detail_api', args=[self.id])

    @property
    def get_ins(self):
        return self.data['in']

    @property
    def get_outs(self):
        return self.data['out']

    @property
    def inputs(self):
        ins = self.data['in']
        ins3 = {key: ins[key] for key in list(ins.keys())[:3]}
        return ins3

    @property
    def outputs(self):
        outs = self.data['out']
        outs3 = {key: outs[key] for key in list(outs.keys())[:3]}
        return outs3

    @property
    def ac_rate(self):
        ac = self.submission_set.filter(status_id=3).count()
        all_c = self.submission_set.count()
        if all_c != 0:
            return round(ac * 100 / all_c, 1)
        else:
            return 0

    @property
    def ac_subs(self):
        return self.submission_set.filter(status_id=3).count()

    @property
    def wa_subs(self):
        return self.submission_set.exclude(status_id=3).count()

    def save(self, **kwargs):
        if self.id:
            return super(Problem, self).save(**kwargs)
        if Problem.objects.count():
            prev_id = Problem.objects.last().id
            self.id = '{:05d}'.format(int(prev_id) + 1)
        else:
            self.id = '{:05d}'.format(1)
        return super(Problem, self).save(**kwargs)
