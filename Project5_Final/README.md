Free Self-Evaluation System

The mainly used files are under folder onlinetest which is also the app I created for the project. This project is aiming at helping school and students doing online self evaluation for students daily study. 

<b>The system provides four main functions</b> 
<ol>
<li>The main page provided four functions. Each of items has a collapsiable button and details can be obtained by using it. We also provide a table of tests that are available to students.</li>

<li>First function - doing self evaluation of each subject. The self evaluation is functioned as test, single choice questions. In the test, we provide a simple clock implemented by using Javascript and this clock will inform that times up. But it will not force student to submit since this is functioned as self evaluation. We set the time for each test, and student can set test time when using randomly generation in 3. After each test got finished, the test will have a grade for the student. Student can redo the test no matter how many times they want since this is provided for self-evaluation, not for test usage.</li>

<li>Second function - reviewing the history tests. The reviewing will cover subject, test name, finishing date and grades. Student can see all test records they did in the past in this section and they can alo review the test contents and explanation of the each question in their test by clicking the explanations. We also use some emoji to describe how student behave and use the emoji to mark the question are correct or wrong.</li>

<li>Third Function - randomly generating tests. Student can randomly generate new test for self-evaluation to make up the knowledge. The questions will be randomly chosen for the database which is maintained by school administrators. This section uses Casacade Design in order to limit the errors when making choices, trying to reduce probabilities of error choices.</li>

<li>Fourth Function - simple analysis for test. The analysis gives out the data of students' grade to show their performanc. Since each question of each subject has some key point knowledge and we considered them as category. For example knowledge a is category_a. If student has some many category_a in the table and plot, this dentoes they do not have a good knowledge of knwoleege a. And we make a summary of which key point of knowledge they are not good at -- by using the amount of question of wrong answer from students. We also provide the average grades of student himself/herself and all studnets' average grades in order to let student know where they are at</li>

<li>We also make the mobile responsive for some pages that need this function.</li>
</ol>


<b>File Information Templates</b> 
<ul>
<li>templates/onlinetests/anareco.html: Function Analysis</li>
<li>templates/onlinetests/exam.html: Function Exam Display</li>
<li>templates/onlinetests/generatenewtest.html: Function Generate Random New Test</li>
<li>templates/onlinetests/index.html: Function Login Page</li>
<li>templates/onlinetests/layout.html: Function Layout for Extension Usage</li>
<li>templates/onlinetests/review.html: Function Review Page</li>
<li>templates/onlinetests/student_exam.html: Function Exam List Page</li>
<li>templates/onlinetests/student_review.html: Function Review List Page</li>
<li>templates/onlinetests/student.html: Function Student Main Page</li>
</ul>

<b>File Information Static</b> 
<ul>
<li>static/auctions/bulma.css  Version 1 CSS file, not used</li>
<li>static/auctions/styles.css Version 1 CSS file, not used</li>
</ul>

<b>File Information Static</b> 
<ul>
<li>static/js/echarts.js Echartjs Complete Version</li>
</ul>

<b>File Information Static</b> 
<ul>
<li>static/onlinetest/echarts.min.js Mainly Used for Plotting in Analysis</li>
<li>static/onlinetest/generatenewtest.js Userd for Test Generations Casacade Design</li>
<li>static/onlinetest/review.js Collapsiable Button</li>
<li>static/onlinetest/student.js Collapsiable Button</li>
<li>static/onlinetest/timecounter.js Clock for Self-Evaluation</li>
</ul>


<b>How to Run:</b><br>
python3 manage.py runserver<br>
Test User:15210101 Passwd:123456<br>

<b>Environment:</b><br>
Windows 10, WSL2 Ubuntu 20.04<br>




