var attempt = 3;
function validate(){
    var usuar=document.getElementById("username").value;
    var password=document.getElementById("password").value;
    if(username=="Admin" && password=="passwordsmarthome"){
        alert("Ingreso Exitosamente!");
        window.location="index2.html";
        return false;
    }
    else{
        attempt--;
    }
    alert("Intentos restantes:"+attempt)
    if(attempt==0){
        document.getElementById("username").disable=True;
        document.getElementById("password").disable=True;
        document.getElementById("sumbit").disable=True;
    }

}