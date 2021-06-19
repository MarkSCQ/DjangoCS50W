document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_mail);
  document.querySelector('#compose-form').addEventListener('submit', send_mail());

  // By default, load the inbox
  load_mailbox('inbox');
});
// Author:   https://github.com/MarkSCQ/


function compose_mail() {
  // ! Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-content').style.display = 'none';
  document.querySelector('#emails-bodycontent').style.display = 'none';
  // ! Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_mail(event) {
  event.preventDefault();
  var val_reci = document.querySelector('#compose-recipients').value;
  var val_subj = document.querySelector('#compose-subject').value;
  var val_body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: val_reci,
      subject: val_subj,
      body: val_body
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    });
}

function tableCreator(first, second, third) {

  var tbdy = document.createElement('table');
  tbdy.style.padding = "1px";
  tbdy.style.width = '800px';

  tbdy.style.borderCollapse = "collapse";
  var tr = document.createElement('tr');
  var td1 = document.createElement('td');
  var td2 = document.createElement('td');
  var td3 = document.createElement('td');

  td1.style.padding = "5px";
  td2.style.padding = "5px";
  td3.style.padding = "5px";
  td1.style.textAlign = "left";
  td2.style.textAlign = "left";
  td3.style.textAlign = "right";

  td1.style.width = '200px';
  td2.style.width = '300px';
  td3.style.width = '300px';

  td1.innerHTML = "<b>" + first + "</b>";
  td2.innerHTML = "<b>" + second + "</b>";
  td3.innerHTML = "<b>" + third + "</b>";
  tr.appendChild(td1);
  tr.appendChild(td2);
  tr.appendChild(td3);

  tbdy.appendChild(tr);
  return tbdy;
}


function load_mailbox(mailbox) {

  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails-content').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-bodycontent').style.display = 'none';
  document.querySelector('#emails-bodycontent').textContent = '';
  document.querySelector('#emails-content').textContent = '';
  // ! use if to judge mailbox name
  // ! what is fetch then response, how this data come
  fetch(`/emails/${mailbox}`, {
    method: 'get',
  })
    .then(response => response.json())
    .then(emails => {
      console.log(emails)
      // construct every email in the box
      emails.forEach(element => {
        console.log("----- Element -----")
        console.log(element["sender"]);
        console.log("----- Element -----")
        var divsender_label = document.createElement("div");
        sd = element['sender'];
        divsender_label.innerHTML = "<b>Sender</b>" + " :   " + sd;
        var divsubject_label = document.createElement("div");
        sb = element['subject'];
        divsubject_label.innerHTML = "<b>Subject</b>" + " :   " + sb;
        var divtimestamp_label = document.createElement("div");
        tm = element['timestamp'];
        divtimestamp_label.innerHTML = "<b>Time</b>" + " :   " + tm;

        var ddv = document.createElement("div");
        ddv.innerHTML += '&nbsp;';

        var ee = document.createElement('button');
        ee.id = element['id'];
        ee.className = "BTN_read";
        ee.className += " btn btn-sm btn-outline-primary";

        // ! three elements of the button people, title and time
        var first = "<b>" + sd + "</b>";
        var second = "<b>" + sb + "</b>";
        var third = "<b>" + tm + "</b>";
        var tabss = tableCreator(first, second, third);
        ee.appendChild(tabss);

        ee.style.border = "none";

        var divContainer = document.createElement('div');

        if (element["read"]) {
          ee.style.backgroundColor = "#B8B8B8";
        }
        if (element["read"] == "false") {
          ee.style.backgroundColor = "white";
        }
        divContainer.appendChild(ee);
        divContainer.appendChild(ddv);
        divContainer.appendChild(ddv);
        document.getElementById("emails-content").appendChild(divContainer);
        ee.addEventListener('click', () => email_contents(element['id'], mailbox));

      }
      );
    })
  // TODO make a if else to see which box I am going to use
}


