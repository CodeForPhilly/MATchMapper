import { Component } from "react"
import {withRouter} from 'react-router-dom'
import axios from "axios"

import FilterBar from "../components/FilterBar.js"
import NavBar from "../components/NavBar.js"
import TableCell from "../components/TableCell.js"
import ProgressBar from "../components/ProgressBar.js"

import "../styles/table.css"

class TablePage extends Component {
    constructor(props){
        super(props)
        this.state = {
            table_info: {
                display_name: "",
                display_cols: "",
                update_recency: 0
            },
            isLoaded: false,
            tableScroll: {
                x: null,
                y: null
            },
            sticking: {
                top: false,
                left: false
            },
            column_visibility: {
                col_FACILITY: false,
                col_TELEHEALTH: false,
                col_PHONE: false,
                col_ADDRESS: false,
                col_ZIPCODE: false,
                col_WALKINHOURS: false,
                col_MATINFO: false,
                col_WHICHMAT: false,
                col_BUPRENORPHINE: false,
                col_NALTREXONE: false,
                col_METHADONE: false,
                col_PAYMENTOPTIONS: false,
                col_SERVICES: false,
                col_ADDITIONALINFORMATION: false,
                col_ADDITIONALNOTES: false,
                col_CERTIFICATIONDATE: false,
                col_DATASOURCES: false
            },
            current_request_elements: {
                keyword: "",
                included_values_string: "None",
                excluded_values_strings: "None"
            },
            isLoading: false
        }
        this.render = this.render.bind(this)
        this.toLegalURL = this.toLegalURL.bind(this)
        this.enableColumns = this.enableColumns.bind(this)
        this.handleScroll = this.handleScroll.bind(this)
        this.makeRequest = this.makeRequest.bind(this)
        this.applyFilters = this.applyFilters.bind(this)
    }

    componentDidMount(){
        this.props.history.listen((location) => {
            console.log(this.state.table_info.table_name)
            console.log(location)
            this.makeRequest(this.request_URL_from_params())
        })
        this.makeRequest(this.request_URL_from_params())
    }

