window.onload = function () {
  const div = document.querySelector('.moving-div');
  if (window.innerWidth > 800) {
    div.style.left = '-10%';
  } else {
    div.style.left = '0%';
  }
  div.style.opacity = '1';
};

const moveableDiv = document.querySelector(".items-cards");
let initialBottomPosition = 40;

window.addEventListener("scroll", () => {
  const scrolled = window.scrollY;

  // Calculate the new bottom position
  const newBottomPosition = initialBottomPosition + scrolled;

  // Limit the bottom position to not go above 40px from the top
  const minBottomPosition = 40;
  const maxBottomPosition = 80; // 40px initial + 40px move limit
  const limitedBottomPosition = Math.min(Math.max(newBottomPosition, minBottomPosition), maxBottomPosition);

  // Apply the new position to the div
  moveableDiv.style.transition = "bottom 1s ease";
  moveableDiv.style.bottom = `${limitedBottomPosition}px`;
});

const counter_div = document.querySelector(".counter");
const counter = document.querySelector(".counterM");
const moving_div2 = document.querySelector(".moving-div2");
const targetCount = parseInt(counter.getAttribute("data-count"));
const moving_div3 = document.querySelector(".moving-div3");
const animationDuration = 2000;
const animationStep = 50;
let isCounting = false;

const updateCount = () => {
  const currentCount = parseInt(counter.textContent);
  const increment = Math.ceil(targetCount / (animationDuration / animationStep));

  if (currentCount + increment < targetCount) {
    counter.textContent = currentCount + increment;
    setTimeout(updateCount, animationStep);
  } else {
    counter.textContent = targetCount;
  }
};

const startCounterOnScroll = () => {
  const options = {
    rootMargin: "0px",
    threshold: 0.5,
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !isCounting) {
        isCounting = true;
        observer.unobserve(entry.target);
        counter_div.classList.add("animate-counter");
        moving_div2.classList.add("move_now");
        moving_div3.classList.add("move_now3");
        updateCount();
      }
    });
  }, options);

  observer.observe(counter);

  const moving_div4 = document.querySelector(".moving-div4");
  const observer4 = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        moving_div4.classList.add("move_now4");
      }
    });
  }, options);

  observer4.observe(moving_div4);


  const moving_div5 = document.querySelector(".moving-div5");
  const observer5 = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        moving_div5.classList.add("move_now4");
      }
    });
  }, options);

  observer5.observe(moving_div5);

  const moving_div6 = document.querySelector(".moving-div6");
  const observer6 = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        moving_div6.classList.add("move_now4");
      }
    });
  }, options);

  observer6.observe(moving_div6);

  const moving_div7 = document.querySelector(".moving-div7");
  const observer7 = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        moving_div7.classList.add("move_now4");
      }
    });
  }, options);

  observer7.observe(moving_div7);

  const moving_div8 = document.querySelector(".moving-div8");
  const observer8 = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        moving_div8.classList.add("move_now4");
      }
    });
  }, options);

  observer8.observe(moving_div8);

  const moving_div9 = document.querySelector(".moving-div9");
  const observer9 = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        moving_div9.classList.add("move_now4");
      }
    });
  }, options);

  observer9.observe(moving_div9);

  const moving_div10 = document.querySelector(".ddd");
  const observer10 = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        moving_div10.classList.add("pulsate");
      }
    });
  }, options);

  observer10.observe(moving_div10);
};

startCounterOnScroll();
