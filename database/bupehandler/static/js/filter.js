
// Onclick
//  * If toggling on: add to string, refresh
//  * If toggling off: remove from string, remove predicated from string, refresh
// Onload
//  * Read filters from url and highight in sidebar including expanding predicated

function removeBlanks(a){
  for(var i = 0; i < a.length; i++){
    if(a[i] == ""){
      a.splice(i, 1)
    }
  }
  return a
}

var enabledFilters = []

async function expandSubfilters(){
  var subfilterSections = document.querySelectorAll(".subfilter")
  for(var section of subfilterSections){
    var predicate = section.getAttribute("predicate")
    if(enabledFilters.includes(predicate)){
      section.classList.add("visible")
    }
  }
}

async function highlightSelected(){
  var criteria = document.querySelectorAll(".filterCriteria")
  for(var criterion of criteria){
    var value = criterion.querySelector("input").value
    if(enabledFilters.includes(value)){
      criterion.classList.add("selected")
    }
  }
}

async function highlightSingle(filter){
  for(var criterion of document.querySelectorAll(".filterCriteria")){
    if(criterion.querySelector("input").value == filter){
      criterion.classList.add("selected")
    }
  }
}

async function unhighlightSingle(filter){
  for(var criterion of document.querySelectorAll(".filterCriteria")){
    if(criterion.querySelector("input").value == filter){
      criterion.classList.remove("selected")
    }
  }
}

async function toggleHighlight(el){
  if(enabledFilters.includes(el.querySelector("input").value)){
    unhighlightSingle(el)
  }
  else {
    highlightSingle(el)
  }
}

function readFilters(){
  var filterString = window.location.pathname.split("/")[3]
  filters = removeBlanks(filterString.split("&"))
  for(var filter of filters){
    enableFilter(filter.replace("%3D","="))
  }
  expandSubfilters()
  highlightSelected()
}
readFilters()

async function enableFilter(filter){
  highlightSingle(filter)
  enabledFilters.push(filter)
}

async function disableFilter(filter){
  unhighlightSingle(filter)
  for(var i = 0; i < enabledFilters.length; i++){
    if(enabledFilters[i] == filter){
      enabledFilters.splice(i, 1)
    }
  }
}

async function disablePredicatedFilters(filter){
  var subfilterSections = document.querySelectorAll(".subfilter")
  for(var section of subfilterSections){
    var predicate = section.getAttribute("predicate")
    if(predicate == filter){
      section.classList.remove("visible")
      for(var predicatedFilter of section.querySelectorAll(".filterCriteria")){
        disableFilter(predicatedFilter.querySelector("input").value)
      }
    }
  }
}

function toggleFilter(filter){
  if(enabledFilters.includes(filter)){
    disableFilter(filter)
    disablePredicatedFilters(filter)
  }
  else {
    enableFilter(filter)
    expandSubfilters()
  }
  setFilters()
}

function setFilters(){
  var splitPath = window.location.pathname.split("/")
  splitPath[3] = enabledFilters.join("&").replace("=", "%3D")
  splitPath = removeBlanks(splitPath)
  window.location.pathname = splitPath.join("/")
}

function removeBlanks(array){
  var filtered = array.filter(function (el) {
      return el != "";
  })
  return filtered
}

function clearFilters(){
  window.location.pathname = "/" + removeBlanks(window.location.pathname.split("/")).slice(0,2).join("/")
}

$(".filterCriteria").click(function(e){
  // toggleHighlight(e.currentTarget)
  console.log(e.currentTarget.querySelector("input").value)
  toggleFilter(e.currentTarget.querySelector("input").value)
});

$("#applyFilters").click(function(e){
  setFilters()
});

$("#clearFilters").click(function(e){
  clearFilters()
})

// var filterStringFull = ""
//
// function removePredicated(filter){
//   console.log(filter)
//   for(var subfilter of document.querySelectorAll(".subfilter")){
//     var predicate = subfilter.getAttribute("predicate")
//     if(predicate == filter.replace("%3D","=")){
//       for(var predicatedFilter of subfilter.querySelectorAll(".filterCriteria input")){
//         toggleFilter(predicatedFilter.value, true)
//       }
//     }
//   }
// }
//
// function toggleFilter(filter, noEnable){
//   // Convert addition to URL style
//   var filterStringAddition = filter.replace("=","%3D")
//
//   // Split current filterString into individual filters
//   var filterString = filterStringFull
//   var splitFilters = filterString.split("&")
//
//   // If already includes filter, disable filter and its predicated filters
//   if(splitFilters.includes(filterStringAddition)){
//     var itemIndex = splitFilters.indexOf(filterStringAddition)
//     splitFilters.splice(itemIndex, 1)
//
//       console.log("removing " + filterStringAddition)
//     removePredicated(filterStringAddition)
//   }
//   // Else, add it to the filterString
//   else if(!noEnable) {
//     splitFilters.push(filterStringAddition)
//   }
//   // Remove blank filters
//   for(var filter of splitFilters){
//     if(filter == ""){
//       var itemIndex = splitFilters.indexOf(filter)
//       splitFilters.splice(itemIndex, 1)
//     }
//   }
//   filterStringFull = splitFilters.join("&")
//   console.log(filterStringFull)
// }
//
// jQuery(".filterCriteria").click(function(e){
//   toggleFilter(e.currentTarget.querySelector("input").value)
//   var splitPath = window.location.pathname.split("/")
//   splitPath[3] = filterStringFull
//   for(var element of splitPath){
//     if(element == ""){
//       var itemIndex = splitPath.indexOf("")
//       splitPath.splice(itemIndex, 1)
//     }
//   }
//   window.location.pathname = splitPath.join("/")
// });
//
// function readFilters(){
//   var splitPath = window.location.pathname.split("/")
//   var filterString = splitPath[3]
//   filterStringFull = filterString
//   var splitFilters = filterString.split("&")
//   // For each filter in path
//   for(var filter of splitFilters){
//     // Show as selected in sidebar
//     for(var criteria of document.querySelectorAll(".filterCriteria")){
//       var value = criteria.querySelector("input").value
//       if(value == filter.replace("%3D","=")){
//         criteria.classList.add("selected")
//       }
//     }
//     // Enable predicated subfilters
//     for(var subfilter of document.querySelectorAll(".subfilter")){
//       var predicate = subfilter.getAttribute("predicate")
//       if(predicate == filter.replace("%3D","=")){
//         subfilter.classList.add("visible")
//       }
//     }
//   }
// }
//
// readFilters()
