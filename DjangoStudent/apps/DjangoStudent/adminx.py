# @Time : 2022/2/10 21:37
# @Author : 王龙飞
# @File : adminx.py
# @Version : 1.0
# @Description : xadmin数据模型,用以设置页面显示和关联数据库字段
from re import A
from site import USER_BASE
from sre_constants import CH_LOCALE
from tkinter import N
import xadmin
import sys,os

#import_excel = True
sys.path.append("..")
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from xadmin import views
from .models import Students,Class,Subjects,User
from xadmin.views.website import LoginView #导入LoginView模块，可以控制登录页面标题

from django.http import HttpResponseRedirect
from xlrd import open_workbook,xldate_as_tuple
from datetime import  datetime

# 主题设置
class BaseSetting(object):
    # 后台的主题功能，xadmin默认是关掉的，所以要打开
    enable_themes = True
    use_bootswatch = True

# 全局设置
class GlobalSetting(object):
    # 设置base_site.html的Title(页头名称)，再页面左上角显示
    site_title = 'slxy-学籍管理系统'
    # 设置base_site.html的Footer(页脚)，再页脚显示
    site_footer = 'slxy-学籍管理系统'
    # 设置菜单折叠
    menu_style = "accordion"

#登录标题显示
class LoginViewAdmin(LoginView):
    title = 'slxy-学籍管理系统'


# Student显示设置,让这些字段可以显示在页面上
class StudentsAdmin(object):
    # 列表中显示的字段
    list_display = ('student_id', 'name', 'sex', 'id_card', 'national','Native_place','Account_type','Date_of_birth', 'enter_date', 'class_name',)

    # 内联复选框(选课系统可以上多选)
    style_fields = {'subjects': 'checkbox-inline', }

    # 搜索(姓名, 班级, 课程),之后再页面中就可以根据字典进行搜索
    search_fields = ('student_id', 'class_name__class_name', 'subjects__name',)

    # 过滤器(按性别)
    list_filter = ('sex',)

    # 导入excel插件
    import_excel = True
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            execl_file = request.FILES.get('excel')
            files = open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            table = files.sheets()[0]
            rows = table.nrows  #获取行数
            cols = table.ncols  #获取列数
            for r in range(1, rows):
                student_id = table.cell(r, 0).value
                name = table.cell(r, 1).value
                sex = table.cell(r, 2).value
                id_card = table.cell(r, 3).value
                national = table.cell(r, 4).value
                Native_place = table.cell(r, 5).value
                Account_type = table.cell(r, 6).value
                Date_of_birth = str(datetime(*xldate_as_tuple(table.cell(r, 7).value,0)))[0:10]
                enter_date = str(datetime(*xldate_as_tuple(table.cell(r, 8).value,0)))[0:10]
                class_name = table.cell(r, 9).value
                address = table.cell(r, 10).value
                Change_record = table.cell(r, 11).value
                Disciplinary_records = table.cell(r, 12).value
                specialty = table.cell(r, 13).value
                remarks = table.cell(r, 14).value
                try:
                    a = Students.objects.filter(student_id=student_id)
                    if a:
                        continue
                    elif student_id == None or student_id == '':
                        continue
                    else:
                        students = Students()
                        students.student_id = int(student_id)
                        students.name = name
                        students.sex = sex
                        #print('性别………………',sex)
                        students.id_card=int(id_card)
                        students.address=address
                        students.enter_date=enter_date
                        #外键字段插入时，先获取外键表中字段id
                        students.class_name_id = Class.objects.filter(class_name=int(class_name)).first()
                        students.Date_of_birth = Date_of_birth
                        students.Native_place = Native_place
                        students.Account_type =Account_type
                        students.specialty = specialty
                        students.Disciplinary_records = Disciplinary_records
                        students.Change_record = Change_record
                        students.national =national
                        students.remarks=str(remarks) if remarks else ' '
                        students.save()
                except:
                    pass
            return HttpResponseRedirect('/xadmin/DjangoStudent/students/')
        # 必须返回，不然报错（或者注释掉）
        return super(StudentsAdmin, self).post(request, *args, **kwargs)


# Class显示设置
class ClassAdmin(object):
    # 列表中显示的字段
    list_display = ('class_name',)


# Subject显示设置
class SubjectsAdmin(object):
    # 列表中显示的字段
    list_display = ('name', 'score',)


# Teachers显示设置
#class TeachersAdmin(object):
#    # 列表中显示的字段
#    list_display = ('name',)
#    import_excel = True
#
#    def post(self, request, *args, **kwargs):
#        if 'excel' in request.FILES:
#            execl_file = request.FILES.get('excel')
#            files = open_workbook(filename=None, file_contents=request.FILES['excel'].read())
#            table = files.sheets()[0]
#            rows = table.nrows  # 获取行数
#            cols = table.ncols  # 获取列数
#            for r in range(1, rows):
#                name = table.cell(r, 0).value
#                try:
#                    a = Teachers.objects.filter(name=name)
#                    if a:
#                        continue
#                    elif name == None or name == '':
#                        continue
#                    else:
#                        teacer = Teachers()
#                        teacer.name = name
#                        teacer.save()
#                except:
#                    pass
#            # excel_into_model('course', 'Course', excel_file=files)
#            return HttpResponseRedirect('http://127.0.0.1:8000/xadmin/DjangoStudent/teachers/')
#            # pass
#        # 必须返回，不然报错（或者注释掉）
#        return super(TeachersAdmin, self).post(request, *args, **kwargs)

class UserAdmin(object):
    # 列表中显示的字段
    list_display = ('username', 'password',)

    import_excel = True
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            execl_file = request.FILES.get('excel')
            files = open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            table = files.sheets()[0]
            rows = table.nrows  # 获取行数
            cols = table.ncols  # 获取列数
            for r in range(1, rows):
                username = table.cell(r, 0).value
                password = table.cell(r, 1).value
                
                print(username,int(password))
                #try:
                a = User.objects.filter(username=username)
                if a:
                    continue
                elif username == None or username == '':
                    continue
                else:
                    user = User()
                    #user.username = username
                    user.username = Students.objects.filter(student_id=int(username)).first()
                    user.password = int(password)
                    user.save()
                #except:
                #    pass
            # excel_into_model('course', 'Course', excel_file=files)
            return HttpResponseRedirect('http://127.0.0.1:8000/xadmin/DjangoStudent/user/')
            # pass
        # 必须返回，不然报错（或者注释掉）
        return super(UserAdmin, self).post(request, *args, **kwargs)


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(Students, StudentsAdmin)
xadmin.site.register(Class, ClassAdmin)
xadmin.site.register(Subjects, SubjectsAdmin)
#xadmin.site.register(Teachers, TeachersAdmin)
xadmin.site.register(User, UserAdmin)


xadmin.site.register(LoginView, LoginViewAdmin)