$(function(){

    //Logout - onclick
    $('#logout').click(function(event){
        const client = new XMLHttpRequest();
        client.onload = function (){
                if (this.status != 204) {
                    
                    console.error({
                        code : this.status,
                        details : JSON.parse(this.responseText)
                    });
                }
                window.location="/";
            }
        client.open("DELETE", "/users/logout",true);
        client.send();
        event.preventDefault();
    });

    //Logout all devices- onclick
    $('#logoutAD').click(function(event){
        const client = new XMLHttpRequest();
        client.onload = function (){
                if (this.status != 204) {
                    
                    console.error({
                        code : this.status,
                        details : JSON.parse(this.responseText)
                    });
                }
                window.location="/";
            }
        client.open("DELETE", "/users/logoutAll",true);
        client.send();
        event.preventDefault();
    });

    //Months by year - on start
    const availableDataClient = new XMLHttpRequest();
          availableDataClient.onload= function(){
            const response =JSON.parse(this.responseText);
            if(this.status == 200)
            {
              const results=[];
              let crt=0
              response.months.forEach(element => {
                results.push({
                  "id": crt,
                  "text": element
                });
                crt++;
              });
              $('#availableMonths').select2({
                data: results
              });       
            }
            else{
                    console.error({
                        code : this.status,
                        details : response.months
                    })
                }
          };
          availableDataClient.open("GET", "/months/availableByYear/"+new Date().getFullYear());
          availableDataClient.send();
});

function getMonthFromString(mon){
    return new Date(Date.parse(mon +" 1, 2012")).getMonth()+1;
}

function clientCallGET(url, onSuccess){
    const client = new XMLHttpRequest();
    client.onload=function(){
        if (this.status == 200) {
            onSuccess(JSON.parse(this.responseText))
        }
        else{
            console.error({
                code : this.status,
                details : JSON.parse(this.responseText)
            })
        }
    };
    client.open("GET", url);
    client.send();
}