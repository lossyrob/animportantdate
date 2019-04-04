from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone
# Create your models here.


class Group(models.Model):
    ''' A group is an organisation that receives an invitation. '''

    def __str__(self):
        return self.display_name

    pnr = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Confirmation Code",
    )

    main_email = models.EmailField(blank=True)

    address_1 = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Address Line 1",
    )
    address_2 = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Address Line 2",
    )
    address_3 = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Adress Line 3",
    )

    telephone = models.CharField(
        max_length=20,
        blank=True,
    )

    favorite_dancing_songs = models.TextField(
        blank=True,
        verbose_name="What's your favorite songs to dance to?"
    )

    changes = models.TextField(
        blank=True,
        verbose_name="Any changes to your information above not captured by the form?"
    )

    comments = models.TextField(
        blank=True,
        verbose_name="Any additional comments?"
    )

    # 4 chars to allow for ICAO if absolutely necessary
    home_airport = models.CharField(
        max_length=4,
        blank=True,
    )

    display_name = models.CharField(max_length=255)
    events = models.ManyToManyField(
        "Event",
        blank=True,
    )


class GroupOptions(models.Model):
    '''Attendee questions'''

    group = models.ForeignKey(Group)

    #     Where are you staying?

    WHERE_STAY_UNKNOWN = 1
    WHERE_STAY_CAMP = 2
    WHERE_STAY_HOTEL =  3
    WHERE_STAY_TENT = 4
    WHERE_STAY_OTHER = 5

    WHERE_STAY_CHOICES = (
        (WHERE_STAY_UNKNOWN, "No Response"),
        (WHERE_STAY_CAMP, "I'd like to stay at the camp, in one of the vintage bunk beds."),
        (WHERE_STAY_HOTEL, "I'm getting a hotel block, as described on the website"),
        (WHERE_STAY_TENT, "I'd like to stay at the camp in a tent (that I bring)"),
        (WHERE_STAY_OTHER, "I'll be staying somewhere else, don't worry about it!")
    )

    where_stay = models.IntegerField(
        choices=WHERE_STAY_CHOICES,
        default=WHERE_STAY_UNKNOWN,
    )

    #     If staying at camp, what do you need? (Checkboxes)

    camp_options_party = models.BooleanField(
        default=False,
        verbose_name = 'I plan on partying either until the sun rises or my body yells "hey! get some rest!"')
    camp_options_reasonable = models.BooleanField(
        default=False,
        verbose_name="I love weddings, but I still need to get to bed at a reasonable hour.")
    camp_options_heavy_sleeper = models.BooleanField(
        default=False,
        verbose_name='I am a heavy sleeper.')
    camp_options_light_sleeper = models.BooleanField(
        default=False,
        verbose_name='I am a light sleeper.')
    camp_options_bathroom = models.BooleanField(
        default=False,
        verbose_name='I need the bathroom that I use to be in the same building as I sleep.')
    camp_options_ac = models.BooleanField(
        default=False,
        verbose_name='I need air conditioning.')

    #     Mobility questions

    number_of_rides = models.IntegerField(
        default=0,
        verbose_name='How many people in your group would like a ride up the hill to the ceremony and back down at the conclusion?'
    )

    number_of_seated = models.IntegerField(
        default=0,
        verbose_name='How many people in your group would like to sit throughout the ceremony?')

    other_mobility = models.TextField(
        verbose_name="Are there other mobility questions that we aren't considering that we should be aware of?",
        blank=True)

    has_reviewed = models.BooleanField(
        default=False,
        verbose_name='I have reviewed these questions and are all set with our answers!'
    )

class Person(models.Model):

    def __str__(self):
        return self.name

    RSVP_UNKNOWN = 1
    RSVP_ATTENDING = 2
    RSVP_NOT_ATTENDING = 3

    RSVP_CHOICES = (
        (RSVP_UNKNOWN, "No Response"),
        (RSVP_ATTENDING, "Attending"),
        (RSVP_NOT_ATTENDING, "Not attending"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    group = models.ForeignKey(Group)
    rsvp_status = models.IntegerField(
        choices=RSVP_CHOICES,
        default=RSVP_UNKNOWN,
    )
    name_flagged = models.BooleanField()

    DIET_NONE = 1
    DIET_VEGETARIAN = 2
    DIET_VEGAN = 3
    DIET_KOSHER = 4
    DIET_GLUTEN_FREE = 5
    DIET_OTHER = 6

    DIET_CHOICES = (
        (DIET_NONE, "None"),
        (DIET_VEGETARIAN, "Vegetarian"),
        (DIET_VEGAN, "Vegan"),
        (DIET_KOSHER, "Kosher"),
        (DIET_GLUTEN_FREE, "Gluten Free"),
        (DIET_OTHER, "Other"),
    )

    dietary_restrictions = models.IntegerField(
        choices=DIET_CHOICES,
        default=DIET_NONE,
    )


class Event(models.Model):

    def __str__(self):
        return self.name

    short_name = models.CharField(
        max_length=20,
        help_text="This is used to look up an event, e.g. by the "
                  "group_has_event tag.",
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    address = models.TextField()
    directions_url = models.CharField(max_length=255)
    description = models.TextField()


class Mailout(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event)
    subject = models.CharField(max_length=255)
    plain_text = models.TextField()


class MailSent(models.Model):

    def __str__(self):
        return "%s sent to %s" % (self.mailout, self.recipient)

    recipient = models.ForeignKey(Person)
    mailout = models.ForeignKey(Mailout)
    datestamp = models.DateTimeField(default=timezone.now)
