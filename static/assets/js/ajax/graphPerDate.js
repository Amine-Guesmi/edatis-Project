$(document).ready(function(){
  // load when page is ready
  obj = {"bdname" : bd, "etat" : "0", "withCompanes" : "0"};
  $.ajax({
    url : "/dashbord/analyse/globalStats/dateStats",
    type : 'post',
    data : obj,
    dataType : 'json',
    success: function(data){
      analysePerDateChart.destroy();
      // ***
      analysePerDateChart = loadAnalysePerTimeChart(data["dates"],data["clic"], data["open"], data["recieved"], "statsperDate");

      //** ***
      $("#loading-date-date").css("visibility", "hidden");

    }
  });

  // all action with listener

  var loadTimelineCharteOfCompanes = function () {
    if ($("#statsWithCompanesName").prop("checked")){
      if ($("#allCompanes :selected").length > 0){
        var comp = "";
        allCompanes = $("#allCompanes").val();
        for (var id in allCompanes ){
            comp += allCompanes[id]+","
        }
        msg = "";
        if($("#typeAnalyse").val() == "all"){
            obj = {"bdname" : bd, "etat" : "0", "action" : $("#typeAnalyse").val(), "companes" : comp.substring(0, comp.length - 1), "withCompanes" : "1"};
            msg = "Stats Of "+$("#allCompanes :selected").length +" companes";
        }
        else if ($("#typeAnalyse").val() == "week" || $("#typeAnalyse").val() == "month" ||  $("#typeAnalyse").val() == "sixMonth" ){
            obj = {"bdname" : bd, "etat" : "1", "action" : $("#typeAnalyse").val(), "companes" : comp.substring(0, comp.length - 1), "withCompanes" : "1"};
            msg = "Stats Of "+$("#allCompanes :selected").length +" companes for last "+ $("#typeAnalyse").val() ;
        }

        $("#loading-date-date").css("visibility", "visible");
        $.ajax({
          url : "/dashbord/analyse/globalStats/dateStats",
          type : 'post',
          data : obj,
          dataType : 'json',
          success: function(data){
            analysePerDateChart.destroy();
            analysePerDateChart = loadAnalysePerTimeChart(data["dates"],data["clic"], data["open"], data["recieved"], "statsperDate", msg);
            $("#loading-date-date").css("visibility", "hidden");
            $.notify({
              icon: 'add_alert',
              title: '<strong>success</strong>',
              message: 'Chart Updated Succesfuly'
              },
            {
              type: 'success'
            });
          }
        });
      }else{
        $.notify({
          icon: 'add_alert',
          title: '<strong>error</strong>',
          message: 'You don\'t select Any Item in list Of companes '
          },
        {
          type: 'danger'
        });
      }
    }else{
      obj = {"bdname" : bd, "etat" : "1", "action" : $("#typeAnalyse").val(), "withCompanes" : "0"};
      msg = "Stats Of All Companes compane last "+$("#typeAnalyse").val();
      if ($("#typeAnalyse").val() == "all"){
          obj["etat"] = "0";
          msg = "Stats Of All Companes companes";
      }
      $("#loading-date-date").css("visibility", "visible");

      $.ajax({
        url : "/dashbord/analyse/globalStats/dateStats",
        type : 'post',
        data : obj,
        dataType : 'json',
        success: function(data){
          analysePerDateChart.destroy();
          analysePerDateChart = loadAnalysePerTimeChart(data["dates"],data["clic"], data["open"], data["recieved"], "statsperDate", msg);
          $("#loading-date-date").css("visibility", "hidden");
          $.notify({
            icon: 'add_alert',
            title: '<strong>success</strong>',
            message: 'Chart Updated Succesfuly'
            },
          {
            type: 'success'
          });
        }
      });
    }
  }




  $("#btn-analyseWithDate").click(loadTimelineCharteOfCompanes );

  //End Ready Fn
});
