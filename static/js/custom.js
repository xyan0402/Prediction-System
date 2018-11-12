var markers = [];
var coordinates = [];
var radii = [];
var jsonData = [];
mUpdate = function(x){};
dataMarkers = [];

$(function () {

    function initMap() {

        //the center of the map (currently Georgia Tech!) 
        var location = new google.maps.LatLng(33.7756, -84.3963);

        var mapCanvas = document.getElementById('wideMap');
        var mapOptions = {
            center: location,
            zoom: 11,
            //panControl: false,
            scrollwheel: false,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        map = new google.maps.Map(mapCanvas, mapOptions);

        // var markerImage = '../img/png/marker.png';
        // var markerImage = 'marker.png';


        // For showing some info on markers
        // Maybe I will use it in the future ;)
        var contentString = '<div class="info-window">' +
                '<h3>Info Window Content</h3>' +
                '<div class="info-content">' +
                '<p> some information! </p>' +
                '</div>' +
                '</div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString,
            maxWidth: 400
        });

        // marker.addListener('click', function () {
        //     infowindow.open(map, marker);
        // });


        //Listener on click (to pick a point)
        google.maps.event.addListener(map, 'click', function(event) {
            placeMarker(event.latLng);
            var latitude = event.latLng.lat();
            var longitude = event.latLng.lng();
            coordinates.push([latitude,longitude]);
            
            console.log( latitude + ', ' + longitude );

            radius = new google.maps.Circle({map: map,
                radius: 1000,
                center: event.latLng,
                fillColor: '#777',
                fillOpacity: 0.6,
                strokeColor: '#AA0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                draggable: false,   // Dragable
                editable: true      // Resizable
            });
            radii.push(radius);          

            // Center of map
            map.panTo(new google.maps.LatLng(latitude,longitude));
        });

        function placeMarker(location) {
            // console.log(location)
            var marker = new google.maps.Marker({
                position: location, 
                map: map   
                // ,icon: markerImage
            });
            
            // Remove the previous marker
            if (markers.length>0){
                tmp=markers.pop();
                tmp.setMap(null);
                tmp=radii.pop();
                tmp.setMap(null);
                tmp=coordinates.pop();
            }
            markers.push(marker);   
        }
    }

    google.maps.event.addDomListener(window, 'load', initMap);

    // Displaying all nodes
    mUpdate = function showMarkers(nodes){
        console.log("# of nodes = "+nodes.length)
        // console.log("dataMarkers RESET  --> Current length = "+dataMarkers.length)
        for (var i=0; i<dataMarkers.length; i++){
            dataMarkers[i].setMap(null);
        }
        dataMarkers=[];
        for (var i=0; i<nodes.length; i++){
            
            // pos = new google.maps.LatLng(1.0*nodes[0][0], 1.0*nodes[0][1])
            var pos = {lat: nodes[i][0], lng: nodes[i][1]};
            // console.log(pos)

            var marker = new google.maps.Marker({
                // position: new google.maps.LatLng(nodes[0][0], nodes[0][1]),
                position: pos,
                animation: google.maps.Animation.DROP,
                map: map,
                title: ''


            });
            dataMarkers.push(marker);
            // marker.setMap(map);
        }
        // console.log("Now Length = "+dataMarkers.length)
        for (var i=0; i<dataMarkers.length; i++){
            dataMarkers[i].setMap(map);
        }
    }

    // AJAX Commnications
    $('#button1').click(function(){
        var beds  = $('#no_beds').val();
        var baths = $('#no_baths').val();
        var area  = $('#area').val();
        var resv  = $('#param').val();

        console.log("READ: beds= "+beds+" | baths= "+baths+" | area= "+area);
        console.log("coordinates"+coordinates[0]);
        console.log("radii= "+radii[0].radius);
        console.log("clicked");
        
        //DATA SENT TO SERVER
        jsonData = {"beds": beds,
                    "baths": baths,
                    "area": area,
                    "resv": param,
                    "point": coordinates[0],
                    "radius": radii[0].radius
                    };

        $.ajax({
            url: '/testFrontend',
            contentType: 'application/json',
            data: jsonData,
            type: 'POST',
            
            success: function(response){
                console.log("successfully received response from server");
                $('#outputs').append('<p id="res"> successfully communicated</p>');
                
            },
            error: function(error){
                console.log("No response from server/No connection :(");
                $('#outputs').html(error);
            }

        });

    });

});


function addMarker(location){
    var marker = new google.maps.Marker({
    position: location,
    map: map
    });
    markers.push(marker);
}


//-------------- Some test functions ---------------//
function updateMarkers(nodes){
    mUpdate(nodes);
}


function testMe1(nodes){
    console.log('Length = '+nodes.length)
    console.log(nodes);
    
    for (var i = 0; i<=nodes.length; i++){
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(nodes[0][0], nodes[0][1]),
            map: map,
            title: 'info'
        });
    }
}

function testMe(x){
    console.log("Test-A");
    console.log(x);
}

function testMe2(){
    console.log("Test-B");
}