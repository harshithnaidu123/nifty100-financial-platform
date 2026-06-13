from django.urls import path

from .views import (CompanyDetailAPIView, FactAnalysisViewSet,
                    FactBalanceSheetViewSet, FactCashFlowViewSet,
                    FactMlScoresViewSet, FactProfitLossViewSet,
                    company_dashboard, company_list, company_search,
                    compare_companies, home, sector_dashboard, smart_screener)

urlpatterns = [

    path(
    'dashboard/<str:symbol>/',
    company_dashboard,
    name='company_dashboard'
),

path(
    'screener/',
    smart_screener,
    name='smart_screener'
),

path(
    'sector-dashboard/',
    sector_dashboard,
    name='sector_dashboard'
),

path(
    'search/',
    company_search,
    name='company_search'
),

path(
    'compare/',
    compare_companies,
    name='compare_companies'
),

    # Home Page
    path('', home, name='home'),

    # Company List Page
    path(
        'companies/',
        company_list,
        name='companies'
    ),

    # APIs

    path(
        'analysis/',
        FactAnalysisViewSet.as_view({'get': 'list'})
    ),

    path(
        'balance-sheet/',
        FactBalanceSheetViewSet.as_view({'get': 'list'})
    ),

    path(
        'balance-sheet/<str:symbol>/',
        FactBalanceSheetViewSet.as_view({'get': 'list'})
    ),

    path(
        'cashflow/',
        FactCashFlowViewSet.as_view({'get': 'list'})
    ),

    path(
        'cashflow/<str:symbol>/',
        FactCashFlowViewSet.as_view({'get': 'list'})
    ),

    path(
        'profit-loss/',
        FactProfitLossViewSet.as_view({'get': 'list'})
    ),

    path(
        'profit-loss/<str:symbol>/',
        FactProfitLossViewSet.as_view({'get': 'list'})
    ),

    path(
        'ml-scores/',
        FactMlScoresViewSet.as_view({'get': 'list'})
    ),

    path(
        'company/<str:symbol>/',
        CompanyDetailAPIView.as_view()
    ),
]