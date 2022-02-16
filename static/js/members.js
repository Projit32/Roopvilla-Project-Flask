function removeOrRevokeMember(){
  let url="/members?complete=";
  let memberData = memberMap.get($("#memberSelect").val());
  let flatRemoval= $("#removeFlat").val();
  let requestData={
    email: memberData.emails[0],
    flat:flatRemoval
  }
  let loadData=undefined;
  if($("#removeMember").prop("checked")){
    url+="Y";
  }
  else{
    url+="N";
    loadData=memberData.name;
  }

  APICall("DELETE", url, requestData, loadData);
}

function setAdminPrivilage(){
  let memberData = memberMap.get($("#memberSelect").val());
  let privilage= $("#newPrivilage").prop("checked");
  let requestData={
    flat: memberData.flat[0],
    admin_privilages: privilage
  }
  APICall("OPTIONS", "/members/changeAdminPrivilages", requestData, memberData.name);

}
function updatePassword(){
  let memberData = memberMap.get($("#memberSelect").val());
  let newPassword= $("#newPassword").val();
  let requestData={
    flat: memberData.flat[0],
    password: newPassword
  }
  APICall("PATCH", "/members/changePassword", requestData, memberData.name);
}

function fetchUnoccupiedFlats(){
  const client = new XMLHttpRequest();
  client.onload = function (){
      if (this.status === 200) {
        let target=$("#unoccupiedFlats").html("");
        const data = JSON.parse(this.responseText);
        data.data.unoccupiedFlats.forEach(element=>{
          let template=`<option value="${element}">${element}</option>`;
          target.append(template);
        });
      }
      else{
        console.log(JSON.parse(this.responseText))
      }
  }
  client.open("GET","/flats/unoccupiedFlats",true);
  client.send();
}

function setEmails(){
  let memberData = memberMap.get($("#memberSelect").val());
  let emailList= $("#newEmails").val().split(',');
  let requestData={
    flat: memberData.flat[0],
    emails: emailList
  }
  APICall("PUT", "/members/setEmails", requestData, memberData.name);
}

function APICall(method, url, data, loadData){
  const successCodes=[200,201,204];
  const client = new XMLHttpRequest();
  client.onload = function (){
      if (successCodes.includes(this.status)) {
        displayMssage(true);
        fetchMemberData(loadData);
        $("input[type='text']").val("");
      }
      else{
        displayMssage(false);
      }
  }
  client.open(method,url,true);
  client.setRequestHeader("Content-type","application/json");
  client.send(JSON.stringify(data));

}

function completeRemoveClick(checked){
  if(checked){
    $("#removalAlert").show(300);
    $('#removeFlat').prop('disabled', true);
  }
  else{
    $("#removalAlert").hide(300);
    $('#removeFlat').prop('disabled', false);
  }
}
function updateMemberDetails(value)
{
  let memberData = memberMap.get(value);

  //setting emails
  let target = $("#currentEmails").html("");
  memberData.emails.forEach(element=>{
    target.append(`<li>${element}</li>`);
  });

  // check Admin Privilages
  $("#newPrivilage").prop('checked', memberData.is_admin);

  //Set Deletion Flats
  let removeSelectTarget = $("#removeFlat").html("");
  memberData.flat.forEach(element=>{
    removeSelectTarget.append(`<option value="${element}">${element}</option>`);
  });

  if($("#removeMember").prop('checked'))
  {
    $('#removeMember').trigger('click');
    completeRemoveClick(false);
  }
  
}

let memberMap= new Map();
function fetchMemberData(defaultValue){
  fetchUnoccupiedFlats();
  const client = new XMLHttpRequest();
  client.onload = function (){
    const data =JSON.parse(this.responseText);
      if (this.status == 200) {
        let target=$('#memberSelect').html("");
        data['data'].forEach(element => {
          memberMap.set(element.name, element);
          const template = `
          <option value="${element.name}">${element.name} -- ${element.flat}</option>`;
          target.append(template);
        });
        if(defaultValue){
          $("#memberSelect").val(defaultValue).change();
        }
        else{
          $("#memberSelect").val(data['data'][0].name).change();
        }
      }
      else{
        console.log(data);
      }
  }
  client.open("GET", "/members",true);
  client.send();

}

$(function(){
$("#MAsuccessMessage").hide();
$("#MAerrorMessage").hide();
$("#removalAlert").hide();
$("#updateTime").html(new Date());

//Load member data
fetchMemberData();

//Create Member
$("#createMember").submit(function(event){
    event.preventDefault();
    const data = $(this).serializeArray();
    let formData = {}
    data.forEach((element)=>{
        formData[element.name]=element.value;
    });
    
    //business logic
    let requestData={
      name: formData.name,
      emails: formData.emails.split(','),
      flats: $("#unoccupiedFlats").val()
    };
    APICall("POST","/members",requestData, formData.name);
    this.reset();
});
});

function displayMssage(is_success){
$("#statusMessage").html("");
if(is_success){
  $("#statusMessage").html("<b>Successfully Updated!</b><br>");
  $("#statusMessage").css("color","green");
}
else{
  $("#statusMessage").html("<b>Couldn't Update!</b><br>");
  $("#statusMessage").css("color","red");
}
$("#updateTime").html(new Date());
$("#statusMessage").fadeTo(3500, 500).slideUp(1000, function() {
  $("#statusMessage").hide();
});
}
