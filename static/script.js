// const navItems = document.querySelectorAll(".nav-item");

// navItems.forEach((navItem, i) => {
//   navItem.addEventListener("click", () => {
//     navItems.forEach((item, j) => {
//       item.className = "nav-item";
//     });
//     navItem.className = "nav-item active";
//   });
// });

// //! Light/Dark Mode

// const moonIcon = document.querySelector(".moon");
// const sunIcon = document.querySelector(".sun");
// const nightImage = document.querySelector(".night-img");
// const morningImage = document.querySelector(".morning-img");
// const toggle = document.querySelector(".toggle");

// function switchTheme() {
//   document.body.classList.toggle("darkmode");
//   if (document.body.classList.contains("darkmode")) {
//     sunIcon.classList.remove("hidden");
//     moonIcon.classList.add("hidden");
//     morningImage.classList.add("hidden");
//     nightImage.classList.remove("hidden");
//     localStorage.setItem("theme", "dark");
//   } else {
//     sunIcon.classList.add("hidden");
//     moonIcon.classList.remove("hidden");
//     morningImage.classList.remove("hidden");
//     nightImage.classList.add("hidden");
//     localStorage.setItem("theme", "light");
//   }
// }

//! Share Button Popup

// const sharebtns = document.querySelectorAll(".share-btn");

// sharebtns.forEach((btn) => {
//   btn.addEventListener("click", (event) => {
//     const popup = btn.closest(".event-footer").querySelector(".popup");

//     btn.classList.toggle("active");
//     popup.classList.toggle("active");

//     event.stopPropagation();
//   });
// });

// document.addEventListener("click", (event) => {
//   const popups = document.querySelectorAll(".popup");

//   popups.forEach((popup) => {
//     if (popup.classList.contains("active") && !popup.contains(event.target)) {
//       popup.classList.remove("active");

//       const shareBtn = popup
//         .closest(".event-footer")
//         .querySelector(".share-btn");
//       shareBtn.classList.remove("active");
//     }
//   });
// });





 
  document.addEventListener('DOMContentLoaded', function () {
      var allpost = document.getElementById('allpost');
      var mypost = document.getElementById('mypost');
      var allfeed = document.getElementById('allfeed');
      var myfeed = document.getElementById('myfeed');
      mypost.addEventListener('click', function () {
          myfeed.classList.remove("gone")
          allfeed.classList.add("gone")
          // Redirect to feed page
      });
      allpost.addEventListener('click', function () {
          allfeed.classList.remove("gone")
          myfeed.classList.add("gone")

          // Redirect to feed page
      });


  })
