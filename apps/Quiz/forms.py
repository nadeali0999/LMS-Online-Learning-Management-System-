from django import forms
from .models import Question


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz')
        super().__init__(*args, **kwargs)
        for question in quiz.questions.all():
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=[
                    (question.option1, question.option1),
                    (question.option2, question.option2),
                    (question.option3, question.option3),
                    (question.option4, question.option4),
                ],
                widget=forms.RadioSelect
            )
