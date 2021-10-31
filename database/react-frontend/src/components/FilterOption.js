import { Component } from "react"


class FilterOption extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this);
        this.state = {
            toggleState: 0
        }
        this.toggleAffirmative = this.toggleAffirmative.bind(this);
        this.toggleNegative = this.toggleNegative.bind(this);
        this.getValue = this.getValue.bind(this);
        this.clear = this.clear.bind(this);
    }

    toggleAffirmative(){
        var newState = 0
        if(this.state.toggleState != 1){
            newState = 1
        }
        this.state.toggleState = newState
        this.props.applyFilters()
    }
    toggleNegative(){
        var newState = 0
        if(this.state.toggleState != -1){
            newState = -1
        }
        this.state.toggleState = newState
        this.props.applyFilters()
    }
    getValue(){
        if(this.state.toggleState == 1){
            console.log(this.props)
            return this.props.affirmativeValue
        }
        if(this.state.toggleState == -1){
            return this.props.negativeValue
        }
        return null
    }

    clear(){
        this.state.toggleState = 0
    }

    render(){
        return(
            <div className="filterCriteria">
                <label>{this.props.label}</label>
                <div className={"specifier equal" + (this.state.toggleState==1 ? " selected" : "")} onClick={this.toggleAffirmative}><p>✓</p></div>
                <div className={"specifier notequal" + (this.state.toggleState==-1 ? " selected" : "")} onClick={this.toggleNegative}><p>✗</p></div>
            </div>
        )
    }
}

export default FilterOption
