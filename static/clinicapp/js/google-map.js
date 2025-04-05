function init() {
    // Set up the map with center and zoom (Leaflet expects [lat, lng])
    var map = L.map('map').setView([-0.1861074,35.2713812], 13);

    // Add OpenStreetMap tile layer with attribution
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Array of addresses to geocode
    var addresses = ['Koru Mission Hospital'];

    // For each address, use the Nominatim API for geocoding
    addresses.forEach(function(address) {
      // Create URL for Nominatim geocoding
      var url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(address);
      
      $.getJSON(url, function(data) {
        if (data && data.length > 0) {
          var p = data[0]; // Use the first result
          var latlng = [parseFloat(p.lat), parseFloat(p.lon)];

          // Add a marker with a custom icon (if available)
          var customIcon = L.icon({
            iconUrl: '/static/clinicapp/images/loc.png', // ensure this image exists
            iconSize: [25, 41],        // adjust as needed
            iconAnchor: [12, 41]       // point of the icon which will correspond to marker's location
          });

          L.marker(latlng, { icon: customIcon }).addTo(map);
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', init);