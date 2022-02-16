let rateMap= new Map();
function checkRates(value){
  
  let template=`
            <div class="input-group mb-3">
              <span class="input-group-text">Currennt : ₹${rateMap.get(value)}/sq.ft</span>
              <span class="input-group-text">New : ₹</span>
              <input type="number" class="form-control" placeholder="${rateMap.get(value)}" id="newRate">
              <button class="btn btn-outline-primary" type="button" onclick="updateRate()">Update</button>
            </div>
  `;
  $("#rateDetails").html(template);
}

function updateRate(){
  if($("#newRate").val()===''){
    displayMssage("#EFUalertMessage");
    return;
  }
  let value=$("#flatRates").find(":selected").text();
  let updateData={
    flat_number: value,
    rate: $("#newRate").val()
  };

  const client = new XMLHttpRequest();
  client.onload = function (){
    const data =JSON.parse(this.responseText);
      if (this.status == 200) {
          fetchRates();
          $("#flatRates").val(value).change();
          displayMssage("#EFUsuccessMessage");
      }
      else{
        console.log(data);
        displayMssage("#EFUerrorMessage");
      }
  }
  client.open("PATCH", "/emergencyFunds/updateRate",true);
  client.setRequestHeader("Content-type","application/json");
  client.send(JSON.stringify(updateData));
}

function fetchRates(defaultValue){

  const EFclient = new XMLHttpRequest();
  EFclient.onload = function (){
    const data =JSON.parse(this.responseText);
      if (this.status == 200) {
        $("#rateDetails").html("")
        let target=$('#flatRates').html("");
        data['data'].forEach(element => {
          rateMap.set(element.flat, element.rate);
          const template = `
          <option value="${element.flat}">${element.flat}</option>`;
          target.append(template);
        });
        if(defaultValue){
          $("#flatRates").val(defaultValue).change();
        }
        else{
          $("#flatRates").val(data['data'][0].flat).change();
        }
      }
      else{
        console.log(data);
      }
  }
  EFclient.open("GET", "/emergencyFunds/getFlatRates",true);
  EFclient.send();

}

function displayMssage(id){
  $(id).fadeTo(2000, 500).slideUp(1000, function() {
    $(id).hide();
  });
}

$(function(){
  $("#EFCsuccessMessage").hide();
  $("#EFCerrorMessage").hide();
  $("#EFUsuccessMessage").hide();
  $("#EFUerrorMessage").hide();
  $("#EFUalertMessage").hide();

  //Load Ef data
  fetchRates();

  //Create EF
  $("#createEF").click(function(){

    const client = new XMLHttpRequest();
    client.onload = function (){
      const data =JSON.parse(this.responseText);
        if (this.status == 201) {
            fetchRates();
            displayMssage("#EFCsuccessMessage");
        }
        else{
          console.log(data);
          displayMssage("#EFCerrorMessage");;
        }
    }
    client.open("POST", "/emergencyFunds/initialize",true);
    client.send();
  });

  
});