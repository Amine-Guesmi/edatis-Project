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
          }else{
              $('#modal-user .modal-content').html(data.html_form);
          }
        }
      });
      return false;
  };
  // Create
  $(".show-form").click(ShowForm);
  $("#modal-user").on("submit", ".create-form", SaveForm);
  // Update
  $("#users-table").on("click", ".show-form-update", ShowForm);
  $("#modal-user").on("submit", ".update-form", SaveForm);
  // delete
  $("#users-table").on("click", ".show-form-delete", ShowForm);
  $("#modal-user").on("submit", ".delete-form", SaveForm);
});
