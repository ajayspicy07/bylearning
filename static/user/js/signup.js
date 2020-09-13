$(document).ready(function(){
   	$("#username").change(function(){
   		var username = $(this).val();

   		$.ajax({
   			url: "/validate-username/",
   			data :{
   				'username':username
   			},
   			success : function(message){
   				$(" #validate-username").html(message);
                }
   		});
   	});
});