from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Subject, SingleChoice, SingleChoiceImage, SingleChoiceAnswer, ClassInfo, Teacher, Student, Test, StudentAnswer, StudentGrades
# from django.contrib.auth.admin import UserAdmin


class SingleChoice_Admin(admin.ModelAdmin):
    list_display = ("SingleChoiceIndex", "SingleChoiceMark",
                    "SingleChoiceContent", "SingleChoiceCategory", "SingleChoiceSubject")
    ordering = ("SingleChoiceIndex",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=SingleChoice.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class SingleChoiceImage_Admin(admin.ModelAdmin):
    list_display = ("SingleChoiceQues", "SingleChoiceImageName", "SingleChoiceImageID",
                    "SingleChoiceImage")
    ordering = ("SingleChoiceQues",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=SingleChoiceImage.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class SingleChoiceAnswer_Admin(admin.ModelAdmin):
    list_display = ("SingleChoiceID",
                    "SingleChoiceAnswerA", "SingleChoiceAnswerB", "SingleChoiceAnswerC", "SingleChoiceAnswerD", "SingleChoiceCorrect",)
    ordering = ("SingleChoiceID",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=SingleChoiceAnswer.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


# class administratiorAdmin(admin.ModelAdmin):
#     pass


class ClassInfo_Admin(admin.ModelAdmin):
    list_display = ("ClassID",)
    ordering = ("ClassID",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=ClassInfo.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class Teacher_Admin(admin.ModelAdmin):
    list_display = ("TeacherID", "TeacherName",
                    "TeacherGender", "TeacherDepartment", "TeacherEmail", "TeacherPassword", "TeacherBirthday")
    ordering = ("TeacherID",)
    actions = ['cancel_orders', ]
    filter_horizontal = ("TeacherClass", "TeacherSubject",)

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=Teacher.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class Student_Admin(admin.ModelAdmin):
    list_display = ("StudentID", "StudentClass",
                    "StudentName", "StudentGender", "StudentDepartment", "StudentEmail", "StudentPassword", "StudentBirthday")
    ordering = ("StudentID",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=Student.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class Subject_Admin(admin.ModelAdmin):
    list_display = ("SubjectCode", "SubjectName",)
    ordering = ("SubjectCode", "SubjectName",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=Subject.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class Test_Admin(admin.ModelAdmin):
    list_display = ("TestName", "TestID",
                    "TestDescription", "TestSubject", "TestDate", "TestTimeLimit", )

    ordering = ("TestName", "TestSubject")
    filter_horizontal = ("TestClass", "TestSingleChoiceQues",)

    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=Test.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class StudentAnswer_Admin(admin.ModelAdmin):
    list_display = ("TestID", "StudentID",
                    "SingleChoiceQues", "Answer")
    ordering = ("TestID", "StudentID", "SingleChoiceQues",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=StudentAnswer.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


class StudentGrades_Admin(admin.ModelAdmin):
    list_display = ("StudentID", "TestID","Subject",
                    "Grade", "DoneState", "GradeDate")
    ordering = ("StudentID", "TestID", "Grade",)
    actions = ['cancel_orders', ]

    def cancel_orders(self, request, queryset):
        queryset.update(order_status=StudentAnswer.CANCELLED)
    cancel_orders.short_description = "Mark selected orders as cancelled"


admin.site.register(SingleChoice, SingleChoice_Admin)

admin.site.register(SingleChoiceImage, SingleChoiceImage_Admin)
admin.site.register(SingleChoiceAnswer, SingleChoiceAnswer_Admin)
admin.site.register(ClassInfo, ClassInfo_Admin)
admin.site.register(Teacher, Teacher_Admin)
admin.site.register(Student, Student_Admin)
admin.site.register(Subject, Subject_Admin)

admin.site.register(Test, Test_Admin)

admin.site.register(StudentAnswer, StudentAnswer_Admin)

admin.site.register(StudentGrades, StudentGrades_Admin)
