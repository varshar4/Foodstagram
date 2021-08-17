var postButton = document.getElementById("new-post-button")
var newPostModal = document.getElementById("new-post-modal")
var newPostForm = document.getElementById("new-post")
var imageSrc = document.getElementById("cp-image-src")
var uploadedImage = document.getElementById("cp-image-uploaded")
postButton.onclick = function (event) {
  if (newPostModal.style.display != "grid") {
    newPostModal.style.display = "grid"
  }
}

newPostModal.onclick = function (event) {
  if (event.target == newPostModal) {
    newPostModal.style.display = "none"
  }
}

imageSrc.addEventListener("change", function () {
  const files = imageSrc.files
  if (files.length == 0) {
    uploadedImage.src = ""
    uploadedImage.style.backgroundColor = "black"
  } else {
    const file = files[0]
    uploadedImage.style.backgroundImage = `url(${URL.createObjectURL(file)})`
  }
})

document.getElementById("cp-return-url").value = window.location.href
