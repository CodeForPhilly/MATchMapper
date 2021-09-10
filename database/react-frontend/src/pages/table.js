import { Component } from "react"
import {withRouter} from 'react-router-dom'
import axios from "axios"

import FilterBar from "../components/FilterBar.js"
import NavBar from "../components/NavBar.js"

class TablePage extends Component {
    constructor(props){
        super(props)
        this.state = {
            table_info: {
                display_name: ""
            },
            isLoaded: false
        }
        this.render = this.render.bind(this)
        this.toLegalURL = this.toLegalURL.bind(this)
    }

    componentDidMount(){
        var { table_name, included_values, excluded_values } = this.props.match.params
        var searchParams = new URLSearchParams(this.props.location.search)
        this.setState({ urlParams: this.props.match.params, searchParams: searchParams })
        axios.get(`/headless/${table_name}/${included_values ? included_values : "None"}/${excluded_values ? excluded_values : "None"}`).then(res => {
            const data = res.data
            this.setState({ objects: data.objects, table_info: data.table_info, isLoaded: true })
            document.title = this.state.table_info.display_name
        })
    }

    toLegalURL(url){
        if(url == null){
            return ""
        }
        var splitIllegal = url.split(":")
        if(splitIllegal[0] == "https" || splitIllegal[0] == "http"){
            return url
        }
        else {
            return "//" + url
        }
    }

