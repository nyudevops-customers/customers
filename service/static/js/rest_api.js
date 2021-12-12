$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.customer_id);
        $("#firstname").val(res.firstname);
        $("#lastname").val(res.lastname);
        $("#email_id").val(res.email_id);
        $("#address").val(res.address);
        $("#phone_number").val(res.phone_number);
        $("#card_number").val(res.card_number);
        $("#active").val(res.active);
        if (res.active == true) {
            $("#active").val("true");
        } else {
            $("#active").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#firstname").val("");
        $("#lastname").val("");
        $("#email_id").val("");
        $("#address").val("");
        $("#phone_number").val("");
        $("#card_number").val("");
        $("#active").val("");

    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        var firstname = $("#firstname").val();
        var lastname = $("#lastname").val();
        var email_id = $("#email_id").val();
        var address = $("#address").val();
        var phone_number = $("#phone_number").val();
        var card_number = $("#card_number").val();
        var active = $("#active").val() == "true";

        var data = {
            "firstname": firstname,
            "lastname": lastname,
            "email_id": email_id,
            "address": address,
            "phone_number": phone_number,
            "card_number": card_number,
            "active": active
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {
        var customer_id =$("#customer_id").val();
        var firstname = $("#firstname").val();
        var lastname = $("#lastname").val();
        var email_id = $("#email_id").val();
        var address = $("#address").val();
        var phone_number = $("#phone_number").val();
        var card_number = $("#card_number").val();
        var active = $("#active").val() == "true";

        var data = {
            //"customer_id": customer_id,
            "firstname": firstname,
            "lastname": lastname,
            "email_id": email_id,
            "address": address,
            "phone_number": phone_number,
            "card_number": card_number,
            "active": active
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            //flash_message(res.responseJSON.message)
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + customer_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Deactivate a Customer
    // ****************************************

    // $("#deactivate-btn").click(function () {

    //     var customer_id = $("#customer_id").val();

    //     var ajax = $.ajax({
    //             type: "PUT",
    //             url: "/customers/" + customer_id + "/deactivate",
    //             contentType: "application/json"
    //         })

    //     ajax.done(function(res){
    //         // console.log(res)
    //         update_form_data(res)
    //         flash_message("Success")
    //       //  show_in_search_results_by_user_id()
    //     });

    //     ajax.fail(function(res){
    //         flash_message(res.responseJSON.message)
    //     });

    // });


    // ****************************************
    // Activate a Customer
    // ****************************************

    $("#activate-btn").click(function () {

        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id + "/activate",
                contentType: "application/json"
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        var firstname = $("#firstname").val();
        var lastname = $("#lastname").val();
        var email_id = $("#email_id").val();
        var address = $("#address").val();
        var phone_number = $("#phone_number").val();
        var card_number = $("#card_number").val();
        var active = $("#active").val() == "true";

        var queryString = ""
        if (firstname) {
            queryString += 'firstname=' + firstname
        }
        if (lastname) {
            if (queryString.length > 0) {
                queryString += '&lastname=' + lastname
            } else {
                queryString += 'lastname=' + lastname
            }
        }
        if (email_id) {
            if (queryString.length > 0) {
                queryString += '&email_id=' + email_id
            } else {
                queryString += 'email_id=' + email_id
            }
        }
        
        if (phone_number) {
            if (queryString.length > 0) {
                queryString += '&phone_number=' + phone_number
            } else {
                queryString += 'phone_number=' + phone_number
            }
        }
       
        if (active) {
            if (queryString.length > 0) {
                queryString += '&activer=' + active
            } else {
                queryString += 'active=' + active
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">FirstName</th>'
            header += '<th style="width:40%">LastName</th>'
            header += '<th style="width:40%">Email id</th>'
            header += '<th style="width:40%">Address</th>'
            header += '<th style="width:40%">Phone number</th>'
            header += '<th style="width:40%">Card number</th>'
            header += '<th style="width:10%">Active</th></tr>'
            $("#search_results").append(header);
            var firstCustomer = "";
            for(var i = 0; i < res.length; i++) {
                var customer = res[i];
                var row = "<tr><td>"+customer.customer_id+"</td><td>"+customer.firstname+"</td><td>"+customer.lastname+"</td><td>"+customer.address+"</td><td>"+customer.email_id+"</td><td>"+customer.phone_number+"</td><td>"+customer.card_number+"</td><td>"+customer.active+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstCustomer = customer;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
