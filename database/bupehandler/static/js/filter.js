/*
Onclick/search
  If search
    searchTerm = input.value
  If filter
    Toggle locally
      If negative
        If enabling
          Highlight filter
          Strip "!" from value
          Add to list of enabledNotFilters
        If disabling
          Unhighlight the filter
          Toggle predicated filters
            Strip "!" from value
            Remove from enabledNotFilters
      If positive
        If enabling
          Highlight filter
          Add to list of enabledIsFilters
        If disabling
          Unhighlight the filter
          Toggle predicated filters
            Remove from enabledIsFilters

  Change url
    basePathElements = removeBlanks(window.location.pathname.split("/")).splice(0,2)
    isFilterString = enabledIsFilters.join("&")
    notFilterString = enabledNotFilters.join("&")
    if isFilterString == ""
      isFilterString = "None"
    if notFilterString == ""
      notFilterString = "None"
    filterPathElements = [isFilterString, notFilterString, searchTerm]
    fullPath = basePathElements.concat(filterPathElements)
    window.location.pathname = fullPath

Onload
  if window.location.pathname.split("/").length > 3
    filterPathElements = window.location.pathname.split("/").splice(3)
    enabledIsFilterString = filterPathElements[0]
    enabledIsFilters = [filter.replace("%3D","=") for filter in enabledIsFilterString.split("&")]
    highlightEnabledIsFilters()
    if window.location.pathname.split("/").length > 4
      enabledNotFilterString = filterPathElements[1]
      enabledNotFilters = [filter.replace("%3D","=") for filter in enabledNotFilterString.split("&")]
      highlightEnabledNotFilters()
      if window.location.pathname.split("/").length > 5
        searchTerm = filterPathElements[2]
        fillSearchBar()
*/

var enabledIsFilters = []
var enabledNotFilters = []
var searchTerm = "None"

function readFilters(){
  if(window.location.pathname.split("/").length > 3){
    var filterPathElements = window.location.pathname.split("/").splice(3)
    var enabledIsFilterString = filterPathElements[0]
    if(enabledIsFilterString != "None" && enabledIsFilterString != ""){
      for(filter of enabledIsFilterString.split("&")){
        enableFilter(filter.replace("%3D","="), false)
        revealPredicated(filter.replace("%3D","="), false)
      }
    }
    if(filterPathElements.length >= 2){
      var enabledNotFilterString = filterPathElements[1]
      if(enabledNotFilterString != "None" && enabledNotFilterString != ""){
        for(filter of enabledNotFilterString.split("&")){
          enableFilter(filter.replace("%3D","="), true)
          revealPredicated(filter.replace("%3D","="), true)
        }
      }
    }
    if(filterPathElements.length >= 3){
      searchTerm = filterPathElements[2]
      fillSearchBar()
    }
  }
}

function revealPredicated(absoluteValue, isNegative){
  var predicationString = absoluteValue
  if(isNegative){
    predicationString = predicationString.replace("=","!=")
  }
  for(var subfilterSection of document.querySelectorAll(".subfilter")){
    if(subfilterSection.getAttribute("predicate") == predicationString){
      subfilterSection.classList.add("visible")
    }
  }
}

function disablePredicated(absoluteValue, isNegative){
  var predicationString = absoluteValue
  if(isNegative){
    predicationString = predicationString.replace("=","!=")
  }
  for(var subfilterSection of document.querySelectorAll(".subfilter")){
    if(subfilterSection.getAttribute("predicate") == predicationString){
      for(var filterCriteria of subfilterSection.querySelectorAll(".filterCriteria")){
        if(filterCriteria.classList.contains("selected")){
          var filterValue = filterCriteria.querySelector("input").value
          var isNegative = (filterValue.split("=")[1].charAt(0) == "!")
          var absoluteValue = filterValue.replace("=!", "=")
          disableFilter(absoluteValue, isNegative)
        }
      }
    }
  }
}

function fillSearchBar(){
  document.querySelector("#searchBar").value = searchTerm
}

$(document).ready(function() {
  readFilters()
})

// $(".filterCriteria").click(function(e){
//   toggleFilter(e.currentTarget.querySelector("input").value)
// })

$(".equal").click(function(e){
  console.log("hello")
  toggleFilter(e.currentTarget.parentElement.querySelector("input").value)
})
$(".notequal").click(function(e){
  toggleFilter(e.currentTarget.parentElement.querySelector("input").value.replace("=","=!"))
})

