from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .ml_model import detect_content
from .sms import send_sms_alert

@api_view(["POST"])
def register_user(request):
    # serializer = UserSerializer(data=request.data)
    UserData = request.data()
    return Response(UserData['username'])
    # if serializer.is_valid():
    #     data = serializer.validated_data
    #     if User.objects(username=data['username']):
    #         return Response({"message": "Username already exists"}, status=409)
    #     User(**data).save()
    #     return Response({"message": "User registered"})
    # return Response(serializer.errors, status=400)

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
