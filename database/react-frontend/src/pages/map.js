import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import axios from "axios";
import ScriptTag from "react-script-tag";
// eslint-disable-next-line import/no-webpack-loader-syntax
import mapboxgl from "!mapbox-gl";
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";

import FilterBar from "../components/FilterBar.js";
import NavBar from "../components/NavBar.js";
import Map from "../components/Map.js";
import ProgressBar from "../components/ProgressBar.js";

import "../styles/map.css";
import "mapbox-gl/dist/mapbox-gl.css";

mapboxgl.accessToken =
  "pk.eyJ1IjoibWF0Y2htYXBwZXIiLCJhIjoiY2tvMWJmZW9wMGtjdzMxb2k0NWhpeW0xMSJ9.ChZtypQ-p77nXwERIAt3Iw";

class MapPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      table_info: {
        display_name: "",
        display_cols: "",
      },
      isLoaded: false,
      tableScroll: {
        x: null,
        y: null,
      },
      sticking: {
        top: false,
        left: false,
      },
      column_visibility: {
        col_FACILITY: false,
        col_TELEHEALTH: false,
        col_PHONE: false,
        col_ADDRESS: false,
        col_ZIPCODE: false,
        col_WALKINHOURS: false,
        col_MATINFO: false,
        col_WHICHMAT: false,
        col_BUPRENORPHINE: false,
        col_NALTREXONE: false,
        col_METHADONE: false,
        col_PAYMENTOPTIONS: false,
        col_SERVICES: false,
        col_ADDITIONALINFORMATION: false,
        col_ADDITIONALNOTES: false,
        col_CERTIFICATIONDATE: false,
        col_DATASOURCES: false,
      },
      current_request_elements: {
        keyword: "",
        included_values_string: "None",
        excluded_values_strings: "None",
      },
      mapParams: {
        table_name: "",
        included_values: "None",
        excluded_values: "None",
        keyword: "",
        destination_name: "name1",
      },
      mapKey: 0,
      maxDistance: "5",
      showSearchByAddress: false,
      isLoading: false,
    };
    this.naming_dict = {
      sitecodes_samhsa_ftloc: "service_name",
      siterecs_samhsa_ftloc: "name1",
      siterecs_samhsa_otp: "program_name",
      siterecs_dbhids_tad: "name1",
      ba_dbhids_tad: "name_ba",
      siterecs_hfp_fqhc: "name_short",
      siterecs_other_srcs: "name1",
      sites_all: "name1",
      Siterecs_dbhids_tads: "name1",
    };
    this.map = React.createRef();
    this.render = this.render.bind(this);
    this.getUrlParams = this.getUrlParams.bind(this);
    this.makeRequest = this.makeRequest.bind(this);
    this.request_URL_from_params = this.request_URL_from_params.bind(this);
    this.applyFilters = this.applyFilters.bind(this);
    this.distanceChanged = this.distanceChanged.bind(this);
    this.toggleSearchByAddress = this.toggleSearchByAddress.bind(this);
  }

  componentDidMount() {
    this.getUrlParams();
    this.makeRequest(this.request_URL_from_params());
  }

  request_URL_from_params() {
    var { table_name, query, keyword } = this.props.match.params;
    var included_values = [];
    var excluded_values = [];
    var keyword = "";
    if (query) {
      for (var param of query.split("&")) {
        if (param.split("=")[0] == "keyword") {
          keyword = param.split("=")[1];
        } else if (param.includes("!=")) {
          excluded_values.push({
            key: param.split("!=")[0],
            value: param.split("!=")[1],
          });
        } else {
          included_values.push({
            key: param.split("=")[0],
            value: param.split("=")[1],
          });
        }
      }
    }
    var included_values_strings = [];
    var excluded_values_strings = [];
    for (var pair of included_values) {
      included_values_strings.push(pair.key + "=" + pair.value);
    }
    for (var pair of excluded_values) {
      excluded_values_strings.push(pair.key + "=" + pair.value);
    }
    var django_query = `/headless/${table_name}/${
      included_values_strings.length > 0
        ? included_values_strings.join("&")
        : "None"
    }/${
      excluded_values_strings.length > 0
        ? excluded_values_strings.join("&")
        : "None"
    }${keyword.length > 0 ? "/" + keyword : ""}`;
    return django_query;
  }

  makeRequest(django_query, refresh) {
    console.log("starting request");
    this.setState({ isLoading: true });
    var keyword =
      django_query.split("/").length > 5
        ? django_query.split("/")[django_query.split("/").length - 1]
        : "";
    var excluded_values_strings =
      django_query.split("/")[django_query.split("/").length - 2];
    var included_values_strings =
      django_query.split("/")[django_query.split("/").length - 3];
    this.setState({
      current_request_elements: {
        keyword: keyword,
        included_values_string: included_values_strings,
        excluded_values_strings: excluded_values_strings,
      },
    });
    axios.get(django_query).then((res) => {
      const data = res.data;
      this.setState(
        { objects: data.objects, table_info: data.table_info },
        () => console.log(this.state.table_info)
      );
      document.title = this.state.table_info.display_name;
      this.setState({ isLoaded: true });
      if (refresh) {
        this.setState({ mapKey: this.state.mapKey + 1 });
      }
      console.log("request completed");
      this.setState({ isLoading: false });
    });
  }

  getUrlParams() {
    var { table_name, query, keyword } = this.props.match.params;
    var included_values = [];
    var excluded_values = [];
    var keyword = "";
    if (query) {
      for (var param of query.split("&")) {
        if (param.split("=")[0] == "keyword") {
          keyword = param.split("=")[1];
        } else if (param.includes("!=")) {
          excluded_values.push({
            key: param.split("!=")[0],
            value: param.split("!=")[1],
          });
        } else {
          included_values.push({
            key: param.split("=")[0],
            value: param.split("=")[1],
          });
        }
      }
    }
    var included_values_strings = [];
    var excluded_values_strings = [];
    for (var pair of included_values) {
      included_values_strings.push(pair.key + "=" + pair.value);
    }
    for (var pair of excluded_values) {
      excluded_values_strings.push(pair.key + "=" + pair.value);
    }
    this.setState({
      mapParams: {
        table_name: table_name,
        included_values:
          included_values_strings.length > 0
            ? included_values_strings.join("&")
            : "None",
        excluded_values:
          excluded_values_strings.length > 0
            ? excluded_values_strings.join("&")
            : "None",
        keyword: keyword.length > 0 ? keyword : "",
        destination_name: this.naming_dict[table_name],
      },
    });
  }

  applyFilters(groups, sortingInfo, keyword) {
    var included_values = [];
    var excluded_values = [];
    for (var group of groups) {
      for (var filter of group.ref.current.props.filters) {
        if (filter.ref.current.getValue() != null) {
          for (var condition of filter.ref.current.getValue().split("&")) {
            if (condition.includes("!=")) {
              excluded_values.push(condition.replace("!=", "="));
            } else {
              included_values.push(condition);
            }
          }
        }
      }
    }
    var sortingElement =
      sortingInfo.direction == "-"
        ? sortingInfo.keys.replace("=", "=-")
        : sortingInfo.keys;
    var query_url = `/headless/${this.state.table_info.table_name}/${
      included_values.length > 0 ? included_values.join("&") : "None"
    }/${excluded_values.length > 0 ? excluded_values.join("&") : "None"}${
      keyword.length > 0 ? "/" + keyword : ""
    }${sortingInfo.keys.length > 0 ? "/?" + sortingElement : ""}`.replace(
      "//",
      "/"
    );
    // console.log(query_url)
    this.makeRequest(query_url, true);
    this.setState(
      {
        mapParams: {
          table_name: this.state.table_info.table_name,
          included_values:
            included_values.length > 0 ? included_values.join("&") : "None",
          excluded_values:
            excluded_values.length > 0 ? excluded_values.join("&") : "None",
          keyword: keyword.length > 0 ? "/" + keyword : "",
          destination_name: this.naming_dict[this.state.table_info.table_name],
        },
      },
      function () {
        console.log(this.state.mapParams);
        this.map.current.clearMap();
        this.map.current.requestGeoData();
      }
    );
  }

  distanceChanged(e) {
    this.setState({ maxDistance: e.target.value });
  }

  toggleSearchByAddress() {
    this.setState({ showSearchByAddress: !this.state.showSearchByAddress });
  }

  render() {
    if (this.state.isLoaded) {
      console.log(this.map);
      return (
        <div id="body">
          <link rel="preconnect" href="https://fonts.gstatic.com" />
          <link
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap"
            rel="stylesheet"
          />
          <ProgressBar isLoading={this.state.isLoading} />
          <NavBar />
          <Map
            mapParams={this.state.mapParams}
            tableInfo={this.state.table_info}
            ref={this.map}
            showSearchModal={this.state.showSearchByAddress}
          >
            <FilterBar
              applyFilters={this.applyFilters}
              table_filters_raw={this.state.table_info.filters}
              showSort={false}
            >
              <button id="clearSearch" onClick={this.toggleSearchByAddress}>
                Show distance search
              </button>
            </FilterBar>
          </Map>
        </div>
      );
    } else {
      return null;
    }
  }
}

export default withRouter(MapPage);
