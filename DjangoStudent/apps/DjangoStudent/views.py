from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Students
import pymysql
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        userName = request.POST.get('username')
        passWord = request.POST.get('pwd')
        user_tup = (userName, passWord)
        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='mysite4')
        cursor = db.cursor()
        sql = 'select * from user'
        cursor.execute(sql)
        all_users = cursor.fetchall()
        cursor.close()
        db.close()
        has_user = 0
        i = 0
        while i < len(all_users):
            if user_tup == all_users[i]:
                print(all_users[0])
                has_user = 1
            i += 1
        if has_user == 1:
            return redirect('/student/show_students/')
        else:
            # 登陆失败
            return render(request, 'login.html', {'msg': "用户名或密码错误!!"})

#注册
def register(request):
    return render(request,'register.html')


#定义一个函数，用来保存注册的数据
def save(request):
    has_regiter = 0   #用来记录当前账号是否已存在，0：不存在 1：已存在
    a = request.GET   #获取get()请求
    #通过get()请求获取前段提交的数据
    userName = a.get('username')
    passWord = a.get('password')
    #连接数据库
    db = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='mysite4',charset='utf8mb4')
    #创建游标
    cursor = db.cursor()
    #SQL语句
    sql1 = 'select * from user'
    #执行SQL语句
    cursor.execute(sql1)
    #查询到所有的用户存储到all_users中
    all_users = cursor.fetchall()
    i = 0
    while i < len(all_users):
        if userName in all_users[i]:
            ##表示该账号已经存在
            has_regiter = 1
        i += 1
    if has_regiter == 0:
        # 将用户名与密码插入到数据库中
        sql2 = '''insert into user(student_id,password) values('{}','{}')'''.format(userName,passWord)
        #cursor.execute(sql2,(userName,passWord))
        cursor.execute(sql2)
        db.commit()
        cursor.close()
        db.close()
        return render(request, 'login.html')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该账号已存在')

def show_students(request):
    """
    显示学生列表
    :param request:
    :return:
    """
    student_list = Students.objects.all()
    return render(request, 'show_students.html', {'student_list': student_list})