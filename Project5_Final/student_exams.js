 // var bt = document.getElementsByClassName("setclick");
// console.log(bt)
// set buttons clickable or not
// TestButtonControlor();

function TestButtonControlor() {
    // var arr = Array.from(document.getElementsByClassName("setclick"));
    var arr = document.getElementsByClassName("setclick");
    console.log(arr[0].value)

    console.log(arr.length)

    for (var i = 0; i < arr.length; i++) {
        console.log(arr[i].id)
        console.log(arr[i])
        if (arr[i].value === "FINISHED") {
            document.getElementById(arr[i].id).disabled = true;
        }
        else {
            document.getElementById(arr[i].id).disabled = false;

        }

    }
}

function TimeChecker() {
    var timestrings = document.getElementsByClassName("test_time")
    var dateString = "2010-08-09 01:02:03";
    var reggie = /(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})/;
    var dateArray = reggie.exec(dateString);
    var dateObject = new Date(
        (+dateArray[1]),
        (+dateArray[2]) - 1, // Careful, month starts at 0!
        (+dateArray[3]),
        (+dateArray[4]),
        (+dateArray[5]),
        (+dateArray[6])
    );
}