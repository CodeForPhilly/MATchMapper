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