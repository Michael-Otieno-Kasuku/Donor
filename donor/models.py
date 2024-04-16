from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    county_name = models.CharField(max_length=255, unique=True, help_text="Enter a valid County Name")

    def __str__(self):
        return self.county_name

class Constituency(models.Model):
    constituency_id = models.AutoField(primary_key=True)
    county_id = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency_name = models.CharField(max_length=255, unique=True, help_text="Enter a valid Constituency Name")

    def __str__(self):
        return self.constituency_name

class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True)
    constituency_id = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    ward_name = models.CharField(max_length=255, unique=True, help_text="Enter a valid Ward Name")

    def __str__(self):
        return self.ward_name
        
def validate_blood_group_type(value):
    if value not in ['A', 'B','AB','O']:
        raise ValidationError('Blood group type can either be "A" or "B" or "AB" or "O"')

class BloodGroup(models.Model):
    blood_group_id = models.AutoField(primary_key=True)
    BLOOD_GROUP_TYPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]
    blood_group_type = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_TYPE_CHOICES,
        help_text="Choose a valid blood group type",
        validators=[validate_blood_group_type]
    )

    def __str__(self):
        return self.blood_group_type

class PotentialDonor(models.Model):
    potential_donor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200, help_text="Enter a valid first name")
    last_name = models.CharField(max_length=200, help_text="Enter a valid last name")
    blood_group_id = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=200, unique=True, help_text="Enter a valid email address")
    password_hash = models.CharField(max_length=128, help_text="Enter a valid password")  # Store hashed password

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def clean(self):
        # Custom validation for password field
        if len(self.password_hash) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

    def __str__(self):
        return self.email_address

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_description = models.CharField(max_length=255, unique=True, help_text="Enter a valid Event Description")

    def __str__(self):
        return self.event_description

class DonationCenter(models.Model):
    donation_center_id = models.AutoField(primary_key=True)
    ward_id = models.ForeignKey(Ward, on_delete=models.CASCADE)
    donation_center_name = models.CharField(max_length=255, unique=True, help_text="Enter a valid Donation Center Name")

    def __str__(self):
        return self.donation_center_name

class FutureEvent(models.Model):
    future_event_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    donation_center_id = models.ForeignKey(DonationCenter, on_delete=models.CASCADE)
    application_deadline = models.DateTimeField(help_text="Enter application deadline")
    start_date = models.DateTimeField(help_text="Enter Start Date")
    end_date = models.DateTimeField(help_text="Enter End Date")

    def clean(self):
        # Custom validation for application_deadline field
        if self.application_deadline <= timezone.now():
            raise ValidationError("Application deadline must be in the future.")

    def is_application_closed(self):
        """Check if the application deadline has passed."""
        return self.application_deadline < timezone.now()
    
    def is_past_event(self):
        if self.end_date <timezone.now():
            return True
        else:
            return False


    def __str__(self):
        return f"{self.event_id}"

class DonateBlood(models.Model):
    donate_blood_id = models.AutoField(primary_key=True)
    future_event_id = models.ForeignKey(FutureEvent, on_delete=models.CASCADE)
    potential_donor_id = models.ForeignKey(PotentialDonor, on_delete=models.CASCADE)
    ticket_number=models.CharField(max_length=255,unique=True,help_text=" Enter Valid Ticket Number")

    def __str__(self):
        return self.ticket_number
    
class PastEvent(models.Model):
    past_event_id = models.AutoField(primary_key=True)
    future_event_id = models.ForeignKey(FutureEvent, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.future_event_id)
    
    def clean(self):
        if self.future_event_id.start_date >= timezone.now():
            raise ValidationError("The start date of the corresponding FutureEvent must be in the past.")
    
class DonationHistory(models.Model):
    donation_history_id = models.AutoField(primary_key=True)
    past_event_id = models.ForeignKey(PastEvent, on_delete=models.CASCADE)
    potential_donor_id=models.ForeignKey(PotentialDonor,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.past_event_id
