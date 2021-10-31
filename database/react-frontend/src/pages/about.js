import React, { Component } from "react"
import {withRouter} from 'react-router-dom'

import NavBar from "../components/NavBar.js"

import "../styles/about.css"
import logo from "../images/MM_infinity-logo_philly-blues.png"
import skyline from "../images/PhillySkyline_ly_seeImageCreditsTXT.png"

class AboutPage extends Component {

    render(){
        return(
            <div id="body">
                <NavBar/>
                <div id="aboutbody">
                    <p align="center">
                        <img src={logo} height="25%"/>
                    </p>
                    <h1 id="matchmapper">MATchMapper</h1>
                    <p>The Philadelphia area is among the regions hit hardest by the opioid epidemic. Fortunately, Philly is also home
                        to hundreds of dedicated professionals skilled at treating opioid use disorder. However, information on these
                        providers is split across several search tools and is sometimes outdated or innaccurate. MATchMapper aims to
                        address these issues by providing a search tool that unifies existing data sources and corrects many errors. We
                        hope that this tool will be useful to many in the community including individuals seeking treatment, healthcare
                        providers making referrals, and public health officials seeking to understand treatment availability. Please do
                        not hesitate to <a href="mailto:matchmapper.philadelphia@gmail.com">contact us</a> with questions and
                        suggestions.</p>
                        <p align='center'><img src={skyline} width="85%"/></p>
                    <h2 id="data-sources">Data Sources</h2>
                    <p>MATchMapper builds on the excellent work of existing projects to produce an extensive, up-to-date database of
                        treatment resources. The original data sources can be found below:</p>
                    <h3 id="philadelphia-department-of-behavioral-health-and-intellectual-disability-services">Philadelphia Department
                        of Behavioral Health and Intellectual Disability Services</h3>
                    <p><a href="https://dbhids.org/mat">Medication Assisted Treatment Directory</a></p>
                    <p><a href="https://dbhids.org/wp-content/uploads/2021/07/TAD-7.28.2021.pdf">Bed Availability Reports</a></p>
                    <h3 id="substance-abuse-and-mental-health-services-administration">Substance Abuse and Mental Health Services
                        Administration</h3>
                    <p><a href="https://findtreatment.samhsa.gov">Behavioral Treatment Services Locator</a></p>
                    <p><a href="https://dpt2.samhsa.gov/treatment/directory.aspx">Opioid Treatment Program Directory</a></p>
                    <p><a
                            href="https://www.samhsa.gov/medication-assisted-treatment/practitioner-program-data/treatment-practitioner-locator?field_bup_state_value=45">Buprenorphine
                            Practitioner Locator</a></p>
                    <h3 id="health-federation-of-philadelphia">Health Federation of Philadelphia</h3>
                    <p><a href="https://healthfederation.org/Members">Community Health Center Directory</a></p>
                    <h3 id="health-resources-and-services-administration">Health Resources and Services Administration</h3>
                    <p><a href="https://findahealthcenter.hrsa.gov">Federally Qualified Health Center Finder</a></p>
                    <h3 id="pennsylvania-department-of-drug-and-alcohol-problems">Pennsylvania Department of Drug and Alcohol Problems
                    </h3>
                    <p><a href="https://apps.ddap.pa.gov/gethelpnow/SAISSearchDrop.aspx?county=Philadelphia">Get Help Tool</a></p>
                    <h2 id="the-team">The Team</h2>
                    <p><a href="https://codeforphilly.org/projects/matchmapper">MATchMapper</a> is a project of <a
                            href="https://codeforphilly.org">Code for Philly</a>, the local chapter of <a
                            href="https://www.codeforamerica.org">Code for America</a>, a nation-wide not-for-profit network of
                        volunteers who apply their technical skills to a variety of civic challenges. The project began in February 2020
                        as part of Code for Philly's Opioid Data Hackathon. Since then, our team has continued to improve the
                        MATchMapper tool, benefitting greatly from feedback from a variety of public health experts in Philadelphia.</p>
                    <p>A large roster of volunteers has made MATchMapper possible. Our team includes a mix of students and experienced
                        professionals with skills in areas including web development, data science, product management and research.</p>
                    <h3 id="current-contributors">Current Contributors</h3>
                    <ul>
                        <li>Bill Coll</li>
                        <li>Brandon Cohen</li>
                        <li>Caroline Smith</li>
                        <li>Chip Clofine</li>
                        <li>David Bowden</li>
                        <li>Isaac Wasserman</li>
                        <li>Josephine Dru</li>
                        <li>Lyvia Yan</li>
                        <li>Maisie Smith</li>
                        <li>Sam Tan</li>
                        <li>Tung Do</li>
                    </ul>
                    <h3 id="past-contributors">Past Contributors</h3>
                    <ul>
                        <li>Becca Nock</li>
                        <li>Ben Campos</li>
                        <li>Dave Slinger</li>
                        <li>Holly Giang</li>
                        <li>Joey Logan</li>
                        <li>Luke Shi</li>
                        <li>Yuxin Chen</li>
                    </ul>
                </div>
            </div>
        )
    }
}

export default withRouter(AboutPage)