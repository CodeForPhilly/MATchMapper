import React, { Component } from "react"
import FilterOption from "./FilterOption"

class FilterGroup extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this)
        this.state = {
        }
        this.clear = this.clear.bind(this)
    }

    componentDidMount(){
        
    }

    clear(){
        for(var filterOption of this.props.filters){
            filterOption.ref.current.clear()
        }
    }

    render(){
        return(
            <div className="filterGroup">
                <div class="filterGroupHeader">{this.props.name}:</div>
                <div className="subfilter visible">
                    {this.props.filters.map((filter) => 
                        <FilterOption label={filter.label} affirmativeValue={filter.affirmativeValue} negativeValue={filter.negativeValue} ref={filter.ref} applyFilters={this.props.applyFilters}/>
                    )}
                </div>
            </div>
        )
    }
}

export default FilterGroup
