var currentevent;
var currenteventno;
var answercolors;
  
var quizstr = '<div style="float:right;"><input onclick="EvaluerQuiz()" name="Submit" type="button" id = "submit" value="Se rigtige svar"/></div>'

var pausestr = '<div style="float:right;"><input onclick="PauseAndThink()" name="Submit" type="button" id = "submit" value="Ok, forstået."/></div>'



    

function SetCurtain(){
    document.getElementById("overlay").style.display = "block";
}

function RemoveCurtain(){
    document.getElementById("overlay").style.display = "none";
}


function PauseAndThink(){
    RemoveCurtain();
    myVideo.play();
}

function EvaluerQuiz(){
    answercolors = currentevent[2];
    for(i = 0; i < answercolors.length; i++)
	document.getElementById("ans"+i).style.color = answercolors[i];
    RemoveCurtain();
};

var myVideo = document.getElementById("video1"); 

myVideo.ontimeupdate = function(){EventHandler()};
myVideo.onplay = function(){PlayHandler()};
myVideo.onseeking = function(){EventSeekHandler()};


function PlayHandler(){
    for(i = 0; i < answercolors.length; i++){
	document.getElementById("ans"+i).style.color = "black";
        document.getElementById("yo"+i).checked = false;		   
    }
}
		   
		   
var currenteventno = -1;

function EventHandler(){

    var tid = myVideo.currentTime, i;
    var txt;
    
    for(i = eventtimes.length-1; i>= 0; i--){
	if(tid >= eventtimes[i])
	    break;
    }

    if (i == currenteventno)
	return;

    currenteventno = i;
    currentevent = events[currenteventno];
    txt = currentevent[1];

    if (currentevent[0] == "quiz")
        txt = quizstr + txt;

    if (currentevent[0] == "remarkpause")
	txt = pausestr + txt;
    
    document.getElementById("expl").innerHTML = txt;

    if (currentevent[0] == "quiz" || currentevent[0] == "remarkpause"){
	SetCurtain();
	myVideo.pause();
    }

    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}

function EventSeekHandler(){

    var tid = myVideo.currentTime, i;
    var txt;
    
    for(i = eventtimes.length-1; i>= 0; i--){
	if(tid >= eventtimes[i])
	    break;
    }

    if (i == currenteventno)
	return;

    currenteventno = i;
    currentevent = events[currenteventno];
    txt = currentevent[1];

    if (currentevent[0] == "quiz")
        txt = quizstr + txt;

    if (currentevent[0] == "remarkpause")
	txt = pausestr + txt;


    
    document.getElementById("expl").innerHTML = txt;

    if (currentevent[0] == "quiz" || currentevent[0] == "remarkpause"){
	myVideo.pause();
    }

    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}


