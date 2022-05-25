var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].onclick = function(){
        this.classList.toggle("active");
        this.nextElementSibling.classList.toggle("show");
  }
}

function nameFunction(){
 	var element = document.getElementById("fullName").value;
}
function myFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("myCheck");
  // Get the output text

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
  
    submit('foco',1);
  } else {

    submit('foco',0);
  }
}

function myFunction4(value) {
   var text = document.getElementById("text");
    
  // If the checkbox is checked, display the output text
  if (value==1){
    text.style.display = "block";
    alert("Alguien esta tocando el Timbre!")

  } else {
    text.style.display = "none";
  }
}
function actualiza(){
$('#hola').load(location.href+" #hola","");

}
function camara(valor){
  var video = document.getElementById("camara1");
  if(valor==200){
   
    video.style.display = "block";
  }
  else{
     alert("La camara 1 no esta conectada")
     video.style.display = "none";
  }
}
function camara2(valor){
  var video = document.getElementById("camara2");
  if(valor==200){
    video.style.display = "block";
  }
  else{
     alert("La camara 2 no esta conectada")
     video.style.display = "none";
  }
}

setInterval(actualiza,2000);
function deactivateAll(){
    var buttons = document.getElementsByTagName('button');
    for(button in buttons)
        button.classList.remove("on")
}

function activate(sender){
    if(sender == null)
        return;
    sender.classList.add("on");
}

function handle(sender, action, value){
    var element = document.getElementById("fullName").value;
    // deactivateAll();
    // activate(sender);
    if(value==10){
      	submit(action, element);
    }
    else{
    submit(action, value);}
}

function submit(action, value){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        'action' : action,
        'value' :  value,
    }));
}
