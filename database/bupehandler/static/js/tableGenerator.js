var screenWidth = $( window ).width()

// if(screenWidth < 900){
//   console.log("displaying mobile table")
//   $("table#main-table").style("display", "none");
//   $("table#mobile-table").style("display", "none");
//   $(document).ready( function () {
//       $('#table table#mobile-table').DataTable({
//           paging: false,
//           scrollX: true,
//           scrollCollapse: true,
//           fixedColumns: {
//             leftColumns: 1
//           },
//           responsive: true
//       })
//   })
// }
// else {
  $(document).ready( function () {
      $('#table table#main-table').DataTable({
          paging: false,
          // scrollX: true,
          scrollCollapse: true,
          fixedColumns: {
            leftColumns: 1
          },
          responsive: true
      })
  })
// }
