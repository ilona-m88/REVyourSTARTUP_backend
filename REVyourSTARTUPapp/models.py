from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

#TODO: create appropriate models for rev form applicable to the json interface

class MainForm(models.Model):
    # This model will work as the 'Hub' for attaching all the different forms onto
    # by a specific user's id as a primary key. All of the seperate forms will be a foriegn key
    
    main_form_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    form_name = models.CharField(blank=True, null=True, max_length=255)
    rev_form = models.ForeignKey('RevForm', on_delete=models.CASCADE, blank=True, null=True)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.form_name)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(MainForm, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'main_form'


class RevForm(models.Model):
    # The main table for the revform
    
    # Refer to dataStructure_RevForm.json for visualization of table columns
    rev_form_id = models.AutoField(primary_key=True)

    # "valuationParameters"
    last_year_total_revenue = models.IntegerField()
    amount_needed = models.IntegerField()
    
    # "hit3YearGoals"
    three_years_effective_interest = models.IntegerField()
    five_years_effective_interest = models.IntegerField()
    seven_years_effective_interest = models.IntegerField()
    
    revenue_multiplier = models.IntegerField()
    exit_amount = models.IntegerField()
    
    # "exitYears"
    year0_percentage = models.IntegerField()
    year0_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year0_force_to = models.IntegerField()
    year1_percentage = models.IntegerField()
    year1_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year1_force_to = models.IntegerField()
    year2_percentage = models.IntegerField()
    year2_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year2_force_to = models.IntegerField()
    year3_percentage = models.IntegerField()
    year3_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year3_force_to = models.IntegerField()
    year4_percentage = models.IntegerField()
    year4_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year4_force_to = models.IntegerField()
    year5_percentage = models.IntegerField()
    year5_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    year5_force_to = models.IntegerField()

    equity_percentage = models.IntegerField()
    year3_company_worth = models.DecimalField(max_digits=12, decimal_places=2)
    exit_revenue_multiplier = models.IntegerField()
    revenue_needed_year3 = models.DecimalField(max_digits=12, decimal_places=2)
    growth_projection = models.IntegerField()
    # end "valuationParameters"

    # "realityCheck1"
    total_market = models.DecimalField(max_digits=12, decimal_places=2)
    captured_at_year5 = models.IntegerField()

    # "customerSegmentsYear3"
    #customer_segments_year3 = models.ForeignKey('RevFormRowsIndex', models.DO_NOTHING, related_name='customer_segment_year3')

    # "customerSegmentsYear2"
    #customer_segments_year2 = models.ForeignKey('RevFormRowsIndex', models.DO_NOTHING, related_name='customer_segment_year2')

    # "customerSegmentsYear1"
    #customer_segments_year1 = models.ForeignKey('RevFormRowsIndex', models.DO_NOTHING, related_name='customer_segment_year1')

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(RevForm, self).save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'rev_form'


class RevFormRowsIndex(models.Model):
    # This table acts as an index for referring to the different customer segments, the field
    # 'revform_rows_name' should be named accordingly. This will provide a single point of indexing
    # all of the different row entries, which are not known at the time of revform creation.

    revform_rows_index_id = models.AutoField(primary_key=True)
    rev_form= models.ForeignKey(RevForm, on_delete=models.CASCADE, blank=True, null=True, related_name='rev_form')

    # This name can correlate to "customerSegmentsYear3" or "customerSegmentsYear1" etc...
    revform_rows_name = models.CharField(max_length=255)

    row_count = models.IntegerField()

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.revform_rows_name)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(RevFormRowsIndex, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'rev_form_rows_index'


class RevFormRows(models.Model):
    # This table is referred to by the index, and will carry the information of applicable to
    # individual rows in the revform

    revform_rows_id = models.AutoField(primary_key=True)
    revform_rows_index = models.ForeignKey(RevFormRowsIndex, on_delete=models.CASCADE, blank=True, null=True)

    segment_name = models.CharField(max_length=255)
    avg_revenue_per_customer = models.DecimalField(max_digits=12, decimal_places=2)
    quick_modeling_percentage = models.IntegerField()
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    customers = models.IntegerField()
    your_percentage = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)

    created = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.segment_name)

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(RevFormRows, self).save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'revform_rows'