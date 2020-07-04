$(document).ready(function(){

  var recommandationAction= function(){
    ok = true;
    if ($("#compName").val().length === 0 ){
      ok = false;
      notif("Compane Name Is Empty !", "Error", "danger")
    }
    if ($("#compSent").val().length === 0 || $("#compSent").val()==0  ){
      ok = false;
      notif("Number Of Sent Is Empty !", "Error", "danger")
    }
    now = new Date();
    var month =(now.getMonth()+1);
    var day = now.getDate();
    if ($("#compDate").val().length === 0 ){
      ok = false;
      notif("Date of Sent is Empty Is Empty !", "Error", "danger")
    }else if ((new Date().getTime() + (30 * 24 * 60 * 60 * 1000)) > new Date($("#compDate").val()).getTime()){
      ok = false;
      notif("the difference between the date you choose and today's date greater than 30 days !", "warning", "warning")
    }
    if ($("#compHour").val().length === 0 ){
      ok = false;
      notif("Hour of sent is Empty Is Empty !", "Error", "danger")
    }
    if(ok){
      $("#titleCompPredict").html("");
      obj = {'compName' :$("#compName").val(),'compSent': $("#compSent").val() ,'date' : $("#compDate").val() , 'hour' : parseInt(($("#compHour").val().split(':'))[0]), 'databaseSave' : "0"};
      if($("#saveResultToogle").prop("checked"))
        obj["databaseSave"] = "1";
      $('#rasultRecommondation').modal('show');
      $("#loaderGif").show();
      $("#compAnalyseGlobal").hide();
      $.ajax({
        type: 'POST',
        url:"/dashbord/recommandation/predict",
        dataType : 'json',
        data : obj,
        success: function(data){
          setTimeout(function(){$("#loaderGif").hide(); $("#compAnalyseGlobal").show();$("#titleCompPredict").html("Predictive Analyse (<strong style='color : #154360  '>"+obj["compName"]+")</strong>");notif("Operation Succesfuly", "success", "success")}, 1000);
          chart_sent_recieved_inqueue.destroy();
          chart_clic_open.destroy();
          chart_sent_recieved_inqueue = loadChart(data.data_sent_recieved_inqueue, ["#52BE80", "#5DADE2", "#D98880"], ["sent", "recieved", "Inqueue"], "compGlobalStat","Sent Recieved Inqueue Predictive","horizontalBar", false);
      		chart_clic_open= loadChart(data.data_open_clic, ["#52BE80", "#154360", "#3498DB "], ["recieved", "open", "clic"], "compGlobalStatDevices","Sent Recieved Inqueue Predictive","bar", false);
          if (obj["databaseSave"] == "1"){
            $("#compNumber").text(data.nbComp);
            $("#compClics").text(data.clics);
            $("#compOpens").text(data.opens);
            $("#compRecieved").text(data.recieved);
            chart_sent_recieved_inqueue_global.destroy();
            chart_clic_open_global.destroy();
            analysePerDateChart.destroy();
            chart_sent_recieved_inqueue_global= loadChart([data.sent, data.recieved, data.in_queue], ["#52BE80", "#5499C7", "#D98880"], ["sent", "recieved", "Inqueue"], "open_clic_devices1","Sent Recieved Inqueue Predictive","horizontalBar", false);
            chart_clic_open_global = loadChart([data.recieved, data.opens, data.clics], ["#5499C7", "#138D75", "#8E44AD"], ["recieved", "opens", "clicks"], "open_clic_devices2","Sent Recieved Inqueue Predictive","bar", false);
            analysePerDateChart = loadAnalysePerTimeChart(data.labels,data.clicsLst, data.opensLst, data.recievedLst, "statPerDate", "Stats Of All Virtual Comapanes");
            $('.allCompListe').html(data.comp_list);
          }
          resetForm();
          allActionBtn();
        }
      });
    }

};
var compDetails = function(){
  var btn = $(this);
  $("#loaderGif").hide();
  $("#compAnalyseGlobal").show();
  $.ajax({
    url : btn.attr('data-url'),
    type : 'get',
    dataType : 'json',
    success: function(data){
      chart_sent_recieved_inqueue.destroy();
      chart_clic_open.destroy();
      chart_sent_recieved_inqueue = loadChart([data.sent, data.recieved, (data.sent - data.recieved)], ["#52BE80", "#5DADE2", "#D98880"], ["sent", "recieved", "Inqueue"], "compGlobalStat","Sent Recieved Inqueue Predictive","horizontalBar", false);
      chart_clic_open= loadChart([data.recieved, data.opens, data.clics], ["#52BE80", "#154360", "#3498DB "], ["recieved", "open", "clic"], "compGlobalStatDevices","Sent Recieved Inqueue Predictive","bar", false);
      $("#titleCompPredict").html("Predictive Analyse (<strong style='color : #154360  '>"+data.compName+")</strong>");
      $('#rasultRecommondation').modal('show');
      allActionBtn();
    }
  });
};

  var showModalDeleteComp = function(){
    var btn = $(this);
    $.ajax({
      url : btn.attr('data-url'),
      type : 'get',
      dataType : 'json',
      beforeSend: function(){
          $('.modal-delete_comp').modal('show');
      },
      success: function(data){
        $('.modal-delete_comp .modal-content').html(data.html_modal);
        $(".btn-dismiss-delete").click(function(){
            $('.modal-delete_comp').modal('hide');
        });
        allActionBtn();
      }
    });
  };

  var deleteComp = function(){
    var btn = $(this);
    $.ajax({
      url : btn.attr('data-url'),
      type : 'get',
      dataType : 'json',
      success: function(data){
        $("#compNumber").text(data.compNumber);
        $("#compClics").text(data.clics);
        $("#compOpens").text(data.opens);
        $("#compRecieved").text(data.recieved);
        chart_sent_recieved_inqueue_global.destroy();
        chart_clic_open_global.destroy();
        analysePerDateChart.destroy();
        chart_sent_recieved_inqueue_global= loadChart([data.sent, data.recieved, data.in_queue], ["#52BE80", "#5499C7", "#D98880"], ["sent", "recieved", "Inqueue"], "open_clic_devices1","Sent Recieved Inqueue Predictive","horizontalBar", false);
        chart_clic_open_global = loadChart([data.recieved, data.opens, data.clics], ["#5499C7", "#138D75", "#8E44AD"], ["recieved", "opens", "clicks"], "open_clic_devices2","Sent Recieved Inqueue Predictive","bar", false);
        analysePerDateChart = loadAnalysePerTimeChart(data.labels,data.clicsLst, data.opensLst, data.recievedLst, "statPerDate", "Stats Of All Virtual Comapanes");
        $('.allCompListe').html(data.comp_list);
        $('.modal-delete_comp').modal('hide');
        notif("Operation Succesfuly", "success", "success")
        allActionBtn();
      }
    });
  };

  function allActionBtn(){
    $('#btn-addComp').unbind('click');
    $('.btn-details').unbind('click');
    $('.btn-deleteComp').unbind('click');
    $('.modal-delete_comp').unbind('click');

    $("#btn-addComp").on("click", recommandationAction);
    //details of comp
    $(".btn-details").on('click',compDetails);
    //delete Actions
    $(".btn-deleteComp").on("click", showModalDeleteComp);
    $(".modal-delete_comp").on("click", ".compFinalDelete", deleteComp);
  }
  //add compane Simulation
  allActionBtn();
  //notify fn
  function notif(msg, header, clas){
    $.notify({
      icon: 'add_alert',
      title: '<strong>'+header+'</strong>',
      message: msg
      },
    {
      type: clas
    });
  }
  function resetForm(){
    $("#compName").val("");
    $("#compSent").val("");
    $("#compDate").val("");
    $("#compHoure").val("");
  }
  //Csrf Token
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });
});
