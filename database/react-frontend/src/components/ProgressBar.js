import React, { Component } from "react"

import { NProgress } from '@tanem/react-nprogress'

import Bar from "./ProgressBar-Bar.js"
import Container from "./ProgressBar-Container.js"

class ProgressBar extends Component {
    constructor(props){
        super(props)
    }

    render(){
        return(
            <NProgress isAnimating={this.props.isLoading} incrementDuration={200}>
                {({ animationDuration, isFinished, progress }) => (
                <Container animationDuration={animationDuration} isFinished={isFinished}>
                    <Bar animationDuration={animationDuration} progress={progress} />
                </Container>
                )}
            </NProgress>
        )
    }
}

export default ProgressBar
