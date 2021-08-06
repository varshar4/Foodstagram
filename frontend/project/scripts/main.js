var modal = document.getElementById("modal");
var signUp = document.getElementById("sign-up");
var signForm = document.getElementById("sign-up-form")
var logIn = document.getElementById("log-in")
var logForm = document.getElementById("log-in-form")
var span = document.getElementsByClassName("close")[0];

// on sign up click, show modal, open sign up form and hide log in form 
signUp.onclick = function () {
  modal.style.display = "block";
  signForm.style.display = "block";
  logForm.style.display = "none"; 
}

// on log in click, show modal, open log in form and hide sign up form
logIn.onclick = function () {
  modal.style.display = "block";
  signForm.style.display = "none";
  logForm.style.display = "block"; 
}

// close modal on user click of [x]
span.onclick = function () {
  modal.style.display = "none";
}

// close modal on user click outside the area
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// close modal if form is submitted
function submitForm() {
  modal.style.display = "none";
}