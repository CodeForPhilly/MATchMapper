import { Component } from "react"

import "../styles/navBar.css"
import logo from "../images/MM_infinity-logo_luxwhite_labeled.png"

class NavBar extends Component {
    constructor(props){
        super(props)
        this.render = this.render.bind(this);
    }

    componentDidMount(){
        // const page_type = window.location.pathname.split("/").filter(e => e != "")[0]
        // const table_name = window.location.pathname.split("/").filter(e => e != "")[1]
        // for(var navItem of document.querySelectorAll("#nav-options li")){
        //     var linkUrl = navItem.querySelector("a").getAttribute("href")
        //     var pathnameWithoutFilters = "/" + page_type + "/" + table_name
        //     if(linkUrl == pathnameWithoutFilters){
        //     navItem.classList.add("selected")
        //     }
        // }
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