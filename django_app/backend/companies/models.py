# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DimCompany(models.Model):
    symbol = models.TextField(blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_company'


class DimHealthLabel(models.Model):
    label_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_health_label'


class DimSector(models.Model):
    sector_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_sector'


class DimYear(models.Model):
    year_id = models.BigIntegerField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_year'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FactAnalysis(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.TextField(blank=True, null=True)
    compounded_sales_growth = models.TextField(blank=True, null=True)
    compounded_profit_growth = models.TextField(blank=True, null=True)
    stock_price_cagr = models.TextField(blank=True, null=True)
    roe = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_analysis'


class FactBalanceSheet(models.Model):
    symbol = models.TextField(primary_key=True)

    year = models.TextField(blank=True, null=True)
    equity_capital = models.FloatField(blank=True, null=True)
    reserves = models.BigIntegerField(blank=True, null=True)
    borrowings = models.BigIntegerField(blank=True, null=True)
    total_assets = models.BigIntegerField(blank=True, null=True)
    debt_to_equity = models.BigIntegerField(blank=True, null=True)
    equity_ratio = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_balance_sheet'


class FactCashFlow(models.Model):
    symbol = models.TextField(primary_key=True)

    year = models.TextField(blank=True, null=True)
    operating_activity = models.BigIntegerField(blank=True, null=True)
    investing_activity = models.BigIntegerField(blank=True, null=True)
    financing_activity = models.BigIntegerField(blank=True, null=True)
    free_cash_flow = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_cash_flow'


class FactMlScores(models.Model):
    symbol = models.TextField(primary_key=True)

    overall_score = models.FloatField(blank=True, null=True)
    health_label = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_ml_scores'


class FactProfitLoss(models.Model):
    symbol = models.TextField(primary_key=True)

    year = models.TextField(blank=True, null=True)
    sales = models.BigIntegerField(blank=True, null=True)
    net_profit = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_profit_loss'


class FactProsCons(models.Model):
    symbol = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    is_pro = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_pros_cons'
