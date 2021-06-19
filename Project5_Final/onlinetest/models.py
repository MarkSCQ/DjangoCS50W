from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

import uuid
import datetime
# from django.db import models
# Create your models here.
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
DEPARTMENT = (
    ('CS', 'Computer Science'),
    ('AM', 'Applied Mathematics'),
    ('AS', 'Asian Studies'),
    ('MS', 'Military Science'),
    ('LJ', 'Law and Justice'),
    ('IT', 'Information Technology'),
    ('GD', 'Graphic Design'),
)

ANSWERSELECT = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

TEST_STATE = (
    ("OPEN", "OPEN"),
    ("CLOSE", "CLOSE")
)

DONE_STATE = {
    ('FINISHED', 'FINISHED'),
    ('UNFINISHED', 'UNFINISHED')
}


class Subject(models.Model):
    SubjectCode = models.CharField(
        max_length=200, default="", verbose_name="Subject Code")
    SubjectName = models.CharField(
        max_length=200, default="", verbose_name="Subject Name")
    SubjectID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Subject ID")
    SubjectLogo = models.ImageField(null=True, blank=True,
                                    upload_to="uploads/", verbose_name="Subject Logo")

    def __str__(self):
        return self.SubjectName

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = verbose_name


class SingleChoice(models.Model):
    SingleChoiceIndex = models.AutoField(
        primary_key=True, verbose_name="Single Choice Index")

    SingleChoiceMark = models.PositiveSmallIntegerField(
        default=5, blank=True, null=True, verbose_name="Single Choice Mark")

    SingleChoiceContent = models.TextField(
        verbose_name="Single Choice Content")

    SingleChoiceCategory = models.CharField(
        max_length=200, verbose_name="Single Choice Category")

    SingleChoiceSubject = models.ForeignKey(
        Subject, null=True, on_delete=models.CASCADE, verbose_name="Single Choice Subject")

    def __str__(self):
        return str(self.SingleChoiceIndex) + ". " + self.SingleChoiceContent + " ("+str(self.SingleChoiceMark)+")"

    class Meta:
        verbose_name = "Single Choice"
        verbose_name_plural = verbose_name


# def getcurrentusername(instance, filename):
#     return "/uploads/{0}/{1}".format(instance.user.username, filename)

class SingleChoiceImage(models.Model):
    SingleChoiceImageID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Image ID")
    SingleChoiceQues = models.ForeignKey(
        SingleChoice, null=True, on_delete=models.SET_NULL, verbose_name="Single Choice Question")
    SingleChoiceImageName = models.TextField(verbose_name="Image Description")
    SingleChoiceImage = models.ImageField(
        upload_to="uploads/", verbose_name="Image")

    def __str__(self):
        return str(self.SingleChoiceImageID)

    class Meta:
        verbose_name = "Single Choice Image"
        verbose_name_plural = verbose_name


class SingleChoiceAnswer(models.Model):
    SingleChoiceID = models.ForeignKey(
        SingleChoice, null=True, on_delete=models.CASCADE, verbose_name="Single Choice ID")
    # SingleChoiceAnswerIndex = models.CharField(
    #     max_length=4, verbose_name="Single Choice Index")

    SingleChoiceAnswerA = models.CharField(default="aaa",
                                           max_length=200, verbose_name="A")

    SingleChoiceAnswerB = models.CharField(default="bbb",
                                           max_length=200, verbose_name="B")

    SingleChoiceAnswerC = models.CharField(default="ccc",
                                           max_length=200, verbose_name="C")

    SingleChoiceAnswerD = models.CharField(default="ddd",
                                           max_length=200, verbose_name="D")
    # TeacherDepartment = models.CharField(    verbose_name='Department', max_length=20, choices=DEPARTMENT, default=None)
    SingleChoiceCorrect = models.CharField(
        verbose_name="Single Choice True Answer", max_length=20, choices=ANSWERSELECT, default=None)
    SingleChoiceExplanation = models.TextField(
        default="Explanation of A: XXXXX; Explanation of B: XXXXX; Explanation of C: XXXXX; Explanation of D: XXXXX;", verbose_name="Explanation")

    def __str__(self):
        return str(self.SingleChoiceID.SingleChoiceIndex)+" "+self.SingleChoiceCorrect

    class Meta:
        verbose_name = "Single Choice Answer"
        verbose_name_plural = verbose_name


class ClassInfo(models.Model):
    ClassID = models.CharField(
        max_length=20, primary_key=True, verbose_name="Class ID")

    def __str__(self):
        return "Class ID: " + self.ClassID

    class Meta:
        verbose_name = "Class Info"
        verbose_name_plural = verbose_name

    def get_num_bid_info(self):
        return Student.objects.filter(StudentClass=self.ClassID).count()