function reply_mail(address_, date_, to_, title_, previous_content_) {
  /**
   * 1. doing hide and display
   * 2. prefill the contents with address and title
   * 3. Reply is another prefill format of compose
   */

  // ! hide and display
  // ! document.querySelector().style.display = "";
  document.querySelector("#emails-bodycontent").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  // ! prefill the contents with address and title
  const prefillString_address = "From: " + address_;
  const prefillString_date = "Date: " + date_;
  const prefillString_to = "To: " + to_
  const prefillString_title = "Subject: " + title_;
  const prefillString_previous_content = previous_content_;


  // ! \Pre-fill the body of the email with a line like "On Jan 1 2020, 12:00 AM foo@example.com wrote:" followed by the original text of the email.

  const prefillcontent = "On " + prefillString_date + " " + prefillString_to + " wrote: " + prefillString_previous_content
  document.querySelector("#compose-recipients").value = address_;
  document.querySelector("#compose-subject").value = "Re: " + title_;
  document.querySelector("#compose-body").value = prefillcontent + "";
}

// TODO include all elements in one email. 
// TODO from XXX; to XXX; when XXX; Reply btn; Archive Btn;
function email_contents(mailid, towhere) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-content').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-bodycontent').style.display = 'block';
  document.querySelector('#emails-bodycontent').textContent = '';

  // ! get one mail by id
  fetch('/emails/' + mailid, {
    method: "GET"
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);

      var send_jsn = document.createElement('div');
      send_jsn.innerHTML = "<b>Sender</b>" + " :   " + data["sender"];

      var rece_jsn = document.createElement('div');
      rece_jsn.innerHTML = "<b>Recipients</b>" + " :   " + data["recipients"];

      var subj_jsn = document.createElement('div');
      subj_jsn.innerHTML = "<b>Subject</b>" + " :   " + data["subject"];

      var body_jsn = document.createElement('div');
      body_jsn.innerHTML = "<b>Body</b>" + " :   " + data["body"];

      var time_jsn = document.createElement('div');
      time_jsn.innerHTML = "<b>Timestamp</b>" + " :   " + data["timestamp"];

      var sbreply = document.createElement('button');
      sbreply.innerHTML = "Reply";
      sbreply.className = "replybtn";
      sbreply.className += " btn btn-sm btn-outline-primary";

      var sbarchive = document.createElement('button');
      sbarchive.name = "archive_btn"
      if (data.archived == true) {
        sbarchive.innerHTML = "Unarchive";
      }
      else {
        sbarchive.innerHTML = "Archive";
      }
      sbarchive.className = "archivebtn";
      sbarchive.className += " btn btn-sm btn-outline-primary";

      var division = document.createElement('div');
      division.appendChild(send_jsn);
      division.appendChild(rece_jsn);
      division.appendChild(subj_jsn);
      division.appendChild(time_jsn);
      division.appendChild(body_jsn);
      var divAr = document.createElement("div");
      var divRp = document.createElement("div");
      divAr.append(sbarchive);
      divRp.append(sbreply);
      if (towhere != "sent") {
        var table_ = document.createElement("table");
        var tr = document.createElement("tr")
        var td1 = document.createElement("td");
        var td2 = document.createElement("td");
        td1.appendChild(divAr)
        td2.appendChild(divRp)
        tr.appendChild(td1)
        tr.appendChild(td2)
        table_.appendChild(tr)
        document.getElementById("emails-bodycontent").appendChild(table_);
      }

      document.getElementById("emails-bodycontent").appendChild(division);
      sbreply.addEventListener("click", () =>
        reply_mail(data["sender"], data["timestamp"], data["recipients"], data["subject"], data["body"])
      );
      sbarchive.addEventListener("click", () => {

        fetch('emails/' + mailid, {
          method: "PUT",
          body: JSON.stringify({
            archived: !data["archived"]
          })
        }).then(() => {
          load_mailbox('inbox');
        });
      });
    });
  fetch('/emails/' + mailid, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  });
}
