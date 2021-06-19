# Author:   https://github.com/MarkSCQ/

from django.http import HttpResponse
from django.shortcuts import render

from typing import List, Dict
from typing import Union

import markdown2
from onlinetest.models import Subject, SingleChoice, SingleChoiceImage, SingleChoiceAnswer, ClassInfo, Teacher, Student, Test, StudentAnswer, StudentGrades
from django.template.defaulttags import register
from django import template
import sys

from django.http import JsonResponse
import traceback

import numpy as np
from collections import Counter

# def PurifyInput(record):
#     """
#         Remove all space at beginning or tail
#     """
#     return "".join(record.rstrip().lstrip())

DONE_STATE = {
    ('FINISHED', 'FINISHED'),
    ('UNFINISHED', 'UNFINISHED')
}


def Todos(message):
    # the current todo are changed to those are opened for testing.
    # when one test is opened to one student, it would be assigned to student

    todo_test = Student.objects.get(StudentID=message).StudentTest.all()

    todo_test_details = [[i.TestName, i.TestDescription,
                          i.TestSubject, i.TestDate, i.TestTimeLimit] for i in todo_test]

    sg = StudentGrades.objects.filter(StudentID=Student.objects.get(
        StudentID=message), DoneState="UNFINISHED")

    unfinished_subject_test = {}

    undonedic = {}

    for i in sg:
        if i.Subject.SubjectName not in undonedic:
            undonedic[i.Subject.SubjectName] = [i.TestID.TestName]
        else:
            undonedic[i.Subject.SubjectName].append(i.TestID.TestName)

    test_sub = {}
    for i in undonedic:
        for j in undonedic[i]:
            if j not in test_sub:
                test_sub[j] = i

    testtime = {}
    for key in undonedic:
        for tn in undonedic[key]:
            testobj = Test.objects.get(TestName=tn)
            if tn not in testtime:
                dtime = testobj.TestDate.strftime("%Y-%m-%d, %H:%M")
                testtime[tn] = dtime
            else:
                dtime = testobj.TestDate.strftime("%Y-%m-%d, %H:%M")
                testtime[tn] = dtime

    return todo_test_details


@register.filter
def keys(d, key_name):
    value = 0
    try:
        value = d[key_name]
    except KeyError:
        value = 0
    return value


def index(request):
    return render(request, "onlinetest/index.html")


def login(request):
    if request.method == "POST":
        # Attempt to sign user in
        idcode = request.POST.get('idcode')
        password = request.POST.get('password')
        identity = request.POST.get('identity')
        if identity == "teacher":
            # render to current teacher page
            try:
                Tea = Teacher.objects.all().get(TeacherID=idcode)
            except:
                return render(request, "onlinetest/index.html", {
                    "message": str(idcode),
                    "alert_msg": "Invalid username and/or password."
                })
            if Tea.TeacherPassword == password:
                return render(request, "onlinetest/teacher.html", {
                    "message": str(idcode),
                    "alert_msg": "Invalid username and/or password."
                })
            else:
                return render(request, "onlinetest/index.html", {
                    "message": str(idcode),
                    "alert_msg": "Invalid username and/or password."
                })
        elif identity == "student":
            # identity to current student page

            try:
                Stu = Student.objects.all().get(StudentID=idcode)
            except:
                return render(request, "onlinetest/index.html", {
                    "message": str(idcode),
                    "alert_msg": "Invalid username and/or password."
                })
            if Stu.StudentPassword == password:
                todo_test_details = Todos(idcode)
                nameTag = ["Test Name",
                           "Description",
                           "Subject",
                           "Open Time",
                           "Time Limit"
                           ]
                return render(request, "onlinetest/student.html", {
                    "message": str(idcode),
                    "todo_test_details": todo_test_details,
                    "nameTag": nameTag
                    # "testtime": testtime,
                    # "test_sub": test_sub
                })
            else:
                return render(request, "onlinetest/index.html", {
                    "message": str(idcode),
                    "alert_msg": "Invalid username and/or password."
                })
        else:
            return render(request, "onlinetest/index.html", {
                "message": str(idcode),
                "alert_msg": "Invalid username and/or password."

            })
    else:
        return render(request, "onlinetest/index.html", {
            "message": str(idcode),
            "alert_msg": "Invalid username and/or password."
        })


