# Generated by Django 5.0.2 on 2024-04-12 11:25

import django.db.models.deletion
import donor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BloodGroup',
            fields=[
                ('blood_group_id', models.AutoField(primary_key=True, serialize=False)),
                ('blood_group_type', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], help_text='Choose a valid blood group type', max_length=3, validators=[donor.models.validate_blood_group_type])),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('county_id', models.AutoField(primary_key=True, serialize=False)),
                ('county_name', models.CharField(help_text='Enter a valid County Name', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DonationCenter',
            fields=[
                ('donation_center_id', models.AutoField(primary_key=True, serialize=False)),
                ('donation_center_name', models.CharField(help_text='Enter a valid Donation Center Name', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_description', models.CharField(help_text='Enter a valid Event Description', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('constituency_id', models.AutoField(primary_key=True, serialize=False)),
                ('constituency_name', models.CharField(help_text='Enter a valid Constituency Name', max_length=255, unique=True)),
                ('county_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.county')),
            ],
        ),
        migrations.CreateModel(
            name='FutureEvent',
            fields=[
                ('future_event_id', models.AutoField(primary_key=True, serialize=False)),
                ('application_deadline', models.DateTimeField(help_text='Enter application deadline')),
                ('start_date', models.DateTimeField(help_text='Enter Start Date')),
                ('end_date', models.DateTimeField(help_text='Enter End Date')),
                ('donation_center_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.donationcenter')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.event')),
            ],
        ),
        migrations.CreateModel(
            name='PastEvent',
            fields=[
                ('past_event_id', models.AutoField(primary_key=True, serialize=False)),
                ('future_event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.futureevent')),
            ],
        ),
        migrations.CreateModel(
            name='PotentialDonor',
            fields=[
                ('potential_donor_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(help_text='Enter a valid first name', max_length=200)),
                ('last_name', models.CharField(help_text='Enter a valid last name', max_length=200)),
                ('email_address', models.EmailField(help_text='Enter a valid email address', max_length=200, unique=True)),
                ('password_hash', models.CharField(help_text='Enter a valid password', max_length=128)),
                ('blood_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.bloodgroup')),
            ],
        ),
        migrations.CreateModel(
            name='DonationHistory',
            fields=[
                ('donation_history_id', models.AutoField(primary_key=True, serialize=False)),
                ('past_event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.pastevent')),
                ('potential_donor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.potentialdonor')),
            ],
        ),
        migrations.CreateModel(
            name='DonateBlood',
            fields=[
                ('donate_blood_id', models.AutoField(primary_key=True, serialize=False)),
                ('ticket_number', models.CharField(help_text=' Enter Valid Ticket Number', max_length=255, unique=True)),
                ('future_event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.futureevent')),
                ('potential_donor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.potentialdonor')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('ward_id', models.AutoField(primary_key=True, serialize=False)),
                ('ward_name', models.CharField(help_text='Enter a valid Ward Name', max_length=255, unique=True)),
                ('constituency_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.constituency')),
            ],
        ),
        migrations.AddField(
            model_name='donationcenter',
            name='ward_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.ward'),
        ),
    ]