class Teacher(models.Model):
    TeacherID = models.CharField(
        max_length=20, primary_key=True, verbose_name="Teacher ID")
    TeacherName = models.CharField(max_length=20, verbose_name='Name')
    TeacherGender = models.CharField(
        max_length=6, choices=GENDER, default='Male', verbose_name='Gender')
    TeacherDepartment = models.CharField(
        verbose_name='Department', max_length=20, choices=DEPARTMENT, default=None)
    TeacherEmail = models.EmailField(verbose_name='Email', default=None)
    TeacherPassword = models.CharField(
        verbose_name='Password', max_length=15, default='123456')
    TeacherBirthday = models.DateField(verbose_name='Birthday')

    TeacherSubject = models.ManyToManyField(
        Subject, blank=True, verbose_name="Teacher Subject")
    TeacherClass = models.ManyToManyField(
        ClassInfo, blank=True, verbose_name="Class ID")

    def __str__(self):
        return self.TeacherID + " " + self.TeacherName

    class Meta:
        verbose_name = "Teacher Info"
        verbose_name_plural = verbose_name


class Test(models.Model):
    TestName = models.CharField(max_length=200, verbose_name="Test Name")

    TestDescription = models.TextField()

    TestID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Test ID")

    # TestCreator = models.ForeignKey(
    #     Teacher, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Test Creator")

    TestSubject = models.ForeignKey(
        Subject, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Test Subject")

    TestClass = models.ManyToManyField(
        ClassInfo,  blank=True, verbose_name="Test Class")
   
    TestDate = models.DateTimeField(
        null=True, auto_now_add=True, verbose_name="Test date")

    TestTimeLimit = models.PositiveSmallIntegerField(
        default=60, blank=True, null=True)

    # TestState = models.

    TestSingleChoiceQues = models.ManyToManyField(
        SingleChoice,  blank=True, verbose_name="Test Single Choice Questions")

    def __str__(self):
        return self.TestName

    class Meta:
        verbose_name = "Test Info"
        verbose_name_plural = verbose_name


class Student(models.Model):
    StudentID = models.CharField(
        max_length=20, primary_key=True, verbose_name="Student ID")
    StudentClass = models.ForeignKey(
        ClassInfo, null=True, on_delete=models.CASCADE, verbose_name="Class ID")
    StudentName = models.CharField(verbose_name='Name', max_length=20)
    StudentGender = models.CharField(
        verbose_name='Gender', max_length=6, choices=GENDER, default='Male')
    StudentDepartment = models.CharField(
        verbose_name='Department', max_length=20, choices=DEPARTMENT, default=None)
    StudentEmail = models.EmailField(verbose_name='Email', default=None)
    StudentPassword = models.CharField(
        verbose_name='Password', max_length=15, default='123456')
    StudentBirthday = models.DateField(verbose_name='Birthday')

    StudentTest = models.ManyToManyField(
        Test,  blank=True, verbose_name="Test")

    def __str__(self):
        return self.StudentID + " " + self.StudentName

    class Meta:
        verbose_name = "Student Info"
        verbose_name_plural = verbose_name


class StudentGrades(models.Model):
    TestID = models.ForeignKey(
        Test, null=True, on_delete=models.SET_NULL,  verbose_name="Test")
    StudentID = models.ForeignKey(
        Student, null=True, on_delete=models.CASCADE, verbose_name="Student ID")
    GradeID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Grade ID")
    Grade = models.FloatField(default=-1, verbose_name="Grades")
    # ! True -> finished
    # ! False -> unfinished
    DoneState = models.CharField(
        max_length=20, choices=DONE_STATE, default="UNFINISHED", verbose_name="Done State")

    GradeDate = models.DateTimeField(
        null=True, blank=True, default=timezone.now)

    Subject = models.ForeignKey(
        Subject, null=True, on_delete=models.SET_NULL,  verbose_name="Subject")

    def __str__(self):
        return str(self.Grade)

    class Meta:
        verbose_name = "Student Grades"
        verbose_name_plural = verbose_name


class StudentAnswer(models.Model):

    TestID = models.ForeignKey(
        Test, null=True, on_delete=models.SET_NULL,  verbose_name="Test")
    StudentID = models.ForeignKey(
        Student, null=True, on_delete=models.CASCADE, verbose_name="Student ID")
    SingleChoiceQues = models.ForeignKey(
        SingleChoice, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Single Choice Question")

    Answer = models.CharField(max_length=4, verbose_name="Student Answer")

    AnswerID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Answer ID")

    Grade = models.ForeignKey(
        StudentGrades, null=True, on_delete=models.SET_NULL,  verbose_name="Student Grade")

    def __str__(self):
        return str(self.Answer)

    class Meta:
        verbose_name = "Student Answers"
        verbose_name_plural = verbose_name


# class history_recored(models.Model):
#     TestID=models.ForeignKey()
#     StudentID=models.ForeignKey()
#     Date = models.DateTimeField()
#     StudentAnswer=models.ManyToManyField()
#     Grades = models.FloatField()
