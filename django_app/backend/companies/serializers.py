from rest_framework import serializers

from .models import (FactAnalysis, FactBalanceSheet, FactCashFlow,
                     FactMlScores, FactProfitLoss)


class FactAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactAnalysis
        fields = '__all__'


class FactBalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactBalanceSheet
        fields = '__all__'


class FactCashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCashFlow
        fields = '__all__'


class FactProfitLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactProfitLoss
        fields = '__all__'


class FactMlScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactMlScores
        fields = '__all__'