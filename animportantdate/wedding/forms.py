from . import models
from django import forms
from django.utils.translation import ugettext_lazy as _

class AuthForm(forms.Form):

    pnr = forms.CharField(
        max_length=6,
        label="Confirmation code",
    )


class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = [
            "main_email",
            "telephone",
            "address_1",
            "address_2",
            "address_3",
            "favorite_dancing_songs",
            "changes",
            "comments"
        ]

    def make_required(self, field):
        self.fields[field].required = True

    def __init__(self, *a, **k):
        super(GroupForm, self).__init__(*a, **k)
        required_fields = [
            "main_email",
            "address_1",
            "address_3",
            "telephone",
        ]
        for i in required_fields:
            self.make_required(i)

class PersonForm(forms.ModelForm):

    class Meta:
        model = models.Person
        fields = [
            "name",
            "email",
            "rsvp_status",
            "dietary_restrictions"
        ]

    def make_required(self, field):
        self.fields[field].required = True

    def __init__(self, *a, **k):
        super(PersonForm, self).__init__(*a, **k)
        required_fields = [
            "name",
            "rsvp_status"
        ]
        for i in required_fields:
            self.make_required(i)


class DoMailoutForm(forms.Form):
    ACTION_PREVIEW = 1
    ACTION_SEND_MAIL = 2

    ACTIONS = (
        (ACTION_PREVIEW, "Preview"),
        (ACTION_SEND_MAIL, "Send mailout"),
    )

    people = forms.ModelMultipleChoiceField(queryset=models.Person.objects)
    action = forms.TypedChoiceField(choices=ACTIONS, coerce=int)
