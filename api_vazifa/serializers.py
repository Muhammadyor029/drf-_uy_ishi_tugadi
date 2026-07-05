from rest_framework import serializers

class ObHavoSerializer(serializers.Serializer):
    harorat = serializers.FloatField() 
    namlik = serializers.IntegerField()   
    shamol = serializers.FloatField()   
    vaqt = serializers.CharField()       