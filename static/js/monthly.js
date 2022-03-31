  function fetchEstimates(){
    APICall("GET", "/estimates", undefined, function (data) {
        estimateMap.clear();
        data['data'].forEach(element=>{
          const now = Date.now()+Math.floor(Math.random() * 100000000000);
          fixed={
            name:element.name,
            amount:element.monthly
          }
      
          estimateMap.set(now.toString(), fixed);
        });
        displayEstimateTable();
    });
  }

  function createDistributionForm(){
    disableMonthandYear(true);
    fetchEstimates();
    showOnly("#createForm");
  }

  function setDefaultersForm(){
    disableMonthandYear(false);
    showOnly("#defaultersForm");
  }

  function updatePaymentsForm(){
    disableMonthandYear(false);
    showOnly("#paymentsForm");
  }

  function deleteDistributionForm(){
    disableMonthandYear(false);
    showOnly("#deleteForm");
  }
  function updateExpensesForm(){
    disableMonthandYear(false);
    showOnly("#expensesForm");
  }

  function disableMonthandYear(set_disable){
    $("#mainMonth").prop('disabled', set_disable);
    $("#mainYear").prop('disabled', set_disable);
  }

  function APICallPromise(method, url, data) {
    return new Promise(function (resolve, reject) {
      showLoading();
      const successCodes = [200, 201];
      const client = new XMLHttpRequest();
      client.onload = function () {
          if (successCodes.includes(this.status)) {
              displayMssage(true, undefined);
              resolve(JSON.parse(this.responseText))
          }
          else if (this.status === 204) {
              displayMssage(true, undefined);
              if (callback) {
                resolve()
              }
          }
          else {
              try {
                  let response = JSON.parse(this.responseText)
                  console.log(response);
                  displayMssage(false, response.error);
                  reject(response);
              }
              catch (err) {
                  displayMssage(false, undefined);
                  reject(err);
              }
              
          }
      }
      client.open(method, url, true);
      if (data) {
          client.setRequestHeader("Content-type", "application/json");
          client.send(JSON.stringify(data));
      }
      else {
          client.send();
      }
    });
  }

  function deleteMonth(){
    let url = `/months?year=${parseInt(selectedYear)}&month=${monthsList.indexOf(selectedMonth)+1}`;
    selectedMonth=undefined;
    selectedYear=undefined;
    APICall("DELETE", url ,undefined, undefined, true);
  }
  /**
   * 
   * Expenses
   * 
   * 
  * */

  async function fetchEstimatesAndExpenses(){
    expenseMap.clear();
    let expenses=await APICallPromise("GET", `/expenses?month=${selectedMonth}&year=${parseInt(selectedYear)}`,undefined);
    let estimates=await APICallPromise("GET", `/estimates`,undefined);
    estimates.data.forEach(element=>{
      expenseMap.set((Date.now()+Math.floor(Math.random() * 100000000000)).toString(), {
        name:element.name,
        category:"FXD",
        amount:element.monthly
      });
    });
    expenses.data.forEach(element=>{
      expenseMap.set((Date.now()+Math.floor(Math.random() * 100000000000)).toString(), {
        name:element.name,
        category:element.type,
        amount:element.amount
      });
    });
    displayExpensesTable();
  }

  let expenseMap = new Map();
  function AddExpense(){
    if(!$("#expenseName").val() || !$("#expenseAmount").val){
      return;
    }
    const now = Date.now();
    data={
      name:$("#expenseName").val(),
      category:$("#expenseCategory").find(":selected").text(),
      amount:$("#expenseAmount").val()
    }

    expenseMap.set(now.toString(), data);
    //reset
    $("#expenseName").val("");
    $('#expenseCategory').prop('selectedIndex',0)
    $("#expenseAmount").val("");
    displayExpensesTable();
  }

  function editExpense(id){
    let data = expenseMap.get(id);
    $("#expenseName").val(data.name);
    $('#expenseCategory').val(data.category);
    $("#expenseAmount").val(data.amount);
    expenseMap.delete(id);
    displayExpensesTable();
  }

  function deletExpense(id){
    expenseMap.delete(id);
    displayExpensesTable()
  }

  function displayExpensesTable(){
    let target=$("#expensesList").html("");

    expenseMap.forEach((value, key)=>{
      const template=`<tr>
      <td>${value.name}</td>
      <td>${value.category}</td>
      <td>₹${value.amount}</td>
      <td>
        <div class="btn-group" role="group" aria-label="Basic example">
            <button type="button" class="btn btn-warning btn-sm" value=${key} onclick="editExpense(this.value);">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
              </svg>
            </button>
            <button type="button" class="btn btn-danger btn-sm" value=${key} onclick="deletExpense(this.value);">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
              </svg>
            </button>
        </div>
      </td>
      </tr>
      `;
      target.append(template);
    });
  }
  /**
   * 
   * Estimates
   * 
   * 
  * */
  let estimateMap = new Map();
  function AddEstimate(){
    if(!$("#estimateName").val() || !$("#estimateAmount").val){
      return;
    }
    const now = Date.now();
    data={
      name:$("#estimateName").val(),
      amount:$("#estimateAmount").val()
    }

    estimateMap.set(now.toString(), data);
    //reset
    $("#estimateName").val("");
    $("#estimateAmount").val("");
    displayEstimateTable();
  }

  function editEstimate(id){
    let data = estimateMap.get(id);
    $("#estimateName").val(data.name);
    $("#estimateAmount").val(data.amount);
    estimateMap.delete(id);
    displayEstimateTable();
  }

  function deletEstimate(id){
    estimateMap.delete(id);
    displayEstimateTable()
  }

  function displayEstimateTable(){
    let target=$("#estimateList").html("");

    estimateMap.forEach((value, key)=>{
      const template=`<tr>
      <td>${value.name}</td>
      <td>₹${value.amount}</td>
      <td>
        <div class="btn-group" role="group" aria-label="Basic example">
            <button type="button" class="btn btn-warning btn-sm" value=${key} onclick="editEstimate(this.value);">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
              </svg>
            </button>
            <button type="button" class="btn btn-danger btn-sm" value=${key} onclick="deletEstimate(this.value);">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
              </svg>
            </button>
        </div>
      </td>
      </tr>
      `;
      target.append(template);
    });
  }

  function APICall(method, url, data, callback, refreshData){
    showLoading()
    const successCodes=[200,201];
    const client = new XMLHttpRequest();
    client.onload = function (){
        if (successCodes.includes(this.status)) {
          displayMssage(true,"Data Fetched and Populated!");
          if(callback){
            callback(JSON.parse(this.responseText));
          }
          if(refreshData){fetchMonthlyData();}
        }
        else if(this.status === 204){
          displayMssage(true,undefined);
          if(callback){
            callback();
          }
          if(refreshData){fetchMonthlyData();}
        }
        else{
          try{
            let response=JSON.parse(this.responseText)
            console.log(response);
            displayMssage(false,response.error);
          }
          catch(err){
            displayMssage(false,undefined);
          }
        }
    }
    client.open(method,url,true);
    if(data){
      client.setRequestHeader("Content-type","application/json");
      client.send(JSON.stringify(data));
    }
    else{
      client.send();
    }
    
  }

  function showOnly(id){
    $(".selectable").hide();
    $(id).show(500);
  }

  function updateYearlyDetails(value){
    selectedYear=value;
    let months=monthlyMap.get(parseInt(value));
    let target=$('#mainMonth').html("");
    months.forEach(element=>{
      const template = `
      <option value="${element}">${element}</option>`;
      target.append(template);
    });
    if(selectedMonth && months.includes(selectedMonth)){
      $("#mainMonth").val(selectedMonth).change();
    }
    else{
      $("#mainMonth").val(months[0]).change();
    }
    
  }

  async function updateMonthlyDetails(value){
    selectedMonth=value;
    await fetchEstimatesAndExpenses();
    //expense Monthly Data
    $("#updateExpenseLabel").html(`Update Expenses for ${selectedMonth} of ${selectedYear}`);

    //Delete monthly data
    $("#removalWarning").html(`You are about to delete the month <b>${selectedMonth}</b> of year <b>${selectedYear}</b>`);

    //Defaulters Data
    APICall("GET", `/months/defaulterStatus?year=${parseInt(selectedYear)}&month=${monthsList.indexOf(selectedMonth)+1}`, undefined, function(data){
      let target=$("#defaultersOptions").html("");
      data['data'].forEach(element=>{
        let template=`<b>${element.flat}</b> <input class="form-check-input" type="checkbox" role="switch" name="${element.flat}" ${element.defaulter? "checked": ""}><br>`;
        target.append(template);
      });
    });

    //Payment Data
    APICall("GET", `/months/paymentStatus?year=${parseInt(selectedYear)}&month=${monthsList.indexOf(selectedMonth)+1}`, undefined, function(data){
      let target=$("#paymentOptions").html("");
      data['data'].forEach(element=>{
        let template=`<b>${element.flat}</b> <input class="form-check-input" type="checkbox" role="switch" name="${element.flat}" ${element.payment === "YES"? "checked": ""}><br>`;
        target.append(template);
      });
    });
  }

  const monthsList=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"];
  let selectedYear=0;
  let selectedMonth=0;
  let monthlyMap= new Map()

  function fetchMonthlyData(){
    APICall("GET", "/months", undefined, function(data){
      let target=$('#mainYear').html("");
          data['data'].forEach(element => {
            monthlyMap.set(element.year, element.months);
            const template = `
            <option value="${element.year}">${element.year}</option>`;
            target.append(template);
          });
          if(selectedYear){
            $("#mainYear").val(selectedYear).change();
          }
          else{
            $("#mainYear").val(data['data'][0].year).change();
          }
    }, false);
  }

  $(function(){
    fetchMonthlyData();
    $(".selectable").hide();

    for(let i =0 ;i<monthsList.length;i++)
    {
      let template=`<option value="${i+1}">${monthsList[i]}</option>`;
      $("#expensesSelect").append(template);
      $("#createMonthList").append(template);
    }
    
    //create distribution form submit
    APICall("GET", `/members`,undefined, function(data){
      let target=$("#payersOptions").html("");
      data['data'].forEach(element=>{
        element.flat.forEach(item=>{
          let template=`<b>${item}</b> <input class="form-check-input" type="checkbox" role="switch" name="${item}"}><br>`;
          target.append(template);
        })
      });
    }, false);

    $("#createMonthlyForm").submit(function(event){
      event.preventDefault();
      const data = $(this).serializeArray();
      let formData = {}
      data.forEach((element)=>{
          formData[element.name]=element.value;
      });

      let checks = $('input[type="checkbox"]', this);
      let paying=[];
      let notPaying=[];
      checks.get().forEach(check=>{
        if(check.checked){
          paying.push(check.name);
        }
        else{
          notPaying.push(check.name);
        }
      });

      console.log(paying.length, !paying.length);
      if(!paying.length){
        displayMssage(false,"Atleast 1 paying member should be present!");
        return;
      }

      let estimates=[];
      estimateMap.forEach((value,key)=>{
        estimates.push({ITEM:value.name, Price:Number(value.amount)});
      })

      const requestData ={
        estimates,
        payingFlats: paying,
        notPayingFlats: notPaying
      }
      APICall("POST", `/months?year=${parseInt(formData['createDistYear'])}&month=${parseInt(formData['createDistMonth'])}`,requestData, (data)=>{
        estimateMap.clear();
        this.reset();
        displayEstimateTable();
      }, true);
    });

    //update expenses form submit
    APICall("GET", `/months/estimationCategories`,undefined, function(data){
      let target=$("#expenseCategory").html("");
      data['data'].forEach(element=>{
        let template=`<option value="${element}">${element}</option>`;
        target.append(template);
      });
    }, false);

    $("#setExpensesForm").submit(function(event){
      event.preventDefault();
      const data = $(this).serializeArray();
      let formData = {}
      data.forEach((element)=>{
          formData[element.name]=element.value;
      });
      if(!expenseMap.size){
        displayMssage(false,"Atleast 1 expense should be added!");
        return;
      }

      let expenditures =[]
      expenseMap.forEach((value, key)=>{
        expenditures.push({
          NAME:value.name,
          CATEGORY:value.category,
          COST:Number(value.amount)
        });
      });
      let electricity={
        month:parseInt(formData['bill_month']),
        year:parseInt(formData['bill_year']),
        units:Number(formData['bill_units']),
        amount:Number(formData['bill_amount'])
      }
      
      const requestData={
        expenditures,
        electricity
      }
      APICall("PUT", `/months/expenses?year=${parseInt(selectedYear)}&month=${monthsList.indexOf(selectedMonth)+1}`,requestData, (data)=>{
        expenseMap.clear();
        this.reset();
        displayExpensesTable();
      }, false);
    });

    //change payment status form submit
    $("#setPaymentsForm").submit(function(event){
      event.preventDefault();
      let checks = $('input[type="checkbox"]', this);
      let paid=[];
      let notPaid=[];
      checks.get().forEach(check=>{
        if(check.checked){
          paid.push(check.name);
        }
        else{
          notPaid.push(check.name);
        }
      });

      const reqData={
        data:[
          {
            flats:paid,
            status: "YES"
          },
          {
            flats:notPaid,
            status: "NO"
          }
        ]
      }
      APICall("PATCH", `/months/paymentStatus?year=${parseInt(selectedYear)}&month=${monthsList.indexOf(selectedMonth)+1}`,reqData, undefined, true );
    });


    //change defaulters status form submit
    $("#changeDefaultersForm").submit(function(event){
      event.preventDefault();
      let checks = $('input[type="checkbox"]', this);
      let defaulted=[];
      let notDefaulted=[];
      checks.get().forEach(check=>{
        if(check.checked){
          defaulted.push(check.name);
        }
        else{
          notDefaulted.push(check.name);
        }
      });

      const reqData={
        data:[
          {
            flats:defaulted,
            status: true
          },
          {
            flats:notDefaulted,
            status: false
          }
        ]
      }
      APICall("PUT", `/months/defaulterStatus?year=${parseInt(selectedYear)}&month=${monthsList.indexOf(selectedMonth)+1}`,reqData, undefined, true );
    });

    $("#message").hide();
  });

  function showLoading()
  {
    $("#message").css("color","white");
    $("#message").html(`<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...`);
    $("#message").fadeTo(100, 0.4);
  }

  function displayMssage(is_success,message){
    if(is_success){
      $("#message").html(`<b>${message? message : "Successfully Updated!"}</b><br>`);
      $("#message").css("color","green");
    }
    else{
      $("#message").html(`<b>${message? message : "Couldn't Update!"}</b><br>`);
      $("#message").css("color","red");
    }

    $("#message").fadeTo(2000, 1).slideUp(1500, function() {
      $("#message").hide();
    });
  }