from rest_framework.views import APIView
from rest_framework import response,status,permissions

# Services goes here
from services.services import translate_services

class TranslateServicesView(APIView):

    target_language = 'id'
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request):
        try:
            input_text = request.data['text']

            return response.Response(data={
                'target':self.target_language,
                'text':translate_services(input_text,self.target_language)
            },status=status.HTTP_200_OK)
        
        except KeyError:
            return response.responses(data={
                "status":"fail",
                "message":"Fail To Fetch Data, There should be 'text' in POST request"
            },status=status.HTTP_400_BAD_REQUEST)