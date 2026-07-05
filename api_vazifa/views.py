import requests 
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .serializers import ObHavoSerializer 

TASHQI_FOYDALANUVCHILAR_URL = 'https://jsonplaceholder.typicode.com/users' 

class UserListAPIView(APIView): 
    
    def get(self, request): 
        try:
            
            sorov = requests.get(TASHQI_FOYDALANUVCHILAR_URL, timeout=10) 
            sorov.raise_for_status() 
        except requests.RequestException: 
           
            return Response(
                {'error': "Tashqi API bilan bog'lanib bo'lmadi"}, 
                status=status.HTTP_502_BAD_GATEWAY 
            )
        
        tashqi_malumotlar = sorov.json()
        
        natija = [ 
            { 
                'id': foydalanuvchi['id'],
                'full_name': foydalanuvchi['name'], 
                'username': foydalanuvchi['username'], 
                'email': foydalanuvchi['email'], 
                'city': foydalanuvchi['address']['city'],     
                'company': foydalanuvchi['company']['name'],  
            } 
            for foydalanuvchi in tashqi_malumotlar 
        ]
        
        
        shahar = request.query_params.get('city') 
        if shahar: 
            natija = [u for u in natija if u['city'].lower() == shahar.lower()]
            
        return Response(natija, status=status.HTTP_200_OK) 


class UserDetailAPIView(APIView):
    
    def get(self, request, user_id):
        url = f"{TASHQI_FOYDALANUVCHILAR_URL}/{user_id}"
        try:
            sorov = requests.get(url, timeout=10) 
            
            
            if sorov.status_code == 404 or sorov.json() == {}: 
                return Response(
                    {'error': "Foydalanuvchi topilmadi"}, 
                    status=status.HTTP_404_NOT_FOUND 
                )
            sorov.raise_for_status() 
        except requests.RequestException: 
            return Response(
                {'error': "Tashqi API bilan bog'lanib bo'lmadi"},
                status=status.HTTP_502_BAD_GATEWAY
            )
            
        foydalanuvchi = sorov.json()
        
        
        toza_malumot = {
            'id': foydalanuvchi['id'],
            'full_name': foydalanuvchi['name'],
            'username': foydalanuvchi['username'],
            'email': foydalanuvchi['email'],
            'city': foydalanuvchi['address']['city'],
            'company': foydalanuvchi['company']['name'],
        }
        return Response(toza_malumot, status=status.HTTP_200_OK)


class ObHavoAPIView(APIView): 
    
    def get(self, request): 
        lat = request.query_params.get('lat') 
        lon = request.query_params.get('lon') 
        
        
        if not lat or not lon: 
            return Response( 
                {'xato': "lat va lon parametrlari kerak"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        ob_havo_url = 'https://api.open-meteo.com/v1/forecast' 
        parametrlar = { 
            'latitude': lat, 
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m', 
            'timezone': 'auto', 
        } 
        
        try:
            sorov = requests.get(ob_havo_url, params=parametrlar, timeout=10) 
            sorov.raise_for_status() 
        except requests.RequestException: 
            return Response(
                {'xato': "Ob-havo API ishlamadi"}, 
                status=status.HTTP_502_BAD_GATEWAY 
            )
            
        joriy_ob_havo = sorov.json().get('current', {}) 
        
        
        o_zbekcha_malumot = { 
            'harorat': joriy_ob_havo.get('temperature_2m'), 
            'namlik': joriy_ob_havo.get('relative_humidity_2m'), 
            'shamol': joriy_ob_havo.get('wind_speed_10m'), 
            'vaqt': joriy_ob_havo.get('time'), 
        } 
        
        
        serializer = ObHavoSerializer(data=o_zbekcha_malumot) 
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)