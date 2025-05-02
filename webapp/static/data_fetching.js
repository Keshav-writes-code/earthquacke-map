const map = L.map("map").setView([51.505, -0.09], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);
/**
 * Fetch Data from the Flask Endpoint
 * @param {string} start_time - The title of the book.
 * @param {string} end_time - The author of the book.
 * @returns {Array<Object>}
 */
async function get_data(start_time, end_time) {
  try {
    const res = await fetch("/get_data");
    const data = await res.json();
    return data;
  } catch (e) {
    consle.log(e);
  }
}
(async () => {
  const data = await get_data();
  data.forEach((v) => {
    L.marker([v.latitude, v.longitude])
      .addTo(map)
      .bindPopup(v.place)
      .openPopup();
  });
})();
