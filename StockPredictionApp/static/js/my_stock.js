$(document).ready(function(){

  $.get("/stockInfo",data={'stockTicker':stock_name,'infoType':'high'},function(result){
    $("#t_high").text(result.toFixed(2));
  });

  $.get("/stockInfo",data={'stockTicker':stock_name,'infoType':'low'},function(result){
    $("#t_low").text(result.toFixed(2));
  });

  $.get("/stockInfo",data={'stockTicker':stock_name,'infoType':'average'},function(result){
    $("#t_average").text(result.toFixed(2));
  });

  $.get("/stockPrediction",data={'stockTicker':stock_name,'predType':'dnn','predPeriod':'longTerm'},function(result){
    console.log(result);
    $("#t_dnn_long").text(result.toFixed(2));
  });

  $.get("/stockPrediction",data={'stockTicker':stock_name,'predType':'svr','predPeriod':'longTerm'},function(result){
    console.log(result);
    $("#t_svr_long").text(result.toFixed(2));
  });

  $.get("/stockPrediction",data={'stockTicker':stock_name,'predType':'bayes','predPeriod':'longTerm'},function(result) {
    console.log(result);
    $("#t_bayesian_long").text(result.toFixed(2));
  });

  $.get("/stockPrediction",data={'stockTicker':stock_name,'predType':'dnn','predPeriod':'shortTerm'},function(result){
    console.log(result);
    $("#t_dnn_short").text(result.toFixed(2));
  });

  $.get("/stockPrediction",data={'stockTicker':stock_name,'predType':'svr','predPeriod':'shortTerm'},function(result){
    console.log(result);
    $("#t_svr_short").text(result.toFixed(2));
  });

  $.get("/stockPrediction",data={'stockTicker':stock_name,'predType':'bayes','predPeriod':'shortTerm'},function(result){
    console.log(result)
    $("#t_bayesian_short").text(result.toFixed(2));
  });

});