def GetQuestions(TestObj):
    question_contents = []
    for i in TestObj.TestSingleChoiceQues.all():
        question_contents.append(i.SingleChoiceContent)
    return question_contents

# SCA_obj SingleChoiceAnswer Object


def GetChoiceContent(SCA_obj):
    return {
        "A": SCA_obj.SingleChoiceAnswerA,
        "B": SCA_obj.SingleChoiceAnswerB,
        "C": SCA_obj.SingleChoiceAnswerC,
        "D": SCA_obj.SingleChoiceAnswerD,
    }


def GetChoices(TestObj):

    question_contents = GetQuestions(TestObj)
    answer_contents = {}
    for i in question_contents:
        SCA_obj = SingleChoiceAnswer.objects.get(
            SingleChoiceID=SingleChoice.objects.get(SingleChoiceContent=i))
        answer_contents[i] = GetChoiceContent(SCA_obj)

    return answer_contents


def BuildIndexQuestion(questions_list):
    return {k: str(v+1)+"."+k for v, k in enumerate(questions_list)}


def testfun(request):
    testname = "test"

    question = ["Q1_CONTENT", "Q2_CONTENT", "Q3_CONTENT", "Q4_CONTENT"]
    answer = {
        "Q1_CONTENT": {"A": "A_Content1", "B": "B_Content1", "C": "C_Content1", "D": "D_Content1"},
        "Q2_CONTENT": {"A": "A_Content2", "B": "B_Content2", "C": "C_Content2", "D": "D_Content2"},
        "Q3_CONTENT": {"A": "A_Content3", "B": "B_Content3", "C": "C_Content3", "D": "D_Content3"},
        "Q4_CONTENT": {"A": "A_Content4", "B": "B_Content4", "C": "C_Content4", "D": "D_Content4"}}
    return render(request, "onlinetest/student_homework.html", {
        "question": question,
        "answer": answer,
        "testname": testname
    })


def CalculateGrade(TrueAns, StuAns, GradeList):
    if len(TrueAns) == 0 or len(StuAns) == 0 or len(GradeList) == 0:
        return 0
    grade = 0
    for i in range(len(TrueAns)):
        if TrueAns[i] == StuAns[i]:
            grade += GradeList[i]
    return grade


def submitans(request):
    testid = request.POST.get("testid")
    current_user = request.POST.get("current_user")
    subject = request.POST.get("subject")
    # current_user_alltests = Student.objects.all().get(StudentID=current_user).StudentTest.all()
    TargetTest = Test.objects.all().get(TestID=testid).TestSingleChoiceQues.all()

    TargetTestContent = [i.SingleChoiceContent for i in TargetTest]
    SingleChoiceList = [i for i in TargetTest]

    ans = []
    for i in TargetTestContent:
        ans.append(str(request.POST.get(i))[-1])

    true_ans = []
    for i in TargetTest:
        true_ans.append(SingleChoiceAnswer.objects.get(
            SingleChoiceID=i).SingleChoiceCorrect)

    grade_list = []
    for i in TargetTest:
        grade_list.append(i.SingleChoiceMark)

    ans_grade = CalculateGrade(true_ans, ans, grade_list)
    student_grade = StudentGrades(TestID=Test.objects.get(TestID=testid),
                                  StudentID=Student.objects.get(
                                      StudentID=current_user),
                                  Grade=ans_grade,
                                  DoneState="FINISHED",
                                  Subject=Subject.objects.get(SubjectName=subject))
    student_grade.save()
    # ! TO be recovered
    for i in range(len(ans)):
        tmp = StudentAnswer(
            TestID=Test.objects.get(TestID=testid),
            StudentID=Student.objects.get(StudentID=current_user),
            SingleChoiceQues=SingleChoiceList[i],
            Answer=ans[i],
            Grade=student_grade
        )

        tmp.save()

    st = ""

    for i in grade_list:

        st += str(i)
    # 1. get answers

    # 2. save answers

    # ! return to test page

    # current_user = message

    student_done_test = StudentGrades.objects.filter(
        StudentID=Student.objects.get(StudentID=current_user), DoneState="FINISHED")
    student_done_test_names = [i.TestID.TestName for i in student_done_test]

    all_tests_obj = AllTests(current_user)
    all_test_names = [i.TestName for i in all_tests_obj]
    all_test_ids = [str(i.TestID) for i in all_tests_obj]
    # all_test_ids = [i.TestID for i in all_tests_obj]

    all_test_ids_dic = {}
    for i in all_test_ids:
        if i not in all_test_ids_dic:
            all_test_ids_dic[i] = Test.objects.get(TestID=i).TestName

        #  [i.TestID for i in all_tests_obj]
    filtered_test = []

    for i in all_test_names:
        if i not in student_done_test_names:
            filtered_test.append(i)

    test_logos = {}
    for i in all_test_ids:
        test_logos[i] = Test.objects.get(
            TestID=i).TestSubject.SubjectLogo.url

    test_desc = {}
    for i in all_test_ids:

        test_desc[i] = Test.objects.get(
            TestID=i).TestDescription

    clickable_dict = {}

    for i in all_test_names:
        if i not in student_done_test_names:
            clickable_dict[i] = "UNFINISHED"
        else:
            clickable_dict[i] = "FINISHED"

    return render(request, "onlinetest/student_exams.html", {
        "idcode": current_user,
        "all_test_ids": all_test_ids,
        "all_test_ids_dic": all_test_ids_dic,
        "clickable_dict": clickable_dict,
        "test_logos": test_logos,
        # "all_test_ids": all_test_ids,
        "test_desc": test_desc
    })

    # return HttpResponse(st)


