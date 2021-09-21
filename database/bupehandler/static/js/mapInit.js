// if stuck, try this url : window.location.origin + "/api/geodata/siterecs_samhsa_ftloc/name1=Al-Assist
// TODO: change url to get the filter values. 
// TODO: maybe change the center to the average of all the latitude and longitude, aka center of every location we have found. 
$(document).ready(function() {
    function outerHTML(node){
    return node.outerHTML || new XMLSerializer().serializeToString(node);
    }
    var table_name = mapParams.table_name; 
    var param_values = mapParams.param_values;
    var destination_name = mapParams.destination_name;
    var excluded_values = mapParams.excluded_values; 
    var keyword = mapParams.keyword;
    console.log(param_values)
    param_values = param_values.replaceAll("amp;", "")
    console.log(param_values)
    excluded_values = excluded_values.replaceAll("amp;", "")
    console.log(excluded_values)
    var get_url = "/api/geodata/";
    get_url += table_name + "/";
    if (param_values != "") { 
        get_url += param_values + "/";
        console.log(get_url)
    }
    if (excluded_values != "") { 
        if (param_values == "") { 
        get_url += "None/";
        }
        get_url += excluded_values + "/";
        console.log(get_url)
    }
    if (keyword != "") { 
        if (param_values == "" && excluded_values == "") { 
        get_url += "None/None/";
        }
        else if (excluded_values == "") { 
        get_url += "None/"
        }
        get_url += keyword 
    }
    $.ajax({
            type : "GET",
            url : window.location.origin + get_url, // need to adjust the params to dynamically filter our map
            contentType: 'application/json;charset=UTF-8',
            success: function(data) {
                // Need to hide the access token 
                mapboxgl.accessToken = 'pk.eyJ1IjoibWF0Y2htYXBwZXIiLCJhIjoiY2tvMWJmZW9wMGtjdzMxb2k0NWhpeW0xMSJ9.ChZtypQ-p77nXwERIAt3Iw';
                var map = new mapboxgl.Map({
                    container: 'map',
                    style: 'mapbox://styles/matchmapper/ckog0go3v3k1417nn7gex8ebr',
                    center: [-75.158924, 39.9629223],
                    zoom: 11
                });


                // Load Mapbox Geocoder
                const geocoder = new MapboxGeocoder({
                    accessToken: mapboxgl.accessToken,
                    mapboxgl: mapboxgl, // Set the mapbox-gl instance
                    marker: true, // Use the geocoder's default marker style,
                    placeholder: "Search for Site by Address"
                  });
          
                // Add Geocoder to modal
                //map.addControl(geocoder, 'top-right');
                $('#geocodeWidget')[0].appendChild(geocoder.onAdd(map));

                // Event listener for geocoder completion
                geocoder.on('result', ({ result }) => {
                    const searchResult = result.geometry;
                    const options = { units: 'miles' };
                    
                    // Loop through sites and calculate distance to geocoder address
                    for (const loc of data.loc) {
                        loc.distance = turf.distance(
                            searchResult,
                            [loc.longitude, loc.latitude],
                            options
                        );
                    }

                    // find site with min distance
                    const closest = data.loc.sort((a, b) => {
                        if (a.distance > b.distance) {
                          return 1;
                        }
                        if (a.distance < b.distance) {
                          return -1;
                        }
                        return 0; // a must be equal to b
                    })[0];

                    // fit the map on the entered location and the closest site
                    map.fitBounds([searchResult.coordinates, [closest.longitude, closest.latitude]], {padding: 600});

                    // Load popup of closest location
                    link_object = window.location.origin + "/table/" + table_name + "/oid=" + closest.oid + "/";
                    console.log(closest)
                    const popup = new mapboxgl.Popup()
                        .setLngLat([closest.longitude, closest.latitude])
                        .setHTML("<a href=" + link_object + ">" + JSON.stringify(closest.name1) + "</a><br><a href='" + closest.website1 + "'>Website</a><br>Phone: " + closest.phone1 )
                        .addTo(map);
                });

                // Add zoom and rotation controls to the map.
                map.addControl(new mapboxgl.NavigationControl());


                document.querySelector("#sitecount").textContent = data['loc'].length
                var link_object; 
                for (i = 0; i < data['loc'].length; i++) {
                    link_object = window.location.origin + "/table/" + table_name + "/oid=" + data['loc'][i]['oid'] + "/";
                    var marker = new mapboxgl.Marker()
                        .setLngLat([data['loc'][i]['longitude'], data['loc'][i]['latitude']])
                        .setPopup(new mapboxgl.Popup().setHTML("<a href=" + link_object + ">" + JSON.stringify(data['loc'][i][destination_name]) + "</a><br><a href='" + data['loc'][i].website1 + "'>Website</a><br>Phone: " + data['loc'][i].phone1))
                        .addTo(map);
                }
            }
        });
});


function toggleSearchModal() {
    $("#siteSearch").toggle();
}