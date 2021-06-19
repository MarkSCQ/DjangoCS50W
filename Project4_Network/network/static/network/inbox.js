document.addEventListener('DOMContentLoaded', function () {
    document
        .querySelector('#allposts')
        .addEventListener('click', () => sbPostProcess());
    document
        .querySelector('#following')
        .addEventListener('click', () => sbFollingProcess());
    document
        .querySelector('#profile')
        .addEventListener('click', () => sbMyProfileProcess());

    // document
    //     .querySelector('#make_post')
    //     .addEventListener('click', sbMakePostProcess);
    document
        .querySelector('#postToStore')
        .addEventListener('submit', sendPost);

    document
        .querySelector('#modify_post')
        .addEventListener('submit', updatePost);
});


function sendPost(event) {
    // event.preventDefault();
    const postcontent = document.querySelector("#POST_content").value;
    console.log(postcontent);
    // debugger
    fetch("/makeposts", {
        method: "POST",
        body: JSON.stringify({
            postcontent: postcontent,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
        })
        .catch((error) => console.log(error));
    event.preventDefault();
    return false;
}

function tablecreator(post_name, post_time, post_content, post_id) {
    var tbdy = document.createElement("table");
    var tr1 = document.createElement("tr");
    var td1 = document.createElement("td");
    td1.innerHTML = ("<b>" + post_name + "</b>").fontsize(6);
    tr1.appendChild(td1)
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

function processLike(postid) {
    var inival = (document.getElementById(`button_${postid}`).value === 'true');
    console.log(`current state ${inival}`);
    // console.log(`postid ${postid}`);
    debugger
    fetch(`/postLike/${postid}`, {
        method: "PUT",
        body: JSON.stringify({
            likestate: !(inival),
        })
    })
        .then((response) => response.json())
        .then((result) => {
            // debugger
            // console.log(result);
            var stateServer = result["current_state"];
            var buttonname = "button_" + postid;
            var txtname = "like_" + postid;
            if (stateServer == true) {
                document.getElementById(buttonname).style.backgroundColor = "#008CBA";
                document.getElementById(buttonname).style.color = "White";
                document.getElementById(buttonname).value = "true";
                var counter = parseInt(document.getElementById(txtname).innerHTML);

                document.getElementById(txtname).innerHTML = (counter + 1);
            }
            else {
                document.getElementById(buttonname).style.backgroundColor = "White";
                document.getElementById(buttonname).style.color = "Black";
                var counter = parseInt(document.getElementById(txtname).innerHTML);
                document.getElementById(buttonname).value = "false";

                document.getElementById(txtname).innerHTML = (counter - 1);
            }
            // getAllPosts()
        })
        .catch((error) => {
            console.log(error);
            console.log(postid);
        });
}

function likeCounter(arr) {
    return arr.length;
}

function getAllPosts() {
    document.getElementById("posts_display").innerHTML = '';
    document.getElementById("profile_display").innerHTML = '';

    fetch("/getAllPosts")
        .then((response) => response.json())
        .then((records) => {
            records.forEach(record => {
                // console.log("--------------------------")
                // console.log(record.postid);\
                // console.log(record.post_owner);
                // console.log(record.post_date);
                // console.log(record.post_content);
                // console.log(record.post_state);
                // console.log("--------------------------")
                // console.log(record);
                // since it uses DNN then there existing some errors like side faces or side profiles MTCNN cannot recognize
                // the error rate is 45/1089

                const post_owner = record.post_owner;
                const post_date = record.post_date;
                const post_content = record.post_content;
                const post_id = record.postid;
                var ddv = document.createElement("div");
                ddv.innerHTML += '&nbsp;';
                var likes = likeCounter(record.post_likers);
                console.log(`likes ${post_id}  ${likes}`);
                var tb = tablecreator(post_owner, post_date, post_content, post_id)
                var divHolder = document.createElement("div");
                divHolder.appendChild(tb);
                divHolder.appendChild(ddv);
                var plike = document.createElement("p");
                plike.id = `like_${post_id}`;
                plike.innerHTML = `${likes}`;
                var pwords = document.createElement("p");
                pwords.innerHTML = " people like this post."
                var btn_like = document.createElement("button");
                btn_like.id = `button_${post_id}`;
                btn_like.value = record.curr_like;
                btn_like.innerHTML = "Like!";
                var hrr = document.createElement("hr");
                hrr.style.width = "600px";
                // add one function to bind user name
                //  make profile_display div here
                //  use one function to wrap all the contents
                divHolder.addEventListener("click", () => sbProfileDisplayDiv(post_owner))

                // add one function to bind like or dislike        
                btn_like.addEventListener("click", () => {
                    console.log("LIKE!");
                    console.log(record.postid);
                    // processLike(post_id, record.curr_like);
                    processLike(post_id);

                    // getAllPosts()
                })
                // console.log(record.curr_like);

                var current_user = document.getElementById("nav_username").innerHTML;
                if (record.curr_like == true) {
                    console.log(`${current_user} in postlikers`);
                    btn_like.style.backgroundColor = "#008CBA";
                    btn_like.style.color = "White";
                }
                // console.log(`${record.post_likers}`);

                var likesection = document.createElement("div");
                var divlikespeople = document.createElement("div");
                plike.style.display = "inline";
                pwords.style.display = "inline";

                divlikespeople.appendChild(plike);
                divlikespeople.appendChild(pwords);

                likesection.appendChild(btn_like);
                likesection.appendChild(divlikespeople);
                document.getElementById("posts_display").appendChild(divHolder);
                document.getElementById("posts_display").appendChild(likesection);
                document.getElementById("posts_display").appendChild(hrr);
            });

            // |---------------------------------|
            // |Name                             |
            // |Time                             |
            // |Content                          |
            // |Like                             |
            // |---------------------------------|
        })
        .catch((error) => console.error(error));
}

function updatePost(event) {
    // delete the old one 
    const postid = String(document.querySelector("#modify_post_ID").value);
    const newcontent = document.querySelector("#modify_post_content").value;
    console.log(postid);
    console.log(newcontent);

    fetch("/postupdate", {
        method: "POST",
        body: JSON.stringify({
            postID: postid,
            postcontent: newcontent,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
        })
        .catch((error) => {
            console.log(error);
            console.log(postid);
            console.log(newcontent);
        });
    event.preventDefault();

    return false;
}


function editMyPost(oldContent, postID) {
    console.log(`content   ${oldContent}`)
    // console.log(`id   ${postId}`)
    document.getElementById("make_post").style.display = "none";
    document.getElementById("following_display").style.display = "none";
    document.getElementById("posts_display").style.display = "none";
    document.getElementById("profile_display").style.display = "none";
    document.getElementById("testdiv").style.display = "none";
    document.getElementById("modify_post").style.display = "block";

    document.getElementById("modify_post_content").value = String(oldContent);
    document.getElementById("modify_post_ID").value = postID;

    // delete the item with POST ID 

}


function getMyProfile() {
    document.getElementById("profile_display").innerHTML = '';
    // document.getElementById('modify_post').style.display = 'block';
    fetch("/getProfile_mine")
        .then((response) => response.json())
        .then((records) => {
            console.log(records);
            // use one local for loop to display all contents in
            // records["postmine"]
            var userPosts = records["postmine"];
            console.log("===========================");
            console.log(userPosts);
            console.log("===========================");

            var postsHolder = document.createElement("div");
            for (i = 0; i < userPosts.length; i++) {
                var onePostTable_DIV = document.createElement("div");
                var tbls = onePost(userPosts[i]);
                onePostTable_DIV.appendChild(tbls);
                postsHolder.appendChild(onePostTable_DIV);
            }
            var userFollowing = tableFollow(records["following"], "Following");
            var userFollower = tableFollow(records["followers"], "Followers");
            // var editPost = document.createElement("button");
            // editMyPost.addEventListener("click",()=>
            // {
            //     editMyPost()
            // })
            // var divEditPost = document.createElement("div");
            var divtfollowing = document.createElement("div");
            var divtfollower = document.createElement("div");
            var divtposts = document.createElement("div");
            divtposts.appendChild(postsHolder);
            divtfollowing.appendChild(userFollowing);
            divtfollower.appendChild(userFollower);

            // divEditPost.appendChild(editPost);
            document.getElementById("profile_display").appendChild(divtposts);
            document.getElementById("profile_display").appendChild(divtfollowing);
            document.getElementById("profile_display").appendChild(divtfollower);

        });
}


// FIXME click one item and then prefit the modify_post form 
// use one function to make one post, one post is one table. do no tmake them together
function tablePosts(posts) {
    var divholder = document.createElement("div")

    for (i = 0; i < posts.length; i++) {
        var tableBody = document.createElement("table");
        tableBody.style.width = '600px';
        var tr = document.createElement("tr");
        var td1 = document.createElement("td");
        var td1_1 = document.createElement("td");
        td1.innerHTML = (posts[i]["post_content"]).fontsize(5);
        td1.style.textAlign = "left";
        tr.appendChild(td1);
        var pct = posts[i]["post_content"];
        var pid = posts[i]["postid"];
        var editbutton = document.createElement("button");
        editbutton.innerHTML = "EDIT";
        td1_1.innerHTML = editbutton;
        editbutton.addEventListener("click", () => editMyPost(pct, pid));

        if (String(document.getElementById("nav_uername").innerHTML) != posts[i]["post_owner"]) {
            editbutton.style.display = "none";
        }
        else {
            tr.appendChild(editbutton);
        }
        var tr1 = document.createElement("tr");
        var td2 = document.createElement("td");
        td2.innerHTML = (posts[i]["post_date"]).fontsize(2);
        td2.style.textAlign = "right";

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


function onePost(apost) {
    console.log("-----------------------------------")
    console.log(apost)
    console.log("-----------------------------------")

    var tableBody = document.createElement("table");
    tableBody.style.width = '600px';
    var tr = document.createElement("tr");
    var td1 = document.createElement("td");
    var td1_1 = document.createElement("td");
    console.log(apost)
    td1.innerHTML = (String(apost["post_content"])).fontsize(5);
    td1.style.textAlign = "left";
    tr.appendChild(td1);
    var pct = apost["post_content"];
    var pid = apost["postid"];
    var editbutton = document.createElement("button");
    editbutton.innerHTML = "EDIT";
    td1_1.innerHTML = editbutton;
    editbutton.addEventListener("click", () => editMyPost(pct, pid));
    if (String(document.getElementById("nav_username").innerHTML) != String(apost["post_owner"])) {
        editbutton.style.display = "none";
    }
    else {
        tr.appendChild(editbutton);
    }

    var tr1 = document.createElement("tr");
    var td2 = document.createElement("td");
    td2.innerHTML = (String(apost["post_date"])).fontsize(2);
    td2.style.textAlign = "right";

    tr1.appendChild(td2);
    tableBody.appendChild(tr);
    tableBody.appendChild(tr1);
    var fgl = document.createElement("hr");
    fgl.style.width = "600px";
    // divholder.appendChild(tableBody);
    // divholder.appendChild(fgl);
    var divholder = document.createElement("div");
    divholder.appendChild(tableBody);
    return divholder;
}


function tableFollow(follow, msg = "") {
    var tableBody = document.createElement("table")
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
    }
    else {
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
    console.log(`userFollowing ${userFollowing.length}`)
    console.log(`userFollower ${userFollower.length}`)
    console.log(`user_name ${user_name}`)

    // use table to hold small shit like posts following and follower
    var tablefollowing = tableFollow(userFollowing, "Following");
    var tablefollower = tableFollow(userFollower, "Follower");
    // FIXME use a for loop to iterate all the contents in the userPosts
    // then put all small tables in the div
    var postsHolder = document.createElement("div");
    // console.log(userPosts)

    for (i = 0; i < userPosts.length; i++) {
        var onePostTable_DIV = document.createElement("div");
        var tbls = onePost(userPosts[i]);
        onePostTable_DIV.appendChild(tbls);
        postsHolder.appendChild(onePostTable_DIV);
    }

    // var tableposts = tablePosts(userPosts);

    var divtfollowing = document.createElement("div");
    var divtfollower = document.createElement("div");
    var divtposts = document.createElement("div");


    divtfollowing.appendChild(tablefollowing);
    divtfollower.appendChild(tablefollower);
    divtposts.appendChild(postsHolder);

    if (String(document.getElementById("nav_username").innerHTML) != String(user_name)) {

        var divuname = document.createElement("div");
        divuname.innerHTML = ("<b>" + user_name + "</b>").fontsize(6);
        document.getElementById("profile_display").appendChild(divuname);
        // console.log(`nav user anme    ${document.getElementById("nav_uername").innerHTML}`)
    }
    document.getElementById("profile_display").appendChild(divtposts);
    document.getElementById("profile_display").appendChild(divtfollowing);
    document.getElementById("profile_display").appendChild(divtfollower);
}


function sbProfileDisplayDiv(username) {
    console.log(`username: ${username}`);
    document.getElementById("profile_display").style.display = "block";
    document.querySelector("#profile_display").innerHTML = '';
    // document.querySelector("#user_following").innerHTML = '';
    // document.querySelector("#user_followers").innerHTML = '';
    document.getElementById("posts_display").style.display = "none";
    fetch(`/getProfile/${username}`)
        .then((response) => response.json())
        .then((records) => {
            console.log(records);
            console.log("--------------------------");
            console.log(records["user"]);
            console.log(records["following"]);
            console.log(records["followers"]);
            console.log(records["postmine"]);
            console.log("--------------------------");
            // cast all these shit to html page
            recordsCastHtml(records);
        })
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
    getMyProfile();
    // cast all these shit to html page
}


//комбат


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
/*1
*/