def AllTests(current_user):
    current_user_db = Student.objects.get(StudentID=current_user)
    all_tests = current_user_db.StudentTest.all()
    return all_tests

# pass the name by using function name/<str:name>. The name is embeded in the url tag
# <a href="{% url 'categorysub' one.category_item %}">{{one.category_item}}</a>


def MakeQuestion():
    pass


def GenerateNewTest(request, message):
    # for which test?
    # for which subject?
    # number of the questions
    # limit of time

    # ! get Test Name
    sub_test = {}
    for i in Test.objects.all():
        if i.TestSubject.SubjectName not in sub_test:
            sub_test[i.TestSubject.SubjectName] = [i.TestName]
        else:
            sub_test[i.TestSubject.SubjectName].append(i.TestName)
    sub_list = list(sub_test.keys())
    # ! get Test Subject

    # ! roll questions

    return render(request, "onlinetest/generatenewtest.html", {
        "sub_list": sub_list,
        "sub_test": sub_test,
        "message": message
    })


def StudentOneTest(request, testid, idcode):
    # to get one
    current_user = idcode
    # to get student's class
    # current_class = Student.objects.all().get(
    #     StudentID=current_user).StudentClass.ClassID
    # get all student's tests and filter with testname, return of below is lists of querySet
    # Example: tt: <QuerySet [<Test: Algorithm A CSJ>, <Test: Algorithm B CSJ>]>  type(tt[0]): onlinetest.models.test
    current_user_alltests = Student.objects.all().get(
        StudentID=current_user).StudentTest.all()

    TargetTest = Test.objects.get(TestID=testid)
    # for i in current_user_alltests:
    #     if i.TestID == testid:
    #         TargetTest = i

    msg = "test"
    subject = Test.objects.get(TestID=testid).TestSubject.SubjectName
    if TargetTest is None:
        return render(request, "onlinetest/exam.html", {
            "message": "notest"
        })
    else:
        qss = GetQuestions(TargetTest)
        # ! add index number to Questions
        # ! Constructing another dictionary, key is original  content, values are the index with contents
        # index_ques = BuildIndexQuestion(qss)
        # ST = ""
        # for i in index_ques:

        #     ST += i+"_"+index_ques[i]+" "
        anss = GetChoices(TargetTest)
        timelimit = TargetTest.TestTimeLimit
        return render(request, "onlinetest/exam.html", {
            "message": msg,
            "qs": qss,
            "anss": anss,
            "current_user": current_user,
            "testid": testid,
            "subject": subject,
            "timelimit": timelimit
            # "index_ques": index_ques
        })

    # for i in unfinished_subject_test:
    # test belong to user's class
    # class_id = Student.objects.get(StudentID=message).StudentClass.ClassID
    # all_tests = Test.objects.all().filter(TestClass=ClassInfo.objects.get(ClassID=class_id))

    # sub_names = set(Subject.objects.values_list("SubjectName",flat=True))

    # donedic = {}

    # sg_obj = StudentGrades.objects.all()
    # for i in sg_obj:
    #     # ! subjects and all the tests has been done
    #     donedic[i.Subject.SubjectName] = []
    # for i in donedic:
    #     # ! to find the unfinished test
    #     # ! i is the name of each subject
    #     # ! find subject i's test
    #     i_all_tests_names = Test.objects.all().filter(TestSubject=Subject.objects.get(SubjectName=i))
    #     i_finished_test_obj = StudentGrades.objects.filter(DoneState="FINISHED",Subject=Subject.objects.get(SubjectName=i))
    #     i_finished_test_names = [i.TestID.TestName for i in i_finished_test_obj]
    #     print(i_all_tests_names)
    #     print(i_finished_test_names)
    #     donedic[i] = i_finished_test_names
    #     print(i_all_tests_names)
    #     print(i_finished_test_names)
    # try:
    # sb = i.TestID.Subject.SubjectName

    # get subject, get unfinished

    # donedic[]=
    # ！subjects not finished today