$("#clearFilters").click(function(e){
  clearFilters()
})

$("#searchBar").on('keypress',function(e) {
  if(e.which == 13) {
      search(e.currentTarget.value)
  }
})

function toggleFilter(filterValue){
  var isNegative = (filterValue.split("=")[1].charAt(0) == "!")
  var absoluteValue = filterValue.replace("!","")
  if(isNegative){
    if(enabledNotFilters.includes(absoluteValue)){
      disableFilter(absoluteValue, isNegative)
    } else {
      enableFilter(absoluteValue, isNegative)
      if(enabledIsFilters.includes(absoluteValue)){
        disableFilter(absoluteValue, !(isNegative))
      }
    }
  } else {
    if(enabledIsFilters.includes(absoluteValue)){
      disableFilter(absoluteValue, isNegative)
    } else {
      enableFilter(absoluteValue, isNegative)
      if(enabledNotFilters.includes(absoluteValue)){
        disableFilter(absoluteValue, !(isNegative))
      }
    }
  }
  applyFilters()
}

function enableFilter(absoluteValue, isNegative){
  highlight(absoluteValue, isNegative)
  if(isNegative){
    enabledNotFilters.push(absoluteValue)
  } else {
    enabledIsFilters.push(absoluteValue)
  }
}

function disableFilter(absoluteValue, isNegative){
  unhighlight(absoluteValue, isNegative)
  disablePredicated(absoluteValue, isNegative)
  if(isNegative){
    enabledNotFilters = excludeFromArray(enabledNotFilters, absoluteValue)
  } else {
    enabledIsFilters = excludeFromArray(enabledIsFilters, absoluteValue)
  }
}

function getElementByFilter(absoluteValue, isNegative){
  for(var el of document.querySelectorAll(".filterCriteria")){
    if(el.querySelector("input").value == absoluteValue){
      if(isNegative){
        return el.querySelector(".notequal")
      } else {
        return el.querySelector(".equal")
      }
    }
  }
  return null
}

function highlight(absoluteValue, isNegative){
  var el = getElementByFilter(absoluteValue, isNegative)
  el.classList.add("selected")
}

function unhighlight(absoluteValue, isNegative){
  var el = getElementByFilter(absoluteValue, isNegative)
  el.classList.remove("selected")
}

function unhighlightAll(){
  for(var el of document.querySelectorAll(".filterCriteria")){
    el.classList.remove("selected")
  }
}

function excludeFromArray(arr, val){
  return arr.filter(function(value, index, arr){ 
    return value != val;
  })
}

function search(term){
  if(term == ""){
    searchTerm = "None"
  } else{
    searchTerm = term
  }
  applyFilters()
}

function applyFilters(){
  var basePathElements = removeBlanks(window.location.pathname.split("/")).splice(0,2)
  var isFilterString = enabledIsFilters.join("&")
  var notFilterString = enabledNotFilters.join("&")
  if(isFilterString == ""){
    isFilterString = "None"
  }
  if(notFilterString == ""){
    notFilterString = "None"
  }
  var filterPathElements = [isFilterString, notFilterString, searchTerm]
  var fullPathElements = basePathElements.concat(filterPathElements)
  while(fullPathElements[fullPathElements.length - 1] == "None"){
    fullPathElements.pop()
  }
  console.log(searchTerm)
  var fullPath = fullPathElements.join("/")
  window.location.pathname = fullPath
  console.log(fullPath)
}

function clearFilters(){
  enabledIsFilters = []
  enabledNotFilters = []
  searchTerm = "None"
  unhighlightAll()
  applyFilters()
}








// function removeBlanks(a){
//   for(var i = 0; i < a.length; i++){
//     if(a[i] == ""){
//       a.splice(i, 1)
//     }
//   }
//   return a
// }

// var enabledFilters = []

// async function expandSubfilters(){
//   var subfilterSections = document.querySelectorAll(".subfilter")
//   for(var section of subfilterSections){
//     var predicate = section.getAttribute("predicate")
//     if(enabledFilters.includes(predicate)){
//       section.classList.add("visible")
//     }
//   }
// }

// async function highlightSelected(){
//   var criteria = document.querySelectorAll(".filterCriteria")
//   for(var criterion of criteria){
//     var value = criterion.querySelector("input").value
//     if(enabledFilters.includes(value)){
//       criterion.classList.add("selected")
//     }
//   }
// }

