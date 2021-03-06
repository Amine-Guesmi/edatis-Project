
$(document).ready(function(){
  var ShowForm = function(){
    var btn = $(this);
    $.ajax({
      url : btn.attr('data-url'),
      type : 'get',
      dataType : 'json',
      beforeSend: function(){
          $('#modal-user').modal('show');
      },
      success: function(data){
        $('#modal-user .modal-content').html(data.html_form);
      }
    });
  };
  var SaveForm = function(){
    var form = $(this);
      $.ajax({
        url : form.attr('data-url'),
        data : form.serialize(),
        type : form.attr('method'),
        dataType : 'json',
        success : function(data){
          if (data.form_is_valid){
              $('#users-table tbody').html(data.users_list);
              $('#modal-user').modal('hide');
              $.notify({
       					icon: 'add_alert',
       					title: '<strong>Succesfuly</strong>',
       					message: 'Operation done Succesfuly'
       					},
       				{
       					type: 'success'
       				});
          }else{
              $('#modal-user .modal-content').html(data.html_form);
              var errors = ""
              for(var key in data.err_msg){
                    errors += "<span><b>"+ key +"</b>"+data.err_msg[key][0]+"</span>";
              }
              $('#alert-errors').css("display", "block");
              $('#alert-errors .show-errors').html(errors);
          }
        }
      });
      return false;
  };

  var chargeChartContact = function(){
    btn = $(this).attr('id');
    $('.btn-load').attr('disabled', true);
    if (btn == 'btn-Desktop'){
      obj = {'mode' : $('#mode-Desktop').val(), 'type' : $('#type-Desktop').val(), 'mail_sending_id' : mail_sending_id , 'device':'desktop', 'bdname' : bdname, 'chartType' : '1'}
      Attributes = {'label': ["True", "False"] , 'color' : ["#4CAF50", "#E74C3C"]};
    }
    else if(btn == 'btn-tablet'){
      obj = {'mode' : $('#mode-tablet').val(), 'type' : $('#type-tablet').val(), 'mail_sending_id' : mail_sending_id, 'device':'tablet', 'bdname' : bdname, 'chartType' : '1'}
      Attributes = {'label': ["True", "False"] , 'color' : ["#1B4F72", "#E74C3C"]};
    }
    else if(btn == 'btn-mobile'){
      obj = {'mode' : $('#mode-mobile').val(), 'type' : $('#type-mobile').val(), 'mail_sending_id' : mail_sending_id, 'device':'mobile', 'bdname' : bdname, 'chartType' : '1'}
      Attributes = {'label': ["True", "False"] , 'color' : ["#76448A", "#E74C3C"]};
    }
    else{
      obj = {'mode' : $('#mode-devices').val(), 'type' : $('#type-devices').val(), 'mail_sending_id' : mail_sending_id, 'device': 'devices', 'bdname' : bdname, 'chartType' : '2'}
      Attributes = {'label': ["Desktop", "tablet", "phone"] , 'color' : ["#4CAF50", "#1B4F72", "#76448A"]};
    }
    $('#loading-'+obj.device).css("visibility", "visible");
    $.ajax({
      type: 'POST',
      url:"/dashbord/analyse/contact",
      dataType : 'json',
      data : obj,
      success: function (data) {
        $('#loading-'+obj.device).css("visibility", "hidden");
        $('.btn-load').attr('disabled', false);
        if(obj.chartType == '1'){
          if (obj.type == "open")
            dataSet = [data.nb, parseInt($('#allOpen').text())]
          else if (obj.type == "clic")
            dataSet = [data.nb, parseInt($('#allClic').text())]
        }else{
            dataSet = [data.desktop, data.tablet, data.mobile];
        }
        charts = {"desktop_chart" : chart1, "tablet_chart" : chart2, "mobile_chart" : chart3, "devices_chart" : chart4};
        charts[obj.device+"_chart"].destroy();
        charts[obj.device+"_chart"] = loadChart(dataSet, Attributes.color, Attributes.label, obj.device+"_chart", obj.device+" "+obj.type+" Per Contact ("+obj.mode+")", 'doughnut', true);
        $.notify({
          icon: 'add_alert',
          title: '<strong>Succesfuly</strong>',
          message: 'graph Update is Succesfuly'
          },
        {
          type: 'success'
        });
      }
    });
  }

  var chargeChartCompagne = function(){
    $('.btn-load').attr('disabled', true);
    btn = $(this).attr('id');
    now = new Date();
    obj = {};
    var month = ((now.getMonth().length+1) === 1)? (now.getMonth()+1) : '0' + (now.getMonth()+1);
    var day = now.getDate();
    firstDate = '2015-05-05';
    secondDate = now.getFullYear()+'-'+day+'-'+month;
    if ($('#dateOption').prop("checked")){
        firstDate = $('#firstDate').val();
        secondDate = $('#secondDate').val();
      }
      alert(bdname);
    if (btn == 'btn-charge'){
      $(".loading").css("visibility", "visible");
      obj = {'mail_sending_id' : mail_sending_id ,'action' : 'charge-all-charts', 'bdname' : bdname, 'type_devices' : $('#type-open-clic-devices').val(), 'mode_sending_recieved' : $('#mode-sending-recienved').val(), 'mode_open_clic' : $('#mode-open-clic').val(), 'mode_open_clic_devices' : $('#mode-open-clic-devices').val(), 'firstDate' : firstDate , 'secondDate' : secondDate }
      if($('#mail_sending_id').val() != '')
        obj['mail_sending_id'] = $('#mail_sending_id').val();
    }else if (btn == 'btn-sending-recieved'){
      $('#loading-sending-recieved-inqueue').css("visibility", "visible");
      obj = {'mail_sending_id' : mail_sending_id ,'action' : 'sending-recieved-inqueue', 'bdname' : bdname,  'mode' : $('#mode-sending-recienved').val(), 'firstDate' : firstDate , 'secondDate' : secondDate }
    }else if (btn == 'btn-open-clic'){
      $('#loading-open-clic').css("visibility", "visible");
      obj = {'mail_sending_id' : mail_sending_id ,'action' : 'open-clic', 'bdname' : bdname,  'mode' : $('#mode-open-clic').val(), 'firstDate' : firstDate , 'secondDate' : secondDate }
    }else if (btn == 'btn-open-clic-devices'){
      $('#loading-devices-open-clic').css("visibility", "visible");
      obj = {'mail_sending_id' : mail_sending_id ,'action' : 'charge-open-clic-devices-chart', 'bdname' : bdname,  'mode' : $('#mode-open-clic-devices').val(), 'firstDate' : firstDate , 'secondDate' : secondDate }
    }

    $.ajax({
      url : '/dashbord/analyse/compagne',
      type : 'post',
      dataType : 'json',
      data : obj,
      success: function(data){
        $(".loading").css("visibility", "hidden");
        $('.btn-load').attr('disabled', false);
        var   d = new Date();
        var dateAnalyse = d.getFullYear()+"/"+ (d.getMonth()+1)+"/"+d.getDate()+" "+d.getHours()+":"+d.getMinutes()+":"+d.getSeconds() ;
        if (data.error == '0'){
          $.notify({
            icon: 'add_alert',
            title: '<strong>Warning</strong>',
            message: 'first date or second date is Empty'
            },
          {
            type: 'danger'
          })
        }
        else if (data.error == '1'){
          $.notify({
            icon: 'add_alert',
            title: '<strong>Warning</strong>',
            message: 'first date larger than second date'
            },
          {
            type: 'danger'
          })
        }
        else if (data.error == '2') {
          $.notify({
            icon: 'add_alert',
            title: '<strong>Warning</strong>',
            message: 'this mail sending id doest not exist '
            },
          {
            type: 'danger'
          });
        }
        else if (data.error == '-1' && data.action == '0' ){
            recievedExist = false;
            table.clear();
            table.draw();
            chart_send_Recieved_inqueue.destroy();
            chart_open_clic.destroy();
            chart_open_clic_devices.destroy();
            chart_send_Recieved = loadChartMultiple( data.chart_sending, data.chart_recieved_inqueue, ["#2471A3 ", "#17A589", "#E10B0B"], ["sent ", "Recieved", 'Inqueue'], "sending_abotie", "Number Mail sending ,Recieved and Inqueue Per compagne", 'doughnut', true);
            chart_open_clic = loadChart( data.chart_open_clic,["#52BE80", "#154360", "#3498DB "], ["recieved", "Open ", "Clic"], "open_clic", "Open / Clic Per compagne", 'horizontalBar', false);
            chart_open_clic_devices = loadBarChart(["Desktop", "Tablet", "mobile"], "Open" , "Clic", data.chart_devices_open, data.chart_devices_clic, "open_clic_devices", "#3e95cd","#8e5ea2", "Stats For Ech Tyoe Of devices");

            if (obj["mode_sending_recieved"] == "Predictive"){
              var sendChart1 = (data.chart_recieved_inqueue[1]>=normaleCharte.chartRecieved[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var recievedChart1 = (data.chart_recieved_inqueue[2]>=normaleCharte.chartRecieved[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              if (recievedExist == false){
                  table.row.add([mail_sending_id, bdname, dateAnalyse ,normaleCharte.chartRecieved[1],"<span>"+data.chart_recieved_inqueue[1]+"</span>"+sendChart1 , "<span class='badge badge-success text-center'>Recieved</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                  recievedExist = true;
              }
              table.row.add([mail_sending_id, bdname, dateAnalyse,normaleCharte.chartRecieved[2],"<span>"+data.chart_recieved_inqueue[2]+"</span>"+recievedChart1 , "<span class='badge badge-danger text-center'>Inqueue</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
            }
            if (obj["mode_open_clic"] == "Predictive"){
              console.log(data.chart_open_clic);
              var recievedChart2  = (data.chart_open_clic[0] >= normaleCharte.chartOpenClic[0]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var openChart2      =  (data.chart_open_clic[1] >= normaleCharte.chartOpenClic[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var clicChart2      = (data.chart_open_clic[2] >= normaleCharte.chartOpenClic[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              if (recievedExist == false){
                  table.row.add([mail_sending_id, bdname, dateAnalyse,normaleCharte.chartOpenClic[0],"<span>"+data.chart_open_clic[0]+"</span>"+recievedChart2, "<span class='badge badge-success'>&nbsp;Recieved &nbsp;</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                  recievedExist = true;
              }
              table.row.add([mail_sending_id, bdname, dateAnalyse,normaleCharte.chartOpenClic[1],"<span>"+data.chart_open_clic[1]+"</span>"+openChart2 , "<span class='badge badge-primary'>open</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
              table.row.add([mail_sending_id, bdname, dateAnalyse,normaleCharte.chartOpenClic[2],"<span>"+data.chart_open_clic[2]+"</span>"+clicChart2 , "<span class='badge badge-info'>clic</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
            }
            if (obj["mode_open_clic_devices"] == "Predictive"){
              var openDesktopchart3  =  (data.chart_devices_open[0] >= normaleCharte.chartOpenDevices[0]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var openTableteChart3  =  (data.chart_devices_open[1] >= normaleCharte.chartOpenDevices[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var openMobileChart3   =  (data.chart_devices_open[2] >= normaleCharte.chartOpenDevices[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var clicDesktopChart3  =  (data.chart_devices_clic[0] >= normaleCharte.chartClicDevices[0]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var clicTabletChart3   =  (data.chart_devices_clic[1] >= normaleCharte.chartClicDevices[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              var clicMobileChart3   =  (data.chart_devices_clic[2] >= normaleCharte.chartClicDevices[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
              //open
              table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartOpenDevices[0],"<span>"+data.chart_devices_open[0]+"</span>"+openDesktopchart3 , "<span class='badge badge-success'>&nbsp;Open Desktop &nbsp;</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
              table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartOpenDevices[1],"<span>"+data.chart_devices_open[1]+"</span>"+openTableteChart3 , "<span class='badge badge-primary'>Open Tablet</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
              table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartOpenDevices[2],"<span>"+data.chart_devices_open[2]+"</span>"+openMobileChart3 , "<span class='badge badge-info'>Open Mobile</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
              // Clic
              table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartClicDevices[0],"<span>"+data.chart_devices_clic[0]+"</span>"+clicDesktopChart3 , "<span class='badge badge-success'>&nbsp;Clic Desktop &nbsp;</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
              table.row.add([mail_sending_id, bdname,dateAnalyse,normaleCharte.chartClicDevices[1],"<span>"+data.chart_devices_clic[1]+"</span>"+clicTabletChart3 , "<span class='badge badge-primary'>Clic Tablet</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
              table.row.add([mail_sending_id, bdname,dateAnalyse,normaleCharte.chartClicDevices[2],"<span>"+data.chart_devices_clic[2]+"</span>"+clicMobileChart3 , "<span class='badge badge-info'>Clic Mobile</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
            }
            table.draw();
            $('.mail_sending_id').html(obj.mail_sending_id);
            $('#mail_sending_id').val('');
              //normaleCharte = {"chartSend" : data.chart_sending , "chartRecieved" : data.chart_recieved_inqueue, "chartOpenClic" : data.chart_open_clic , "chartOpenDevices" : data.chart_devices_open , "chartClicDevices" : data.chart_devices_clic};
            mail_sending_id = obj.mail_sending_id;
            $.notify({
              icon: 'add_alert',
              title: '<strong>Succefully</strong>',
              message: 'all graph is Updated Succesfuly '
              },
            {
              type: 'success'
            });
        }else if (data.error == '-1' && data.action == '3' ){
            chart_open_clic_devices.destroy();
            chart_open_clic_devices = loadBarChart(["Desktop", "Tablet", "mobile"], "Open" , "Clic", data.chart_devices_open, data.chart_devices_clic, "open_clic_devices", "#3e95cd","#8e5ea2", "Stats For Ech Tyoe Of devices");
            if (obj["mode"] == "Predictive"){
                var openDesktopchart3  =  (data.chart_devices_open[0] >= normaleCharte.chartOpenDevices[0]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                var openTableteChart3  =  (data.chart_devices_open[1] >= normaleCharte.chartOpenDevices[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                var openMobileChart3   =  (data.chart_devices_open[2] >= normaleCharte.chartOpenDevices[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                var clicDesktopChart3  =  (data.chart_devices_clic[0] >= normaleCharte.chartClicDevices[0]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                var clicTabletChart3   =  (data.chart_devices_clic[1] >= normaleCharte.chartClicDevices[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                var clicMobileChart3   =  (data.chart_devices_clic[2] >= normaleCharte.chartClicDevices[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                // Open
                table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartOpenDevices[0],"<span>"+data.chart_devices_open[0]+"</span>"+openDesktopchart3 , "<span class='badge badge-success'>&nbsp;Open Desktop &nbsp;</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartOpenDevices[1],"<span>"+data.chart_devices_open[1]+"</span>"+openTableteChart3 , "<span class='badge badge-primary'>Open Tablet</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartOpenDevices[2],"<span>"+data.chart_devices_open[2]+"</span>"+openMobileChart3 , "<span class='badge badge-info'>Open Mobile</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                // Clic
                table.row.add([mail_sending_id, bdname,dateAnalyse ,normaleCharte.chartClicDevices[0],"<span>"+data.chart_devices_clic[0]+"</span>"+clicDesktopChart3 , "<span class='badge badge-success'>&nbsp;Clic Desktop &nbsp;</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                table.row.add([mail_sending_id, bdname,dateAnalyse,normaleCharte.chartClicDevices[1],"<span>"+data.chart_devices_clic[1]+"</span>"+clicTabletChart3 , "<span class='badge badge-primary'>Clic Tablet</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                table.row.add([mail_sending_id, bdname,dateAnalyse,normaleCharte.chartClicDevices[2],"<span>"+data.chart_devices_clic[2]+"</span>"+clicMobileChart3 , "<span class='badge badge-info'>Clic Mobile</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                table.draw();
            }
            $.notify({
              icon: 'add_alert',
              title: '<strong>Succefully</strong>',
              message: 'graph is Updated Succesfuly '
              },
            {
              type: 'success'
            });
        }else if (data.error == '-1' && data.action == '2' ){
            chart_open_clic.destroy();
            chart_open_clic = loadChart( data.chart_open_clic, ["#52BE80", "#154360", "#3498DB "], ["recieved", "Open ", "Clic"], "open_clic", "Open / Clic Per compagne", 'horizontalBar', false);
            $('#loading-open-clic').css("visibility", "hidden");
            if (obj["mode"] == "Predictive"){
                var recievedChart2  = (data.chart_open_clic[0] >= normaleCharte.chartOpenClic[0]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                var openChart2      =  (data.chart_open_clic[1] >= normaleCharte.chartOpenClic[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                var clicChart2      = (data.chart_open_clic[2] >= normaleCharte.chartOpenClic[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
                if (recievedExist == false){
                    table.row.add([mail_sending_id, bdname, dateAnalyse,normaleCharte.chartOpenClic[0],"<span>"+data.chart_open_clic[0]+"</span>"+recievedChart2 , "<span class='badge badge-success'>&nbsp;Recieved &nbsp;</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                    recievedExist = true;
                }
                table.row.add([mail_sending_id, bdname, dateAnalyse,normaleCharte.chartOpenClic[1],"<span>"+data.chart_open_clic[1]+"</span> "+openChart2 , "<span class='badge badge-primary'>open</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                table.row.add([mail_sending_id, bdname, dateAnalyse,normaleCharte.chartOpenClic[2],"<span>"+data.chart_open_clic[2]+"</span>"+clicChart2 , "<span class='badge badge-info'>clic</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                table.draw();
            }
            $.notify({
              icon: 'add_alert',
              title: '<strong>Succefully</strong>',
              message: 'graph is Updated Succesfuly '
              },
            {
              type: 'success'
            });
        }else if (data.error == '-1' && data.action == '1' ){
          chart_send_Recieved_inqueue.destroy();
          chart_send_Recieved = loadChartMultiple( data.chart_sending, data.chart_recieved_inqueue, ["#2471A3 ", "#17A589", "#E10B0B"], ["sent ", "Recieved", 'Inqueue'], "sending_abotie", "Number Mail sending ,Recieved and Inqueue Per compagne", 'doughnut', true);
          if (obj["mode"] == "Predictive"){
            var sendChart1 = (data.chart_recieved_inqueue[1]>=normaleCharte.chartRecieved[1]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
            var recievedChart1 = (data.chart_recieved_inqueue[2]>=normaleCharte.chartRecieved[2]) ? "<i  style='color : green; float :right' class='material-icons'>arrow_circle_up</i>":"<i  style='color : red; float :right' class='material-icons'>arrow_circle_down</i>";
            if (recievedExist == false){
                table.row.add([mail_sending_id, bdname, dateAnalyse ,normaleCharte.chartRecieved[1],"<span>"+data.chart_recieved_inqueue[1]+"</span>"+sendChart1 , "<span class='badge badge-success text-center'>Recieved</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
                recievedExist = true
            }
            table.row.add([ mail_sending_id, bdname, dateAnalyse,normaleCharte.chartRecieved[2],"<span>"+data.chart_recieved_inqueue[2]+"</span>"+recievedChart1 , "<span class='badge badge-danger text-center'>Inqueue</span>",  '<button class="btn " type="button" style="background : #EC7063">Delete<div class="ripple-container"></div></button>']);
            table.draw();
          }
          $.notify({
            icon: 'add_alert',
            title: '<strong>Succefully</strong>',
            message: 'graph is Updated Succesfuly '
            },
          {
            type: 'success'
          });
        }
      }
    });
  }

    var updateGlobalStat = function(){
      obj = {};
      btn = $(this).attr('id');
      $("#loading-card").css("visibility", "visible");
      $('#btn-charge-globalStat').attr('disabled', true);
      $('#btn-charge-allglobalStat').attr('disabled', true);
      if ( btn =="btn-charge-globalStat"){
        obj["target"] = "stat_hour";
        if ($('#dateOption').prop("checked")){
            obj["firstDate"] = $('#firstDate').val();
            obj["secondDate"] = $('#secondDate').val();
          }else{
            now = new Date()
            var month = now.getMonth()+1;
            var day = now.getDate();
            obj["firstDate"] = '2015-01-01';
            obj["secondDate"] = now.getFullYear()+'-'+month+'-'+day;
          }
      }else{
        obj["target"] = "global_stat";
      }

      obj["bdname"] = bd;
      $.ajax({
      url : "/dashbord/analyse/globalStat",
      type : 'post',
      data : obj,
      dataType : 'json',
      success: function(data){
        $('#btn-charge-globalStat').attr('disabled', false);
        $('#btn-charge-allglobalStat').attr('disabled', false);
        $("#loading-card").css("visibility", "hidden");
        if (data["error"] == "-1"){
          $("#allbdNames").val(bd);
          $.notify({
            icon: 'add_alert',
            title: '<strong>warning</strong>',
            message: 'This Client is Not Exist in DataLake '
            },
          {
            type: 'danger'
          });
        }else{
          recieved = data["recieved"] ;
          open =  data["open"] ;
          clic =  data["clic"] ;
          send =  data["send"] ;
          inqueue = send - recieved;
          $('#nbMailSend').text(send);
          changeStatsGlobale (open, recieved, clic, send);
          $.notify({
            icon: 'add_alert',
            title: '<strong>Succefully</strong>',
            message: 'graph is Updated Succesfuly '
            },
          {
            type: 'success'
          });
        }
      }
    });
  };

  var sendStatsMails = function(){
    mails = "";
    for (var i = 0; i < $(".tagsinput").val().split(',').length; i++){
      mails += $(".tagsinput").val().split(',')[i]+",";
    }
    console.log(JSON.stringify(all_analyse_result));
    $.ajax({
      url :"/dashbord/analyse/globalStats/sendMail" ,
      type : 'post',
      data : {"mails" : mails.substring(0, mails.length - 1), "rates" : JSON.stringify(all_analyse_result)},
      dataType : 'json',
      success: function(data){
        $.notify({
          icon: 'add_alert',
          title: '<strong>Succefully</strong>',
          message: 'mail Sending successfully '
          },
        {
          type: 'success'
        });
        $("#modal-sendMail").modal('hide');
      }
    });
  }


  //show modal Send mail
  $("#btn-send-report").click(function(){
    if (table.data().count() == 0 ) {
       $.notify({
         icon: 'add_alert',
         title: '<strong>warning</strong>',
         message: 'You don\'t  any data to send '
         },
       {
         type: 'warning'
       });
    }else{
        $("#modal-sendMail").modal('show');
    }
  });
  //Send mail
  $(".btn-sendMails").click(sendStatsMails);
  //Analyse globalStat
  $("#btn-charge-globalStat").click(updateGlobalStat);
  $("#btn-charge-allglobalStat").click(updateGlobalStat);
  //Analyse per compagne
  $("#btn-charge").click(chargeChartCompagne);
  $("#btn-sending-recieved").click(chargeChartCompagne);
  $("#btn-open-clic").click(chargeChartCompagne);
  $("#btn-open-clic-devices").click(chargeChartCompagne);
  //Analyse per contact
  $("#btn-Desktop").click(chargeChartContact);
  $("#btn-tablet").click(chargeChartContact);
  $("#btn-mobile").click(chargeChartContact);
  $("#btn-devices").click(chargeChartContact);
  // Create User
  $(".show-form").click(ShowForm);
  $("#modal-user").on("submit", ".create-form", SaveForm);
  // Update User
  $("#users-table").on("click", ".show-form-update", ShowForm);
  $("#modal-user").on("submit", ".update-form", SaveForm);
  // delete User
  $("#users-table").on("click", ".show-form-delete", ShowForm);
  $("#modal-user").on("submit", ".delete-form", SaveForm);
  //activate user
  $("#users-table").on("click", ".show-form-activate", ShowForm);
  $("#modal-user").on("submit", ".activate-form", SaveForm);


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
