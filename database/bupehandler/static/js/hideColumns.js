function hideColumn(column_ID){
    let columns = document.querySelectorAll("th")
    var childNumber = 1
    for(var column of columns){
        if(column.textContent == column_ID){
            break
        }
        else{
            childNumber++
        }
    }

    let selector = `th:nth-child(${childNumber}), td:nth-child(${childNumber})`
    let rule = selector + "{ display: none; }"
    console.log(rule)
    var sheet = window.document.styleSheets[1]
    sheet.insertRule(rule, sheet.cssRules.length)
}

function removeBlanks(array){
    var filtered = array.filter(function (el) {
        return el != "";
    })
    return filtered
}

let tableID = removeBlanks(window.location.pathname.split("/"))[1]
console.log(tableID)

// if(tableID == "siterecs_dbhids_tad"){
//     hideColumn("Telehealth")
// }
// else if(tableID == "siterecs_hfp_fqhc"){
//     hideColumn("Telehealth")
// }
// else if(tableID == "siterecs_samhsa_otp"){
//     hideColumn("Telehealth")
// }

function autoHideEmpty(){
    let columns = document.querySelectorAll("th")
    let rows = Array.from(document.querySelectorAll("tr")).slice(1)
    var childNumber = 1
    for(var column of columns){
        console.log("Reviewing column: " + column.textContent)
        colEmpty = true
        for(var row of rows){
            const hasChar = new RegExp('[a-zA-Z]');
            if(hasChar.test(row.querySelectorAll("td, th")[childNumber - 1].textContent)){
                console.log("Found text in column: " + row.querySelectorAll("td, th")[childNumber - 1].textContent)
                colEmpty = false
                break
            }
        }
        if(colEmpty){
            let selector = `th:nth-child(${childNumber}), td:nth-child(${childNumber})`
            let rule = selector + "{ display: none; }"
            console.log(rule)
            var sheet = window.document.styleSheets[1]
            sheet.insertRule(rule, sheet.cssRules.length)
        }
        childNumber++
    }
}
autoHideEmpty()