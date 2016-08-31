var lat = document.getElementById("usr_latitude");
var lng = document.getElementById("usr_longitude");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setPosValues, showError);
    } else {
        lat.value = 'no_entry';
        lng.value = 'no_entry';
        console.log('not supported by browser')
    }
}

function setPosValues(position) {
    lat.value = position.coords.latitude;
    lng.value = position.coords.longitude;
    console.log('geo location success');
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.log("User denied the request for Geolocation.");
            geoLocationFailed();
            break;
        case error.POSITION_UNAVAILABLE:
            console.log("Location information is unavailable.");
            geoLocationFailed();
            break;
        case error.TIMEOUT:
            console.log("The request to get user location timed out.");
            geoLocationFailed();
            break;
        case error.UNKNOWN_ERROR:
            console.log("An unknown error occurred.");
            geoLocationFailed();
            break;
    }
}

function geoLocationFailed() {
    lat.value = 'no_entry';
    lng.value = 'no_entry';
}