// async function highlightSingle(filter){
//   for(var criterion of document.querySelectorAll(".filterCriteria")){
//     if(criterion.querySelector("input").value == filter){
//       criterion.classList.add("selected")
//     }
//   }
// }

// async function unhighlightSingle(filter){
//   for(var criterion of document.querySelectorAll(".filterCriteria")){
//     if(criterion.querySelector("input").value == filter){
//       criterion.classList.remove("selected")
//     }
//   }
// }

// async function toggleHighlight(el){
//   if(enabledFilters.includes(el.querySelector("input").value)){
//     unhighlightSingle(el)
//   }
//   else {
//     highlightSingle(el)
//   }
// }

// function readFilters(){
//   var urlString = window.location.pathname.split("/")
//   while(urlString.length < 6){
//     urlString.push("")
//   }
//   var normalfilterString = window.location.pathname.split("/")[3]
//   if(normalfilterString == "None"){
//     var normalFilters = []
//   }
//   else {
//     var normalFilters = removeBlanks(normalfilterString.split("&"))
//   }
//   var notfilterString = window.location.pathname.split("/")[4]
//   if(notfilterString == "None"){
//     var notFilters = []
//   }
//   else {
//     var notFilters = removeBlanks(notFilters.split("&"))
//   }
//   for(var filter of notFilters){
//     filter = filter.replace("=", "!=").replace("%3D","!=")
//   }
//   filters = normalFilters.concat(notFilters)
//   for(var filter of filters){
//     enableFilter(filter.replace("%3D","="))
//   }
//   expandSubfilters()
//   highlightSelected()
// }
// readFilters()
// console.log(enabledFilters)

// async function enableFilter(filter){
//   highlightSingle(filter)
//   enabledFilters.push(filter)
//   console.log(enabledFilters)
// }

// async function disableFilter(filter){
//   unhighlightSingle(filter)
//   console.log("disabling")
//   for(var i = 0; i < enabledFilters.length; i++){
//     if(enabledFilters[i] == filter){
//       enabledFilters.splice(i, 1)
//     }
//   }
// }

// async function disablePredicatedFilters(filter){
//   var subfilterSections = document.querySelectorAll(".subfilter")
//   for(var section of subfilterSections){
//     var predicate = section.getAttribute("predicate")
//     if(predicate == filter){
//       section.classList.remove("visible")
//       for(var predicatedFilter of section.querySelectorAll(".filterCriteria")){
//         disableFilter(predicatedFilter.querySelector("input").value)
//       }
//     }
//   }
// }

// function toggleFilter(filter){
//   if(enabledFilters.includes(filter)){
//     disableFilter(filter)
//     disablePredicatedFilters(filter)
//   }
//   else {
//     enableFilter(filter)
//     expandSubfilters()
//   }
//   setFilters()
// }

// function setFilters(){
//   normalFilters = []
//   notFilters = []
//   for(var filter of enabledFilters){
//     if(filter.split("=")[1].charAt(0) == "!"){
//       notFilters.push(filter)
//     }
//     else {
//       normalFilters.push(filter)
//     }
//   }
//   var splitPath = window.location.pathname.split("/")

//   while(splitPath.length < 6){
//     splitPath.push("")
//   }

//   if(normalFilters.length == 0){
//     splitPath[3] == "None"
//   }
//   else {
//     splitPath[3] = normalFilters.join("&").replace("=", "%3D")
//   }
//   if(notFilters.length == 0){
//     splitPath[4] == "None"
//   }
//   else {
//     splitPath[4] = notFilters.join("&").replace("=", "%3D")
//   }
//   splitPath = removeBlanks(splitPath)
//   window.location.pathname = splitPath.join("/")
// }

// function removeBlanks(array){
//   var filtered = array.filter(function (el) {
//       return el != "";
//   })
//   return filtered
// }

// function clearFilters(){
//   enabledFilters = []
//   setFilters()
// }

// $(".filterCriteria").click(function(e){
//   console.log(e.currentTarget.querySelector("input").value)
//   toggleFilter(e.currentTarget.querySelector("input").value)
// });

// $("#clearFilters").click(function(e){
//   clearFilters()
// })

// $(document).on('keypress',function(e) {
//   if(e.which == 13) {
//       alert('You pressed enter!');
//   }
// });

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
