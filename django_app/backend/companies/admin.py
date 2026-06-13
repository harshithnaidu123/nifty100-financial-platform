from django.contrib import admin

from .models import (FactAnalysis, FactBalanceSheet, FactCashFlow,
                     FactMlScores, FactProfitLoss)

admin.site.register(FactAnalysis)
admin.site.register(FactMlScores)

# Don't register these tables because they have no primary key
# admin.site.register(FactBalanceSheet)
# admin.site.register(FactCashFlow)
# admin.site.register(FactProfitLoss)