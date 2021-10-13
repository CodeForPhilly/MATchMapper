import { Component } from "react"
import FilterOption from "./FilterOption"

class FilterGroup extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this);
        this.state = {
        }
    }

    componentDidMount(){
        
    }

    render(){
        return(
            <div className="filterGroup">
                <div class="filterGroupHeader">{this.props.name}:</div>
                <div className="subfilter visible">
                    {this.props.filters.map((filter) => 
                        <FilterOption label={filter.label} affirmativeValue={filter.affirmativeValue} negativeValue={filter.negativeValue}/>
                    )}
                </div>
            </div>
        )
    }
}

export default FilterGroup
