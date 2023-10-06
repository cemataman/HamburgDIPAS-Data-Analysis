// Initialize the tile layer
const map = L.map('map', {
  scrollWheelZoom: 'center',
  zoomSnap: 0.05,
  wheelPxPerZoomLevel: 100
}).setView([0, 0], 2);

// Initialize the tile layer
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);

let colorIndex = 0;
const baseColors = [
    [255, 0, 0],       // red
  [0, 0, 255],       // blue
  [128, 0, 128],     // yellow
  [0, 255, 0],       // green
  [255, 165, 0],     // orange
  [255, 255, 0],     // purple
  [255, 192, 203],   // pink
  [0, 128, 128]      // teal
  // [211, 30, 37], // red
  // [49, 64, 123], // blue
  // [138, 63, 100], // yellow
  // [54, 158, 75], // green
  // [93, 181, 183], // light blue
  // [243, 168, 188], // pink
  // [243, 188, 46], // dark yellow
  // [209, 192, 43] // purple
];
let fileColors = {};

function wrapText(text, maxLength) {
  let wrappedText = '';
  let words = text.split(' ');
  let line = '';

  words.forEach((word) => {
    if ((line + word).length > maxLength) {
      wrappedText += line.trim() + '<br>';
      line = '';
    }
    line += word + ' ';
  });

  wrappedText += line.trim();
  return wrappedText;
}

const legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {
  const div = L.DomUtil.create('div', 'info legend');
  const grades = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1];  // sentiment scores range
  let labels = [];

  // loop through our density intervals and generate a label with a colored square for each interval
  for (let i = 0; i < grades.length; i++) {
    const ratio = (grades[i] + 1) / 2;  // convert range from [-1, 1] to [0, 1]
    const color = `rgb(${Math.round(255 * (1 - ratio))}, ${Math.round(255 * (1 - ratio))}, ${Math.round(255 * (1 - ratio))})`;
    labels.push(`<i style="background:${color}"></i> ${grades[i]}`);
  }

  div.innerHTML = labels.join('<br>');
  return div;
};

legend.addTo(map);

function getColorBasedOnFileAndValue(file, value) {
  if (!fileColors[file.name]) {
    fileColors[file.name] = baseColors[colorIndex % baseColors.length];
    colorIndex++;
  }

  let color = fileColors[file.name];

  // Value must be between -1 and 1
  const ratio = (value + 1) / 2;
  const red = Math.round(color[0] * ratio);
  const green = Math.round(color[1] * ratio);
  const blue = Math.round(color[2] * ratio);

  return `rgb(${red},${green},${blue})`;
}

function createCustomIcon(color) {
  return L.divIcon({
    className: 'custom-marker',
    html: `<i class="fa-regular fa-location-pin" style="font-size: 24px; color: ${color};"></i>`,
    iconSize: [24, 24],
    iconAnchor: [12, 24],
    tooltipAnchor: [0, -24]
  });
}

function processCSVData(file) {
  Papa.parse(file, {
    header: true,
    complete: function (results) {
      const excelData = results.data
        .map(row => {
          return {
            'Titel (eng)' : row['Titel (eng)'],
            'Beschreibung (eng)': row['Beschreibung (eng)'],
            latitude: parseFloat(row.Latitude),
            longitude: parseFloat(row.Longitude),
            'sentiment scores': parseFloat(row['sentiment scores'])
          };
        })
        .filter(data => {
          return !isNaN(data.latitude) && !isNaN(data.longitude) && !isNaN(data['sentiment scores']);
        });

      // Add markers to map for each data point
      excelData.forEach(data => {
        const color = getColorBasedOnFileAndValue(file, data['sentiment scores']);
        const customIcon = createCustomIcon(color);

        const marker = L.marker([data.latitude, data.longitude], { icon: customIcon }).addTo(map);
        marker.bindPopup(`<div class="custom-popup-text"><strong>Titel (eng): ${wrapText(data['Titel (eng)'], 100)}</strong><br>Beschreibung (eng): ${wrapText(data['Beschreibung (eng)'], 100)}</div>`, {
          className: 'custom-popup',
          closeButton: false,
          autoClose: false,
          closeOnClick: false
        }).on('mouseover', function () {
          this.openPopup();
        }).on('mouseout', function () {
          this.closePopup();
        });
      });

      // Fit map bounds to show all markers
      const group = new L.featureGroup(excelData.map(data => L.marker([data.latitude, data.longitude])));
      map.fitBounds(group.getBounds());
    }
  });
}


// Add an event listener for the CSV file input
document.getElementById('csv-files').addEventListener('change', function (event) {
  const files = event.target.files;

  // Process each CSV file and display markers on map
  for (const file of files) {
    processCSVData(file);
  }
});