import React, { Component } from "react"
class Bar extends Component {
    render(){
        return(
          <div
          style={{
            background: '#29d',
            height: 2,
            left: 0,
            marginLeft: `${(-1 + this.props.progress) * 100}%`,
            position: 'fixed',
            top: 0,
            transition: `margin-left ${this.props.animationDuration}ms linear`,
            width: '100%',
            zIndex: 1031,
          }}
        >
          <div
            style={{
              boxShadow: '0 0 10px #29d, 0 0 5px #29d',
              display: 'block',
              height: '100%',
              opacity: 1,
              position: 'absolute',
              right: 0,
              transform: 'rotate(3deg) translate(0px, -4px)',
              width: 100,
            }}
          />
        </div>
        )
    }
}

export default Bar