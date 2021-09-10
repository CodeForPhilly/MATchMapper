import { Component } from "react"

class FilterBar extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this);
    }

    componentDidMount(){
    }

    render(){
        return(
            <div id="sidebar">
                <button id="clearFilters">Start Over &#10005;</button>
                <div id="filterOptions">
                    <h2>Search:</h2>
                    <input id="searchBar" type="text" placeholder="Search..."/>
                    { this.props.showSort != false ? (
                        <div>
                            <h2>Sort:</h2>
                            <div id="sortOptions">
                                <label>By:</label>
                                <select id="sortBy">
                                    <option selected disabled hidden value=""></option>
                                    <option value="order=name1">Facility Name</option>
                                    <option value="order=street1&order=street2">Address</option>
                                    <option value="order=city">City</option>
                                    <option value="order=state_usa&order=city">State</option>
                                    <option value="order=zipcode">Zip Code</option>
                                </select>
                                <label>Order:</label>
                                <select id="orderingOptions">
                                    <option selected disabled hidden value="None"></option>
                                    <option value="">Ascending</option>
                                    <option value="-">Descending</option>
                                </select>
                            </div>
                        </div>
                    ) : null}
                    <h2>Filter:</h2>
                    <label>Filter your search with the following criteria:</label>
                    <div id="filterContainer"></div>
                </div>
            </div>
      )
    }
}

export default FilterBar
