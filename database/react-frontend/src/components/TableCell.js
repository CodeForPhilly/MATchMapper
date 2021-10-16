import { Component } from "react"


class TableCell extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this);
        this.state = {
            visibility: false
        }
    }

    componentDidMount(){
        var column_name = null;
        for(var name of this.props.className.split(" ")){
            if(name.substring(0,4) == "col_"){
                column_name = name
            }
        }
        this.setState({visibility: this.props.visibility[column_name]})
    }

    render(){
        var sticking;
        if(!this.props.sticking){
            sticking = {top: false, left: false}
        } else {
            sticking = this.props.sticking
        }
        return(
            <>{ this.state.visibility ? 
                <>{ this.props.isHeader ? 
                    <th className={this.props.className + (sticking.top ? " stuck" : "")}>{ this.props.children }</th>
                    : <td className={this.props.className + (sticking.left ? " stuck" : "")}>{ this.props.children }</td>
                }</>
            : null}</>
        )
    }
}

export default TableCell
