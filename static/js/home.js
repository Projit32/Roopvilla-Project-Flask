let featureMap = new Map();
function fetchFeatures() {
    featureMap.clear();
    APICall("GET", "/features", undefined, (data) => {
        data.data.forEach(element => {
            featureMap.set(element.id, element);
        });
        displayFeatureTable();
    });
}

function displayFeatureTable() {
    let target = $("#featureList").html("");

    featureMap.forEach((value, key) => {
        const template = `<tr>
        <td class="text-truncate">
            <span class="d-inline-block text-truncate" style="max-width: 250px;">
                ${value.heading + " " + (value.focused ? value.focused : "")}
            </span></td>
        <td class="text-truncate">
            <span>
                ${value.date}
            </span></td>
        <td>
            <div class="btn-group" role="group" aria-label="Basic example">
                <button type="button" class="btn btn-warning btn-sm" value=${key} onclick="editFeature(this.value);">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                    <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
                </svg>
                </button>
                <button type="button" class="btn btn-danger btn-sm" value=${key} onclick="deleteFeature(this.value);">
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

function editFeature(featureID) {
    const data = featureMap.get(featureID);
    console.log(data);
    for (let key in data) {
        $("#updateFeature input[name=" + key + "]").val(decodeURIComponent(data[key]));
    }
}

function deleteFeature(featureID) {
    const id = featureMap.get(featureID)['id'];
    APICall("DELETE", "/features", { id }, () => {
        fetchFeatures();
    });
}

$(function () {
    $(".selectable").hide();
    $("#message").hide();
    fetchFeatures();
    fetchExpiredSessions();
    fetchEstimate();

    //Create Form Submit
    $("#createFeatureForm").submit(function (event) {
        event.preventDefault();
        const data = $(this).serializeArray();
        let formData = {}
        data.forEach((element) => {
            if (element.value !== '') {
                formData[element.name] = element.value;
            }

        });
        formData['date'] = new Date().toUTCString()
        console.log(formData);
        APICall("POST", "/features", formData, () => {
            $("#createFeatureForm").trigger('reset');
            fetchFeatures();
        });
    });

    //Update Form Submit
    $("#updateFeatureForm").submit(function (event) {
        event.preventDefault();
        const data = $(this).serializeArray();
        let formData = {}
        data.forEach((element) => {
            if (element.value !== '') {
                formData[element.name] = element.value;
            }
        });
        formData['date'] = new Date().toUTCString()
        console.log(formData);
        APICall("PUT", "/features", formData, () => {
            $("#updateFeatureForm").trigger('reset');
            fetchFeatures();
        });
    });
})

function showOnly(id) {
    $(".selectable").hide();
    $(id).fadeIn(500);
}
function displayMssage(is_success, message) {
    if (is_success) {
        $("#message").html(`<b>${message ? message : "Successfully Updated!"}</b><br>`);
        $("#message").css("color", "green");
    }
    else {
        $("#message").html(`<b>${message ? message : "Couldn't Update!"}</b><br>`);
        $("#message").css("color", "red");
    }

    $("#message").fadeTo(2000, 1).slideUp(1500, function () {
        $("#message").hide();
    });
}
function showLoading() {
    $("#message").css("color", "white");
    $("#message").html(`<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...`);
    $("#message").fadeTo(100, 0.4);
}

function APICall(method, url, data, callback) {
    showLoading();
    const successCodes = [200, 201];
    const client = new XMLHttpRequest();
    client.onload = function () {
        if (successCodes.includes(this.status)) {
            displayMssage(true, undefined);
            if (callback) {
                callback(JSON.parse(this.responseText));
            }
        }
        else if (this.status === 204) {
            displayMssage(true, undefined);
            if (callback) {
                callback();
            }
        }
        else {
            try {
                let response = JSON.parse(this.responseText)
                console.log(response);
                displayMssage(false, response.error);
            }
            catch (err) {
                displayMssage(false, undefined);
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

}

function deleteExpiredSessions(id) {
    APICallWithButtonLoading("DELETE", "/sessions/expiredSessions", undefined, function () { fetchExpiredSessions(); }, "#" + id)
}
function toggleLoadingButton(id, load, defaultText) {
    const template = `
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Loading...
    `;
    $(id).prop('disabled', load);
    $(id).html(load ? template : defaultText);
}
function fetchExpiredSessions() {
    APICall("GET", "/sessions/expiredSessions", undefined, function (data) {
        if (data.data.expiredSessions > 0) {
            $("#sessionCount").css("color", "#F57919");
        }
        else if (data.data.expiredSessions > 25) {
            $("#sessionCount").css("color", "red");
        }
        else {
            $("#sessionCount").css("color", "green");
        }
        $("#sessionCount").html(`<b>${data.data.expiredSessions}</b>`);
    });
}

function APICallWithButtonLoading(method, url, data, callback, button_id) {
    let defaultText = undefined
    if (button_id) {
        defaultText = $(button_id).html();
        toggleLoadingButton(button_id, true, undefined);
    }
    const successCodes = [200, 201];
    const client = new XMLHttpRequest();
    client.onload = function () {
        if (button_id) {
            toggleLoadingButton(button_id, false, defaultText);
        }

        if (successCodes.includes(this.status)) {
            if (callback) {
                callback(JSON.parse(this.responseText));
            }
        }
        else if (this.status === 204) {
            if (callback) {
                callback();
            }
        }
        else {
            try {
                let response = JSON.parse(this.responseText)
                console.log(response);
                displayMssage(false, response.error);
            }
            catch (err) {
                displayMssage(false, undefined);
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

}

function addEstimateField(){
    let target = $("#estimatesList");

    let content = `
    <form class="input-group mb-3 my-2"  onsubmit="addNewEstimate(event, this);">
        <span class="input-group-text">Item Name</span>
        <input type="text" class="form-control form-select-sm"  name='name' required>
        <span class="input-group-text">Monthly</span>
        <input type="number" class="form-control form-select-sm"  name='monthly' step="0.1" required  onkeyup="updateAnnual(this);">
        <span class="input-group-text">Annually</span>
        <input type="number" class="form-control form-select-sm"  name='annually' step="0.1" required onkeyup="updateMonth(this);">
        <button class="btn btn-primary" type="submit">Add Feature</button>
    </form>`;

    target.append(content);
}
function editEstimate(e,form) {
    e.preventDefault();
    const data = $(form).serializeArray();
    let formData = {}
    data.forEach((element) => {
        if (element.value !== '') {
            formData[element.name] = element.value;
        }
    });
    let btn=$("button[type=submit]",form);
    console.log(btn);
    APICallWithButtonLoading("PATCH", "/estimates", formData, function(data){
        fetchEstimate();
    }, btn);
}
function addNewEstimate(e,form) {
    e.preventDefault();
    const data = $(form).serializeArray();
    let formData = {}
    data.forEach((element) => {
        if (element.value !== '') {
            formData[element.name] = element.value;
        }
    });
    let btn=$("button[type=submit]",form);
    console.log(btn);
    APICallWithButtonLoading("POST", "/estimates", formData, function(data){
        fetchEstimate();
    },btn);
}
function deleteEstimate(id, btn){
    data={id};
    console.log(data);
    APICallWithButtonLoading("Delete", "/estimates", data, function(data){
        fetchEstimate();
    },btn);
}

function fetchEstimate(){
    APICall("GET", "/estimates", undefined, function (data) {
        let target=$("#estimatesList").html("");
        console.log(data);
        data['data'].forEach(element=>{
            let content = `
                <form class="input-group mb-3 my-2"  onsubmit="editEstimate(event, this);">
                    <input type="text" class="form-control form-select-sm visually-hidden" required name="id" value="${element.id}">
                    <span class="input-group-text">Item Name</span>
                    <input type="text" class="form-control form-select-sm" value="${element.name}" name='name' required>
                    <span class="input-group-text">Monthly</span>
                    <input type="number" class="form-control form-select-sm" value="${element.monthly}" name='monthly' step="0.1" required onkeyup="updateAnnual(this);">
                    <span class="input-group-text">Annually</span>
                    <input type="number" class="form-control form-select-sm" value="${element.annually}" name='annually' step="0.1" required onkeyup="updateMonth(this);">
                    <button class="btn btn-warning" type="submit">Update Feature</button>
                    <button class="btn btn-danger" type="button" onclick='deleteEstimate("${element.id}",this);'>Remove Feature</button>
                </form>`;

            target.append(content);
        });
    });
}

function updateAnnual(month){
    console.log(month.value);
    if(month.value)
    {
        const annually=Number(month.value)*12;
        $("input[name='annually']",$(month).parent()).val(annually.toFixed(1));
    }
}
function updateMonth(annual){
    console.log(annual.value);
    if(annual.value)
    {
        const monthly=Number(annual.value)/12;
        $("input[name='monthly']",$(annual).parent()).val(monthly.toFixed(1));
    }
}