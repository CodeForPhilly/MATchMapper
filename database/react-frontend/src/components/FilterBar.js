import React, { Component } from "react"

import FilterGroup from "./FilterGroup";

import "../styles/filterBar.css"

class FilterBar extends Component {
    constructor(props){
        super(props)
        this.state = {
            filterGroups: [],
            keyword: "",
            sortKeys: "",
            sortDirection: ""
        }
        this.render = this.render.bind(this)
        this.clear = this.clear.bind(this)
        this.applyFilters = this.applyFilters.bind(this)
        this.setDirection = this.setDirection.bind(this)
        this.setSorting = this.setSorting.bind(this)
        this.handleKeyDown = this.handleKeyDown.bind(this)
        this.handleKeywordChange = this.handleKeywordChange.bind(this)
    }

    componentDidMount(){
        var raw_filter_rows = []
        for(var row of this.props.table_filters_raw.split("|").slice(1)){
            raw_filter_rows.push(row.split(";"))
        }
        var filtersByGroup = {}
        for(var row of raw_filter_rows){
            if(row[5] + row[6] !== ""){
                var filter = { label: row[2], affirmativeValue: row[5], negativeValue: row[6], ref: React.createRef() }
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
                sortedFilterGroupNames.push(row[1])
            }
        }
        var sortedFilterGroups = []
        for(var name of sortedFilterGroupNames){
            sortedFilterGroups.push({name: name, filters: filtersByGroup[name], ref: React.createRef()})
        }
        this.setState({filterGroups: sortedFilterGroups});
    }

    clear(){
        for(var group of this.state.filterGroups){
            group.ref.current.clear()
        }
        this.state.keyword = ""
        this.state.sortDirection = ""
        this.state.sortKeys = ""
        this.applyFilters()
    }

    applyFilters(){
        this.props.applyFilters(this.state.filterGroups, {keys: this.state.sortKeys, direction: this.state.sortDirection}, this.state.keyword)
    }

    setSorting(e){
        this.state.sortKeys = e.target.value
        this.applyFilters()
    }

    setDirection(e){
        this.state.sortDirection = e.target.value
        if(this.state.sortKeys == ""){
            this.state.sortKeys = "order=name1"
        }
        this.applyFilters()
    }

    handleKeyDown(e){
        if(e.key === "Enter"){
            this.applyFilters()
        }
        else {
            console.log(e.key)
        }
    }
    handleKeywordChange(e){
        this.setState({keyword: e.target.value})
    }

    render(){
        return(
            <div id="sidebar">
                <button id="clearFilters" onClick={this.clear}>Start Over &#10005;</button>
                <div id="filterOptions">
                    <h2>Search:</h2>
                    <input id="searchBar" type="text" placeholder="Search..." onKeyDown={this.handleKeyDown} onChange={this.handleKeywordChange} value={this.state.keyword}/>
                    {this.props.children}
                    { this.props.showSort !== false ? (
                        <div>
                            <h2>Sort:</h2>
                            <div id="sortOptions">
                                <label>By:</label>
                                <select id="sortBy" defaultValue="" onChange={this.setSorting} value={this.state.sortKeys}>
                                    <option disabled hidden value=""></option>
                                    <option value="order=name1">Facility Name</option>
                                    <option value="order=street1&order=street2">Address</option>
                                    <option value="order=city">City</option>
                                    <option value="order=state_usa&order=city">State</option>
                                    <option value="order=zipcode">Zip Code</option>
                                </select>
                                <label>Order:</label>
                                <select id="orderingOptions" defaultValue="" onChange={this.setDirection} value={this.state.sortDirection}>
                                    <option value="">Ascending</option>
                                    <option value="-">Descending</option>
                                </select>
                            </div>
                        </div>
                    ) : null}
                    <h2>Filter:</h2>
                    <label>Filter your search with the following criteria:</label>
                    <div id="filterContainer">
                        {this.state.filterGroups.map((group) => <FilterGroup applyFilters={this.applyFilters} name={group.name} key={group.name} filters={group.filters} ref={group.ref}/>)}
                    </div>
                </div>
            </div>
      )
    }
}

export default FilterBar
