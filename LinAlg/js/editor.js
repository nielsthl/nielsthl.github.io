var filnavn;
var renderevent = 0;
var delayrender = 3000; // 3 sec delay on rendering


function renderLaTeX(texinput){
    
    $.ajax({
	//url : "http://146.185.175.81/eduitech/ilatex/",
        url : "/django/ilatex/",
	//url : "/ilatex/",
	type : "POST", 
	data : { //csrfmiddlewaretoken : csrftoken, 
	    inputstr : texinput},
	dataType : "json"
    }).done(function( result ) {
	$('#rendered').html(result.html);
	refreshRender(); // Render KaTeX
	PR.prettyPrint(); // Render prettyprint code
    });
}


// Live rendering

silentKeys = [
    "Shift",
    "Control",
    "ArrowUp", "ArrowRight", "ArrowDown", "ArrowLeft",
    "PageUp",
    "PageDown"
    ]

$("#texinput").keyup(function(e){

    if (silentKeys.indexOf(e.key) > -1)
	return
    
    var elem =  document.getElementById("texinput");
    texinput = elem.value;
    if (renderevent)
        clearTimeout(renderevent);
    renderevent = setTimeout(function(){renderLaTeX(texinput);}, delayrender); 
});

    
// Explicit submit

$("#submit").click(function(e) {
    
    e.preventDefault();

    // First check if we need to search textarea from selection in #rendered:

    var elemt = document.getElementById("texinput");
    var texinput = elemt.value;
   
    var searchstr = window.getSelection().toString();
    var pos = -1;
    
    if (searchstr) {
	pos = texinput.search(searchstr);
	if (pos > 0) {
	    elemt.focus();
	    elemt.setSelectionRange(pos, pos+searchstr.length);
	    return;
	}
    }

    // Proceed to rendering i.e. no luck in search above
    
    var start = elemt.selectionStart;
    var end = elemt.selectionEnd;

    if (start < end) {
	texinput = elem.value.substring(start, end);
    }
    
    elemt.focus();
    
    renderLaTeX(texinput);
});


// Load file from disk
    
function loadfile(input){
			       
    var reader = new FileReader();
    reader.onload = function(e){
        document.getElementById('texinput').value = e.target.result;
    }
    reader.readAsText(input.files[0]);
    var fakefilnavn = $('input[type=file]').val() // Returns C:\fakepath\<filnavn>
    var filnavnlist = fakefilnavn.split("\\");
    filnavn = filnavnlist[filnavnlist.length-1];  
};
    

// Get file from Django model

$("#getdb").click(function(e) {
	
    filnavn =  document.getElementById("tekster").value;

    $.ajax({
        url : "/django/ilatex/getdb/",
	//url : "/ilatex/getdb/",
	type : "POST", 
	data : { //csrfmiddlewaretoken : csrftoken,
	    filstr : filnavn},
	dataType : "json"
    }).done(function( result ) {
	document.getElementById('texinput').value = result.html ;
    });
});
		  
// Save textarea to Django model using globel filnavn


$("#save").click(function(e) {
	
    var elem =  document.getElementById("texinput");	
    var texinput = elem.value;
    
    $.ajax({
	url : "/django/ilatex/save/",
	//url : "/ilatex/save/",
	type : "POST", 
	data : { //csrfmiddlewaretoken : csrftoken,
	    filstr : filnavn,
	    inputstr : texinput},
	dataType : "json"
    }).done(function( result ) {
	alert(result.html);
    });
});		    
				    		    
		  
		  
		  
