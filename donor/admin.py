from django.contrib import admin

from . models import PotentialDonor,County,Constituency,Ward,BloodGroup,DonationCenter,Event,FutureEvent,PastEvent,DonationHistory,DonateBlood

models_to_register = [ PotentialDonor,County,Constituency,Ward,BloodGroup,DonationCenter,Event,FutureEvent,PastEvent,DonationHistory,DonateBlood]

for model in models_to_register:
    admin.site.register(model)
