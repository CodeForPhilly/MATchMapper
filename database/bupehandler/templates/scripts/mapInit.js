// if stuck, try this url : window.location.origin + "/api/geodata/siterecs_samhsa_ftloc/name1=Al-Assist
// TODO: change url to get the filter values. 
// TODO: maybe change the center to the average of all the latitude and longitude, aka center of every location we have found. 
let globalData;
let markerList = [];
let myCircle;
let destination_name;
let geocoder;

$(document).ready(function() {
    function outerHTML(node){
        return node.outerHTML || new XMLSerializer().serializeToString(node);
    }
    var table_name = mapParams.table_name; 
    var param_values = mapParams.param_values;
    var destination_name = mapParams.destination_name;
    var excluded_values = mapParams.excluded_values;

    var keyword = mapParams.keyword;
    param_values = param_values.replaceAll("amp;", "")
    excluded_values = excluded_values.replaceAll("amp;", "")
    var get_url = "/api/geodata/";
    get_url += table_name + "/";
    console.log(1)
    console.log(get_url)
    if (param_values != "" && param_values != "None") { 
        console.log(1)
        get_url += param_values + "&archival_only=False/";
        console.log(get_url)
    }
    else { 
        console.log(2)
        get_url += "archival_only=False/"
        console.log(get_url)
    }
    if (excluded_values != "None" && excluded_values != "") { 
        console.log(3)
        get_url += excluded_values + "/";
        console.log(get_url)
    }
    //if(excluded_values == "None"){
    //    excluded_values = "archival_only=True"
    //    console.log("we are safe")
    //} else {
    //    excluded_values += "&archival_only=True"
    //    console.log("we are not safe")
    //}
    if (keyword != "") { 
        if (excluded_values == "None" || excluded_values == "") { 
        get_url += "None/"
        console.log(4)
        console.log(get_url)
        }
        get_url += keyword 
        console.log(5)
        console.log(get_url)
    }



    $.ajax({
            type : "GET",
            url : window.location.origin + get_url, // need to adjust the params to dynamically filter our map
            contentType: 'application/json;charset=UTF-8',
            success: function(data) {
                globalData = data;
                // Need to hide the access token 
                mapboxgl.accessToken = 'pk.eyJ1IjoibWF0Y2htYXBwZXIiLCJhIjoiY2tvMWJmZW9wMGtjdzMxb2k0NWhpeW0xMSJ9.ChZtypQ-p77nXwERIAt3Iw';
                map = new mapboxgl.Map({
                    container: 'map',
                    style: 'mapbox://styles/matchmapper/ckog0go3v3k1417nn7gex8ebr',
                    center: [-75.158924, 39.9629223],
                    zoom: 11
                });


                // Load Mapbox Geocoder
                geocoder = new MapboxGeocoder({
                    accessToken: mapboxgl.accessToken,
                    mapboxgl: mapboxgl, // Set the mapbox-gl instance
                    marker: false, // Use the geocoder's default marker style,
                    placeholder: "Search for Site by Address"
                  });
          
                // Add Geocoder to modal
                console.log($('#geocodeWidget'))
                $('#geocodeWidget')[0].appendChild(geocoder.onAdd(map));

                /*
                const ref = window.location.href;
                if (ref.indexOf('site_coord') > -1) {
                    window.ref = ref
                    
                    const regex = /(.*?)[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)(.*?)$/;
                    window.regex = regex;
                    const c = ref.match(regex);
                    console.log(c)

                }
                */

                // Event listener for geocoder completion
                geocoder.on('result', ({ result }) => {
                    const searchResult = result.geometry //|| 
                    const options = { units: 'miles' };
                    
                    // Loop through sites and calculate distance to geocoder address
                    for (const loc of data.loc) {
                        loc.distance = turf.distance(
                            searchResult,
                            [loc.longitude, loc.latitude],
                            options
                        );
                    }

                    // filter array by distance in field
                    const dist = parseInt($("#distance")[0].value);     //get distance from text field
                    const data_ = data.loc.filter(d => d.distance < dist);

                    // get count of sites within radius
                    const sitesInFocus = data_.length;

                    // find site with min distance
                    const closest = data_.sort((a, b) => {
                        if (a.distance > b.distance) {
                          return 1;
                        }
                        if (a.distance < b.distance) {
                          return -1;
                        }
                        return 0; // a must be equal to b
                    })[0];

                    // fit the map on the entered location and the closest site
                    // Create a bounding box using the dist variable and right triangle math
                    // keep is simple by using 69 miles = 1 degree
                    halfBound = 2 * dist/(69*Math.sqrt(2));
                    const c = searchResult.coordinates;
                    const bbox = [[c[0] - halfBound, c[1] - halfBound], [c[0] + halfBound, c[1] + halfBound]];
                    map.fitBounds(bbox)//, {padding: 600});

                    // Draw circle of radius
                    myCircle = new MapboxCircle({lat: c[1], lng: c[0]}, dist * 1610, {
                        fillOpacity: 0
                    }).addTo(map);

                    // Clear map and re-draw with different colors
                    markerList = clearMap(markerList);
                    plotMarkers(data, destination_name, sitesInFocus)
                    // Change record totals
                    document.querySelector("#sitecount").textContent = sitesInFocus;

                    // Load popup of closest location
                    // link_object = window.location.origin + "/table/" + table_name + "/oid=" + closest.oid + "/";
                    // const popup = new mapboxgl.Popup()
                    //     .setLngLat([closest.longitude, closest.latitude])
                    //     .setHTML("<a href=" + link_object + ">" + JSON.stringify(closest.name1) + "</a><br><a href='" + closest.website1 + "'>Website</a><br>Phone: " + closest.phone1 )
                    //     .addTo(map);
                });

                // Add zoom and rotation controls to the map.
                map.addControl(new mapboxgl.NavigationControl());

                plotMarkers(data, destination_name);
                document.querySelector("#sitecount").textContent = data['loc'].length;
                
            }
        });
});


// function to toggle the search modal on and off
function toggleSearchModal() {
    $("#siteSearch").toggle();
}


function reloadMap() {
    markerList = clearMap(markerList); 
    plotMarkers(globalData, destination_name); 
    myCircle.remove();
    geocoder.clear();
}

// function to clear map
function clearMap(items) {
    for (i = 0; i < items.length; i++ ) {
        items[i].remove();
    }
    return [];
}

// function to plot the markers
// Optional argument countFocus to plot those sites in a different color
let map;
function plotMarkers(data, dest_name, countFocus = data.length + 1) {

    // sort data
    data = data.loc.sort((a, b) => {
        if (a.distance > b.distance) {
            return 1;
        }
        if (a.distance < b.distance) {
            return -1;
        }
        return 0; // a must be equal to b
    });
    
    var link_object; 
    for (i = 0; i < data.length; i++) {
        link_object = window.location.origin + "/table/" + mapParams.table_name + "/oid=" + data[i]['oid'] + "/";

        // set color based on countFocus
        if (i < countFocus) {
            _color = "#2A76D2"
        } else {
            _color = "#3FB1CE"
        }
        
        var marker = new mapboxgl.Marker({color: _color})
            .setLngLat([data[i]['longitude'], data[i]['latitude']])
            .setPopup(new mapboxgl.Popup().setHTML("<a href=" + link_object + ">" + JSON.stringify(data[i][dest_name]) + "</a><br><a href='" + data[i].website1 + "'>Website</a><br>Phone: " + data[i].phone1))
            .addTo(map);
        markerList.push(marker);
    }
}