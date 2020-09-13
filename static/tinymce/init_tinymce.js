var django = django || {
    "jQuery": jQuery.noConflict(true)
};

var script = document.createElement('script');
script.setAttribute('src',"https://code.jquery.com/jquery-3.3.1.slim.min.js");
document.head.appendChild(script);


var tinymce_script = document.createElement('script');
tinymce_script.setAttribute('src','//cdn.tinymce.com/4/tinymce.min.js');
document.head.appendChild(tinymce_script);

tinymce.init({selector:'.tinymce',
      height : 400,
      max_height: 400,
      min_height: 400,
  
      plugins: ' preview paste importcss searchreplace autolink autosave save directionality  visualblocks visualchars fullscreen image link  codesample table charmap hr pagebreak nonbreaking  toc advlist lists wordcount imagetools  noneditable  charmap anchor',
    
      plugin_preview_width : "400", //This do the trick
      plugin_preview_height : "600",

  
      toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | backcolor alignleft aligncenter alignright alignjustify | superscript subscript  | Blocks | outdent indent |  numlist bullist | forecolor backcolor table hr  removeformat | charmap | fullscreen  preview  |  image  link  anchor codesample |',

      mobile : {
        'menubar' : true,
        'plugins' : ['autosave', 'lists', 'autolink'],
        'toolbar' : ['undo', 'redo', 'bold','italic','indent','styleselect','bullist','numlist','image','backcolor','fullscreen','media','table']
      },


    
      codesample_dialog_height: 500,
      fullscreen_settings : {
          width : "640",
          height : "480"
        },

      toolbar_sticky: true,
      menubar : false,

    
      statusbar: true,
  
      branding : false,
  
    });
