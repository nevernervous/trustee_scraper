from datetime import datetime, date
from dateutil import relativedelta
from itertools import islice

from django.db import models
from django.utils.html import format_html

import mortgage


class PropertyRecord(models.Model):
    trustee = models.CharField(max_length=100, verbose_name='Trustee')
    trustee_file_num = models.CharField(max_length=200, verbose_name='Trustee: File#')
    trustee_sale_datetime = models.DateTimeField(verbose_name='Trustee: Sale DateTime', null=True)
    trustee_continued_datetime = models.DateTimeField(verbose_name='Trustee: Continued DateTime', null=True, blank=True)
    trustee_address = models.CharField(max_length=500, verbose_name='Trustee: Address', null=True)
    trustee_county = models.CharField(max_length=50, verbose_name='Trustee: County', null=True)
    trustee_city = models.CharField(max_length=50, verbose_name='Trustee: City', null=True)
    trustee_zipcode = models.CharField(max_length=50, verbose_name='Trustee: Zip', null=True)
    trustee_state = models.CharField(max_length=50, verbose_name='Trustee: State', null=True)
    trustee_bid = models.FloatField(verbose_name='Trustee: Opening Bid', null=True, blank=True)
    trustee_bid_datetime = models.DateTimeField(verbose_name='Trustee: Opening Bid DateTime', null=True, blank=True)

    is_zillow_processed = models.BooleanField(verbose_name='ZP?', default=False)
    google_maps_address = models.CharField(max_length=500, verbose_name='Address', null=True)
    google_maps_zipcode = models.CharField(max_length=10, verbose_name='ZipCode', null=True)

    zpid = models.PositiveIntegerField(verbose_name='Zillow Property Id', unique=True, null=True, blank=True)

    link_homedetails = models.URLField(max_length=500, verbose_name='Home Details URL', blank=True, null=True)
    link_chartdata = models.URLField(max_length=500, verbose_name='Chart Data URL', blank=True, null=True)
    link_mapthishome = models.URLField(max_length=500, verbose_name='Map This Home URL', blank=True, null=True)
    link_similarsales = models.URLField(max_length=500, verbose_name='Similar Sales URL', blank=True, null=True)

    street_address = models.CharField(max_length=500, verbose_name='Street Address', blank=True, null=True)
    zipcode = models.CharField(max_length=50, verbose_name='ZipCode', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='City', blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name='State', blank=True, null=True)
    county = models.CharField(max_length=100, verbose_name='County', blank=True, null=True)
    latitude = models.CharField(max_length=100, verbose_name='Latitude', blank=True, null=True)
    longitude = models.CharField(max_length=100, verbose_name='Longitude', blank=True, null=True)

    zestimate_amount = models.FloatField(verbose_name='Zestimate', blank=True, null=True)
    zestimate_lastupdated = models.DateField(verbose_name='Last Updated', blank=True, null=True)
    zestimate_30daychange = models.FloatField(verbose_name='30 Day Change', blank=True, null=True)
    zestimate_valuationrangehigh = models.FloatField(verbose_name='Valuation Range High', blank=True, null=True)
    zestimate_valuationrangelow = models.FloatField(verbose_name='Valuation Range Low', blank=True, null=True)
    zestimate_percentile = models.FloatField(verbose_name='Percentile', blank=True, null=True)

    rzestimate_amount = models.FloatField(verbose_name='Rent Zestimate', blank=True, null=True)
    rzestimate_lastupdated = models.DateField(verbose_name='Last Updated', blank=True, null=True)
    rzestimate_30daychange = models.FloatField(verbose_name='30 Day Change', blank=True, null=True)
    rzestimate_valuationrangehigh = models.FloatField(verbose_name='Valuation Range High', blank=True, null=True)
    rzestimate_valuationrangelow = models.FloatField(verbose_name='Valuation Range Low', blank=True, null=True)

    localrealestate_zillowhomevalueindex = models.FloatField(verbose_name='Zillow Home Value Index', blank=True, null=True)
    localrealestate_overviewurl = models.URLField(max_length=500, verbose_name='Region Overview URL', blank=True, null=True)
    localrealestate_forsalebyownerurl = models.URLField(max_length=500, verbose_name='For Sale By Owner URL', blank=True, null=True)
    localrealestate_forsalehomesurl = models.URLField(max_length=500, verbose_name='For Sale Homes URL', blank=True, null=True)

    fipscounty = models.CharField(max_length=10, verbose_name='FIPS County Code', blank=True, null=True)
    usecode = models.CharField(max_length=100, verbose_name='Property Type', blank=True, null=True)
    taxassessment_year = models.PositiveIntegerField(verbose_name='Tax Assessment Year', blank=True, null=True)
    taxassessment_amount = models.FloatField(verbose_name='Tax Assessment Amount', blank=True, null=True)
    yearbuilt = models.PositiveIntegerField(verbose_name='Year Built', blank=True, null=True)
    lotsize_sqft = models.FloatField(verbose_name='Lot Size (sqft)', blank=True, null=True)
    finished_sqft = models.FloatField(verbose_name='Finished (sqft)', blank=True, null=True)
    bathrooms = models.FloatField(verbose_name='Bath', blank=True, null=True)
    bedrooms = models.FloatField(verbose_name='Bed', blank=True, null=True)
    totalrooms = models.FloatField(verbose_name='Total Rooms', blank=True, null=True)
    lastsold_date = models.DateField(verbose_name='Last Sold Date', blank=True, null=True)
    lastsold_price = models.FloatField(verbose_name='Last Sold Price', blank=True, null=True)

    pageviewcount_currentmonth = models.IntegerField(verbose_name='Page View Count: Current Month', null=True, blank=True)
    pageviewcount_total = models.IntegerField(verbose_name='Page View Count: Total', null=True, blank=True)

    posting_status = models.CharField(max_length=500, verbose_name='Posting Status', null=True, blank=True)
    posting_agentname = models.CharField(max_length=500, verbose_name='Posting Agent Name', null=True, blank=True)
    posting_agentprofileurl = models.URLField(max_length=500, verbose_name='Posting Agent Profile Url', null=True, blank=True)
    posting_brokerage = models.CharField(max_length=500, verbose_name='Posting Brokerage', null=True, blank=True)
    posting_type = models.CharField(max_length=500, verbose_name='Posting Type', null=True, blank=True)
    posting_lastupdateddate = models.DateTimeField(verbose_name='Posting Last Updated Date', null=True, blank=True)
    posting_externalurl = models.URLField(max_length=500, verbose_name='Posting External Url', null=True, blank=True)
    posting_mls = models.CharField(max_length=100, verbose_name='Posting MLS', null=True, blank=True)

    price = models.FloatField(verbose_name='Price', null=True, blank=True)

    photogallery_url = models.URLField(max_length=500, verbose_name='Photo Gallery URL', null=True, blank=True)
    image_url1 = models.URLField(max_length=500, verbose_name='Image URL 1', null=True, blank=True)
    image_url2 = models.URLField(max_length=500, verbose_name='Image URL 2', null=True, blank=True)
    image_url3 = models.URLField(max_length=500, verbose_name='Image URL 3', null=True, blank=True)
    image_url4 = models.URLField(max_length=500, verbose_name='Image URL 4', null=True, blank=True)
    image_url5 = models.URLField(max_length=500, verbose_name='Image URL 5', null=True, blank=True)

    year_updated = models.IntegerField(verbose_name='Year Updated', null=True , blank=True)
    num_floors = models.IntegerField(verbose_name='Number of Floors', null=True, blank=True)
    basement = models.CharField(max_length=500, verbose_name='Basement', null=True, blank=True)
    roof = models.CharField(max_length=500, verbose_name='Roof', null=True, blank=True)
    view = models.CharField(max_length=500, verbose_name='View', null=True, blank=True)
    parking_type = models.CharField(max_length=500, verbose_name='Parking Type', null=True, blank=True)
    heating_sources = models.CharField(max_length=500, verbose_name='Heating Sources', null=True, blank=True)
    heating_system = models.CharField(max_length=500, verbose_name='Heating System', null=True, blank=True)
    rooms_desc = models.CharField(max_length=500, verbose_name='Rooms Description', null=True, blank=True)
    covered_parking_spaces = models.IntegerField(verbose_name='Covered Parking Spaces', null=True, blank=True)
    cooling_system = models.CharField(max_length=500, verbose_name='Cooling System', null=True, blank=True)
    appliances = models.CharField(max_length=500, verbose_name='Appliances', null=True, blank=True)
    floor_covering = models.CharField(max_length=500, verbose_name='Floor Covering', null=True, blank=True)
    architecture = models.CharField(max_length=500, verbose_name='Architecture', null=True, blank=True)
    floor_number = models.IntegerField(verbose_name='Floor Number', null=True, blank=True)
    num_units = models.IntegerField(verbose_name='Num of Units', null=True, blank=True)
    home_description = models.TextField(verbose_name='Home Description', null=True, blank=True)
    what_owner_loves = models.TextField(verbose_name='What Owner Loves', null=True, blank=True)
    neighborhood = models.CharField(max_length=500, verbose_name='Neighborhood', null=True, blank=True)
    school_district = models.CharField(max_length=500, verbose_name='School District', null=True, blank=True)
    elementary_school = models.CharField(max_length=500, verbose_name='Elementary School', null=True, blank=True)
    middle_school = models.CharField(max_length=500, verbose_name='Middle School', null=True, blank=True)
    high_school = models.CharField(max_length=500, verbose_name='High School', null=True, blank=True)

    mortgage_30yearfixed_rate = models.FloatField(verbose_name='30 Yr Fixed Rate', null=True, blank=True)
    mortgage_30yearfixed_pi = models.FloatField(verbose_name='30 Yr Fixed Monthly P&I', null=True, blank=True)
    mortgage_15yearfixed_rate = models.FloatField(verbose_name='15 Yr Fixed Rate', null=True, blank=True)
    mortgage_15yearfixed_pi = models.FloatField(verbose_name='15 Yr Fixed Monthly P&I', null=True, blank=True)
    mortgage_51arm_rate = models.FloatField(verbose_name='5/1 ARM Rate', null=True, blank=True)
    mortgage_51arm_pi = models.FloatField(verbose_name='5/1 ARM Monthly P&I', null=True, blank=True)
    mortgage_downpayment = models.FloatField(verbose_name='Down Payment', null=True, blank=True)
    mortgage_monthlypropertytaxes = models.FloatField(verbose_name='Monthly Property Taxes', null=True, blank=True)
    mortgage_monthlyinsurance = models.FloatField(verbose_name='Monthly Insurance', null=True, blank=True)
    is_mortgage_being_saved = models.BooleanField(default=False)

    poz = models.FloatField(verbose_name='POZ', null=True, blank=True)
    polsp = models.FloatField(verbose_name='POLSP', null=True, blank=True)
    an_ren = models.FloatField(verbose_name='AN REN', null=True, blank=True)
    tm_ti = models.FloatField(verbose_name='TM&TI', null=True, blank=True)
    tm_ti_an = models.FloatField(verbose_name='TM&TI - An', null=True, blank=True)
    net = models.FloatField(verbose_name='NET', null=True, blank=True)
    cap = models.FloatField(verbose_name='CAP', null=True, blank=True)
    projected_open = models.FloatField(verbose_name='Projected Open', null=True, blank=True)
    projected_equity = models.FloatField(verbose_name='Projected Equity', null=True, blank=True)
    projected_diff = models.FloatField(verbose_name='PDiff', null=True, blank=True)

    googlemaps_api_comments = models.CharField(max_length=500, verbose_name='Google Maps API Result', null=True, blank=True)
    property1_return_code = models.PositiveIntegerField(verbose_name='Property1: Return Code', null=True, blank=True)
    property1_comments = models.CharField(max_length=500, verbose_name='Property Search API Result', null=True, blank=True)
    property2_return_code = models.PositiveIntegerField(verbose_name='Property2: Return Code', null=True, blank=True)
    property2_comments = models.CharField(max_length=500, verbose_name='Property Details API Result', null=True, blank=True)
    mortgage_return_code = models.PositiveIntegerField(verbose_name='Mortgage: Return Code', null=True, blank=True)
    mortgage_comments = models.CharField(max_length=500, verbose_name='Mortgage API Result', null=True, blank=True)

    created_date = models.DateTimeField(verbose_name='Record Created At', auto_now_add=True, null=True)
    updated_date = models.DateTimeField(verbose_name='Record Updated At', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __repr__(self):
        return '{}: {}'.format(self.trustee, self.trustee_file_num)

    def __unicode__(self):
        return self.__repr__()

    def __str__(self):
        return self.__repr__()

    def save(self, *args, **kwargs):
        if self.trustee_bid_datetime is None and self.trustee_bid is not None:
            self.trustee_bid_datetime = datetime.now()
        if self.is_mortgage_being_saved is True:
            self.calculate_mortgage_parameters()
        return super(PropertyRecord, self).save(*args, **kwargs)

    def calculate_mortgage_parameters(self):
        m30 = mortgage.Mortgage(interest=0.04, amount=self.zestimate_amount * 0.8, months=360)
        self.mortgage_30yearfixed_rate = round(m30.rate() * 100, 2)
        self.mortgage_30yearfixed_pi = round(m30.monthly_payment(), 2)

        m15 = mortgage.Mortgage(interest=0.035, amount=self.zestimate_amount * 0.8, months=180)
        self.mortgage_15yearfixed_rate = round(m15.rate() * 100, 2)
        self.mortgage_15yearfixed_pi = round(m15.monthly_payment(), 2)

        m51arm = mortgage.Mortgage(interest=0.039, amount=self.zestimate_amount * 0.8, months=180)
        self.mortgage_51arm_rate = round(m51arm.rate() * 100, 2)
        self.mortgage_51arm_pi = round(m51arm.monthly_payment(), 2)

        self.mortgage_downpayment = round(self.zestimate_amount * 0.2, 2)
        self.mortgage_monthlypropertytaxes = round(self.zestimate_amount * 0.0125 / 12, 2)
        self.mortgage_monthlyinsurance = 83

        if self.trustee_bid is not None and self.zestimate_amount is not None:
            self.poz = round(self.trustee_bid * 100 / self.zestimate_amount, 2)

        if self.trustee_bid is not None and self.lastsold_price is not None:
            self.polsp = round(self.trustee_bid * 100 / self.lastsold_price, 2)

        if self.rzestimate_amount is not None:
            self.an_ren = round(self.rzestimate_amount * 0.8 * 12, 2)

        if self.mortgage_30yearfixed_pi is not None and self.mortgage_monthlypropertytaxes is not None and self.mortgage_monthlyinsurance is not None:
            self.tm_ti = round(float(self.mortgage_30yearfixed_pi) + float(self.mortgage_monthlypropertytaxes) + float(self.mortgage_monthlyinsurance), 2)
            self.tm_ti_an = round(self.tm_ti * 12, 2)

        if self.an_ren is not None and self.tm_ti_an is not None:
            self.net = round(self.an_ren - self.tm_ti_an, 2)

        if self.net is not None and self.trustee_bid is not None:
            self.cap = round(self.net * 100 / self.trustee_bid, 2)

        self.projected_open = self.calculate_projected_open()

        if self.lastsold_price is None or self.lastsold_date is None or self.zestimate_amount is None or self.projected_open is None:
            self.projected_equity = None
        else:
            self.projected_equity = self.zestimate_amount - self.projected_open

        if self.poz is not None and self.polsp is not None:
            self.projected_diff = self.poz - self.polsp

    def get_doz(self):
        if self.posting_lastupdateddate is not None:
            return (datetime.now() - self.posting_lastupdateddate).days
        else:
            return None
    get_doz.short_description = 'DOZ'

    def format_zestimate_amount(self):
        return '${:,.0f}'.format(self.zestimate_amount) if self.zestimate_amount is not None else ''
    format_zestimate_amount.short_description = 'Zestimate'
    format_zestimate_amount.admin_order_field = 'zestimate_amount'

    def format_rzestimate_amount(self):
        return '${:,.0f}'.format(self.rzestimate_amount) if self.rzestimate_amount is not None else ''
    format_rzestimate_amount.short_description = 'Rent Zestimate'
    format_rzestimate_amount.admin_order_field = 'rzestimate_amount'

    def format_lastsold_price(self):
        return '${:,.0f}'.format(self.lastsold_price) if self.lastsold_price is not None else ''
    format_lastsold_price.short_description = 'Last Sold Price'
    format_lastsold_price.admin_order_field = 'lastsold_price'

    def format_trustee_bid(self):
        return '${:,.0f}'.format(self.trustee_bid) if self.trustee_bid is not None else ''
    format_trustee_bid.short_description = 'Trustee: Opening Bid'
    format_trustee_bid.admin_order_field = 'trustee_bid'

    def format_an_ren(self):
        return '${:,.0f}'.format(self.an_ren) if self.an_ren is not None else ''
    format_an_ren.short_description = 'AN REN'
    format_an_ren.admin_order_field = 'an_ren'

    def format_net(self):
        return '${:,.0f}'.format(self.net) if self.net is not None else ''
    format_net.short_description = 'NET'
    format_net.admin_order_field = 'net'

    def format_finished_sqft(self):
        return '{:,.0f}'.format(self.finished_sqft) if self.finished_sqft is not None else ''
    format_finished_sqft.short_description = 'Finished (sqft)'
    format_finished_sqft.admin_order_field = 'finished_sqft'

    def format_lotsize_sqft(self):
        return '{:,.0f}'.format(self.lotsize_sqft) if self.lotsize_sqft is not None else ''
    format_lotsize_sqft.short_description = 'Lotsize (sqft)'
    format_lotsize_sqft.admin_order_field = 'lotsize_sqft'

    def format_poz(self):
        return '{:,.2f}%'.format(self.poz) if self.poz is not None else ''
    format_poz.short_description = 'POZ'
    format_poz.admin_order_field = 'poz'

    def format_polsp(self):
        return '{:,.2f}%'.format(self.polsp) if self.polsp is not None else ''
    format_polsp.short_description = 'POLSP'
    format_polsp.admin_order_field = 'polsp'

    def format_projected_open(self):
        return '${:,.2f}'.format(self.projected_open) if self.projected_open is not None else None
    format_projected_open.short_description = 'Projected Open'
    format_projected_open.admin_order_field = 'projected_open'

    def format_projected_equity(self):
        return '${:,.2f}'.format(self.projected_equity) if self.projected_equity is not None else None
    format_projected_equity.short_description = 'Projected Equity'
    format_projected_equity.admin_order_field = 'projected_equity'

    def format_projected_diff(self):
        return '{:,.2f}%'.format(self.projected_diff) if self.projected_diff is not None else None
    format_projected_diff.short_description = 'PDiff'
    format_projected_diff.admin_order_field = 'projected_diff'

    def calculate_projected_open(self):
        if self.lastsold_price is None:
            return None
        m = mortgage.Mortgage(interest=0.06, amount=self.lastsold_price, months=360)
        td = datetime.today()
        datediff = relativedelta.relativedelta(date(year=td.year - 1, month=1, day=1), self.lastsold_date)
        num_payments_made = datediff.years * 12 + datediff.months
        try:
            p15 = sum(month[0] for month in islice(m.monthly_payment_schedule(), num_payments_made))
            projected_open = mortgage.dollar(m.amount()) - p15
            return float(projected_open)
        except ValueError:
            return None

    # def get_balance(self):
    #     if self.lastsold_price is None or self.lastsold_date is None:
    #         return ''
    #     balance = self.calculate_projected_open()
    #     return '${:,.2f}'.format(balance) if balance is not None else None
    # get_balance.short_description = 'Projected Open'

    # def get_projected_equity(self):
    #     if self.lastsold_price is None or self.lastsold_date is None or self.zestimate_amount is None:
    #         return None
    #     balance = self.calculate_projected_open()
    #     if balance is None:
    #         return None
    #     projected_equity = self.zestimate_amount - float(balance)
    #     return '${:,.2f}'.format(projected_equity)
    # get_projected_equity.short_description = 'Projected Equity'

    # def get_pdiff(self):
    #     if self.poz is None or self.polsp is None:
    #         return ''
    #     return '{:.2f}'.format(self.poz - self.polsp)
    # get_pdiff.short_description = 'PDiff'

    def format_link_homedetails_url(self):
        if self.link_homedetails is None:
            return None
        return format_html('<a target="_blank" href="{}">{}</a>', self.link_homedetails, 'Z_Home')
    format_link_homedetails_url.short_description = 'Home Details URL'

    def format_link_similarsales_url(self):
        if self.link_similarsales is None:
            return None
        return format_html('<a target="_blank" href="{}">{}</a>', self.link_similarsales, 'Z_Sales')
    format_link_similarsales_url.short_description = 'Similar Sales URL'
