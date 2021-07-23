var filterSettingsRows = table_info.filters.replace(/(?:\r\n|\r|\n)/g," ").split("|")
var filterSettingsLists = []
for(var row of filterSettingsRows){
    filterSettingsLists.push(row.split(";"))
}
legend = filterSettingsLists[0]
var filterSettings = []
for(var row of filterSettingsLists){
    if(row == legend){
        continue
    }
    else {
        var rowObj = {}
        for(var i=0;i<row.length;i++){
            rowObj[legend[i]] = row[i]
        }
        filterSettings.push(rowObj)
    }
}
var filtersByGroup = {}
for(var filter of filterSettings){
    if(filtersByGroup[filter.ui_group] == undefined){
        filtersByGroup[filter.ui_group] = [filter]
    }
    else {
        filtersByGroup[filter.ui_group].push(filter)
    }
}
sortedFilterGroups = Object.values(filtersByGroup).sort(function(a,b){
    var lowestInA = null
    var lowestInB = null
    for(var filter of a){
        if(filter.ui_seq < lowestInA || lowestInA == null){
            lowestInA = filter.ui_seq
        }
    }
    for(var filter of b){
        if(filter.ui_seq < lowestInB || lowestInB == null){
            lowestInB = filter.ui_seq
        }
    }
    return lowestInA - lowestInB
})
for(var filterGroup of sortedFilterGroups){
    filterGroup.sort((a,b) => {
        return a.ui_seq - b.ui_seq
    })
}

function getGroupLeader(group){
    var withLowestUISeq = null
    for(var filter of group){
        if(withLowestUISeq == null || parseInt(filter.ui_seq) < parseInt(withLowestUISeq.ui_seq)){
            withLowestUISeq = filter
        }
    }
    return withLowestUISeq
}

function getLeaderType(leader){
    if(leader.this_field == ""){
        return "header"
    }
    else {
        return "predicate"
    }
}

for(var i in sortedFilterGroups){
    var leader = getGroupLeader(sortedFilterGroups[i])
    leader.type = getLeaderType(leader)
    var others = []
    for(var filter of sortedFilterGroups[i]){
        if(filter != leader){
            others.push(filter)
        }
    }
    sortedFilterGroups[i] = {leader: leader, others: others}
}

function filterHeaderHTML(leader){
    var HeaderElement = document.createElement("DIV")
    HeaderElement.classList.add("filterGroupHeader")
    HeaderElement.innerHTML = leader.ui_label
    return HeaderElement
}

function filterPredicateHTML(leader){
    var HeaderElement = document.createElement("DIV")
    HeaderElement.classList.add("filterCriteria")
    HeaderElement.innerHTML = `
            <label>${leader.ui_label}</label>
            <div class="specifier equal"><p>&#10003;</p></div>
            <div class="specifier notequal"><p>&#10007;</p></div>
            <input type="checkbox" name="${leader.this_field}" value="${leader.this_field}=True"/>
            `
    return HeaderElement
}

function filterSectionHTML(filters, predicate){
    var sectionHTML = document.createElement("DIV")
    sectionHTML.classList.add("subfilter")
    if(predicate != null){
        sectionHTML.setAttribute("predicate", predicate + "=True")
    } else {
        sectionHTML.classList.add("visible")
    }
    for(var filter of filters){
        var criteriaElement = document.createElement("DIV")
        criteriaElement.classList.add("filterCriteria")
        criteriaElement.innerHTML = `
            <label>${filter.ui_label}</label>
            <div class="specifier equal"><p>&#10003;</p></div>
            <div class="specifier notequal"><p>&#10007;</p></div>
            <input type="checkbox" name="${filter.this_field}" value="${filter.this_field}=True"/>
            `
        sectionHTML.appendChild(criteriaElement)
    }
    return sectionHTML
}

function filterGroupHTML(group){
    var leaderHTML = null
    var sectionHTML = null
    if(group.leader.type == "header"){
        leaderHTML = filterHeaderHTML(group.leader)
        sectionHTML = filterSectionHTML(group.others, null)
    } else {
        leaderHTML = filterPredicateHTML(group.leader)
        sectionHTML = filterSectionHTML(group.others, group.leader.this_field)
    }
    var filterGroupHTML = document.createElement("DIV")
    filterGroupHTML.classList.add("filterGroup")
    filterGroupHTML.appendChild(leaderHTML)
    filterGroupHTML.appendChild(sectionHTML)
    return filterGroupHTML
}

$("#filterContainer").ready((e) => {
    for(var group of sortedFilterGroups){
        document.querySelector("#filterContainer").appendChild(filterGroupHTML(group))
    }
    setFilterEventListeners()
})

/*
For each filter group:
- Identify group leader
    - Will have lowest .ui_seq and/or this_field == "" and/or all others .iff_field == this_field
- Identify group leader type
    - If group leader .this_field == "" -> leader type = header
    - If group leader .this_field != "" && all others in group .iff_field == .this_field -> leader type = predicate
- filterGroup = {leader: ..., others: ...}
Generate html:
- For each filter group
    - If leader type == predicate
        - LeaderElement = document.createElement("DIV")
        - LeaderElement.classList.add("filterCriteria")
        - LeaderElement.innerHTML = `
            <label>${group.leader.ui_label}</label>
            <div class="specifier equal"><p>&#10003;</p></div>
            <div class="specifier notequal"><p>&#10007;</p></div>
            <input type="checkbox" name="${group.leader.this_field}" value="${group.leader.this_field}=True"/>
            `
        - PredicatedElement = document.createElement("DIV")
        - PredicatedElement.classList.add("subfilter")
        - PredicatedElement.setAttribute("predicate","${group.leader.this_field}=True")
        - for each filter in group.others
            - criteriaElement = document.createElement("DIV")
            - criteriaElement.classList.add("filterCriteria")
            - criteriaElement.innerHTML = `
            <label>${filter.ui_label}</label>
            <div class="specifier equal"><p>&#10003;</p></div>
            <div class="specifier notequal"><p>&#10007;</p></div>
            <input type="checkbox" name="${filter.this_field}" value="${filter.this_field}=True"/>
            `
            - PredicatedElement.appendChild(criteriaElement)
        - document.querySelector("#filterOptions").appendChild(LeaderElement)
        - document.querySelector("#filterOptions").appendChild(PredicatedElement)
    - Elif leader type == header
        - LeaderElement = document.createElement("DIV")
        - LeaderElement.classList.add("filterSectionHeader")
        - LeaderElement.innerHTML = group.leader.ui_label
        - FilterSection.setAttribute("sectionName",group.leader.ui_group)
        - FilterSection = document.createElement("DIV")
        - FilterSection.setAttribute("sectionName",group.leader.ui_group)
        - for each filter in group.others
            - criteriaElement = document.createElement("DIV")
            - criteriaElement.classList.add("filterCriteria")
            - criteriaElement.innerHTML = `
            <label>${filter.ui_label}</label>
            <div class="specifier equal"><p>&#10003;</p></div>
            <div class="specifier notequal"><p>&#10007;</p></div>
            <input type="checkbox" name="${filter.this_field}" value="${filter.this_field}=True"/>
            `
            - FilterSection.appendChild(criteriaElement)

*/