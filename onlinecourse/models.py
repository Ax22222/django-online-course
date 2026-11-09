from django.db import models
from django.utils.timezone import now

class Question(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True, id__in=selected_ids)
        total_correct = self.choice_set.filter(is_correct=True).count()
        return all_answers.count() == total_correct and len(selected_ids) == total_correct


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission on {self.date_submitted}"
