"use strict";

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#allposts').addEventListener('click', function () {
    return sbPostProcess();
  });
  document.querySelector('#following').addEventListener('click', function () {
    return sbFollingProcess();
  });
  document.querySelector('#profile').addEventListener('click', function () {
    return sbMyProfileProcess();
  }); // document
  //     .querySelector('#make_post')
  //     .addEventListener('click', sbMakePostProcess);

  document.querySelector('#postToStore').addEventListener('submit', sendPost);
});

function sendPost(event) {
  // event.preventDefault();
  var postcontent = document.querySelector("#POST_content").value;
  console.log(postcontent); // debugger

  fetch("/makeposts", {
    method: "POST",
    body: JSON.stringify({
      postcontent: postcontent
    })
  }).then(function (response) {
    return response.json();
  }).then(function (result) {
    console.log(result);
  })["catch"](function (error) {
    return console.log(error);
  });
  event.preventDefault();
  return false;
}

function tablecreator(post_name, post_time, post_content, post_id) {
  var tbdy = document.createElement("table");
  var tr1 = document.createElement("tr");
  var td1 = document.createElement("td");
  td1.innerHTML = ("<b>" + post_name + "</b>").fontsize(6);
  tr1.appendChild(td1);
  var tr2 = document.createElement("tr");
  var td2 = document.createElement("td");
  td2.innerHTML = post_content.fontsize(5);
  tr2.appendChild(td2);
  var tr3 = document.createElement("tr");
  var td3 = document.createElement("td");
  td3.innerHTML = post_time.fontsize(2);
  tr3.appendChild(td3);
  tbdy.appendChild(tr1);
  tbdy.appendChild(tr2);
  tbdy.appendChild(tr3);
  return tbdy;
}

function getAllPosts() {
  document.getElementById("posts_display").innerHTML = '';
  document.getElementById("profile_display").innerHTML = ''; // document.getElementById("user_following").innerHTML = '';
  // document.getElementById("user_followers").innerHTML = '';

  fetch("/getAllPosts").then(function (response) {
    return response.json();
  }).then(function (records) {
    records.forEach(function (record) {
      console.log("--------------------------");
      console.log(record.postid);
      console.log(record.post_owner);
      console.log(record.post_date);
      console.log(record.post_content);
      console.log(record.post_state);
      console.log("--------------------------");
      var post_owner = record.post_owner;
      var post_date = record.post_date;
      var post_content = record.post_content;
      var post_id = record.postid;
      var ddv = document.createElement("div");
      ddv.innerHTML += '&nbsp;';
      var tb = tablecreator(post_owner, post_date, post_content, post_id);
      var divHolder = document.createElement("div");
      divHolder.appendChild(tb);
      divHolder.appendChild(ddv);
      var btn_like = document.createElement("button");
      btn_like.value = record.postid;
      btn_like.innerHTML = "Like!";
      var hrr = document.createElement("hr");
      hrr.style.width = "600px"; // add one function to bind user name
      //   make profile_display div here
      //  use one function to wrap all the contents

      divHolder.addEventListener("click", function () {
        return sbProfileDisplayDiv(post_owner);
      }); // add one function to bind like or dislike        

      btn_like.addEventListener("click", function () {
        console.log("LIKE!");
      });
      document.getElementById("posts_display").appendChild(divHolder);
      document.getElementById("posts_display").appendChild(btn_like);
      document.getElementById("posts_display").appendChild(hrr);
    }); // console.log("This is getallposts() we get him");
    // console.log(records);
    // console.log("This is getallposts() we get him");
    // div width 450
    // |---------------------------------|
    // |Name                             |
    // |Time                             |
    // |Content                          |
    // |Like                             |
    // |---------------------------------|
  })["catch"](function (error) {
    return console.error(error);
  });
}

function newPost() {}

function editMyPost(oldContent, postId) {// set all other div to none and set itself block
  // add listen to submit button
  //
  // document.getElementById("modify_post_content").value = oldContent;
  // fetch content and post_id to function in view
  // modify_post
}