def TestList(request, message):
    current_user = message

    student_done_test = StudentGrades.objects.filter(
        StudentID=Student.objects.get(StudentID=current_user), DoneState="FINISHED")
    student_done_test_names = [i.TestID.TestName for i in student_done_test]

    all_tests_obj = AllTests(current_user)
    all_test_names = [i.TestName for i in all_tests_obj]
    all_test_ids = [str(i.TestID) for i in all_tests_obj]
    # all_test_ids = [i.TestID for i in all_tests_obj]

    all_test_ids_dic = {}
    for i in all_test_ids:
        if i not in all_test_ids_dic:
            all_test_ids_dic[i] = Test.objects.get(TestID=i).TestName

        #  [i.TestID for i in all_tests_obj]
    filtered_test = []

    for i in all_test_names:
        if i not in student_done_test_names:
            filtered_test.append(i)

    test_logos = {}
    for i in all_test_ids:
        test_logos[i] = Test.objects.get(
            TestID=i).TestSubject.SubjectLogo.url

    test_desc = {}
    for i in all_test_ids:

        test_desc[i] = Test.objects.get(
            TestID=i).TestDescription

    # add one status clickable

    # ! make a dict
    # ! clickable {"TEST Name":FINISHED/UNFINISHED, .... }
    clickable_dict = {}

    for i in all_test_names:
        if i not in student_done_test_names:
            clickable_dict[i] = "UNFINISHED"
        else:
            clickable_dict[i] = "FINISHED"

    return render(request, "onlinetest/student_exams.html", {
        "idcode": current_user,
        "all_test_ids": all_test_ids,
        "all_test_ids_dic": all_test_ids_dic,
        "clickable_dict": clickable_dict,
        "test_logos": test_logos,
        # "all_test_ids": all_test_ids,
        "test_desc": test_desc
    })


def ReviewTestsList(request, message):
    current_user = message

    # ! 1. StudentGrade get TestID Obj and Grade (float)
    # ! get the grade records by using student id
    SG = StudentGrades.objects.filter(
        StudentID=Student.objects.get(StudentID=current_user))

    student_grade_records = []

    for i in SG:
        student_grade_records.append([
            i.TestID.TestName, current_user, i.Grade, i.DoneState, i.GradeDate.strftime(
                '%Y.%m.%d'), i.GradeID
        ])
    # ! sort by TestName and TestFinished Time

    student_grade_storted = sorted(student_grade_records, key=lambda x: (
        x[4].split('.')[::-1]), reverse=True)

    # ! 2. Based on TestID Obj get Test Information

    return render(
        request, "onlinetest/student_review.html", {
            "student_grade_storted": student_grade_storted,
            "idcode": message,
        }
    )


def TotalGrade(test_obj):
    return sum([i.SingleChoiceMark for i in test_obj.TestSingleChoiceQues.all()])


