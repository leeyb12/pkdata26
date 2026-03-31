const scrollText = document.getElementById("scrollText");
const leftMenu = document.getElementById("leftMenu");
const rightMenu = document.getElementById("rightMenu");
const endMenu = document.getElementById("endMenu");
const t1 = document.querySelector(".t1");

window.addEventListener("scroll", () => {
const scrollY = window.scrollY;
console.log(scrollY);
/* 스크롤 위치에 따른 텍스트를 변경 */
if (scrollY > 100 && scrollY <= 800) {
  scrollText.textContent = "지금은 1단계 입니다.";
}
if (scrollY > 800 && scrollY <= 1600) {
  scrollText.textContent = "지금은 2단계 입니다.";
  t1.classList.remove("turn");
}
if (scrollY > 1600 && scrollY <= 2400) {
  scrollText.textContent = "지금은 3단계 입니다.";
  t1.classList.add("turn");
}
if (scrollY > 2400 && scrollY <= 3400) {
  scrollText.textContent = "지금은 4단계 입니다.";
  t1.classList.remove("turn");
}
if (scrollY > 3400) {
  scrollText.textContent = "마지막 구간입니다.";
}

if (scrollY > 500 && scrollY < 1900) {
  leftMenu.classList.add("left-show");
  leftMenu.innerHTML = `왼쪽메뉴 <ul>
<li> 실시간 스크롤 값</li>
<li>${scrollY}</li>
<li> 왼쪽메뉴 사라짐</li>
<li> 투명도 0에서 1로</li>
</ul>`;
} else {
  leftMenu.classList.remove("left-show");
}
if (scrollY > 1500 && scrollY < 2800) {
  rightMenu.classList.add("right-show");
} else {
  rightMenu.classList.remove("right-show");
}

if (scrollY > 1900 && scrollY < 3300) {
  leftMenu.classList.add("left-show");
  leftMenu.classList.add("left-menu2");
  leftMenu.innerHTML = `변형메뉴 <ul>
  <li> 변형된 메뉴</li>
  <li>${scrollY}</li>
  <li> 아래로 이동</li>
  <li> 초록색으로 변형</li>
</ul>`;
} else {
  leftMenu.classList.remove("left-menu2");
}
const toTop = () => window.scrollTo({ top: 0, behavior: "smooth" });

if (scrollY > 3350) {
  endMenu.classList.add("end-show");

  setTimeout(toTop, 1500);
} else {
  endMenu.classList.remove("end-show");
}
});