    render(){
        if (this.state.isLoaded) {
            return(
                <div>
                    <NavBar/>
                    <div id="flexContainer">
                        <FilterBar/>
                        
                        <div id="table">
                            <h5 id="resultDescription">
                                <span id="dataSource" className="bold">SOURCE: <a href={this.state.table_info.source_url} target="_blank">{this.state.table_info.display_name}</a></span><br/>
                                <span id="lastUpdatedNotice">Most recent download: <span className="bold">{this.state.table_info.update_recency}</span></span><br/>
                                <span className="bold">{this.state.objects.length}</span> of <span className="bold">{this.state.table_info.records_count}</span> records for <span className="bold">{this.state.table_info.facility_type}</span> {this.state.table_info.source_range}
                            </h5>
                            <div id="extraContainer">
                            <table>
                                <tbody>
                                <tr>
                                    <th className="facilityName col-FACILITY">Facility</th>
                                    <th className="col-TELEHEALTH">Telehealth</th>
                                    <th className="col-PHONE">Phone</th>
                                    <th className="col-ADDRESS">Address</th>
                                    <th className="col-ZIPCODE">Zip Code</th>
                                    <th className="col-WALKINHOURS">Walk-In Hours</th>
                                    <th className="col-MATINFO">MAT Info</th>
                                    <th className="col-WHICHMAT">Which MAT</th>
                                    <th className="col-BUPRENORPHINE">Buprenorphine</th>
                                    <th className="col-NALTREXONE">Naltrexone</th>
                                    <th className="col-METHADONE">Methadone</th>
                                    <th className="col-PAYMENTOPTIONS">Payment Options</th>
                                    <th className="col-SERVICES">Services</th>
                                    <th className="col-ADDITIONALINFORMATION">Additional Information</th>
                                    <th className="col-ADDITIONALNOTES">Additional Notes</th>
                                    <th className="col-CERTIFICATIONDATE">Certification Date</th>
                                    <th className="col-DATASOURCES">Data Source(s)</th>
                                </tr>
                                { this.state.objects.map((site) =>
                                    <tr>
                                        <td className="facilityName wrap col-FACILITY">
                                            <p className="cellText bold">{site.name1}</p>
                                            <p className="cellText semibold">{site.name2}</p>
                                            <p className="cellText semibold">{site.name3}</p>
                                            <p className="cellText"><a target="_blank" href={this.toLegalURL(site.website1)}>{site.website1}</a></p>
                                            <p className="cellText"><a target="_blank" href={this.toLegalURL(site.website2)}>{site.website2}</a></p>
                                        </td>
                                        <td className="nowrap col-TELEHEALTH">
                                            <p className="cellText">
                                                {site.telehealth ? "Yes" : "No"}
                                            </p>
                                        </td>
                                        <td className="nowrap col-PHONE">
                                            <p className="cellText bold">
                                                {site.phone1}
                                            </p>
                                            <p className="cellText semibold">
                                                {site.phone2}
                                            </p>
                                            <p className="cellText semibold">
                                                {site.phone3}
                                            </p>
                                        </td>
                                        <td className="nowrap col-ADDRESS">
                                            <p className="cellText bold">
                                                {site.street1}
                                            </p>
                                            {site.street2 && (
                                                <p className="cellText">
                                                    {site.street2}
                                                </p>
                                            )}
                                            <p className="cellText">
                                                {site.city}, {site.state_usa}
                                            </p>
                                        </td>
                                        <td className="col-ZIPCODE">
                                            <p className="cellText bold">{site.zipcode}</p>
                                        </td>
                                        <td className="col-WALKINHOURS">
                                            <p className="cellText bold">{site.walk_in_hours}</p>
                                        </td>
                                        <td className="col-MATINFO">
                                            <p className="cellText bold">{site.mat_info}</p>
                                        </td>
                                        <td className="nowrap col-WHICHMAT">
                                            <p className="cellText">
                                                {site.mat_avail == "Unclear" && <span>"None confirmed"<br/></span>}
                                                Buprenorphine: <b>{ site.bu }</b><br/>
                                                Naltrexone/Vivitrol: <b>{ site.nu }</b><br/>
                                                Methadone: <b>{site.mu }</b>
                                            </p>
                                        </td>
                                        <td className="nowrap col-BUPRENORPHINE">
                                            { site.bu ? 
                                            <span>
                                                <p className="cellText">
                                                    Prescribed: <br/>
                                                    <span className="bold">BU OPTIONS GO HERE</span>
                                                </p>
                                                <p>
                                                    <span>
                                                        {site.buu != null &&
                                                        <span>
                                                            Used in treatment:
                                                            <span className="bold">
                                                                {site.buu || site.bu ? "Yes" : "No"}
                                                            </span>
                                                            <br/>
                                                        </span>
                                                        }
                                                    </span>
                                                    <span showonlyfor="siterecs_samhsa_ftloc siterecs_dbhids_tad">
                                                        Maintenance:
                                                        <span className="bold">
                                                            {site.bum ? "Yes" : "No"}
                                                        </span>
                                                    </span>
                                                    <br/>
                                                    <span>
                                                        Maintenance for predetermined time:
                                                        <span className="bold">
                                                            {site.bmw ? "Yes" : "No"}
                                                        </span>
                                                    </span>
                                                    <br/>
                                                    <span>
                                                        Detoxification:
                                                        <span className="bold">
                                                            {site.db_field ? "Yes" : "No"}
                                                        </span>
                                                    </span>
                                                    <br/>
                                                </p>
                                            </span>
                                            :
                                            <p className="cellText">Not available at this facility</p>
                                            }
                                        </td>
                                        <td className="nowrap col-NALTREXONE">
                                            {site.nu ?
                                                <p className="cellText">
                                                    {(site.vtrl || site.nxn) && 
                                                        <span>
                                                            Prescribed:
                                                            <span className="bold">NU OPTIONS GO HERE</span>
                                                            <br/>
                                                        </span>
                                                    }
                                                    Used for relapse prevention:
                                                    <span className="bold">
                                                        {site.rpn ? "Yes" : "No"}
                                                    </span>
                                                </p>
                                                :
                                                <p className="cellText">Not available at this facility</p>
                                            }
                                        </td>
                                        <td className="nowrap col-METHADONE"> 
                                            {site.mu ?
                                                <p className="cellText">
                                                    {site.meth != null &&
                                                        <span>
                                                            Prescribed:
                                                            <span className="bold">{site.meth}</span>
                                                            <br/>
                                                        </span>
                                                    }
                                                    Induction:
                                                    <span className="bold">
                                                        {site.mui ? "Yes" : "No"}
                                                    </span>
                                                    <br/>
                                                    Maintenance:
                                                    <span className="bold">
                                                        {site.mm ? "Yes" : "No"}
                                                    </span>
                                                    <br/>
                                                    Maintenance for predetermined time:
                                                    <span className="bold">
                                                        {site.mmw ? "Yes" : "No"}
                                                    </span>
                                                    <br/>
                                                    Detoxification:
                                                    <span className="bold">
                                                        {site.dm ? "Yes" : "No"}
                                                    </span>
                                                </p>
                                                :
                                                <p className="cellText">Not available at this facility</p>
                                            }
                                        </td>
                                        <td className="nowrap col-PAYMENTOPTIONS">
                                            Medicaid: <b>{(site.md == true || site.md == "Yes") && "Yes"}{(site.md == false || site.md == "No") && "No"}{(site.md == "Unclear") && "Unclear"}</b><br/>
                                            Medicare: <b>{(site.mc == true || site.mc == "Yes") && "Yes"}{(site.mc == false || site.mc == "No") && "No"}{(site.mc == "Unclear") && "Unclear"}</b><br/>
                                            Payment assistance available: <b>{(site.pa == true || site.pa == "Yes") && "Yes"}{(site.pa == false || site.pa == "No") && "No"}{(site.pa == "Unclear") && "Unclear"}</b>
                                        </td>
                                        <td className="nowrap col-SERVICES">
                                        Child care: <b>{(site.ccc == true || site.ccc == "Yes") && "Yes"}{(site.ccc == false || site.ccc == "No") && "No"}{(site.ccc == "Unclear") && "Unclear"}</b><br/>
                                        Domestic violence services: <b>{(site.dvh == true || site.dvh == "Yes") && "Yes"}{(site.dvh == false || site.dvh == "No") && "No"}{(site.dvh == "Unclear") && "Unclear"}</b><br/>
                                        Housing services: <b>{(site.hs == true || site.hs == "Yes") && "Yes"}{(site.hs == false || site.hs == "No") && "No"}{(site.hs == "Unclear") && "Unclear"}</b><br/>
                                        Mental health services: <b>{(site.mhs == true || site.mhs == "Yes") && "Yes"}{(site.mhs == false || site.mhs == "No") && "No"}{(site.mhs == "Unclear") && "Unclear"}</b><br/>
                                        Pregnancy care: <b>{(site.pw == true || site.pw == "Yes") && "Yes"}{(site.pw == false || site.pw == "No") && "No"}{(site.pw == "Unclear") && "Unclear"}</b><br/>
                                        Transportation assistance: <b>{(site.ta == true || site.ta == "Yes") && "Yes"}{(site.ta == false || site.ta == "No") && "No"}{(site.ta == "Unclear") && "Unclear"}</b>
                                        </td>
                                        <td className="col-ADDITIONALINFORMATION">{ site.additional_info }</td>
                                        <td className="col-ADDITIONALNOTES">{ site.ref_notes }</td>
                                        <td className="col-CERTIFICATIONDATE">{ site.full_certification }</td>
                                        <td className="nowrap col-DATASOURCES">
                                            {site.id_dbhids_tad && <span><a href="/table/siterecs_dbhids_tad">DBHIDS MAT Directory</a><br/></span>}
                                            {site.ba_dbhids_tad && <span>Bed Availability Updates<br/></span>}
                                            {site.id_samhsa_ftloc && <span><a href="/table/siterecs_samhsa_ftloc">SAMHSA Find Treatment</a><br/></span>}
                                            {site.id_samhsa_otp && <span><a href="/table/siterecs_samhsa_otp">SAMHSA OTPs Directory</a><br/></span>}
                                            {site.id_hfp_fqhc && <span>HRSA or HFP (FQHCs)</span>}
                                        </td>
                                    </tr>
                                ) }
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <script src="scripts/filter.js"></script>
                    <script src="scripts/hideColumns.js"></script>
                </div>
            </div>
            )
        } else{
            return null
        }
    }
}

export default withRouter(TablePage)
