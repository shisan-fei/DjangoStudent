from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Students
import pymysql
import hashlib
from hashlib import md5
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        userName = request.POST.get('Username')
        passWord = request.POST.get('Password')
        passWord_md5=pw_md5(passWord)
        user_tup = (userName, passWord)         #页面输入的用户名，密码
        user_tup_md = (userName, passWord_md5)  #页面输入的用户名，和加密后的密码
        #sql = 'select * from t_user'
        sql1 = '''select * from t_user where username='{}' and password='{}' '''.format(userName,passWord_md5)
        sql2 = '''select * from t_user where username='{}' and password='{}' '''.format(userName,passWord)
        user1=model(sql1)
        user2=model(sql2)
        if user1 == None: #初始密码没有加密 执行sql1后返回none
            print(user2)
            if user2 == None:
                return render(request, 'login.html', {'msg': "用户名或密码错误!!"})
            else:
                if user_tup == user2[0]:   #直接判断执行sql2得到的原始用户名和密码与页面输入的是否相同
                    return show_students(request,student_id=userName)
                else:
                    return render(request, 'login.html', {'msg': "用户名或密码错误!!"})
        elif user_tup_md == user1[0]:  #user[0]就是数据库中用户名和加密的密码
            return show_students(request,student_id=userName)
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
    passWord_md5=pw_md5(passWord)
    #SQL语句
    sql1 = 'select * from t_user'
    all_users=model(sql1)  #执行SQL语句,查询到所有的用户存储到all_users中
    i = 0
    if all_users == None:
        all_users = ()
    while i < len(all_users):
        if userName in all_users[i]:
            print(all_users[i])
            ##表示该账号存在
            has_regiter = 1
        i += 1
    print(has_regiter)
    if has_regiter == 0:
        #return HttpResponse('该账号不存在,请联系管理员添加用户')
        return render(request, 'update.html', {'msg': "该账号不存在,请联系管理员添加用户!!"})
    else:
        sql2 = '''update t_user set password = '{}' where username = '{}' '''.format(passWord_md5,userName)
        model(sql2)
        #return HttpResponse('修改成功')
        return render(request, 'update_success.html')

def show_students(request,student_id):
    """
    显示学生列表
    :param request:
    :return:
    """
    student_list = Students.objects.filter(student_id=student_id)
    print(student_list)
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

#封装一个密码加密函数
def pw_md5(password):
    m=hashlib.md5()  #实例化MD5对象
    new_pw=password.encode()  #不能直接对字符串加密，要先把字符串转换成bytes类型
    m.update(new_pw)  #加密
    return m.hexdigest() 


#print(MD5('123'))
#print(md5('111'))
