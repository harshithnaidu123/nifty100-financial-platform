from django.urls import path

from . import views

urlpatterns = [

path(
    'revenue-forecast/',
    views.revenue_forecast,
    name='revenue_forecast'
),

path(
    'portfolio-builder/',
    views.portfolio_builder,
    name='portfolio_builder'
),

path(
    'sector-analytics/',
    views.sector_analytics,
    name='sector_analytics'
),

path(
    'company-scorecard/',
    views.company_scorecard,
    name='company_scorecard'
),

path(
    'company-deep-dive/',
    views.company_deep_dive,
    name='company_deep_dive'
),

path(
    'executive-dashboard/',
    views.executive_dashboard,
    name='executive_dashboard'
),

path(
    'ai-investment-advisor/',
    views.ai_investment_advisor,
    name='ai_investment_advisor'
),

path(
    'earnings-call-analyzer/',
    views.earnings_call_analyzer,
    name='earnings_call_analyzer'
),

path(
    'risk-intelligence/',
    views.risk_intelligence,
    name='risk_intelligence'
),

path(
    'news-sentiment/',
    views.news_sentiment,
    name='news_sentiment'
),

path(
    'stock-ranking/',
    views.stock_ranking,
    name='stock_ranking'
),

path(
    'financial-copilot/',
    views.financial_copilot,
    name='financial_copilot'
),

path(
    'portfolio-optimizer/',
    views.portfolio_optimizer,
    name='portfolio_optimizer'
),

path(
    'price-prediction/',
    views.price_prediction,
    name='price_prediction'
),

path(
    'financial-analyst/',
    views.financial_analyst,
    name='financial_analyst'
),

]
