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
    param_values = param_values.replace("amp;", "")
    excluded_values = excluded_values.replace("amp;", "")
    console.log(table_name)
    console.log(param_values)
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
                document.querySelector("#sitecount").textContent = data['loc'].length
                var link_object; 
                for (i = 0; i < data['loc'].length; i++) {
                    console.log([data['loc'][i]['latitude'], data['loc'][i]['longitude']])
                    link_object = window.location.origin + "/table/" + table_name + "/oid=" + data['loc'][i]['oid'] + "/";
                    var marker = new mapboxgl.Marker()
                        .setLngLat([data['loc'][i]['longitude'], data['loc'][i]['latitude']])
                        .setPopup(new mapboxgl.Popup().setHTML("<a href=" + link_object + ">" + JSON.stringify(data['loc'][i][destination_name]) + "</a>" ))
                        .addTo(map);
                }
            }
        });
});