    enableColumns(){
        var visible_columns = this.state.table_info.display_cols.replace(/\"|\[|\]|\s|\(|\)/g,"").split(";")
        var newVisibilities = {}
        Object.assign(this.state.column_visibility, newVisibilities)
        for(var name of visible_columns){
            newVisibilities["col_"+name] = true
        }
        this.setState({column_visibility: newVisibilities})
    }

    handleScroll(e){
        var sticking = {top: false, left: false}
        if(e.target.scrollLeft > 0){
            sticking.left = true
        }
        if(e.target.scrollTop > 0){
            sticking.top = true
        }
        if(this.state.sticking.left !== sticking.left || this.state.sticking.top !== sticking.top){
            this.setState({sticking: sticking})
        }
    }

    toLegalURL(url){
        if(url === null){
            return ""
        }
        var splitIllegal = url.split(":")
        if(splitIllegal[0] === "https" || splitIllegal[0] === "http"){
            return url
        }
        else {
            return "//" + url
        }
    }

    bu_options(site){
        var options = []
        if(site.bwn){
            options.push("With naloxone (ex. Suboxone)")
        }
        if(site.bwon){
            options.push("Without naloxone")
        }
        if(site.beri){
            options.push("Injectable extended-release (ex. Sublocade)")
        }
        if(site.bsdm){
            options.push("Sub-dermal implant (Probuphine)")
        }
        return options;
    }

    nu_options(site){
        var options = [];
        if(site.vtrl){
            options.push("Vivitrol (injectable)")
        }
        if(site.nxn){
            options.push("Oral naltrexone")
        }
        return options;
    }

    request_URL_from_params(){
        var { table_name, query, keyword } = this.props.match.params
        var included_values = []
        var excluded_values = []
        var keyword = ""
        if(query){
            for(var param of query.split("&")){
                if(param.split("=")[0]=="keyword"){
                    keyword = param.split("=")[1]
                }
                else if(param.includes("!=")){
                    excluded_values.push({key: param.split("!=")[0], value: param.split("!=")[1]})
                }
                else {
                    included_values.push({key: param.split("=")[0], value: param.split("=")[1]})
                }
            }
        }
        var included_values_strings = []
        var excluded_values_strings = []
        for(var pair of included_values){
            included_values_strings.push(pair.key + "=" + pair.value)
        }
        for(var pair of excluded_values){
            excluded_values_strings.push(pair.key + "=" + pair.value)
        }
        var django_query = `/headless/${table_name}/${included_values_strings.length > 0 ? included_values_strings.join("&") : "None"}/${excluded_values_strings.length > 0 ? excluded_values_strings.join("&") : "None"}${keyword.length > 0 ? "/"+keyword : ""}`
        return django_query
    }

    makeRequest(django_query){
        console.log("starting request")
        this.setState({isLoading: true})
        var keyword = (django_query.split("/").length > 5 ? django_query.split("/")[django_query.split("/").length - 1] : "")
        var excluded_values_strings = django_query.split("/")[django_query.split("/").length - 2]
        var included_values_strings = django_query.split("/")[django_query.split("/").length - 3]
        this.setState({current_request_elements: {keyword: keyword, included_values_string: included_values_strings, excluded_values_strings: excluded_values_strings}})
        axios.get(django_query).then(res => {
            const data = res.data
            this.setState({ objects: data.objects, table_info: data.table_info})
            document.title = this.state.table_info.display_name
            this.enableColumns()
            this.setState({isLoaded: true})
            console.log("request completed")
            this.setState({isLoading: false})
        })
    }

    applyFilters(groups, sortingInfo, keyword){
        var included_values = []
        var excluded_values = []
        for(var group of groups){
            for(var filter of group.ref.current.props.filters){
                if(filter.ref.current.getValue() != null){
                    for(var condition of filter.ref.current.getValue().split("&")){
                        if(condition.includes("!=")){
                            excluded_values.push(condition.replace("!=","="))
                        }
                        else {
                            included_values.push(condition)
                        }
                    }
                }
            }
        }
        var sortingElement = (sortingInfo.direction == "-" ? sortingInfo.keys.replace("=","=-") : sortingInfo.keys)
        var query_url = `/headless/${this.state.table_info.table_name}/${included_values.length > 0 ? included_values.join("&") : "None"}/${excluded_values.length > 0 ? excluded_values.join("&") : "None"}${keyword.length > 0 ? "/"+keyword : ""}${sortingInfo.keys.length > 0 ? "/?" + sortingElement : ""}`
        console.log(query_url)
        this.makeRequest(query_url)
    }

    render(){
        var a = new Date(this.state.table_info.update_recency * 1000)
        var update_recency = (a.getMonth() + 1) + "/" + (a.getDate() + 1) + "/" + a.getFullYear()

        if (this.state.isLoaded) {
            return(
                <div id="body">
                    <ProgressBar isLoading={this.state.isLoading}/>
                    <NavBar/>
                    <div id="flexContainer">
                        <FilterBar applyFilters={this.applyFilters} table_filters_raw={this.state.table_info.filters}/>
                        <div id="table" onScroll={this.handleScroll}>
                            <h5 id="resultDescription">
                                <span id="dataSource" className="bold">SOURCE: <a href={this.state.table_info.source_url} target="_blank">{this.state.table_info.display_name}</a></span><br/>
                                <span id="lastUpdatedNotice">Last synced with source data: <span className="bold">{update_recency}</span></span><br/>
                                <span className="bold">{this.state.objects.length}</span> of <span className="bold">{this.state.table_info.records_count}</span> records for <span className="bold">{this.state.table_info.facility_type}</span> {this.state.table_info.source_range}
                            </h5>
                            <div id="extraContainer">
                            <table>
                                <tbody>
                                <tr>
                                    <TableCell isHeader={true} className="facilityName col_FACILITY" visibility={this.state.column_visibility} sticking={this.state.sticking}>Facility</TableCell>
                                    <TableCell isHeader={true} className="col_TELEHEALTH" visibility={this.state.column_visibility} sticking={this.state.sticking}>Telehealth</TableCell>
                                    <TableCell isHeader={true} className="col_PHONE" visibility={this.state.column_visibility} sticking={this.state.sticking}>Phone</TableCell>
                                    <TableCell isHeader={true} className="col_ADDRESS" visibility={this.state.column_visibility} sticking={this.state.sticking}>Address</TableCell>
                                    <TableCell isHeader={true} className="col_ZIPCODE" visibility={this.state.column_visibility} sticking={this.state.sticking}>ZIP Code</TableCell>
                                    <TableCell isHeader={true} className="col_WALKINHOURS" visibility={this.state.column_visibility} sticking={this.state.sticking}>Walk-In Hours</TableCell>
                                    <TableCell isHeader={true} className="col_MATINFO" visibility={this.state.column_visibility} sticking={this.state.sticking}>MAT Info</TableCell>
                                    <TableCell isHeader={true} className="col_WHICHMAT" visibility={this.state.column_visibility} sticking={this.state.sticking}>Which MAT</TableCell>
                                    <TableCell isHeader={true} className="col_BUPRENORPHINE" visibility={this.state.column_visibility} sticking={this.state.sticking}>Buprenorphine</TableCell>
                                    <TableCell isHeader={true} className="col_NALTREXONE" visibility={this.state.column_visibility} sticking={this.state.sticking}>Naltrexone</TableCell>
                                    <TableCell isHeader={true} className="col_METHADONE" visibility={this.state.column_visibility} sticking={this.state.sticking}>Methadone</TableCell>
                                    <TableCell isHeader={true} className="col_PAYMENTOPTIONS" visibility={this.state.column_visibility} sticking={this.state.sticking}>Payment Options</TableCell>
                                    <TableCell isHeader={true} className="col_SERVICES" visibility={this.state.column_visibility} sticking={this.state.sticking}>Services</TableCell>
                                    <TableCell isHeader={true} className="col_ADDITIONALINFORMATION" visibility={this.state.column_visibility} sticking={this.state.sticking}>Additional Information</TableCell>
                                    <TableCell isHeader={true} className="col_ADDITIONALNOTES" visibility={this.state.column_visibility} sticking={this.state.sticking}>Additional Notes</TableCell>
                                    <TableCell isHeader={true} className="col_CERTIFICATIONDATE" visibility={this.state.column_visibility} sticking={this.state.sticking}>Certification Date</TableCell>
                                    <TableCell isHeader={true} className="col_DATASOURCES" visibility={this.state.column_visibility} sticking={this.state.sticking}>Data Source(s)</TableCell>
                                </tr>
                                { this.state.objects.map((site) =>
                                    <tr key={site.oid}>
                                        <TableCell visibility={this.state.column_visibility} className="facilityName wrap col_FACILITY" sticking={this.state.sticking}>
                                            <p className="cellText bold">{site.name1}</p>
                                            <p className="cellText semibold">{site.name2}</p>
                                            <p className="cellText semibold">{site.name3}</p>
                                            <p className="cellText"><a target="_blank" href={this.toLegalURL(site.website1)}>{site.website1}</a></p>
                                            <p className="cellText"><a target="_blank" href={this.toLegalURL(site.website2)}>{site.website2}</a></p>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_TELEHEALTH">
                                            <p className="cellText">
                                                {site.telehealth ? "Yes" : "No"}
                                            </p>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_PHONE">
                                            <p className="cellText bold">
                                                {site.phone1}
                                            </p>
                                            <p className="cellText semibold">
                                                {site.phone2}
                                            </p>
                                            <p className="cellText semibold">
                                                {site.phone3}
                                            </p>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_ADDRESS">
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
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="col_ZIPCODE">
                                            <p className="cellText bold">{site.zipcode}</p>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="col_WALKINHOURS">
                                            <p className="cellText bold">{site.walk_in_hours}</p>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="col_MATINFO">
                                            <p className="cellText bold">{site.mat_info}</p>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_WHICHMAT">
                                            <p className="cellText">
                                                {site.mat_avail === "Unclear" && <span>"None confirmed"<br/></span>}
                                                Buprenorphine: <b>{ site.bu ? "Yes" : "No" }</b><br/>
                                                Naltrexone/Vivitrol: <b>{ site.nu ? "Yes" : "No"  }</b><br/>
                                                Methadone: <b>{site.mu ? "Yes" : "No"  }</b>
                                            </p>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_BUPRENORPHINE">
                                            { site.bu ? 
                                            <span>
                                                <p className="cellText">
                                                    Prescribed: <br/>
                                                    <span className="bold">
                                                        {this.bu_options(site).map((option)=><span className="block" key={option}>{option + ";"}</span>)}
                                                    </span>
                                                </p>
                                                <p>
                                                    <span>
                                                        {site.buu !== null &&
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
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_NALTREXONE">
                                            {site.nu ?
                                                <p className="cellText">
                                                    {(site.vtrl || site.nxn) && 
                                                        <span>
                                                            Prescribed:
                                                            <span className="bold">{this.nu_options(site).map((option)=><span className="block" key={option}>{option + ";"}</span>)}</span>
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
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_METHADONE"> 
                                            {site.mu ?
                                                <p className="cellText">
                                                    {site.meth !== null &&
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
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_PAYMENTOPTIONS">
                                            Medicaid: <b>{(site.md === true || site.md === "Yes") && "Yes"}{(site.md === false || site.md === "No") && "No"}{(site.md === "Unclear") && "Unclear"}</b><br/>
                                            Medicare: <b>{(site.mc === true || site.mc === "Yes") && "Yes"}{(site.mc === false || site.mc === "No") && "No"}{(site.mc === "Unclear") && "Unclear"}</b><br/>
                                            Payment assistance available: <b>{(site.pa === true || site.pa === "Yes") && "Yes"}{(site.pa === false || site.pa === "No") && "No"}{(site.pa === "Unclear") && "Unclear"}</b>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_SERVICES">
                                        Child care: <b>{(site.ccc === true || site.ccc === "Yes") && "Yes"}{(site.ccc === false || site.ccc === "No") && "No"}{(site.ccc === "Unclear") && "Unclear"}</b><br/>
                                        Domestic violence services: <b>{(site.dvh === true || site.dvh === "Yes") && "Yes"}{(site.dvh === false || site.dvh === "No") && "No"}{(site.dvh === "Unclear") && "Unclear"}</b><br/>
                                        Housing services: <b>{(site.hs === true || site.hs === "Yes") && "Yes"}{(site.hs === false || site.hs === "No") && "No"}{(site.hs === "Unclear") && "Unclear"}</b><br/>
                                        Mental health services: <b>{(site.mhs === true || site.mhs === "Yes") && "Yes"}{(site.mhs === false || site.mhs === "No") && "No"}{(site.mhs === "Unclear") && "Unclear"}</b><br/>
                                        Pregnancy care: <b>{(site.pw === true || site.pw === "Yes") && "Yes"}{(site.pw === false || site.pw === "No") && "No"}{(site.pw === "Unclear") && "Unclear"}</b><br/>
                                        Transportation assistance: <b>{(site.ta === true || site.ta === "Yes") && "Yes"}{(site.ta === false || site.ta === "No") && "No"}{(site.ta === "Unclear") && "Unclear"}</b>
                                        </TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="col_ADDITIONALINFORMATION">{ site.additional_info }</TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="col_ADDITIONALNOTES">{ site.ref_notes }</TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="col_CERTIFICATIONDATE">{ site.full_certification }</TableCell>
                                        <TableCell visibility={this.state.column_visibility} className="nowrap col_DATASOURCES">
                                            {site.id_dbhids_tad && <span><a href="/table/siterecs_dbhids_tad">DBHIDS MAT Directory</a><br/></span>}
                                            {site.ba_dbhids_tad && <span>Bed Availability Updates<br/></span>}
                                            {site.id_samhsa_ftloc && <span><a href="/table/siterecs_samhsa_ftloc">SAMHSA Find Treatment</a><br/></span>}
                                            {site.id_samhsa_otp && <span><a href="/table/siterecs_samhsa_otp">SAMHSA OTPs Directory</a><br/></span>}
                                            {site.id_hfp_fqhc && <span>HRSA or HFP (FQHCs)</span>}
                                        </TableCell>
                                    </tr>
                                ) }
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            )
        } else{
            return null
        }
    }
}

export default withRouter(TablePage)
