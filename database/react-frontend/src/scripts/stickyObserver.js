function handleScroll(){
  var scrollX = document.querySelector("#table").scrollX
  var scrollY = document.querySelector("#table").scrollY
  console.log(scrollX,scrollY)
  if(scrollY > 40){
    document.querySelectorAll("th").classList.add("stuck")
    // $("th").addClass("stuck")
    console.log("stuck headers")
  }
  else {
    document.querySelectorAll("th").classList.remove("stuck")
    console.log("unstuck headers")
  }
  if(scrollX > 0){
    // $(".facilityName:not(th)").addClass("stuck")
    document.querySelectorAll(".facilityName:not(th)").classList.add("stuck")
  }
  else {
    // $(".facilityName:not(th)").removeClass("stuck")
    document.querySelectorAll(".facilityName:not(th)").classList.remove("stuck")
  }
}

document.querySelector("#table").addEventListener("scroll", handleScroll)