function getMyProfile() {
  document.getElementById("profile_display").innerHTML = '';
  document.getElementById('modify_post').style.display = 'block';
  fetch("/getProfile_mine").then(function (response) {
    return response.json();
  }).then(function (records) {
    console.log(records);
    var userPosts = tablePosts(records["postmine"]);
    var userFollowing = tableFollow(records["following"], "Following");
    var userFollower = tableFollow(records["followers"], "Followers"); // var editPost = document.createElement("button");
    // editMyPost.addEventListener("click",()=>
    // {
    //     editMyPost()
    // })
    // var divEditPost = document.createElement("div");

    var divtfollowing = document.createElement("div");
    var divtfollower = document.createElement("div");
    var divtposts = document.createElement("div");
    divtposts.appendChild(userPosts);
    divtfollowing.appendChild(userFollowing);
    divtfollower.appendChild(userFollower); // divEditPost.appendChild(editPost);

    document.getElementById("profile_display").appendChild(divtposts);
    document.getElementById("profile_display").appendChild(divtfollowing);
    document.getElementById("profile_display").appendChild(divtfollower);
  });
} // FIXME add one button in this function to help with edit 


function tablePosts(posts) {
  var divholder = document.createElement("div");

  for (i = 0; i < posts.length; i++) {
    var tableBody = document.createElement("table");
    tableBody.style.width = '600px';
    var tr = document.createElement("tr");
    var td1 = document.createElement("td");
    td1.innerHTML = posts[i]["post_content"].fontsize(5);
    td1.style.textAlign = "left";
    var tr1 = document.createElement("tr");
    var td2 = document.createElement("td");
    td2.innerHTML = posts[i]["post_date"].fontsize(2);
    td2.style.textAlign = "right";
    tr.appendChild(td1);
    tr1.appendChild(td2);
    tableBody.appendChild(tr);
    tableBody.appendChild(tr1);
    var fgl = document.createElement("hr");
    fgl.style.width = "600px";
    divholder.appendChild(tableBody);
    divholder.appendChild(fgl);
  }

  return divholder;
}

function tableFollow(follow) {
  var msg = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : "";
  var tableBody = document.createElement("table");
  var tr = document.createElement("tr");
  var td = document.createElement("td");

  if (follow.length == 0) {
    if (msg == "Following") {
      td.innerHTML = "No Following";
    }

    if (msg == "Follower") {
      td.innerHTML = "No Follower";
    }

    tr.appendChild(td);
    tableBody.appendChild(tr);
  } else {
    td.innerHTML = msg;
    tr.appendChild(td);
    tableBody.appendChild(tr);

    for (i = 0; i < follow.length; i++) {
      var tr = document.createElement("tr");
      var td = document.createElement("td");
      td.innerHTML = follow[i];
      tr.appendChild(td);
      tableBody.appendChild(tr);
    }
  }

  return tableBody;
}

function recordsCastHtml(records) {
  var user_name = records["user"];
  var userPosts = records["postmine"];
  var userFollowing = records["following"];
  var userFollower = records["followers"];
  console.log("userFollowing ".concat(userFollowing.length));
  console.log("userFollower ".concat(userFollower.length));
  console.log("user_name ".concat(user_name)); // use table to hold small shit like posts following and follower

  var tablefollowing = tableFollow(userFollowing, "Following");
  var tablefollower = tableFollow(userFollower, "Follower");
  var tableposts = tablePosts(userPosts);
  var divtfollowing = document.createElement("div");
  var divtfollower = document.createElement("div");
  var divtposts = document.createElement("div");
  divtfollowing.appendChild(tablefollowing);
  divtfollower.appendChild(tablefollower);
  divtposts.appendChild(tableposts);

  if (String(document.getElementById("nav_uername").innerHTML) != String(user_name)) {
    var divuname = document.createElement("div");
    divuname.innerHTML = ("<b>" + user_name + "</b>").fontsize(6);
    document.getElementById("profile_display").appendChild(divuname); // console.log(`nav user anme    ${document.getElementById("nav_uername").innerHTML}`)
  }

  document.getElementById("profile_display").appendChild(divtposts);
  document.getElementById("profile_display").appendChild(divtfollowing);
  document.getElementById("profile_display").appendChild(divtfollower);
}

