const MS_IN_DAY = 86400000;
const now = Date.now();
const oneMonthAgo = now - 2 * MS_IN_DAY;

const fromSlider = document.querySelector("#fromSlider");
const toSlider = document.querySelector("#toSlider");

// Setup slider ranges
fromSlider.min = oneMonthAgo;
fromSlider.max = now;
toSlider.min = oneMonthAgo;
toSlider.max = now;

// Set initial values
fromSlider.value = now - 1 * MS_IN_DAY; // 30 days ago
toSlider.value = now;

// Helpers
function getParsed(currentFrom, currentTo) {
  const from = parseInt(currentFrom.value, 10);
  const to = parseInt(currentTo.value, 10);
  return [from, to];
}

function formatDateTime(ms) {
  return new Date(Number(ms)).toISOString().replace("T", " ").split(".")[0]; // YYYY-MM-DD HH:mm:ss
}

function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
  const rangeDistance = to.max - to.min;
  const fromPosition = from.value - to.min;
  const toPosition = to.value - to.min;
  controlSlider.style.background = `linear-gradient(
    to right,
    ${sliderColor} 0%,
    ${sliderColor} ${(fromPosition / rangeDistance) * 100}%,
    ${rangeColor} ${(fromPosition / rangeDistance) * 100}%,
    ${rangeColor} ${(toPosition / rangeDistance) * 100}%,
    ${sliderColor} ${(toPosition / rangeDistance) * 100}%,
    ${sliderColor} 100%
  )`;
}

function controlFromSlider(fromSlider, toSlider) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, "#C6C6C6", "#25daa5", toSlider);
  if (from > to) {
    fromSlider.value = to;
  }
}

function controlToSlider(fromSlider, toSlider) {
  const [from, to] = getParsed(fromSlider, toSlider);
  fillSlider(fromSlider, toSlider, "#C6C6C6", "#25daa5", toSlider);
  setToggleAccessible(toSlider);
  if (from <= to) {
    toSlider.value = to;
  } else {
    toSlider.value = from;
  }
}

function setToggleAccessible(currentTarget) {
  const toSlider = document.querySelector("#toSlider");
  if (Number(currentTarget.value) <= Number(toSlider.min)) {
    toSlider.style.zIndex = 2;
  } else {
    toSlider.style.zIndex = 0;
  }
}

async function handleSliderRelease() {
  const from = formatDateTime(fromSlider.value);
  const to = formatDateTime(toSlider.value);
  console.log("From:", from);
  console.log("To:", to);

  const data = await get_data(from, to);
  clear_markers();
  update_ui(data);
}

// Initial rendering
fillSlider(fromSlider, toSlider, "#C6C6C6", "#25daa5", toSlider);
setToggleAccessible(toSlider);

// Events
fromSlider.oninput = () => controlFromSlider(fromSlider, toSlider);
toSlider.oninput = () => controlToSlider(fromSlider, toSlider);

fromSlider.addEventListener("mouseup", handleSliderRelease);
toSlider.addEventListener("mouseup", handleSliderRelease);