def ReviewTestDetails(request, message, testname, gradeid):
    st = str(message)+" "+str(testname)

    sg = StudentGrades.objects.all().get(
        StudentID=Student.objects.get(StudentID=message), GradeID=gradeid)

    sg_test = sg.TestID
    sg_test_question = [
        i.SingleChoiceContent for i in sg_test.TestSingleChoiceQues.all()]

    st_ans = StudentAnswer.objects.all().filter(
        StudentID=Student.objects.get(StudentID=message),
        Grade=StudentGrades.objects.get(GradeID=gradeid))

    sg_mark = sg.Grade
    sg_mark = str(sg.Grade)+"/"+str(TotalGrade(sg_test))
    sg_date = sg.GradeDate.strftime("%b %d, %Y, %H:%M")
    # ! questions and student answers
    sg_Ques_SAns = {}
    for key in st_ans:
        sg_Ques_SAns[key.SingleChoiceQues.SingleChoiceContent] = key.Answer

    # ! questions and student answers
    sg_Ques_TAns = {}
    for key in st_ans:
        sg_Ques_TAns[key.SingleChoiceQues.SingleChoiceContent] = SingleChoiceAnswer.objects.get(
            SingleChoiceID=key.SingleChoiceQues).SingleChoiceCorrect
    sg_Ques_TExp = {}
    for key in st_ans:
        sg_Ques_TExp[key.SingleChoiceQues.SingleChoiceContent] = SingleChoiceAnswer.objects.get(
            SingleChoiceID=key.SingleChoiceQues).SingleChoiceExplanation

    # ! 1. get test questions and answers
    TestObj = Test.objects.get(TestName=testname)
    # TestQuestions = Test.objects.get(TestName=testname).TestSingleChoiceQues.all()
    qss = GetQuestions(TestObj)
    anss = GetChoices(TestObj)
    result_status = ""
    tg = TotalGrade(sg_test)
    if sg.Grade == 0:
        result_status = "l0"
    elif sg.Grade < 0.6*tg:
        result_status = "l1"
    elif 0.6*tg <= sg.Grade < 0.8*tg:
        result_status = "l2"
    elif 0.8*tg <= sg.Grade < 0.9*tg:
        result_status = "l3"
    else:
        result_status = "l4"

    """
        # ques_expl = {}
        # for i in qss:
        #     ques_obj = SingleChoice.objects.get(SingleChoiceContent=i)
        #     ques_expl[i] = SingleChoiceAnswer.objects.get(
        #         SingleChoiceID=ques_obj).SingleChoiceExplanation

        # true_ans = {}
        # ques_objs = TestObj.TestSingleChoiceQues.all()
        # for i in SingleChoiceAnswer.objects.all():
        #     if i.SingleChoiceID.SingleChoiceContent in qss:
        #         true_ans[i.SingleChoiceID.SingleChoiceContent] = i.SingleChoiceCorrect



        # ST = ""

        # # ! 2. get student answers
        # student_ans = StudentAnswer.objects.filter(StudentID=Student.objects.get(
        #     StudentID=message), TestID=Test.objects.get(TestName=testname))

        # ques_ans = {}
        # for i in student_ans:
        #     ques_ans[i.SingleChoiceQues.SingleChoiceContent] = i.Answer
        # stu_ans = [ques_ans[i] for i in qss]
        # # ! 3. get grade and finished time

        # for i in stu_ans:
        #     ST += i+"_"

        # for i in ques_ans:
        #     ST += i+"_"+ques_ans[i]+"_"
        # return HttpResponse(ST)
    """
    return render(request, "onlinetest/review.html", {
        "qustions": qss,
        "choices": anss,
        "stu_ans": sg_Ques_SAns,
        "trueans": sg_Ques_TAns,
        "ques_expl": sg_Ques_TExp,
        "idcode": message,
        "sg_mark": sg_mark,
        "sg_date": sg_date,
        "result_status": result_status

    })


def tolog(*args):
    file1 = open("onlinetest/logfile/anareco.txt", "a")
    for i in args:
        file1.writelines(i)
    file1.close()


def RollQuestion(subject, ques_num):
    ques = SingleChoice.objects.filter(
        SingleChoiceSubject=Subject.objects.get(SubjectName=subject))
    return list(np.random.choice(ques, ques_num, replace=True))


def RollQuestionToStr(subject, ques_num):
    ques = SingleChoice.objects.filter(
        SingleChoiceSubject=Subject.objects.get(SubjectName=subject))
    print()
    if len(ques) <= ques_num:
        ques_num=len(ques)
    quesRandom=list(np.random.choice(ques, ques_num, replace=False))
    quesRandom_C=[i.SingleChoiceContent for i in quesRandom]
    st="<br>".join(quesRandom_C)
    return st


