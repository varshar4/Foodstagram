var modal=document.getElementById("modal");var signUp=document.getElementById("sign-up");var signForm=document.getElementById("sign-up-form")
var logIn=document.getElementById("log-in")
var logForm=document.getElementById("log-in-form")
var sMsg=document.getElementsByClassName("message")[0];var lMsg=document.getElementsByClassName("message")[1];var span=document.getElementsByClassName("close")[0];signUp.onclick=function(){modal.style.display="block";signForm.style.display="block";logForm.style.display="none";}
logIn.onclick=function(){modal.style.display="block";signForm.style.display="none";logForm.style.display="block";}
span.onclick=function(){modal.style.display="none";if(sMsg){sMsg.remove();lMsg.remove();}}
window.onclick=function(event){if(event.target==modal){modal.style.display="none";if(sMsg){sMsg.remove();lMsg.remove();}}}
function submitForm(){modal.style.display="none";}
function checkModals(modalNum){if(modalNum===1){modal.style.display="block";signForm.style.display="block";logForm.style.display="none";}else if(modalNum===2){modal.style.display="block";signForm.style.display="none";logForm.style.display="block";}}