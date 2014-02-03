from django.contrib import admin

from external_data_sync.admin import BaseDataSourceAdmin
from .models import DataSource


class DataSourceAdmin(BaseDataSourceAdmin):
    pass


admin.site.register(DataSource, DataSourceAdmin)
