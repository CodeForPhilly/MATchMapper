import { Component } from "react"

import FilterGroup from "./FilterGroup";

import "../styles/filterBar.css"

class FilterBar extends Component {
    constructor(props){
        super(props)
        this.state = {
            filterGroups: []
        }
        this.render = this.render.bind(this);
    }

    componentDidMount(){
        var raw_filter_rows = []
        for(var row of this.props.table_filters_raw.split("|").slice(1)){
            raw_filter_rows.push(row.split(";"))
        }
        var filtersByGroup = {}
        for(var row of raw_filter_rows){
            if(row[5] + row[6] !== ""){
                var filter = { label: row[2], affirmative_value: row[5], negative_value: row[6] }
                if(row[1] in filtersByGroup){
                    filtersByGroup[row[1]].push(filter)
                } else{
                    filtersByGroup[row[1]] = [filter]
                }
            }
        }
        var sortedFilterGroupNames = []
        for(var row of raw_filter_rows.sort(function(a, b) { return a[0] - b[0] })){
            if(!sortedFilterGroupNames.includes(row[1])){
                console.log(row[1] + " not in ")
                console.log(sortedFilterGroupNames)
                sortedFilterGroupNames.push(row[1])
            }
        }
        var sortedFilterGroups = []
        for(var name of sortedFilterGroupNames){
            sortedFilterGroups.push({name: name, filters: filtersByGroup[name]})
        }
        this.setState({filterGroups: sortedFilterGroups});
    }

    applyFilters(){

    }

    render(){
        return(
            <div id="sidebar">
                <button id="clearFilters">Start Over &#10005;</button>
                <div id="filterOptions">
                    <h2>Search:</h2>
                    <input id="searchBar" type="text" placeholder="Search..."/>
                    { this.props.showSort !== false ? (
                        <div>
                            <h2>Sort:</h2>
                            <div id="sortOptions">
                                <label>By:</label>
                                <select id="sortBy" defaultValue="">
                                    <option disabled hidden value=""></option>
                                    <option value="order=name1">Facility Name</option>
                                    <option value="order=street1&order=street2">Address</option>
                                    <option value="order=city">City</option>
                                    <option value="order=state_usa&order=city">State</option>
                                    <option value="order=zipcode">Zip Code</option>
                                </select>
                                <label>Order:</label>
                                <select id="orderingOptions" defaultValue="None">
                                    <option disabled hidden value="None"></option>
                                    <option value="">Ascending</option>
                                    <option value="-">Descending</option>
                                </select>
                            </div>
                        </div>
                    ) : null}
                    <h2>Filter:</h2>
                    <label>Filter your search with the following criteria:</label>
                    <div id="filterContainer">
                        {this.state.filterGroups.map((group) => <FilterGroup applyFilters={this.applyFilters} name={group.name} filters={group.filters}/>)}
                    </div>
                </div>
            </div>
      )
    }
}

export default FilterBar
