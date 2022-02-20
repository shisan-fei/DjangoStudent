from django.shortcuts import render,redirect
from .models import Students
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('pwd')
        # print(user, pwd)
        if user == 'root' and pwd == '123':
            # 登录成功
            #return render(request, 'show_students.html')
            return redirect('/student/show_students/')
        else:
            # 登陆失败
            return render(request, 'login.html', {'msg': "用户名或密码错误!!"})

def show_students(request):
    """
    显示学生列表
    :param request:
    :return:
    """
    student_list = Students.objects.all()
    return render(request, 'show_students.html', {'student_list': student_list})