def CheckChoices(question):

    st=""
    choices=SingleChoiceAnswer.objects.get(SingleChoiceID=SingleChoice.objects.get(
        SingleChoiceContent=question.SingleChoiceContent))
    choiceanswer=[choices.SingleChoiceAnswerA, choices.SingleChoiceAnswerB,
                    choices.SingleChoiceAnswerC, choices.SingleChoiceAnswerD, choices.SingleChoiceCorrect]
    # choiceContent =[i.choincecontent for i in question]
    # for i in question:
    st=" ".join(choiceanswer)
    return st


def allchoices(questionlist):

    st=""
    for i in questionlist:
        st += CheckChoices(i)
        st += "<br>"
    return st
    pass


def GenerateNewTestSave(request):

    number_ques=int(request.POST.get("numques"))
    subject=request.POST.get("subjects")
    toget="testname-"+subject
    test=request.POST.get(toget, "CONTENT")
    message=request.POST.get("idcode")
    numtime=request.POST.get("numtime")

    # ! tests naming
    all_test_names=[i.TestName for i in Test.objects.all().filter(
        TestSubject=Subject.objects.get(SubjectName=subject))]
    test_name_index=[int(i.split(" ")[-1]) for i in all_test_names]
    new_index=max(test_name_index)+1
    # tmp = test.split(" ")
    tmp=test.split(" ")
    tmp=tmp[:-1]
    tmp.append(str(new_index))
    strlist=' '.join(tmp)

    # ! generate the random questions
    QuesList=RollQuestionToStr(subject, number_ques)
    tp=str(type(QuesList))
    # ! store the test genereated

    # ! assign to who? class and student?
    # !
    QuesList_=RollQuestion(subject, number_ques)

    questest=allchoices(QuesList_)

    # ! 1. save Test
    test_description=strlist + " Description"
    new_test=Test(TestName=strlist,
                    TestDescription=test_description,
                    TestSubject=Subject.objects.get(SubjectName=subject),
                    TestTimeLimit=int(numtime))
    new_test.save()
    t=Test.objects.get(TestName=strlist)
    for i in QuesList_:
        t.TestSingleChoiceQues.add(i)

    st=Student.objects.get(StudentID=message)
    st.StudentTest.add(t)
    
    
    Stu=Student.objects.all().get(StudentID=message)

    todo_test_details=Todos(message)
    nameTag=["Test Name",
               "Description",
               "Subject",
               "Open Time",
               "Time Limit"
               ]
    return render(request, "onlinetest/student.html", {
        "message": str(message),
        "todo_test_details": todo_test_details,
        "nameTag": nameTag
        # "testtime": testtime,
        # "test_sub": test_sub
    })

    # return HttpResponse("subject:"+subject+"<br>test:"+test+"<br>ques:"+str(number_ques)+"<br>message:"+message+"<br>newname:"+strlist+"<br>ques:<br>"+QuesList+"<br>questest:<br>"+questest)


def BackToMain(request, message):
    Stu=Student.objects.all().get(StudentID=message)

    todo_test_details=Todos(message)
    nameTag=["Test Name",
               "Description",
               "Subject",
               "Open Time",
               "Time Limit"
               ]
    return render(request, "onlinetest/student.html", {
        "message": str(message),
        "todo_test_details": todo_test_details,
        "nameTag": nameTag
        # "testtime": testtime,
        # "test_sub": test_sub
    })


def AverageGradeSubject():
    subjects=Subject.objects.all()
    subject_name=[i.SubjectName for i in subjects]
    subject_objs=[i for i in subjects]

    avg_sub={}
    for i in subject_objs:
        all_grade_obj=StudentGrades.objects.filter(Subject=i)
        try:
            avg_sub[i.Subject.SubjectName]=sum(
                [i.Grade for i in all_grade_obj])/len(all)
        except Exception as exceptions:
            tolog("AverageGradeSubject", exceptions.message,
                  traceback.format_exc())
            # print("Not exist")
    return avg_sub


# ! perssonal average grades
def AverageGradeSubject_Personal(current_user):
    stu_obj=Student.objects.get(StudentID=current_user)
    sg_objs=StudentGrades.objects.filter(StudentID=stu_obj)

    sub_test={}
    for i in sg_objs:
        if i.Subject.SubjectName not in sub_test:
            sub_test[i.Subject.SubjectName]=[i.Grade]
        else:
            sub_test[i.Subject.SubjectName].append(i.Grade)

    sub_test_avg={}

    for i in sub_test:
        sub_test_avg[i]=round(sum(sub_test[i])/len(sub_test[i]), 2)
    return sub_test_avg