function sbProfileDisplayDiv(username) {
  console.log("username: ".concat(username));
  document.getElementById("profile_display").style.display = "block";
  document.querySelector("#profile_display").innerHTML = ''; // document.querySelector("#user_following").innerHTML = '';
  // document.querySelector("#user_followers").innerHTML = '';

  document.getElementById("posts_display").style.display = "none";
  fetch("/getProfile/".concat(username)).then(function (response) {
    return response.json();
  }).then(function (records) {
    console.log(records);
    console.log("--------------------------");
    console.log(records["user"]);
    console.log(records["following"]);
    console.log(records["followers"]);
    console.log(records["postmine"]);
    console.log("--------------------------"); // cast all these shit to html page

    recordsCastHtml(records);
  });
}

function sbPostProcess() {
  document.getElementById("testdiv").innerHTML = '';
  document.getElementById('make_post').style.display = 'block';
  document.getElementById('posts_display').style.display = 'block';
  document.getElementById('profile_display').style.display = 'none';
  document.getElementById('following_display').style.display = 'none';
  document.getElementById('modify_post').style.display = 'none';
  document.getElementById('testdiv').innerHTML = "posting";
  getAllPosts();
}

function sbFollingProcess() {
  document.getElementById("testdiv").innerHTML = '';
  document.getElementById('make_post').style.display = 'none';
  document.getElementById('posts_display').style.display = 'none';
  document.getElementById('profile_display').style.display = 'none';
  document.getElementById('following_display').style.display = 'block';
  document.getElementById('modify_post').style.display = 'none';
  document.getElementById('testdiv').innerHTML = "following";
}

function sbMyProfileProcess() {
  document.getElementById("testdiv").innerHTML = '';
  document.getElementById('make_post').style.display = 'none';
  document.getElementById('posts_display').style.display = 'none';
  document.getElementById('profile_display').style.display = 'block';
  document.getElementById('following_display').style.display = 'none';
  document.getElementById('modify_post').style.display = 'none';
  document.getElementById('testdiv').innerHTML = "profile";
  getMyProfile(); // cast all these shit to html page
} //комбат
// function sbMakePostProcess() {
//     // Show compose view and hide other views
//     document.getElementById("testdiv").innerHTML = '';
//     document.getElementById("POST_textarea").innerHTML = '';
//     document.getElementById('make_post').style.display = 'block';
//     document.getElementById('posts_display').style.display = 'block';
//     document.getElementById('profile_display').style.display = 'none';
//     document.getElementById('following_display').style.display = 'none';
//     document.getElementById('testdiv').innerHTML = "posting";
// }
// textarea("make_post", true);

/*
            Here I am going to give an example to explain what sharpely value is.
            Assuming there are three coders in my group, two boys 1 and 2, one girl 3.
            lets say 1 is new to coding, he just learned coding for 3 years,
            but has protential when coding with beaufitul girls he works more efficiently,
            2 has been coding for 5 years, and knows a lot
            3 is freshman, and knows little.
            both these two boys has no girlfirend, which is sad. and they want to behave better in front of the girl 3
            Lets define a function v(C) denotes the contribution
            when they works alone, their contribution to the project is described as v({1}) = 100  v({2}) = 125  v({3})= 50
            however, when 1 works with 2, v({1,2})=375, which improves a lot
            when 2 works with 3 v({2,3}) = 370, also improves a lot
            when 1 works with 2 v({1,2}) = 270
            when they work together v({1,2,3}) = 500

            and now there existing 6 kinds of cooperations
            1. boy 1 invites boy 2 and then invite girl 3
            2. boy 1 invites girl 3 and then invite boy 2
            3. boy 2 invites boy 1 and then invite girl 3
            4. boy 2 invites girl 3 and then invite boy 1
            5. girl 3 invites boy 1 and then invite boy 2
            6. girl 3 invites boy 2 and then invite boy 1

            and after finishing the project, they will get rewards from their boss.
            What we are going to do is calculate the each person's contribution to the project based on what we have above
            Here I am going to use contribution margin to calculation contribution of these people.


            accroding this table, we can get average contribution of each person
            and contribution's percentage to total contribution V({1,2,3})=500
            boy 1 is 970/6      32.2%
            boy 2 is 970/6      32.2%
            girl 3 is 1060/6    35.3%


            （Acknowledge: Dr. Ka Lok Man from XJTLU）

*/