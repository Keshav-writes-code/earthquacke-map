const map = L.map("map").setView([51.505, -0.09], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);
const markersGroup = L.layerGroup().addTo(map);
/**
 * Fetch Data from the Flask Endpoint
 * @param {string} start_time - The title of the book.
 * @param {string} end_time - The author of the book.
 * @returns {Array<Object>}
 */
async function get_data(start_time, end_time) {
  try {
    const query = new URLSearchParams({
      start_time: start_time,
      end_time: end_time,
    }).toString();
    const res = await fetch(`/get_data?${query}`);
    const data = await res.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}
(async () => {
  const date = new Date();
  date.setDate(date.getDate() - 1);
  const start_time = date.toISOString();
  const end_time = new Date().toISOString();

  const data = await get_data(start_time, end_time);
  data.forEach((v) => {
    L.marker([v.latitude, v.longitude])
      .addTo(markersGroup)
      .bindPopup(v.place)
      .openPopup();
  });
})();
function clear_markers() {
  markersGroup.clearLayers();
}
