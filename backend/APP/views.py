from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Newuser
from django.contrib.auth.decorators import login_required
import face_recognition
import cv2, numpy
import os
from django.contrib.auth.models import auth
from .models import Register
from functools import wraps

# Create your views here.


def Home(request):
    return render(request, 'APP/index.html')



def register(request):

    return render(request, 'APP/signup.html')



def insertdata(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        conpass = request.POST['password2']
        u = Register(username=uname, email=email, password=password, confirm_password=conpass)

        u.save()
        return redirect('my_login')
    
    else:
        messages.error(request, "Invalid data")
        return redirect('register')

    



def my_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Register.objects.get(username=username)
            print("Retrieved user:", user)  # Debugging statement
            print("Input password:", password)  # Debugging statement
            print("User password:", user.password)

            if user.password == password:
                return render(request, 'APP/dashboard.html')
            else:
                return render(request, 'APP/login.html', {'error_message': 'Invalid username or password'})
            
        except Register.DoesNotExist:
            messages.error(request, "User Doesnot Exist")
            return render(request, 'APP/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'APP/login.html')    





@login_required(login_url='my_login')
def dashboard(request):
    return render(request, 'APP/dashboard.html')





def user_logout(request):

    auth.logout(request)

    return redirect("Home")


def user(request):
    return render(request, 'APP/user.html')



def detect_face(request):
    
    images_folder = os.path.join(os.path.dirname(__file__), 'Faces')

    
    known_faces = []
    known_face_encodings = []

    
    for filename in os.listdir(images_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            
            image_path = os.path.join(images_folder, filename)
            face_image = face_recognition.load_image_file(image_path)

            
            face_encoding = face_recognition.face_encodings(face_image)[0]

            
            known_faces.append(filename)  
            known_face_encodings.append(face_encoding)

    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return HttpResponse("Unable to open camera")

    ret, frame = cap.read()

    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    
    print("Shape of rgb_frame:", rgb_frame.shape)
    print("Type of rgb_frame:", type(rgb_frame))

    
    face_locations = face_recognition.face_locations(rgb_frame)
    
    
    print("Detected face locations:", face_locations)

    
    for face_location in face_locations:
        
        top, right, bottom, left = face_location
        face_encodings = face_recognition.face_encodings(rgb_frame, [face_location])

        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            
            if True in matches:
                return redirect('cardscan')
            else:
                # messages.error(request, "Unauthorized user. Authentication Failed")
                return render(request, 'APP/error.html')

    return HttpResponse("<h1>Face Not Matched<h1>")

    cap.release()


def error(request):
    return render(request, 'APP/error.html')
# @login_required(login_url='user')
def scan_card(request):
    messages.error(request, "Face Successfully Recognized")
    return render(request, 'APP/card.html')


def adduser(request):
    return render(request, 'APP/adduser.html')
    

    

def deleteuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("Post")
        user = get_object_or_404(Newuser, email=email)
        print("user")
        image_filename = user.image.name
        print(image_filename)
        faces_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Faces')
        image_path = os.path.join(faces_folder_path, image_filename)
        if os.path.exists(image_path):
            print("removed")
            os.remove(image_path)

        user.delete()
        print("Deleted")

        return render(request, 'APP/dashboard.html')  
    else:
        return render(request, 'APP/deleteuser.html')


def insertuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        image = request.FILES['image']
        
        faces_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Faces')
        print(faces_folder_path)
        # Save the image to the 'Faces' folder
        fs = FileSystemStorage(location= faces_folder_path)  # Specify the absolute path to the 'Faces' folder
        filename = fs.save(image.name, image)

        # Save the user details to the database
        user = Newuser(username=username, email=email, image=filename)
        user.save()
        
        return render(request, 'APP/dashboard.html')  # Redirect to a success page
    else:
        messages.error(request, "Invalid data")
        return render(request, 'adduser.html') 



def is_card_scanner_available(request):
    scanner_path = '/dev/card_scanner'
    if os.path.exists(scanner_path):
        return redirect('scancard')  
    else:
        return HttpResponse("<h1>Please connect the scanner</h1>")



def scan_card_details():
    try:
        card_scanner = is_valid_card()  
        card_scanner.start_scan()  
        card_number = card_scanner.get_card_number()  
        card_scanner.stop_scan()  
        return card_number  
    except Exception as e:
        print("Error while scanning card:", e)
        return None  

def is_valid_card(card_number):
    valid_card_numbers = ['1234567890123456', '9876543210987654']
    
    if card_number in valid_card_numbers:
        return True  
    else:
        return False
