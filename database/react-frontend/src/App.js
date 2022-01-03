import React from "react"
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom"

import TablePage from "./pages/table.js"
import MapPage from "./pages/map.js"
import AboutPage from "./pages/about.js"

function App() {
  return (
    <div>
      <div id="resources">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-touch-icon.png"/>
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png"/>
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png"/>
        <link rel="manifest" href="/static/site.webmanifest"/>
        <link rel="mask-icon" href="/static/safari-pinned-tab.svg" color="#0f4d90"/>
        <link rel="shortcut icon" href="/static/favicon.ico"/>
        <meta name="msapplication-TileColor" content="#2b5797"/>
        <meta name="msapplication-config" content="/static/browserconfig.xml"/>
        <meta name="theme-color" content="#ffffff"/>
      </div>
      <Router>
      <Switch>
        <Route path="/table/:table_name/:query?">
          <TablePage/>
        </Route>
        <Route path="/map/:table_name/:query?">
          <MapPage/>
        </Route>
        <Route exact path="/">
          <AboutPage/>
        </Route>
      </Switch>
      </Router>
    </div>
  );
}

export default App;
