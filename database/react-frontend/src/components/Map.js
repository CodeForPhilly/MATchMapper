import React, { Component } from "react"
import ScriptTag from 'react-script-tag'
import $ from 'jquery'
import axios from 'axios'
import turf from '@turf/turf'

import mapboxgl from 'mapbox-gl'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';

import 'mapbox-gl/dist/mapbox-gl.css'
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css';

mapboxgl.accessToken = 'pk.eyJ1IjoibWF0Y2htYXBwZXIiLCJhIjoiY2tvMWJmZW9wMGtjdzMxb2k0NWhpeW0xMSJ9.ChZtypQ-p77nXwERIAt3Iw'

class Map extends Component {
  constructor(props){
    super(props)
    this.state = {
      jqueryReady: false,
      mapboxReady: false,
      geocoderElement: null,
      maxDistance: "5"
    }

    this.globalData = {}
    this.markerList = []
    this.myCircle = null
    this.geocoder = null

    this.distanceChanged = this.distanceChanged.bind(this)
    this.plotMarkers = this.plotMarkers.bind(this)
    this.toggleSearchModal = this.toggleSearchModal.bind(this)
    this.clearMap = this.clearMap.bind(this)
    this.reloadMap = this.reloadMap.bind(this)
  }

  generateRequestURL(){
    var mapParams = this.props.mapParams
    var table_name = mapParams.table_name
    var param_values = mapParams.included_values.replaceAll("amp;", "")
    var destination_name = mapParams.destination_name
    var excluded_values = mapParams.excluded_values.replaceAll("amp;", "")
    var keyword = mapParams.keyword
    
    var get_url = "/api/geodata/";
    get_url += table_name + "/";
    
    if (param_values != "" && param_values != "None") {
        get_url += param_values + "&archival_only=False/"
    }
    else {
        get_url += "archival_only=False/"
    }
    if (excluded_values != "None" && excluded_values != "") {
        get_url += excluded_values + "/"
    }
    if (keyword != "") { 
        if (excluded_values == "None" || excluded_values == "") { 
          get_url += "None/"
        }
        get_url += keyword
    }
    return get_url
  }

  requestGeoData(){
    var url = window.location.origin + this.generateRequestURL()
    axios.get(url).then(res => {
      const data = res.data
      this.globalData = data
      console.log(data)
      this.geocoder.on('result', ({ result }) => {
        const searchResult = result.geometry
        // Loop through sites and calculate distance to geocoder address
        for (const loc of data.loc) {
          loc.distance = turf.distance(searchResult, [loc.longitude, loc.latitude], { units: 'miles' })
        }
        // filter array by distance in field
        const dist = parseInt(this.state.maxDistance) //get distance from text field
        const data_ = data.loc.filter(d => d.distance < dist)
        // get count of sites within radius
        const sitesInFocus = data_.length
        // find site with min distance
        const closest = data_.sort((a, b) => {
          if (a.distance > b.distance) {
            return 1;
          }
          if (a.distance < b.distance) {
            return -1;
          }
          return 0; // a must be equal to b
        })[0]
        // fit the map on the entered location and the closest site
        // Create a bounding box using the dist variable and right triangle math
        // keep is simple by using 69 miles = 1 degree
        var halfBound = 2 * dist/(69*Math.sqrt(2));
        const c = searchResult.coordinates;
        const bbox = [[c[0] - halfBound, c[1] - halfBound], [c[0] + halfBound, c[1] + halfBound]];
        this.map.fitBounds(bbox)//, {padding: 600});
        // Draw circle of radius
        this.myCircle = new mapboxgl.MapboxCircle({lat: c[1], lng: c[0]}, dist * 1610, {
            fillOpacity: 0
        }).addTo(this.map)
        // Clear map and re-draw with different colors
        this.markerList = this.clearMap(this.markerList);
        this.plotMarkers(data, this.props.destination_name, sitesInFocus)
        // Change record totals
        this.setState({siteCount: sitesInFocus})
      })

      this.plotMarkers(data, this.props.destination_name);
      // this.setState({siteCount: data['loc'].length})
    })
  }

  // function to toggle the search modal on and off
  toggleSearchModal() {
    this.setState({showSearchModal: !(this.state.showSearchModal)})
  }

  plotMarkers(data, dest_name, countFocus = data.length + 1) {
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
    for (var i = 0; i < data.length; i++) {
        link_object = window.location.origin + "/table/" + this.props.table_name + "/oid=" + data[i]['oid'] + "/";

        // set color based on countFocus
        if (i < countFocus) {
            var _color = "#2A76D2"
        } else {
            var _color = "#3FB1CE"
        }
        var marker = new mapboxgl.Marker({color: _color})
            .setLngLat([data[i]['longitude'], data[i]['latitude']])
            .setPopup(new mapboxgl.Popup().setHTML("<a href=" + link_object + ">" + JSON.stringify(data[i][this.props.mapParams.destination_name]) + "</a><br><a href='" + data[i].website1 + "'>Website</a><br>Phone: " + data[i].phone1))
            .addTo(this.map);
        this.markerList.push(marker);
    }
  }

  componentDidMount(){
    this.map = new mapboxgl.Map({
      container: this.mapContainer, // container ID
      style: 'mapbox://styles/matchmapper/ckog0go3v3k1417nn7gex8ebr',
      center: [-75.158924, 39.9629223],
      zoom: 11
    })
    this.map.addControl(new mapboxgl.NavigationControl());
    this.geocoder = new MapboxGeocoder({
      accessToken: mapboxgl.accessToken,
      mapboxgl: mapboxgl, // Set the mapbox-gl instance
      marker: false, // Use the geocoder's default marker style,
      placeholder: "Search for Site by Address"
    })
    this.state.geocoderElement = this.geocoder.onAdd(this.map).outerHTML
    this.requestGeoData()
  }

  distanceChanged(e){
    this.setState({maxDistance: e.target.value})
  }

  // function to clear map
  clearMap() {
    for (var i = 0; i < this.markerList.length; i++ ) {
        this.markerList[i].remove()
    }
    this.markerList = []
  }

  reloadMap() {
      this.markerList = this.clearMap(this.markerList); 
      this.plotMarkers(this.globalData, this.props.destination_name); 
      this.myCircle.remove();
      this.geocoder.clear();
  }

  render(){
    return (
      <div id="mapContainer">
        <div id="siteSearch" style={{display: "none", overflow: "visible"}}>
            <button id="closeSearchModal" onClick={this.toggleSearchModal}>&#x2715;</button>
            <h2>Search By Address:</h2>
            <label for="distance">Radius (mi.):  </label>
            <input name="distance" id="distance" value="5" type="number" onChange={this.distanceChanged} style={{width: 40}}></input>
            <br/><br/>
            <div id="geocodeWidget" style={{width: "calc(100% - 14px)"}}>{this.state.geocoderElement}</div>
            <br/>
            <button id="clearSearch" onClick={this.reloadMap}>Start Over &#10005;</button>
        </div>
        <div id="map" ref={el => this.mapContainer = el}>
          {this.props.children}
          <p id="sitecount"></p>
        </div>
      </div>
    )
  }
}

export default Map