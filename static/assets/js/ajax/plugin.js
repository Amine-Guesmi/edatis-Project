
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

  var chargeChart = function(){
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
      url:"/dashbord/analyse/test",
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
          alert(obj.chartType);
        }else{
            dataSet = [data.desktop, data.tablet, data.mobile];
        }
        loadChart(dataSet, Attributes.color, Attributes.label, obj.device+"_chart", obj.device+" "+obj.type+" Per Contact ("+obj.mode+")");
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

  $("#btn-Desktop").click(chargeChart);
  $("#btn-tablet").click(chargeChart);
  $("#btn-mobile").click(chargeChart);
  $("#btn-devices").click(chargeChart);
  // Create
  $(".show-form").click(ShowForm);
  $("#modal-user").on("submit", ".create-form", SaveForm);
  // Update
  $("#users-table").on("click", ".show-form-update", ShowForm);
  $("#modal-user").on("submit", ".update-form", SaveForm);
  // delete
  $("#users-table").on("click", ".show-form-delete", ShowForm);
  $("#modal-user").on("submit", ".delete-form", SaveForm);
  //activate
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
