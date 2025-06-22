from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

from rest_framework import status
from bson import ObjectId
from .models import Report
@api_view(["POST"])
def register_user(request):
   
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        userdata = serializer.validated_data

        if User.objects.filter(username=userdata['username']).first():
            return Response({"message": "Username already exists" }, status=status.HTTP_409_CONFLICT)

        
        user = serializer.save()
        Report.objects.create(secret_key=user.secret_key)
        return Response({"message": "User registered successfully" ,"Data" : UserSerializer(user).data }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def login_user(request):
    data = request.data
    try:
        user = User.objects.get(username=data["username"], password=data["password"])
        return Response({"unique_id": str(user.id)})
    except User.DoesNotExist:
        return Response({"message": "Invalid credentials"}, status=401)
    


@api_view(["POST"])
def check_text(request):
    unique_id = request.data.get("sct_id")
    text = request.data.get("text")

    user = User.objects(id=ObjectId(unique_id)).first()
    if not user:
        return Response({"message": "User not found"}, status=404)

    
  
    return Response({"alert": False})

@api_view(["POST"])
def message(request):
    msg = request.data.get('text')
    if not msg :
        return Response({"message" : "message Not recive" } , status=400)
    return Response({"message" : msg})
