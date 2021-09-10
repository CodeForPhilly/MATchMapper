import React from "react"
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom"

import TablePage from "./pages/table.js"

function App() {
  return (
    <div>
      <div id="resources">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/images/apple-touch-icon.png"/>
        <link rel="icon" type="image/png" sizes="32x32" href="/static/images/favicon-32x32.png"/>
        <link rel="icon" type="image/png" sizes="16x16" href="/static/images/favicon-16x16.png"/>
        <link rel="manifest" href="/static/images/site.webmanifest"/>
        <link rel="mask-icon" href="/static/images/safari-pinned-tab.svg" color="#0f4d90"/>
        <link rel="shortcut icon" href="/static/images/favicon.ico"/>
        <meta name="msapplication-TileColor" content="#2b5797"/>
        <meta name="msapplication-config" content="/static/images/browserconfig.xml"/>
        <meta name="theme-color" content="#ffffff"/>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossOrigin="anonymous"></script>
        <link rel="preconnect" href="https://fonts.gstatic.com"/>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
        <link rel="stylesheet" href="/styles/table.css"/>
        <link rel="stylesheet" href="/styles/filterBar.css"/>
        <link rel="stylesheet" href="/styles/navBar.css"/>
        <script src="/scripts/stickyObserver.js"></script>
        <script src="/scripts/filterSettings.js"></script>
      </div>
      <Router>
      <Switch>
        <Route path="/table/:table_name/:included_values?/:excluded_values?">
          <TablePage/>
        </Route>
        {/* <Route path="/map">
          <MapPage/>
        </Route> */}
      </Switch>
      </Router>
    </div>
  );
}

export default App;
