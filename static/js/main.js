const navSlide = () => {
  const burgerMenu = document.querySelector(".burger");
  const nav = document.querySelector(".navbar-nav");
  const navlinks = document.querySelectorAll(".navbar-nav li");

  burgerMenu.addEventListener("click", function () {
    // Toggle drop down menu
    nav.classList.toggle("mobilenav-active");

    // Increase links' opacity
    navlinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = "";
      } else {
        link.style.animation = `linkSlide 0.5s ease forwards ${
          index / 7 + 0.5
        }s`;
      }
    });

    // Toggle burger to cross animation
    burgerMenu.classList.toggle("toggle");
  });
};

navSlide();
