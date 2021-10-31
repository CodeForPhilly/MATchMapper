import { Component } from "react"

import { Link } from "react-router-dom";

import "../styles/navBar.css"
import logo from "../images/MM_infinity-logo_luxwhite_labeled.png"

class NavBar extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this);
    }

    render(){
        return(
            <nav>
                <a href="/" id="nav-logo" style={{ backgroundImage: `url(${logo})`}}> </a>
                <ul id="nav-options">
                    <li className="bold"><a href="/map/sites_all">MAP ALL</a></li>
                    <li className="bold"><a href="/table/sites_all">LIST ALL</a></li>
                    <div className="linebreak"></div>
                    <li><a href="/table/siterecs_dbhids_tad">Local MAT Directory (DBHIDS)</a></li>
                    <li><a href="/table/siterecs_samhsa_ftloc">National Find Treatment Programs (SAMHSA)</a></li>
                    <li><a href="/table/siterecs_samhsa_otp">Opioid Treatment Programs (SAMHSA)</a></li>
                </ul>
            </nav>
      )
    }
}

export default NavBar
