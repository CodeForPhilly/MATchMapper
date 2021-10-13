import { Component } from "react"


class FilterOption extends Component {
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
            <div className="filterCriteria">
                <label>{this.props.label}</label>
                <div className="specifier equal"><p>✓</p></div>
                <div className="specifier notequal"><p>✗</p></div>
            </div>
        )
    }
}

export default FilterOption
