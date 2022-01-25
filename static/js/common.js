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
});
