from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    '''客户信息表'''
    name = models.CharField(max_length=32,blank=True,null=True)
    qq = models.CharField(max_length=64,unique=True)
    qq_name = models.CharField(max_length=64,blank=True,null=True)
    phone = models.CharField(max_length=64,blank=True,null=True)
    source_choice = (
        (0,'转介绍'),
        (1,'QQ群'),
        (2,'官网'),
        (3,'百度推广'),
        (4,'51CTO'),
        (5,'知乎'),
        (6,'市场推广'),
    )

    source = models.SmallIntegerField(choices=source_choice)
    referral_from = models.CharField(verbose_name="转介绍人qq",max_length=64,blank=True)
    consult_course = models.ForeignKey('Course',verbose_name='咨询课程',on_delete=models.CASCADE)
    content = models.TextField(verbose_name='咨询内容')
    tags=models.ManyToManyField('Tag',blank=True,null=True,)
    consultant=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    memo = models.TextField(blank=True,null=True)
    date = models.DateField(verbose_name='咨询日期',auto_now_add=True)
    status_choice = (
        (0,u'已报名'),
        (1,u'待跟进'),
        (2,u'没有意向'),
    )
    status=models.SmallIntegerField(choices=status_choice,default=1,)
    def __str__(self):
        return self.qq
    class Meta:
        verbose_name_plural="客户表"




class Tag(models.Model):
    name=models.CharField(unique=True,max_length=32,verbose_name="标签名")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="标签"




class CustomerFollowup(models.Model):
    customer=models.ForeignKey('Customer',on_delete=models.CASCADE)
    content = models.TextField(verbose_name='跟进内容')
    consultant=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True,verbose_name="跟进日期")
    intention_chioce = (
        (0,'两周内报名'),
        (1,'一个月内报名'),
        (2,'近期无报名计划'),
        (3,'已在其他机构报名'),
        (4,'已报名'),
        (5,'已拉黑'),
    )

    intention=models.SmallIntegerField(choices=intention_chioce)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s:%s>" %(self.customer.qq,self.intention)
    class Meta:
        verbose_name_plural="客户跟进"




class Course(models.Model):
    '''课程表'''
    name = models.CharField(max_length=64,unique=True,verbose_name="课程名")
    price = models.PositiveIntegerField(verbose_name="学费")
    period = models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline=models.TextField(verbose_name="课程大纲")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="课程表"




class Branch(models.Model):
    '''校区'''
    name=models.CharField(max_length=128,unique=True,verbose_name="校区名")
    addr = models.CharField(max_length=128,verbose_name="校区地址")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="校区"



class ClassList(models.Model):
    '''班级表'''
    branch=models.ForeignKey('Branch',verbose_name='分校',on_delete=models.CASCADE)
    course=models.ForeignKey("Course",on_delete=models.CASCADE)
    semester=models.PositiveSmallIntegerField(verbose_name="学期")
    teachers=models.ManyToManyField('UserProfile')
    class_type_choice = (
        (0,'面授（脱产）'),
        (1,'面授（周末）'),
        (2,'网络班'),
    )
    class_type=models.SmallIntegerField(choices=class_type_choice,verbose_name='报班类型')
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField('UserProfile', blank=True, null=True, verbose_name="讲师")
    start_date= models.DateField(verbose_name="开班日期")
    end_date= models.DateField(verbose_name="结业日期",blank=True,null=True)
    def __str__(self):
        return "%s %s %s" %(self.branch,self.course,self.semester)

    class Meta:
        unique_together=('branch','course','semester')
        verbose_name_plural="班级表"

class CourseRecord(models.Model):
    '''上课表'''
    from_class = models.ForeignKey('ClassList', verbose_name='班级',on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name="第几天")
    teacher = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.from_class, self.day_num)

    class Meta:
        unique_together = ("from_class", "day_num")
        verbose_name="上课记录"
        verbose_name_plural="上课记录"

class StudyRecord(models.Model):
    '''学习记录'''
    student=models.ForeignKey("Erollment",on_delete=models.CASCADE)
    course_record=models.ForeignKey("CourseRecord",on_delete=models.CASCADE)
    attendance_choices = (
        (0,'已签到'),
        (1,'迟到'),
        (2,'缺勤'),
        (3,'早退'),
    )
    attendance=models.SmallIntegerField(choices=attendance_choices,default=0)
    score_choices=(
        (100,'A+'),
        (90,'A'),
        (85,'B+'),
        (80,'B'),
        (75,'B-'),
        (70,'C+'),
        (60,'C'),
        (40,'C-'),
        (-50,'D'),
        (-100,'COPY'),
        (0,'N/A'),
    )
    score = models.SmallIntegerField(choices=score_choices,default=0)
    memo=models.TextField(blank=True,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" %(self.student,self.course_record,self.score)
    class Meta:
        unique_together=('student','course_record')
        verbose_name_plural="学习记录"

class Erollment(models.Model):
    '''报名表'''
    customer=models.ForeignKey("Customer",on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey("ClassList",verbose_name="所报班级",on_delete=models.CASCADE)
    consultant=models.ForeignKey('UserProfile',verbose_name="课程顾问",on_delete=models.CASCADE)
    contract_agreed=models.BooleanField(default=False,verbose_name="学员已同意合同")
    contrac_approved=models.BooleanField(default=False,verbose_name="合同已审核")
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.customer,self.enrolled_class)
    class Meta:
        unique_together=("customer","enrolled_class")
        verbose_name_plural="报名表"




class Payment(models.Model):
    customer=models.ForeignKey("Customer",on_delete=models.CASCADE)
    course=models.ForeignKey("Course",verbose_name="所报班级",on_delete=models.CASCADE)
    amount=models.PositiveSmallIntegerField(verbose_name="数额",default=500)
    consultant=models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s %s" %(self.customer,self.amount)
    class Meta:
        verbose_name_plural="缴费表"



class UserProfile(models.Model):
    '''账号表'''
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=32)
    roles=models.ManyToManyField("Role",blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="账号表"

class Role(models.Model):
    '''角色表'''
    name=models.CharField(max_length=32,unique=True)
    menus=models.ManyToManyField("Menu",blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="角色表"

class Menu(models.Model):
    '''菜单名'''
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)
    def __str__(self):
        return self.name
