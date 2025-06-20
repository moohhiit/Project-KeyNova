from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .ml_model import detect_content
from .sms import send_sms_alert
from rest_framework import status

@api_view(["POST"])
def register_user(request):
   
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data

        if User.objects.filter(username=data['username']).first():
            return Response({"message": "Username already exists"}, status=status.HTTP_409_CONFLICT)

        
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def login_user(request):
    data = request.data
    try:
        user = User.objects.get(username=data["username"], password=data["password"])
        return Response({"message": "Login successful", "phone": user.phone})
    except User.DoesNotExist:
        return Response({"message": "Invalid credentials"}, status=401)
    


@api_view(["POST"])
def check_text(request):
    username = request.data.get("username")
    text = request.data.get("text")

    user = User.objects(username=username).first()
    if not user:
        return Response({"message": "User not found"}, status=404)

    detected, details = detect_content(text)
    if detected:
        send_sms_alert(user.phone, details, username)
        return Response({"alert": True, "details": details})
    return Response({"alert": False})
