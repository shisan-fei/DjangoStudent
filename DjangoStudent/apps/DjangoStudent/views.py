from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Students
import pymysql
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        userName = request.POST.get('Username')
        passWord = request.POST.get('Password')
        user_tup = (userName, passWord)
        sql = 'select * from t_user'
        all_users=model(sql)
        sql2 = '''select * from t_students where student_id={}'''.format(userName)
        user_info=model(sql2)
        has_user = 0
        i = 0
        while i < len(all_users):
            if user_tup == all_users[i]:
                has_user = 1
            i += 1
        if has_user == 1:
            return redirect('/student/show_students/')
        else:
            # 登陆失败
            return render(request, 'login.html', {'msg': "用户名或密码错误!!"})

#修改密码
def update_pwd(request):
    return render(request,'update.html')


#定义一个函数，用来保存注册的数据
def save(request):
    has_regiter = 0   #用来记录当前账号是否已存在，0：不存在 1：已存在
    a = request.GET   #获取get()请求
    #通过get()请求获取前段提交的数据
    userName = a.get('username')
    passWord = a.get('password')
    #SQL语句
    sql1 = 'select * from t_user'
    all_users=model(sql1)  #执行SQL语句,查询到所有的用户存储到all_users中
    print('这里',all_users)
    print(userName)
    print(len(all_users))
    i = 0
    while i < len(all_users):
        if userName in all_users[i]:
            print(all_users[i])
            ##表示该账号存在
            has_regiter = 1
        i += 1
    print(has_regiter)
    if has_regiter == 0:
        return HttpResponse('该账号不存在,请联系管理员添加用户')
    else:
        sql2 = '''update t_user set password = '{}' where username = '{}' '''.format( passWord,userName)
        model(sql2)
        #return HttpResponse('修改成功')
        return render(request, 'update_success.html')

def show_students(request):
    """
    显示学生列表
    :param request:
    :return:
    """
    student_list = Students.objects.all()
    return render(request, 'show_students.html', {'student_list': student_list})

#封装一个mysql操作
def model(sql):
    try:
        db = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='123456',
                             db='mysite4',
                             charset='utf8mb4',)

        cruose = db.cursor()
        row=cruose.execute(sql)
        db.commit()
        data = cruose.fetchall()
        if data:
            return data
        else:
            return None
    finally:
        db.close()