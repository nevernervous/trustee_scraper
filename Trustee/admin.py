from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from suit.widgets import SuitSplitDateTimeWidget, AutosizedTextarea

from Trustee import models


class PropertyRecordForm(ModelForm):
    class Meta:
        widgets = {
            'trustee_sale_datetime': SuitSplitDateTimeWidget,
            'posting_lastupdateddate': SuitSplitDateTimeWidget,
            # 'created_date': SuitSplitDateTimeWidget,
            'apistatus': SuitSplitDateTimeWidget,
            'home_description': AutosizedTextarea(attrs={'class': 'span10'})
        }


class PresetsFilter(admin.SimpleListFilter):
    title = _('Preset Filters')
    parameter_name = 'preset'

    def lookups(self, request, model_admin):
        return (
            ('proj_eq_high_low', _('1. Projected Equity (sorted highest to lowest)')),
            ('opening_bid_low_high', _('2. Opening Bid (sorted lowest to highest)')),
            ('poz_low_high', _('3. POZ (sorted lowest to highest)')),
            ('polsp_low_high', _('4. POLSP (sorted lowest to highest)')),
            ('st_louis_proj_open_low_high', _('5. St Louis County (sorted by lowest Projected Open)')),
            ('cole_boone_proj_open_low_high', _('6. Cole & Boone County (sorted by lowest Projected Open)')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'proj_eq_high_low':
            return queryset.filter(projected_equity__isnull=False).order_by('-projected_equity')
        elif self.value() == 'opening_bid_low_high':
            return queryset.filter(trustee_bid__isnull=False).order_by('trustee_bid')
        elif self.value() == 'poz_low_high':
            return queryset.filter(poz__isnull=False).order_by('poz')
        elif self.value() == 'polsp_low_high':
            return queryset.filter(polsp__isnull=False).order_by('polsp')
        elif self.value() == 'st_louis_proj_open_low_high':
            return queryset.filter(
                Q(projected_open__isnull=False) &
                (
                    (Q(trustee_county__icontains='st') & Q(trustee_county__icontains='louis')) |
                    (Q(county__icontains='st') & Q(county__icontains='louis'))
                )
            ).order_by('projected_open')
        elif self.value() == 'cole_boone_proj_open_low_high':
            return queryset.filter(
                Q(projected_open__isnull=False) &
                (
                    Q(trustee_county__icontains='cole') | Q(trustee_county__icontains='boone') |
                    Q(county__icontains='cole') | Q(county__icontains='boone')
                )
            ).order_by('projected_open')


@admin.register(models.PropertyRecord)
class PropertyRecordAdmin(admin.ModelAdmin):
    form = PropertyRecordForm
    list_display = ['trustee', 'trustee_sale_datetime', 'trustee_address', 'trustee_state', 'format_trustee_bid', 'trustee_bid_datetime',
                    'format_poz', 'format_polsp', 'format_projected_diff', 'format_projected_open',
                    'format_projected_equity', 'format_lastsold_price', 'lastsold_date', 'format_zestimate_amount',
                    'format_link_homedetails_url', 'format_link_similarsales_url', 'usecode', 'yearbuilt',
                    'format_finished_sqft', 'format_lotsize_sqft', 'bedrooms', 'bathrooms', 'get_doz',
                    'format_rzestimate_amount', 'format_an_ren', 'format_net', 'pageviewcount_currentmonth',
                    'pageviewcount_total', 'googlemaps_api_comments', 'is_zillow_processed', 'property1_comments',
                    'property2_comments', 'created_date', 'updated_date', 'trustee_file_num',
                    'trustee_county']
    list_display_links = ['trustee_file_num', 'trustee_address']

    list_filter = ['trustee', 'trustee_state', 'trustee_county', 'is_zillow_processed', PresetsFilter]

    search_fields = []
    date_hierarchy = 'trustee_sale_datetime'
    empty_value_display = ''
    readonly_fields = ['created_date', 'updated_date']

    fieldsets = (
        ('Trustee Data', {
            'fields': ['trustee_file_num', 'trustee_sale_datetime', 'trustee_address', 'trustee_city',
                       'trustee_zipcode', ('trustee_county', 'trustee_state'), ('trustee_bid', 'trustee_bid_datetime'),
                       'trustee_continued_datetime'],
            # 'description': 'Data fetched from Kozney',
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Google Maps', {
            'fields': [('google_maps_address', 'google_maps_zipcode')],
            # 'description': 'Data fetched from Google Maps',
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Zillow Process', {
            'fields': [('is_zillow_processed', 'zpid')],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Zillow Address', {
            'fields': [('street_address', 'zipcode'), ('city', 'state'), ('county', 'fipscounty'),
                       ('latitude', 'longitude')],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Zestimate', {
            'fields': [('zestimate_amount', 'zestimate_30daychange'), 'zestimate_lastupdated',
                       ('zestimate_valuationrangehigh', 'zestimate_valuationrangelow'), 'zestimate_percentile'],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Rent Zestimate', {
            'fields': [('rzestimate_amount', 'rzestimate_30daychange'), 'rzestimate_lastupdated',
                       ('rzestimate_valuationrangehigh', 'rzestimate_valuationrangelow')],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Zillow Taxes and Prices', {
            'fields': [('lastsold_date', 'lastsold_price'), ('taxassessment_year', 'taxassessment_amount'), 'price'],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Zillow Home Facts', {
            'fields': ['usecode', 'yearbuilt',
                       ('lotsize_sqft', 'finished_sqft'), ('bathrooms', 'bedrooms'), 'totalrooms',
                       'num_floors', ('basement', 'roof'), 'view',  ('parking_type', 'covered_parking_spaces'),
                       ('heating_sources', 'heating_system'), 'cooling_system', 'appliances', 'floor_covering',
                       'architecture', 'floor_number', 'num_units', 'home_description', 'rooms_desc',
                       'what_owner_loves', 'neighborhood', 'school_district',
                       'elementary_school', 'middle_school', 'high_school'],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Zillow Posting Details', {
            'fields': [('pageviewcount_currentmonth', 'pageviewcount_total'), 'posting_status',
                       'posting_agentname', 'posting_agentprofileurl', 'posting_brokerage', 'posting_type',
                       'posting_lastupdateddate', 'posting_externalurl', 'posting_mls', 'year_updated'],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Zillow Images and URLs', {
            'fields': ['link_homedetails', 'link_chartdata', 'link_mapthishome', 'link_similarsales',
                       'photogallery_url', 'image_url1', 'image_url2', 'image_url3', 'image_url4', 'image_url5',
                       'posting_externalurl', 'posting_agentprofileurl'],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Local Real Estate', {
            'fields': ['localrealestate_zillowhomevalueindex', 'localrealestate_overviewurl',
                       'localrealestate_forsalebyownerurl', 'localrealestate_forsalehomesurl'],
            'classes': ('collapse', 'suit-tab suit-tab-general',),
        }),
        ('Mortgage Data', {
            'fields': [ 'zestimate_amount', ('mortgage_30yearfixed_rate', 'mortgage_30yearfixed_pi'),
                       ('mortgage_15yearfixed_rate', 'mortgage_15yearfixed_pi'),
                       ('mortgage_51arm_rate', 'mortgage_51arm_pi'),
                       ('mortgage_monthlypropertytaxes', 'mortgage_monthlyinsurance'), 'mortgage_downpayment'],
            'classes': ('suit-tab suit-tab-mortgage',),
        }),
        ('Mortgage Calculated Data', {
            'fields': ['poz', 'polsp', 'an_ren', 'tm_ti', 'tm_ti_an', 'net', 'cap'],
            'classes': ('suit-tab suit-tab-mortgage',),
        }),
        ('API Status', {
            'fields': ['googlemaps_api_comments', 'property1_comments', 'property2_comments',
                       'created_date', 'updated_date'],
            'classes': ('suit-tab suit-tab-apistatus',),
        }),
    )
    suit_form_tabs = (('general', 'General'), ('mortgage', 'Mortgage'), ('apistatus', 'API Status'))
