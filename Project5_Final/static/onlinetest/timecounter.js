 
var timelimit = document.getElementById("timelimit").value;
console.log(timelimit)
var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");
var totalSeconds = 0;
setInterval(setTime, 1000);

function setTime() {

    var timelimit = document.getElementById("timelimit").value;
    var totalmins = totalSeconds / 60
    console.log(timelimit)
    var lim = timelimit * 60
    if (totalSeconds == lim) {
        alert(`TIMES UP, reach ${totalmins} minutes!`)
    }
    if (totalmins % timelimit > 1) {
        alert(`TIMES UP, reach ${totalmins} minutes!`)
    }
    document.getElementById("timelast").value = totalSeconds;
    ++totalSeconds;
    secondsLabel.innerHTML = pad(totalSeconds % 60);
    minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
    // console.log(document.getElementById("timelast").value)
}

function pad(val) {
    var valString = val + "";
    if (valString.length < 2) {
        return "0" + valString;
    } else {
        return valString;
    }
}
