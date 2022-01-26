from django import forms
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.layout import Layout, Fieldset,  Submit
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email(value):
    value = str(value[value.index("@")+1:])
    if value != "softcatalyst.com":
        raise ValidationError(
            _('Email is invalid. The email should be a softcatalyst email'),

        )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    feedbackmsg = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(validators=[validate_email])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-feedbackForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-7'
        # self.helper.add_input(Submit('submit', 'Send Feedback'))
        self.helper.layout = Layout(
            Fieldset(
                'This form is to receive your feedback !',
                'name',
                PrependedText('email', '@', placeholder="email"),
                'feedbackmsg'

            ),
            FormActions(
                Submit('submit', 'Send Feedback'),

            ),

        )

