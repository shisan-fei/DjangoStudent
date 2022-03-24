import os
from statistics import mode

from django.db import models

# Create your models here.


# 学生管理系统的教师表
class Teachers(models.Model):
    name = models.CharField(verbose_name='教师姓名',
                            max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_teachers'
        verbose_name = verbose_name_plural = '教师信息'


# 学生管理系统的班级表
class Class(models.Model):
    class_name = models.CharField(primary_key=True,verbose_name='班级',
                                  max_length=100)

    # 声明一对一的关联关系
    headmaster = models.OneToOneField('Teachers',
                                      verbose_name='班主任',
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = 't_class'
        verbose_name = verbose_name_plural = '班级'


# 学生管理系统的学生表
class Students(models.Model):
    student_id = models.CharField(primary_key=True,verbose_name='学号',max_length=8)
    name = models.CharField(verbose_name='学生姓名',
                            max_length=50)

    # 定义图片的保存路径及名称
    def get_photo(self, filename):
        return os.path.join('photo',
                            '%s_%s%s' % (self.class_name,
                                         self.name,
                                         os.path.splitext(filename)[1]))

    photo = models.ImageField(verbose_name='照片',    #blank 设置为True时，页面字段可以为空。
                              upload_to=get_photo,
                              blank=True,
                              null=True)

    sex = models.CharField(verbose_name='性别',
                           max_length=50,
                           choices=(('male', '男'),
                                    ('female', '女')))


    id_card = models.CharField(verbose_name='身份证号',max_length=20)

    address = models.CharField(verbose_name='家庭住址',
                               max_length=250,
                               blank=True)

    enter_date = models.DateField(verbose_name='入学时间')
    Date_of_birth  = models.DateField(verbose_name='出生日期')

    Native_place = models.CharField(verbose_name="籍贯", max_length=20,)

    Account_type = models.CharField(verbose_name="户口类型", max_length=10)

    specialty = models.TextField(verbose_name='特长',blank=True)

    Disciplinary_records =models.TextField(verbose_name='奖惩记录',blank=True)

    remarks = models.TextField(verbose_name='备注',
                               blank=True)

    # 定义外键
    class_name = models.ForeignKey('Class',
                                   verbose_name='所在班级',
                                   on_delete=models.CASCADE)
                                   #blank=True)
    # 声明多对多的关联关系
    subjects = models.ManyToManyField('Subjects',
                                      verbose_name='选修课程'
                                      ,blank=True)

    def __str__(self):
        return self.student_id

    class Meta:
        db_table = 't_students'
        verbose_name = verbose_name_plural = '学生信息'


# 学生管理系统的课程表
class Subjects(models.Model):
    name = models.CharField(verbose_name='课程名称',
                            max_length=50,
                            blank=True)

    score = models.IntegerField(verbose_name='学分',
                                blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_subjects'
        verbose_name = verbose_name_plural = '课程信息'

#学生登录信息表

class User(models.Model):
   #建立与学生表中学号的外键(一对一)，db_column='username'可以让字段会后不加_id
    username = models.OneToOneField(Students, to_field="student_id",primary_key=True,
                                    on_delete=models.CASCADE,verbose_name='用户名',db_column='username',default='')
    password = models.CharField(verbose_name='密码',max_length=10)

    def __str__(self):
         return str(self.username)

    class Meta:
         db_table = 't_user'
         verbose_name = verbose_name_plural = '用户信息'

