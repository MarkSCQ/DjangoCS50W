var subjects = document.getElementById("subjects");
var testnames = document.getElementById("testnamediv")


subjects.addEventListener("change", function () {
    var tnv = document.getElementById("subjects").value;
    var sbs = document.getElementsByClassName("subselect")

    console.log(tnv)
    console.log(sbs)
    for (var i = 0; i < sbs.length; i++) {
        console.log(sbs[i].id)
        if (tnv == sbs[i].id) {
            document.getElementById(sbs[i].id).style.display = "block";
            document.getElementById(`testname-${sbs[i].id}`).required = true;
        }
        else {
            document.getElementById(sbs[i].id).style.display = "none";
            document.getElementById(`testname-${sbs[i].id}`).required = false;

        }
    }
    // document.querySelector("#testnamediv").style.display = "block"
});





// activities.addEventListener("change", function() {
//     if(activities.value == "addNew")
//     {
//         addActivityItem();
//     }
//     console.log(activities.value);
// });

// function addActivityItem() {
//     alert("Adding an item");

//     var option = document.createElement("option");
//     option.value = "test";
//     option.innerHTML = "test";

//     activities.appendChild(option);
// }
