var PERFORMANCE_MODE = false;
var id_color, secondary_color;
var markers_icon;
var map;
var markers = [];
var styles = [
    {
        "featureType": "administrative",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#444444"
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "administrative.province",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative.locality",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "administrative.neighborhood",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "administrative.land_parcel",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
            {
                "color": "#e4e4e4"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "saturation": "-14"
            },
            {
                "lightness": "-11"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "labels",
        "stylers": [
            {
                "saturation": "-41"
            },
            {
                "lightness": "-20"
            },
            {
                "gamma": "3.93"
            }
        ]
    },
    {
        "featureType": "landscape.natural",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "landscape.natural.terrain",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "lightness": 45
            },
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            },
            {
                "saturation": "7"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
            {
                "color": "#ffffff"
            },
            {
                "visibility": "on"
            }
        ]
    }
];


function initializeMap(publisher_data, gender_choices, id_color, secondary_color) {
    // map styles
    var mapholder = document.getElementById('map');
    mapholder.style.height = '80vh';
    mapholder.style.width = '100%';
    mapholder.style.margin = '0px auto';

    // marker styles
    markers_icon = {
            path:   'M18-26.8c0-10.2-8.3-18.5-18.5-18.5S-19-37.1-19-26.8c0,5.1,2.1,9.7,5.4,' +
                    '13L-0.5-0.3l13.1-13.5C15.9-17.1,18-21.7,18-26.8z',
            fillColor: id_color,
            fillOpacity: 1,
            strokeColor: secondary_color,
            strokeWeight: 1,
            scale: 0.6
    };

    // Create a new StyledMapType object, passing it the array of styles,
    // as well as the name to be displayed on the map type control.
    var styledMap = new google.maps.StyledMapType(styles, {name: "Styled Map"});

    // Create a map object, and include the MapTypeId to add
    // to the map type control.
    var mapOptions = {
        zoom: 3,
        center: new google.maps.LatLng(51, 9), // central europe (germany)
        mapTypeControlOptions: {mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']},
        disableDefaultUI: true
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    //Associate the styled map with the MapTypeId and set it to display.
    map.mapTypes.set('map_style', styledMap);
    map.setMapTypeId('map_style');

    // fill markers array
    for(var i = 0; i < publisher_data.length; i++) {
        var gender;
        console.log(publisher_data[i].fields.gender);
        if (!publisher_data[i].fields.gender) {
            gender = gender_choices[0][1];
            console.log('eine 0');
        } else {
            gender = gender_choices[1][1];
            console.log('eine 1');
        }

        markers.push(
            {
                marker_id: publisher_data[i].pk,
                marker_pos: new google.maps.LatLng(
                    publisher_data[i].fields.latitude,
                    publisher_data[i].fields.longitude
                ),
                connected_marker: publisher_data[i].fields.invited_by,
                info_window: new google.maps.InfoWindow({
                    content: 'hello world'
                }),
                title: gender + ', ' + publisher_data[i].fields.city +
                                ', ' + publisher_data[i].fields.region
            }
        );
    }

    draw(id_color);
}


function draw(pin_color) {
    // draw markers
    for (var i = 0; i < markers.length; i++) {
        new google.maps.Marker({
            icon: markers_icon,
            position: markers[i].marker_pos,
            map: map,
            title: markers[i].title
        });
    }

    if (!PERFORMANCE_MODE) {
        for (var i = 0; i < markers.length; i++) {
            if (markers[i].connected_marker != null) {
                for (var k = 0; k < markers.length; k++) {
                    if (markers[i].connected_marker == markers[k].marker_id) {
                        new google.maps.Polyline({
                            path: [markers[i].marker_pos, markers[k].marker_pos],
                            strokeColor: pin_color,
                            strokeOpacity: 1,
                            strokeWeight: 0.8,
                            map: map
                        });
                    }
                }
            }
        }
    }
}