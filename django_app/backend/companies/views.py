import json

from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (FactAnalysis, FactBalanceSheet, FactCashFlow,
                     FactMlScores, FactProfitLoss)
from .serializers import (FactAnalysisSerializer, FactBalanceSheetSerializer,
                          FactCashFlowSerializer, FactMlScoresSerializer,
                          FactProfitLossSerializer)

# -----------------------------
# HOME PAGE VIEW
# -----------------------------

def home(request):

    companies = FactMlScores.objects.order_by(
        '-overall_score'
    )[:10]

    return render(
        request,
        'home.html',
        {
            'companies': companies
        }
    )

# -----------------------------
# API VIEWSETS
# -----------------------------
class FactAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FactAnalysis.objects.all()
    serializer_class = FactAnalysisSerializer


class FactBalanceSheetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FactBalanceSheetSerializer

    def get_queryset(self):
        queryset = FactBalanceSheet.objects.all()

        symbol = self.kwargs.get("symbol")
        if symbol:
            queryset = queryset.filter(symbol=symbol)

        return queryset


class FactCashFlowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FactCashFlowSerializer

    def get_queryset(self):
        queryset = FactCashFlow.objects.all()

        symbol = self.kwargs.get("symbol")
        if symbol:
            queryset = queryset.filter(symbol=symbol)

        return queryset


class FactProfitLossViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FactProfitLossSerializer

    def get_queryset(self):
        queryset = FactProfitLoss.objects.all()

        symbol = self.kwargs.get("symbol")
        if symbol:
            queryset = queryset.filter(symbol=symbol)

        return queryset


class FactMlScoresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FactMlScores.objects.all()
    serializer_class = FactMlScoresSerializer


# -----------------------------
# COMPANY DETAIL API
# -----------------------------
class CompanyDetailAPIView(APIView):

    def get(self, request, symbol):

        analysis = FactAnalysis.objects.filter(
            company_id=symbol
        ).values()

        balance_sheet = FactBalanceSheet.objects.filter(
            symbol=symbol
        ).values()

        cashflow = FactCashFlow.objects.filter(
            symbol=symbol
        ).values()

        profit_loss = FactProfitLoss.objects.filter(
            symbol=symbol
        ).values()

        ml_score = FactMlScores.objects.filter(
            symbol=symbol
        ).values()

        data = {
            "symbol": symbol,
            "analysis": list(analysis),
            "balance_sheet": list(balance_sheet),
            "cashflow": list(cashflow),
            "profit_loss": list(profit_loss),
            "ml_score": list(ml_score)
        }

        return Response(data)


def company_list(request):

    companies = FactAnalysis.objects.all()

    return render(
        request,
        'company_list.html',
        {
            'companies': companies
        }
    )
def company_dashboard(request, symbol):

    company = FactMlScores.objects.filter(
        symbol=symbol
    ).first()

    risk_level = "HIGH"

    if company:

        if company.overall_score >= 80:
            risk_level = "LOW"

        elif company.overall_score >= 50:
            risk_level = "MEDIUM"

        else:
            risk_level = "HIGH"

    profit_data = FactProfitLoss.objects.filter(
        symbol=symbol
    ).order_by('year')

    balance_data = FactBalanceSheet.objects.filter(
        symbol=symbol
    ).order_by('year')

    cashflow_data = FactCashFlow.objects.filter(
        symbol=symbol
    ).order_by('year')

    revenue_years = []
    revenue_values = []
    profit_values = []

    for row in profit_data:
        revenue_years.append(row.year)
        revenue_values.append(row.sales)
        profit_values.append(row.net_profit)

    context = {

        'company': company,
        'risk_level': risk_level,

        'profit_data': profit_data,
        'balance_data': balance_data,
        'cashflow_data': cashflow_data,

        'revenue_years': json.dumps(revenue_years),
        'revenue_values': json.dumps(revenue_values),
        'profit_values': json.dumps(profit_values),

        'balance_years': json.dumps(
            [x.year for x in balance_data]
        ),

        'borrowings': json.dumps(
            [x.borrowings for x in balance_data]
        ),

        'assets': json.dumps(
            [x.total_assets for x in balance_data]
        ),

        'cash_years': json.dumps(
            [x.year for x in cashflow_data]
        ),

        'free_cash_flow': json.dumps(
            [x.free_cash_flow for x in cashflow_data]
        ),

        'operating_cash': json.dumps(
            [x.operating_activity for x in cashflow_data]
        ),
    }

    return render(
        request,
        'company_dashboard.html',
        context
    )


def compare_companies(request):

    companies = FactMlScores.objects.all()

    company_a = None
    company_b = None

    balance_a = None
    balance_b = None

    symbol_a = request.GET.get("company_a")
    symbol_b = request.GET.get("company_b")

    if symbol_a:

        company_a = FactMlScores.objects.filter(
            symbol=symbol_a
        ).first()

        balance_a = FactBalanceSheet.objects.filter(
            symbol=symbol_a
        ).first()

    if symbol_b:

        company_b = FactMlScores.objects.filter(
            symbol=symbol_b
        ).first()

        balance_b = FactBalanceSheet.objects.filter(
            symbol=symbol_b
        ).first()

    return render(
        request,
        "compare_companies.html",
        {
            "companies": companies,

            "company_a": company_a,
            "company_b": company_b,

            "balance_a": balance_a,
            "balance_b": balance_b,

            "symbol_a": symbol_a,
            "symbol_b": symbol_b,
        }
    )

def smart_screener(request):

    companies = FactMlScores.objects.all().order_by(
        '-overall_score'
    )

    return render(
        request,
        'smart_screener.html',
        {
            'companies': companies
        }
    )

def sector_dashboard(request):

    companies = FactMlScores.objects.all().order_by(
        '-overall_score'
    )[:10]

    return render(
        request,
        'sector_dashboard.html',
        {
            'companies': companies
        }
    )

def company_search(request):

    symbol = request.GET.get(
        'symbol',
        ''
    ).strip().upper()

    if FactMlScores.objects.filter(
        symbol=symbol
    ).exists():

        return redirect(
            f'/api/dashboard/{symbol}/'
        )

    return redirect(
        '/api/companies/'
    )