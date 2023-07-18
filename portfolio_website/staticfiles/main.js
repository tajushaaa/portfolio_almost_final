function createBlurCircle() {
  const blurCircle = document.createElement('div');
  blurCircle.classList.add('blur-circle');
  blurCircle.style.left = getRandomValue(0, window.innerWidth - 200) + 'px';
  blurCircle.style.top = getRandomValue(0, window.innerHeight - 200) + 'px';
  blurCircle.style.bottom = getRandomValue(0, window.innerHeight - 200) + 'px';
  document.body.appendChild(blurCircle);
}

function getRandomValue(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

// Create multiple blur circles on the page
const numBlurCircles = 15;
for (let i = 0; i < numBlurCircles; i++) {
  createBlurCircle();
}