def AverageGradeAllPeople():
    sg_objs=StudentGrades.objects.all()

    sub_test={}
    for i in sg_objs:
        if i.Subject.SubjectName not in sub_test:
            sub_test[i.Subject.SubjectName]=[i.Grade]
        else:
            sub_test[i.Subject.SubjectName].append(i.Grade)

    sub_test_avg={}

    for i in sub_test:
        sub_test_avg[i]=round(sum(sub_test[i])/len(sub_test[i]), 2)
    return sub_test_avg


# ? for each testobject do the category counting
def TestWrongCategory(current_user, testobj):
    questions=testobj.TestSingleChoiceQues.all()
    print(testobj.TestName)
    true_ans=[]
    for i in questions:
        true_ans.append(SingleChoiceAnswer.objects.get(
            SingleChoiceID=i).SingleChoiceCorrect)

    st_ans_obj=StudentAnswer.objects.all().filter(
        StudentID=Student.objects.get(StudentID=current_user),
        TestID=testobj)
    st_ans=[i.Answer for i in st_ans_obj]
    st_tru=[SingleChoiceAnswer.objects.get(
        SingleChoiceID=i.SingleChoiceQues).SingleChoiceCorrect for i in st_ans_obj]

    category=[]
    print(st_tru)
    print(len(st_tru))
    print(st_ans)
    print(len(st_ans))

    if len(st_tru) == 0 or len(st_ans) == 0:
        return None
    for i in range(len(st_tru)):
        if st_tru[i] != st_ans[i]:
            category.append(
                st_ans_obj[i].SingleChoiceQues.SingleChoiceCategory)
          # ! key question content; val student ans
    print(category)

    summary_ori=dict(Counter(category))
    print(summary_ori)

    summary_ori=dict(
        sorted(summary_ori.items(), key=lambda item: item[1], reverse=True))

    return summary_ori
    # for i in range(len(true_ans)):
    #     if11
    # pass


def CategoryAnalysis(current_user):

    # ! sub_category_correct[subject] = [category,...]

    # ! sub_category_wrong[subject] = [category,...]
    sub_test={}
    for i in StudentGrades.objects.all().filter(StudentID=Student.objects.get(StudentID=current_user)):
        name=i.Subject.SubjectName
        if name not in sub_test:
            sub_test[name]=[i.TestID]
        else:
            sub_test[name].append(i.TestID)
    b=[]
    for key in sub_test:
        for t in sub_test[key]:
            b.append([t.TestSubject.SubjectName,
                      TestWrongCategory(current_user, t)])
    # ! For which subject, make the ranking of wrong choices category
    return b
    # StudentClass


def TestAnalysisMerge(listdic):
    print("==========================")

    print(listdic)
    b=listdic
    c=[]
    for i in listdic:
        if i[0] not in c:
            c.append(i[0])
    #  c = ['Data Structure A', 'Algorithm A']
    reach={}
    print(b)

    for i in range(1, len(b)):
        # if b[i][i]
        tmp=b[i-1][1]
        X, Y=Counter(b[i][1]), Counter(tmp)
        z=dict(X+Y)
        if b[i-1][0] not in reach:
            reach[b[i-1][0]]=z

        print(reach)
        # ! tobe continued
    return reach


def AnayReco(request, message):
    current_user=message
    current_user_obj=Student.objects.get(StudentID=current_user)
    # t = CategoryAnalysis(message)
    # all data for the past test

    b=CategoryAnalysis(current_user)
    c=TestAnalysisMerge(b)

    sublist=c.keys()
    print("-----------------")
    print(c)
    sub_data={}
    for i in c:
        sub_data[i]=[list(c[i].keys()), list(c[i].values())]
    print("-----------------")

    print(sub_data)
    ag_p=AverageGradeSubject_Personal(current_user)
    ag_a=AverageGradeAllPeople()
    return render(request, "onlinetest/anareco.html",
                  {"message": message,
                   "sub_data": sub_data,
                   "ag_p": ag_p,
                   "ag_a": ag_a
                   })
