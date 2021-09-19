var postButton = document.getElementById("new-post-button");
var newPostModal = document.getElementById("new-post-modal");
var newPostForm = document.getElementById("new-post");
var imageSrc = document.getElementById("cp-image-src");
var uploadedImage = document.getElementById("cp-image-uploaded");

var followModal = document.getElementById("follow-modal");
var followers = document.getElementById("followers");
var following = document.getElementById("following");
var followDiv = document.getElementById("following-div");
var followerDiv = document.getElementById("followers-div");

if (postButton) {
  postButton.onclick = function () {
    if (newPostModal.style.display != "grid") {
      newPostModal.style.display = "grid";
    }
  };
}

newPostModal.onclick = function (event) {
  if (event.target == newPostModal) {
    newPostModal.style.display = "none";
  }
};

var pfpButton = document.getElementById("pfp-button");
var pfpModal = document.getElementById("new-profile-pic-modal");
var pfpImageSrc = document.getElementById("pf-image-src");
var pfpUploadedImage = document.getElementById("pf-image-uploaded");

if (pfpButton) {
  pfpButton.onclick = function () {
    if (pfpModal.style.display != "grid") {
      pfpModal.style.display = "grid";
    }
  };
}

pfpModal.onclick = function (event) {
  if (event.target == pfpModal) {
    pfpModal.style.display = "none";
  }
};

pfpImageSrc.addEventListener("change", function () {
  const files = pfpImageSrc.files;
  if (files.length == 0) {
    pfpUploadedImage.src = "";
    pfpUploadedImage.style.backgroundColor = "black";
  } else {
    const file = files[0];
    pfpUploadedImage.style.backgroundImage = `url(${URL.createObjectURL(file)})`;
  }
});

imageSrc.addEventListener("change", function () {
  const files = imageSrc.files;
  if (files.length == 0) {
    uploadedImage.src = "";
    uploadedImage.style.backgroundColor = "black";
  } else {
    const file = files[0];
    uploadedImage.style.backgroundImage = `url(${URL.createObjectURL(file)})`;
  }
});

document.getElementById("cp-return-url").value = window.location.href;
document.getElementById("pf-return-url").value = window.location.href;

// for follower/following modals

followers.onclick = function () {
  followModal.style.display = "block";
  followerDiv.style.display = "block";
  followDiv.style.display = "none";
};

following.onclick = function () {
  followModal.style.display = "block";
  followerDiv.style.display = "none";
  followDiv.style.display = "block";
};

followModal.onclick = function (event) {
  if (event.target == followModal) {
    followModal.style.display = "none";
  }
};
