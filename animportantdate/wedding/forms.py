from . import models
from django import forms
from django.utils.translation import ugettext_lazy as _

class AuthForm(forms.Form):

    pnr = forms.CharField(
        max_length=20,
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
        ]
        for i in required_fields:
            self.make_required(i)

class GroupOptionsWhereStayForm(forms.ModelForm):

    class Meta:
        model = models.GroupOptions
        fields = [
            "where_stay",
        ]

    def make_required(self, field):
        self.fields[field].required = True

    def __init__(self, *a, **k):
        super(GroupOptionsWhereStayForm, self).__init__(*a, **k)
        required_fields = []
        for i in required_fields:
            self.make_required(i)

    def clean(self):
        cleaned_data = super(GroupOptionsWhereStayForm, self).clean()
        where_stay = cleaned_data.get("where_stay")
        if where_stay == 1:
            msg = "Please let us know where you're staying!"
            self.add_error('where_stay', msg)
        return cleaned_data

class GroupOptionsCampForm(forms.ModelForm):

    class Meta:
        model = models.GroupOptions
        fields = [
            "camp_options_party",
            "camp_options_reasonable",
            "camp_options_heavy_sleeper",
            "camp_options_light_sleeper",
            "camp_options_bathroom",
            "camp_options_ac",
        ]

    def make_required(self, field):
        self.fields[field].required = True

    def __init__(self, *a, **k):
        super(GroupOptionsCampForm, self).__init__(*a, **k)
        required_fields = []
        for i in required_fields:
            self.make_required(i)

class GroupOptionsMobilityForm(forms.ModelForm):

    class Meta:
        model = models.GroupOptions
        fields = [
            "number_of_rides",
            "number_of_seated",
            "other_mobility"
        ]

    def make_required(self, field):
        self.fields[field].required = True

    def __init__(self, *a, **k):
        super(GroupOptionsMobilityForm, self).__init__(*a, **k)
        required_fields = []
        for i in required_fields:
            self.make_required(i)

class GroupOptionsHasReviewedForm(forms.ModelForm):

    class Meta:
        model = models.GroupOptions
        fields = [
            "has_reviewed"
        ]

    def make_required(self, field):
        self.fields[field].required = True

    def __init__(self, *a, **k):
        super(GroupOptionsHasReviewedForm, self).__init__(*a, **k)
        required_fields = [
            "has_reviewed"
        ]
        for i in required_fields:
            self.make_required(i)

    def clean(self):
        cleaned_data = super(GroupOptionsHasReviewedForm, self).clean()
        has_reviewed = cleaned_data.get("has_reviewed")
        if not has_reviewed:
            msg = "Please review the form questions above and make sure you've answered any necessary."
            self.add_error('has_reviewed', msg)
        return cleaned_data



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

    def clean(self):
        cleaned_data = super(PersonForm, self).clean()
        rsvp_status = cleaned_data.get("rsvp_status")
        if rsvp_status == 1:
            msg = "Must set RSVP status."
            self.add_error('rsvp_status', msg)
        return cleaned_data


class DoMailoutForm(forms.Form):
    ACTION_PREVIEW = 1
    ACTION_SEND_MAIL = 2

    ACTIONS = (
        (ACTION_PREVIEW, "Preview"),
        (ACTION_SEND_MAIL, "Send mailout"),
    )

    people = forms.ModelMultipleChoiceField(queryset=models.Person.objects)
    action = forms.TypedChoiceField(choices=ACTIONS, coerce=int)
