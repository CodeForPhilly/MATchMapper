function handleScroll(scrollY, scrollX){
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

// var leftStuck = false;
// var topStuck = false;
//
// const headers = document.querySelectorAll("th")
// const header1 = headers[1]
// const headerStuckObserver = new IntersectionObserver(
//   function([e]){
//     if (e.intersectionRatio == 1) {
//       topStuck = false;
//     }
//     else {
//       topStuck = true;
//     }
//     updateHeaders()
//   },
//   { threshold: [1] }
// );
//
// headerStuckObserver.observe(header1);
//
// const names = document.querySelectorAll(".facilityName")
// const name1 = names[1]
// const namesStuckObserver = new IntersectionObserver(
//   function([e]){
//     if (e.intersectionRatio == 1) {
//       leftStuck = false;
//     }
//     else {
//       leftStuck = true;
//     }
//     updateHeaders()
//   },
//   { threshold: [1] }
// );
//
// var updateHeaders = function(){
//   sticky = [...new Set([...names,...headers])]
//   // if(topStuck){
//   //   for(var cell of headers){
//   //     cell.classList.add("is-pinned")
//   //   }
//   // }
//   // else {
//   //   for(var cell of headers){
//   //     cell.classList.add("is-pinned")
//   //   }
//   // }
//   if(topStuck || leftStuck){
//     for(var cell of sticky){
//       cell.classList.add("is-pinned")
//     }
//   }
//   else {
//     for(var cell of sticky){
//       cell.classList.remove("is-pinned")
//     }
//   }
// }
//
// namesStuckObserver.observe(name1);
