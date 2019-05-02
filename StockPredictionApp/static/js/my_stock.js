/*
$(document).ready(function(){
    $(".btn31").click(function(){
        $.get("/mytest",function(data,statu){

        });
    });

});

$(document).ready(function(){
   $(".btn1").click(function(){
      $.get("/mystring",function(data, status){
         alert("数据: " + data + "\n状态: " + status);
      });
   });

    $(".btn2").click(function(){
      $.get("/mydict",function(data, status){
         alert("name: " + data.name + " age:" + data.age);
      });
   });

    $(".btn3").click(function(){
      $.get("/mylist",function(data, status){
         alert("name: " + data[0]+ " age:" + data[1]);
      });
   });

    $(".btn4").click(function(){
      $.ajax({url:"/mystring", data:{"mydata": "test"},success:function(data){
         alert(data);
      }});
   });

       $(".btn6_2").click(function(){
      $.ajax({url:"/dataFromAjax", data:{"mydata": "test data"},success:function(data){
         alert(data);
      }});
   });

    $(".btn5").click(function(){
      $.ajax({url:"/mydict", success:function(data){
         alert("name: " + data.name + " age:" + data.age);
      }});
   });

    $(".btn6").click(function(){
      $.ajax({url:"/mylist", success:function(data){
         alert("name: " + data[0] + " age:" + data[1]);
      }});
   });

   $(".btn10").click(function(){
        $("p").load("/mystring");
   });

    $(".btn8").click(function(){
        $.getJSON("/mydict",function(data){
            $.each(data, function(i, field){
                $("div").append(field + " ");
            });
        });
    });

    $(".btn9").click(function(){
        $.post("/mydict", function(data, status){
         alert("name: " + data.name + " age:" + data.age);
    });
});
});
*/