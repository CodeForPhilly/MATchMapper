import React, { Component } from "react"
class Container extends Component {
    render(){
        return(
            <div
                style={{
                opacity: this.props.isFinished ? 0 : 1,
                pointerEvents: 'none',
                transition: `opacity ${this.props.animationDuration}ms linear`,
                }}
            >
                {this.props.children}
            </div>
        )
    }
}

export default Container
