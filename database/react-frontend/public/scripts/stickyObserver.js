function handleScroll(){
  var scrollX = document.querySelector("#table").scrollX
  var scrollY = document.querySelector("#table").scrollY
  if(scrollY > 40){
    $("th").addClass("stuck")
    console.log("stuck headers")
  }
  else {
    $("th").removeClass("stuck")
    console.log("unstuck headers")
  }
  if(scrollX > 0){
    $(".facilityName:not(th)").addClass("stuck")
  }
  else {
    $(".facilityName:not(th)").removeClass("stuck")
  }
}

$("#table").onScroll(handleScroll)