let map;
let marker;
let emergencyLocation;
let directionsService;
let directionsRenderer;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 49.235, lng: 7.010 },
        zoom: 13
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    map.addListener('click', function(event) {
        if (marker) {
            marker.setPosition(event.latLng);
        } else {
            marker = new google.maps.Marker({
                position: event.latLng,
                map: map
            });
        }
        emergencyLocation = event.latLng;
    });
}

document.getElementById('emergencyForm').addEventListener('submit', function(e) {
    e.preventDefault();
    if (!emergencyLocation) {
        alert('Please click on the map to select your position');
        return;
    }

    const selectedSkills = Array.from(document.getElementById('skills').selectedOptions).map(option => option.value);
    const teamSize = parseInt(document.getElementById('team_size').value, 10);

    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').innerText = '';

    fetch('/find_service', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            lat: emergencyLocation.lat(),
            lng: emergencyLocation.lng(),
            skills: selectedSkills,
            team_size: teamSize
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        if (data.error) {
            document.getElementById('result').innerText = data.error;
        } else {
            document.getElementById('result').innerText = `Nearest Service: ${data.name}, Distance: ${(data.distance / 1000).toFixed(2)} km, Travel Time: ${(data.duration / 60).toFixed(2)} minutes`;

            const serviceLocation = { lat: parseFloat(data['geometry/location/lat']), lng: parseFloat(data['geometry/location/lng']) };

            directionsService.route({
                origin: emergencyLocation,
                destination: serviceLocation,
                travelMode: google.maps.TravelMode.DRIVING,
            }, (response, status) => {
                if (status === google.maps.DirectionsStatus.OK) {
                    directionsRenderer.setDirections(response);
                } else {
                    window.alert('Directions request failed due to ' + status);
                }
            });
        }
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        console.error('Error:', error);
    });
});
