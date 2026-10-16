const API = window.MDM_API_BASE;
const H = { Authorization: "Bearer " + window.MDM_TOKEN };

const map = L.map("map").setView([36.2, 138.2], 5);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap",
}).addTo(map);
const markers = {};

async function j(url, opts) {
  const r = await fetch(url, { headers: H, ...opts });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function refresh() {
  const data = await j(API + "/devices");
  const tbody = document.querySelector("#list tbody");
  tbody.innerHTML = "";
  for (const d of data.devices) {
    const udid = d.udid || d.UDID || d.id;
    const loc = data.latest[udid];
    const tr = document.createElement("tr");
    tr.innerHTML = `<td class="mono">${udid}</td>
      <td>${loc ? loc.lat.toFixed(5) : "-"}</td>
      <td>${loc ? loc.lon.toFixed(5) : "-"}</td>
      <td>${loc && loc.accuracy ? Math.round(loc.accuracy) + "m" : "-"}</td>
      <td>${loc ? loc.at : "-"}</td>
      <td><button data-udid="${udid}">取得</button></td>`;
    tbody.appendChild(tr);
    if (loc) {
      if (markers[udid]) markers[udid].setLatLng([loc.lat, loc.lon]);
      else markers[udid] = L.marker([loc.lat, loc.lon]).addTo(map).bindPopup(udid);
    }
  }
  tbody.querySelectorAll("button").forEach((b) =>
    b.addEventListener("click", async () => {
      b.textContent = "取得中…";
      try { await j(API + `/devices/${b.dataset.udid}/location`, { method: "POST" }); await refresh(); }
      finally { b.textContent = "取得"; }
    })
  );
}

document.getElementById("refresh").addEventListener("click", refresh);
refresh().catch((e) => console.error(e));
