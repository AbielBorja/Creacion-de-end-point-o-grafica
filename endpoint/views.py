from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ast
import sqlite3
from .models import usuario
from random import randrange


def getInfo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print("Entre en Post")
            username = request.POST['username']
            password = request.POST['password']
            firstName = request.POST['first_name']
            user = authenticate(request, username=username, password=password, firstName=firstName)
            print(user)
            if user is not None:
                print("entre en User not none")
                getInfoUsuario = usuario.objects.filter(usuario=username)
                print(getInfoUsuario[0].toJson())
                getInfoUsuario = getInfoUsuario[0].toJson()
                return render(request, 'endpoint/get.html', {'datos':getInfoUsuario})
            else:
                messages.error(request, ('No user Found'))
                return redirect('GET')  
        else:
            form = RegisterUserForm()
            return render(request, 'endpoint/get.html')
    else:
        return redirect('login')

def signUpView(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print("Estoy dentro de form")
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            userSqliteRegister = usuario()
            userSqliteRegister.progresoPorcentual = randrange(100)
            userSqliteRegister.minutosJugados = randrange(200)
            userSqliteRegister.usuario = username
            userSqliteRegister.password = password
            userSqliteRegister.score = randrange(10000)
            userSqliteRegister.save()
            print("GUarde datos supuestamente")
            messages.success(request, ('Registration seccessful'))
            return redirect('APIs_pages') 
    else:
        form = RegisterUserForm()
        return render(request, 'endpoint/signup.html', {'form':form})

def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('APIs_pages')
        else:
            messages.error(request, ('Bad login'))
            return redirect('login')   
    else:
        return render(request, 'endpoint/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out'))
    return redirect('login')

def private_page(request):
    if request.user.is_authenticated:
        mydb = sqlite3.connect("db.sqlite3")
        curr = mydb.cursor()

        query_progress = '''SELECT usuario, progresoPorcentual, score FROM endpoint_usuario ORDER BY progresoPorcentual DESC'''
        rows1 = curr.execute(query_progress)
        data_progress = []

        for x in rows1:
            data_progress.append([  x[0], x[1],x[2]])

        query_instrument = '''SELECT nombre, tiempoMinutos FROM instrumento'''
        rows2 = curr.execute(query_instrument)
        data_intrument = [['Instruments', 'Minutes']]

        for x in rows2:
            data_intrument.append([x[0],x[1]])

        query_pregunta = '''SELECT mensaje FROM pregunta'''
        query_quiz = '''SELECT correcto, incorrecto FROM quiz'''

        row3 = curr.execute(query_pregunta)
        curr2 = mydb.cursor()
        row4 = curr2.execute(query_quiz)

        data_question = [['Question', 'Correct', 'Incorrect']]

        for x in row3:
            data_quiz = []
            data_quiz.append(x[0])
            
            for i in row4:
                data_quiz.append(i[0])
                data_quiz.append(i[1])
                break
            data_question.append(data_quiz)

        return render(request, 'endpoint/APIs.html', {'values':data_progress, 'values2':data_intrument, 'data_quiz':data_question})
    else:
        return redirect('login')

