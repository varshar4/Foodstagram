var modal=document.getElementById("modal");var signUp=document.getElementById("sign-up");var signForm=document.getElementById("sign-up-form")
var logIn=document.getElementById("log-in")
var logForm=document.getElementById("log-in-form")
var span=document.getElementsByClassName("close")[0];signUp.onclick=function(){modal.style.display="block";signForm.style.display="block";logForm.style.display="none";}
logIn.onclick=function(){modal.style.display="block";signForm.style.display="none";logForm.style.display="block";}
span.onclick=function(){modal.style.display="none";}
window.onclick=function(event){if(event.target==modal){modal.style.display="none";}}
function submitForm(){modal.style.display="none";}