const slice = document.querySelector(".slice"),
  firstImg = slice.querySelectorAll("img")[0],
  arrowIcons = document.querySelectorAll(".wrapper i");

let isDragStart = false,
  isDragging = false,
  prevPageX,
  prevScrollLeft,
  positionDiff;

const showHideIcons = () => {
  // showing and hiding prev/next icon according to slice scroll left value
  let scrollWidth = slice.scrollWidth - slice.clientWidth; // getting max scrollable width
  arrowIcons[0].style.display = slice.scrollLeft == 0
    ? "none"
    : "block";
  arrowIcons[1].style.display = slice.scrollLeft == scrollWidth
    ? "none"
    : "block";
};

arrowIcons.forEach(icon => {
  icon.addEventListener("click", () => {
    let firstImgWidth = firstImg.clientWidth + 14; // getting first img width & adding 14 margin value
    // if clicked icon is left, reduce width value from the slice scroll left else add to it
    slice.scrollLeft += icon.id == "left"
      ? -firstImgWidth
      : firstImgWidth;
    setTimeout(() => showHideIcons(), 60); // calling showHideIcons after 60ms
  });
});

const autoSlide = () => {
  // if there is no image left to scroll then return from here
  if (slice.scrollLeft - (slice.scrollWidth - slice.clientWidth) > -1 || slice.scrollLeft <= 0) 
    return;
  
  positionDiff = Math.abs(positionDiff); // making positionDiff value to positive
  let firstImgWidth = firstImg.clientWidth + 14;
  // getting difference value that needs to add or reduce from slice left to take middle img center
  let valDifference = firstImgWidth - positionDiff;

  if (slice.scrollLeft > prevScrollLeft) {
    // if user is scrolling to the right
    return (
      slice.scrollLeft += positionDiff > firstImgWidth / 3
      ? valDifference
      : -positionDiff);
  }
  // if user is scrolling to the left
  slice.scrollLeft -= positionDiff > firstImgWidth / 3
    ? valDifference
    : -positionDiff;
};

const dragStart = e => {
  // updatating global variables value on mouse down event
  isDragStart = true;
  prevPageX = e.pageX || e.touches[0].pageX;
  prevScrollLeft = slice.scrollLeft;
};

const dragging = e => {
  // scrolling images/slice to left according to mouse pointer
  if (!isDragStart) 
    return;
  e.preventDefault();
  isDragging = true;
  slice.classList.add("dragging");
  positionDiff = (e.pageX || e.touches[0].pageX) - prevPageX;
  slice.scrollLeft = prevScrollLeft - positionDiff;
  showHideIcons();
};

const dragStop = () => {
  isDragStart = false;
  slice.classList.remove("dragging");

  if (!isDragging) 
    return;
  isDragging = false;
  autoSlide();
};

slice.addEventListener("mousedown", dragStart);
slice.addEventListener("touchstart", dragStart);

document.addEventListener("mousemove", dragging);
slice.addEventListener("touchmove", dragging);

document.addEventListener("mouseup", dragStop);
slice.addEventListener("touchend", dragStop);