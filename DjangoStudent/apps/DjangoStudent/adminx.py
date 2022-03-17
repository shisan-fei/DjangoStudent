# @Time : 2022/2/10 21:37
# @Author : 王龙飞
# @File : adminx.py
# @Version : 1.0
# @Description : xadmin数据模型,用以设置页面显示和关联数据库字段
import xadmin
import sys,os

#import_excel = True
sys.path.append("..")
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from xadmin import views
from .models import Students,Class,Subjects,Teachers
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
    list_display = ('student_id', 'name', 'sex', 'id_card', 'address', 'enter_date', 'class_name','subjects','remarks')

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
                address = table.cell(r, 4).value
                #enter_date = table.cell(r, 5).value   表格中日期不能直接取出显示，要使用date模块转换
                enter_date = str(datetime(*xldate_as_tuple(table.cell(r, 5).value,0)))[0:10]
                class_name = table.cell(r, 6).value
                subject_name = table.cell(r, 7).value
                remarks = table.cell(r, 8).value
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
                        if sex == '男':
                            sex = 'male'
                            students.sex = sex
                        elif name == '女':
                            name = 'female'
                            students.sex = sex
                        else:
                            continue
                        print('性别………………',sex)
                        students.id_card=int(id_card)
                        students.address=address
                        students.enter_date=enter_date
                        #外键字段插入时，先获取外键表中字段id
                        students.class_name_id = Class.objects.filter(class_name=int(class_name)).first()
                        students.remarks=str(remarks) if remarks else ' '
                        students.save()
                except:
                    pass
            return HttpResponseRedirect('/xadmin/DjangoStudent/students/')
        # 必须返回，不然报错（或者注释掉）
        return super(StudentsAdmin, self).post(request, *args, **kwargs)

    #def has_delete_permission(self, *args, **kwargs):
    #    # 删除权限
    #    if self.request.user.is_superuser:  # 管理员才能增加
    #        return True
    #    return False
    #def has_add_permission(self, *args, **kwargs):
    #    if self.request.user.is_superuser:  # 管理员才能增加
    #        return True
    #    return False
    #def has_change_permission(self, *args, **kwargs):
    #    if self.request.user.is_superuser:  # 管理员才能修改
    #        self.readonly_fields = []  # 设置管理员可以修改所有字段
    #        return True
    #    return False
    #def queryset(self):
    #    """当前用户只能看到自己的数据"""
    #    user = self.request.user
    #    if user.is_superuser:
    #        # 管理员可以查看所有数据
    #        return self.model._default_manager.get_queryset()
    #    # 当前用户只能查看自己的数据
    #    return self.model.objects.filter(user=user)

    # # 顺序排序
    # ordering = ('age', 'name',)
    # # 逆序排序，在前面加一个减号"-"，例如按年龄倒序排列
    # ordering = ('-age',)

    # 显示数据详情
    # show_detail_fields = ['name']


# Class显示设置
class ClassAdmin(object):
    # 列表中显示的字段
    list_display = ('class_name',)


# Subject显示设置
class SubjectsAdmin(object):
    # 列表中显示的字段
    list_display = ('name', 'score',)


# Teachers显示设置
class TeachersAdmin(object):
    # 列表中显示的字段
    list_display = ('name',)
    import_excel = True

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            execl_file = request.FILES.get('excel')
            files = open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            table = files.sheets()[0]
            rows = table.nrows  # 获取行数
            cols = table.ncols  # 获取列数
            for r in range(1, rows):
                name = table.cell(r, 0).value
                try:
                    a = Teachers.objects.filter(name=name)
                    if a:
                        continue
                    elif name == None or name == '':
                        continue
                    else:
                        teacer = Teachers()
                        teacer.name = name
                        teacer.save()
                except:
                    pass
            # excel_into_model('course', 'Course', excel_file=files)
            return HttpResponseRedirect('http://127.0.0.1:8000/xadmin/DjangoStudent/teachers/')
            # pass
        # 必须返回，不然报错（或者注释掉）
        return super(TeachersAdmin, self).post(request, *args, **kwargs)




xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(Students, StudentsAdmin)
xadmin.site.register(Class, ClassAdmin)
xadmin.site.register(Subjects, SubjectsAdmin)
xadmin.site.register(Teachers, TeachersAdmin)


xadmin.site.register(LoginView, LoginViewAdmin)