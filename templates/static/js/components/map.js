var map;
var marker_styles;
var colors;

function initialize(map_colors) {
    colors = map_colors;

    // map styles
    var map_styles = [
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
                "color": colors[3][1]
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

    // marker styles
    marker_styles = {
            path:   'M18-26.8c0-10.2-8.3-18.5-18.5-18.5S-19-37.1-19-26.8c0,5.1,2.1,9.7,5.4,' +
                    '13L-0.5-0.3l13.1-13.5C15.9-17.1,18-21.7,18-26.8z',
            fillColor: colors[0][1],
            fillOpacity: 1,
            strokeColor: colors[1][1],
            strokeWeight: 1,
            scale: 0.6
    };

    // Create a new StyledMapType object, passing it the array of styles,
    // as well as the name to be displayed on the map type control.
    var styledMap = new google.maps.StyledMapType(map_styles, {name: "SITUATIONS"});

    // Create a map object, and include the MapTypeId to add
    // to the map type control.s
    var mapOptions = {
        zoom: 3,
        center: new google.maps.LatLng(51, 9), // central europe (germany)
        mapTypeControlOptions: {mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']},
        disableDefaultUI: true
    };

    var map_holder = document.getElementById('map_holder');
    map = new google.maps.Map(document.getElementById('map_holder'), mapOptions);

    //Associate the styled map with the MapTypeId and set it to display.
    map.mapTypes.set('map_style', styledMap);
    map.setMapTypeId('map_style');
}

function render(markers, mode, limit) {
    // set first marker and number of markers
    var start_marker = 0;
    if (mode != 0 && markers.length > limit) {
        start_marker = markers.length - limit - 1;
    }

    // draw
    for (var i = start_marker; i < markers.length; i++) {
        if (markers[i][5][1] != null) {
            draw_marker(markers[i]);
            if (markers[i].length > 7 && mode == 0) draw_link(markers[i]);
        }
    }
}

function draw_marker(marker) {
    var new_marker = new google.maps.Marker({
        icon: marker_styles,
        position: new google.maps.LatLng(marker[5][1], marker[6][1]),
        map: map
    });

    var data =  '<div class="row">' +
                    '<div class="col-xs-6">' +
                        '<h6 class="list-group-item-heading" style="color:' + colors[0][1] + '">' +
                            'Date:' +
                        '</h6>' +
                    '</div>' +
                    '<div class="col-xs-6">' +
                        '<p class="list-group-item-text" style="color:' + colors[0][1] + '">' +
                            marker[1][1] +
                        '</p>' +
                    '</div>' +
                '</div>';
    data +=     '<div class="row">' +
                    '<div class="col-xs-6">' +
                        '<h6 class="list-group-item-heading" style="color:' + colors[0][1] + '">' +
                            'Gender:' +
                        '</h6>' +
                    '</div>' +
                    '<div class="col-xs-6">' +
                        '<p class="list-group-item-text" style="color:' + colors[0][1] + '">' +
                            marker[3][1] +
                        '</p>' +
                    '</div>' +
                '</div>';
    data +=     '<div class="row">' +
                    '<div class="col-xs-6">' +
                        '<h6 class="list-group-item-heading" style="color:' + colors[0][1] + '">' +
                            'Location:' +
                        '</h6>' +
                    '</div>' +
                    '<div class="col-xs-6">' +
                        '<p class="list-group-item-text" style="color:' + colors[0][1] + '">' +
                            marker[4][1] +
                        '</p>' +
                    '</div>' +
                '</div>';
    /*
    data    += '<hr>';
    data    += '<button>More info</button>';
    */

    var infowindow = new google.maps.InfoWindow({
      content: data
    });

    google.maps.event.addListener(new_marker, 'mouseover', function() {
        infowindow.open(map, new_marker);
    });

    google.maps.event.addListener(new_marker, 'mouseout', function() {
        infowindow.close();
    });

    google.maps.event.addListener(new_marker, 'click', function() {
        /*Posts*/
        console.log('clicked');
            $("body").css("overflow", "hidden");
                $(".lightbox_detailview").hide(0).fadeIn(300);
                get_post_info(marker[0][1]);
    });
}

function draw_link(marker) {
    if (marker[7] != undefined) {   // has no connection
        if (marker[7][1] != null) {
            new google.maps.Polyline({
                path: [
                    {lat: marker[5][1], lng: marker[6][1]},
                    {lat: marker[7][1], lng: marker[8][1]}
                    ],
                strokeColor: colors[0][1],
                strokeOpacity: 1,
                strokeWeight: 0.8,
                map: map
            });
        }
        /*
        console.log('connected: ' + marker[5][1] + ' ' + marker[6][1] +
                    '\nwith: ' + marker[7][1] + ' ' + marker[8][1]);
        */
    }
}



// --- AJAX by Micha

/*AJAX for POSTVIEW*/
function get_post_info(my_id) {
    console.log('get_post_info called');
    if(my_id > 0){
        $.ajax({
            url : "detail_post/", // the endpoint
            type : "POST", // http method
            data : { post_id : my_id }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log(json);
                $('.list_id').html(""+json.publisher_id);
                $('.list_date').html(""+json.post_publishing_date);
                $('.list_gender').html(""+json.publisher_gender);
                $('.list_occupation').html(""+json.publisher_occupation);
                $('.list_age').html(""+json.publisher_age);
                $('.list_location').html(""+json.publisher_location);
                $('.list_activity').html(""+json.publisher_active_time);
                $('.list_description').html(""+json.post_description);
                $('.list_reason').html(""+json.post_reason);

                $('#publish_image_title').html(""+json.image_title);
                $('#publish_image_author').html(""+json.image_author);
                $('#lightbox_img_pubview').fadeOut(0, function(){
                    $('#lightbox_img_pubview').attr('src',""+json.image_filename);
                }).fadeIn(400);
                COUNT_OF_ALL_POSTS = json.post_count;
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
};

/*AJAX_Setup for django csrf*/
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});