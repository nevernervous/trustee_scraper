# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-15 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trustee', models.CharField(max_length=100, verbose_name=b'Trustee')),
                ('trustee_file_num', models.CharField(max_length=200, verbose_name=b'Trustee: File#')),
                ('trustee_sale_datetime', models.DateTimeField(null=True, verbose_name=b'Trustee: Sale DateTime')),
                ('trustee_address', models.CharField(max_length=500, null=True, verbose_name=b'Trustee: Address')),
                ('trustee_county', models.CharField(max_length=50, null=True, verbose_name=b'Trustee: County')),
                ('trustee_state', models.CharField(max_length=50, null=True, verbose_name=b'Trustee: State')),
                ('trustee_bid', models.FloatField(blank=True, null=True, verbose_name=b'Trustee: Opening Bid')),
                ('is_zillow_processed', models.BooleanField(default=False, verbose_name=b'Is Zillow Processed?')),
                ('google_maps_address', models.CharField(max_length=500, null=True, verbose_name=b'Address')),
                ('google_maps_zipcode', models.CharField(max_length=10, null=True, verbose_name=b'ZipCode')),
                ('zpid', models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name=b'Zillow Property Id')),
                ('link_homedetails', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Home Details URL')),
                ('link_chartdata', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Chart Data URL')),
                ('link_mapthishome', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Map This Home URL')),
                ('link_similarsales', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Similar Sales URL')),
                ('street_address', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Street Address')),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'ZipCode')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'City')),
                ('state', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'State')),
                ('county', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'County')),
                ('latitude', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Latitude')),
                ('longitude', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Longitude')),
                ('zestimate_amount', models.FloatField(blank=True, null=True, verbose_name=b'Zestimate')),
                ('zestimate_lastupdated', models.DateField(blank=True, null=True, verbose_name=b'Last Updated')),
                ('zestimate_30daychange', models.FloatField(blank=True, null=True, verbose_name=b'30 Day Change')),
                ('zestimate_valuationrangehigh', models.FloatField(blank=True, null=True, verbose_name=b'Valuation Range High')),
                ('zestimate_valuationrangelow', models.FloatField(blank=True, null=True, verbose_name=b'Valuation Range Low')),
                ('zestimate_percentile', models.FloatField(blank=True, null=True, verbose_name=b'Percentile')),
                ('rzestimate_amount', models.FloatField(blank=True, null=True, verbose_name=b'Rent Zestimate')),
                ('rzestimate_lastupdated', models.DateField(blank=True, null=True, verbose_name=b'Last Updated')),
                ('rzestimate_30daychange', models.FloatField(blank=True, null=True, verbose_name=b'30 Day Change')),
                ('rzestimate_valuationrangehigh', models.FloatField(blank=True, null=True, verbose_name=b'Valuation Range High')),
                ('rzestimate_valuationrangelow', models.FloatField(blank=True, null=True, verbose_name=b'Valuation Range Low')),
                ('localrealestate_zillowhomevalueindex', models.FloatField(blank=True, null=True, verbose_name=b'Zillow Home Value Index')),
                ('localrealestate_overviewurl', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Region Overview URL')),
                ('localrealestate_forsalebyownerurl', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'For Sale By Owner URL')),
                ('localrealestate_forsalehomesurl', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'For Sale Homes URL')),
                ('fipscounty', models.CharField(blank=True, max_length=10, null=True, verbose_name=b'FIPS County Code')),
                ('usecode', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Property Type')),
                ('taxassessment_year', models.PositiveIntegerField(blank=True, null=True, verbose_name=b'Tax Assessment Year')),
                ('taxassessment_amount', models.FloatField(blank=True, null=True, verbose_name=b'Tax Assessment Amount')),
                ('yearbuilt', models.PositiveIntegerField(blank=True, null=True, verbose_name=b'Year Built')),
                ('lotsize_sqft', models.FloatField(blank=True, null=True, verbose_name=b'Lot Size (sqft)')),
                ('finished_sqft', models.FloatField(blank=True, null=True, verbose_name=b'Finished (sqft)')),
                ('bathrooms', models.FloatField(blank=True, null=True, verbose_name=b'Bathrooms')),
                ('bedrooms', models.FloatField(blank=True, null=True, verbose_name=b'Bedrooms')),
                ('totalrooms', models.FloatField(blank=True, null=True, verbose_name=b'Total Rooms')),
                ('lastsold_date', models.DateField(blank=True, null=True, verbose_name=b'Last Sold Date')),
                ('lastsold_price', models.FloatField(blank=True, null=True, verbose_name=b'Last Sold Price')),
                ('pageviewcount_currentmonth', models.IntegerField(blank=True, null=True, verbose_name=b'Page View Count: Current Month')),
                ('pageviewcount_total', models.IntegerField(blank=True, null=True, verbose_name=b'Page View Count: Total')),
                ('posting_status', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Posting Status')),
                ('posting_agentname', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Posting Agent Name')),
                ('posting_agentprofileurl', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Posting Agent Profile Url')),
                ('posting_brokerage', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Posting Brokerage')),
                ('posting_type', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Posting Type')),
                ('posting_lastupdateddate', models.DateTimeField(blank=True, null=True, verbose_name=b'Posting Last Updated Date')),
                ('posting_externalurl', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Posting External Url')),
                ('posting_mls', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Posting MLS')),
                ('price', models.FloatField(blank=True, null=True, verbose_name=b'Price')),
                ('photogallery_url', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Photo Gallery URL')),
                ('image_url1', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Image URL 1')),
                ('image_url2', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Image URL 2')),
                ('image_url3', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Image URL 3')),
                ('image_url4', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Image URL 4')),
                ('image_url5', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Image URL 5')),
                ('year_updated', models.IntegerField(blank=True, null=True, verbose_name=b'Year Updated')),
                ('num_floors', models.IntegerField(blank=True, null=True, verbose_name=b'Number of Floors')),
                ('basement', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Basement')),
                ('roof', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Roof')),
                ('view', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'View')),
                ('parking_type', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Parking Type')),
                ('heating_sources', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Heating Sources')),
                ('heating_system', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Heating System')),
                ('rooms_desc', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Rooms Description')),
                ('covered_parking_spaces', models.IntegerField(blank=True, null=True, verbose_name=b'Covered Parking Spaces')),
                ('cooling_system', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Cooling System')),
                ('appliances', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Appliances')),
                ('floor_covering', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Floor Covering')),
                ('architecture', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Architecture')),
                ('floor_number', models.IntegerField(blank=True, null=True, verbose_name=b'Floor Number')),
                ('num_units', models.IntegerField(blank=True, null=True, verbose_name=b'Num of Units')),
                ('home_description', models.TextField(blank=True, null=True, verbose_name=b'Home Description')),
                ('what_owner_loves', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'What Owner Loves')),
                ('neighborhood', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Neighborhood')),
                ('school_district', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'School District')),
                ('elementary_school', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Elementary School')),
                ('middle_school', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Middle School')),
                ('high_school', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'High School')),
                ('mortgage_30yearfixed_rate', models.FloatField(blank=True, null=True, verbose_name=b'30 Yr Fixed Rate')),
                ('mortgage_30yearfixed_pi', models.FloatField(blank=True, null=True, verbose_name=b'30 Yr Fixed Monthly P&I')),
                ('mortgage_15yearfixed_rate', models.FloatField(blank=True, null=True, verbose_name=b'15 Yr Fixed Rate')),
                ('mortgage_15yearfixed_pi', models.FloatField(blank=True, null=True, verbose_name=b'15 Yr Fixed Monthly P&I')),
                ('mortgage_51arm_rate', models.FloatField(blank=True, null=True, verbose_name=b'5/1 ARM Rate')),
                ('mortgage_51arm_pi', models.FloatField(blank=True, null=True, verbose_name=b'5/1 ARM Monthly P&I')),
                ('mortgage_downpayment', models.FloatField(blank=True, null=True, verbose_name=b'Down Payment')),
                ('mortgage_monthlypropertytaxes', models.FloatField(blank=True, null=True, verbose_name=b'Monthly Property Taxes')),
                ('mortgage_monthlyinsurance', models.FloatField(blank=True, null=True, verbose_name=b'Monthly Insurance')),
                ('is_mortgage_being_saved', models.BooleanField(default=False)),
                ('poz', models.FloatField(blank=True, null=True, verbose_name=b'POZ')),
                ('polsp', models.FloatField(blank=True, null=True, verbose_name=b'POLSP')),
                ('an_ren', models.FloatField(blank=True, null=True, verbose_name=b'AN REN')),
                ('tm_ti', models.FloatField(blank=True, null=True, verbose_name=b'TM&TI')),
                ('tm_ti_an', models.FloatField(blank=True, null=True, verbose_name=b'TM&TI - An')),
                ('net', models.FloatField(blank=True, null=True, verbose_name=b'NET')),
                ('cap', models.FloatField(blank=True, null=True, verbose_name=b'CAP')),
                ('googlemaps_api_comments', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Google Maps API Result')),
                ('property1_return_code', models.PositiveIntegerField(blank=True, null=True, verbose_name=b'Property1: Return Code')),
                ('property1_comments', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Property Search API Result')),
                ('property2_return_code', models.PositiveIntegerField(blank=True, null=True, verbose_name=b'Property2: Return Code')),
                ('property2_comments', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Property Details API Result')),
                ('mortgage_return_code', models.PositiveIntegerField(blank=True, null=True, verbose_name=b'Mortgage: Return Code')),
                ('mortgage_comments', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'Mortgage API Result')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name=b'Record Created At')),
                ('updated_date', models.DateTimeField(auto_now=True, null=True, verbose_name=b'Record Updated At')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
    ]
