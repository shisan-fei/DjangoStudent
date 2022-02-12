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
    list_display = ('id', 'name', 'sex', 'age', 'address', 'enter_date', 'remarks')

    # 内联复选框(选课系统可以上多选)
    style_fields = {'subjects': 'checkbox-inline', }

    # 搜索(姓名, 班级, 课程),之后再页面中就可以根据字典进行搜索
    search_fields = ('name', 'class_name__class_name', 'subjects__name',)

    # 过滤器(按性别)
    list_filter = ('sex',)

    # 导入excel插件
    import_excel = True
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        # 必须返回，不然报错（或者注释掉）
        return super(StudentsAdmin, self).post(request, *args, **kwargs)

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




xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(Students, StudentsAdmin)
xadmin.site.register(Class, ClassAdmin)
xadmin.site.register(Subjects, SubjectsAdmin)
xadmin.site.register(Teachers, TeachersAdmin)


xadmin.site.register(LoginView, LoginViewAdmin)