
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
        charts[obj.device+"_chart"] = loadChart(dataSet, Attributes.color, Attributes.label, obj.device+"_chart", obj.device+" "+obj.type+" Per Contact ("+obj.mode+")", 'doughnut');
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
    now = new Date()
    obj = {}
    var month = ((now.getMonth().length+1) === 1)? (now.getMonth()+1) : '0' + (now.getMonth()+1);
    var day = ((now.getDate().length+1) === 1)? (now.getDate()) : '0' + (now.getDate());
    firstDate = '2015-05-05';
    secondDate = now.getFullYear()+'-'+month+'-'+day;
    if ($('#dateOption').prop("checked")){
        firstDate = $('#firstDate').val();
        secondDate = $('#secondDate').val();
    if (btn == 'btn-charge'){
      $(".loading").css("visibility", "visible");
      obj = {'mail_sending_id' : mail_sending_id ,'action' : 'charge-all-charts', 'bdname' : bdname, 'type_devices' : $('#type-open-clic-devices').val(), 'mode_sending_recieved' : $('#mode-sending-recienved').val(), 'mode_open_clic' : $('#mode-open-clic').val(), 'mode_open_clic_devices' : $('#mode-open-clic-devices').val(), 'firstDate' : firstDate , 'secondDate' : secondDate }
      if($('#mail_sending_id').val() != '')
        obj['mail_sending_id'] = $('#mail_sending_id').val();
      }
    }else if (btn == 'btn-sending-recieved'){


    }else if (btn == 'btn-open-clic'){
      alert('hello3');
    }else if (btn == 'btn-open-clic-devices'){
      $('#loading-devices-open-clic').css("visibility", "visible");
      obj = {'mail_sending_id' : mail_sending_id ,'action' : 'charge-open-clic-devices-chart', 'bdname' : bdname, 'type': $('#type-open-clic-devices').val() , 'mode' : $('#mode-open-clic-devices').val(), 'firstDate' : firstDate , 'secondDate' : secondDate }
    }

    $.ajax({
      url : '/dashbord/analyse/compagne',
      type : 'post',
      dataType : 'json',
      data : obj,
      success: function(data){
        $(".loading").css("visibility", "hidden");
        $('.btn-load').attr('disabled', false);
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
            chart_send_Recieved.destroy();
            chart_open_clic.destroy();
            chart_open_clic_devices.destroy();
            chart_send_Recieved = loadChart( data.data_sending_recieved, ["#4CAF50", "#E74C3C"], ["mail sending ", "Recieved"], "sending_abotie", "Number Mail sending and Recieved Per compagne", 'pie');
            chart_open_clic = loadChart( data.data_open_clic, ["#4CAF50", "#E74C3C"], ["Open ", "Clic"], "open_clic", "Open / Clic Per compagne", 'pie');
            chart_open_clic_devices = loadChart( data.data_devices_open_clic, ["#4CAF50", "#E74C3C", "#363636"], ["desktop", "tablet", "mobile"], "open_clic_devices", "Open / Clic for Each Devices Per compagne", 'pie');
            $('.mail_sending_id').html(obj.mail_sending_id);
            $('#mail_sending_id').val('');
            mail_sending_id = obj.mail_sending_id;
            $.notify({
              icon: 'add_alert',
              title: '<strong>Succefully</strong>',
              message: 'all graph is Updated Succesfuly '
              },
            {
              type: 'success'
            });
        }else if (data.error == '-1' && data.action == '1' ){
            chart_open_clic_devices.destroy();
            if (data.open){
              chart_open_clic_devices = loadChart( data.data_devices, ["#4CAF50", "#E74C3C", "#363636"], ["desktop", "tablet", "mobile"], "open_clic_devices", "Open / Clic for Each Devices Per compagne", 'pie');
            }else{
              chart_open_clic_devices = loadChart( data.data_devices, ["#4CAF50", "#E74C3C", "#363636"], ["desktop", "tablet", "mobile"], "open_clic_devices", "Open / Clic for Each Devices Per compagne", 'pie');
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
