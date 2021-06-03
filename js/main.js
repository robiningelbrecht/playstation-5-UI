// Init clock.
document.querySelector('.time').innerHTML = moment().format('H:mm');

setInterval(() => {
  document.querySelector('.time').innerHTML = moment().format('H:mm');
}, 60000);

// Init Flickity.
let flkty = new Flickity(document.querySelector('.js-flickity'), {
  contain: false,
  pageDots: false,
  prevNextButtons: false,
  percentPosition: false,
  imagesLoaded: true,
  cellAlign: 'left',
  draggable: false,
});

// Init background.
let body = document.querySelector('body');
body.style.backgroundImage = 'url(' + flkty.cells[0].element.dataset.background + ')';

let slide_positions = flkty.cells.map((slide) => {
  return parseInt(slide.element.style.left);
});

flkty.on('change', function (index) {
  // Set background.
  body.style.backgroundImage = 'url(' + flkty.cells[index].element.dataset.background + ')';

  // Reset positions of all slides to original.
  flkty.cells.forEach((slide, slide_index) => {
    let left = slide_positions[slide_index];
    slide.element.style.left = (left) + "px"
  })

  // Move all slides right to the selected one, 75px to the right.
  flkty.cells.slice(index + 1).forEach((slide, slide_index) => {
    let left = slide_positions[slide_index + index + 1];
    slide.element.style.left = (left + 75) + "px"
  })
});

// Event listener to slide to Flickity index on click.
document.querySelectorAll('.js-flickity .slide').forEach((cell, index) => {
  cell.addEventListener('click', () => {
    flkty.select(index);
  });
});