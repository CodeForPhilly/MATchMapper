import { Component } from "react"

import { Link } from "react-router-dom";

import "../styles/navBar.css"
import logo from "../images/MM_infinity-logo_luxwhite_labeled.png"

class NavBar extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this)
    }

    componentDidMount(){
        // console.log("from navbar:")
        // console.log(window.location.pathname)
    }

    render(){
        return(
            <nav>
                <a href="/" id="nav-logo" style={{ backgroundImage: `url(${logo})`}}> </a>
                <ul id="nav-options">
                    <li className={"bold " + (window.location.pathname.includes("/map/sites_all") ? "selected" : "")}><a href="/map/sites_all">MAP ALL</a></li>
                    <li className={"bold " + (window.location.pathname.includes("/table/sites_all") ? "selected" : "")}><a href="/table/sites_all">LIST ALL</a></li>
                    <div className="linebreak"></div>
                    <li className={(window.location.pathname.includes("/table/siterecs_dbhids_tad") ? "selected" : "")}><a href="/table/siterecs_dbhids_tad">Local MAT Directory (DBHIDS)</a></li>
                    <li className={(window.location.pathname.includes("/table/siterecs_samhsa_ftloc") ? "selected" : "")}><a href="/table/siterecs_samhsa_ftloc">National Find Treatment Programs (SAMHSA)</a></li>
                    <li className={(window.location.pathname.includes("/table/siterecs_samhsa_otp") ? "selected" : "")}><a href="/table/siterecs_samhsa_otp">Opioid Treatment Programs (SAMHSA)</a></li>
                </ul>
            </nav>
      )
    }
}

export default NavBar
