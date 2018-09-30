/*
Copyright (c) 2015 Mitsuo Nakaya
http://renhuuka.com/

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to 
the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
jQuery(function($) {
    var move = null;
    var months = 12;
    output_calendar(move, months);
    // 横移動
    $('#move_controls button').click(function () {
        var months = 12;
        months = $('#period_controls button.active').data('months');
        var move = null;
        var move_now = $('#move_now').data('now');
        if ($(this).hasClass('prev')){
            $('#move_now').data('now', move_now - 1);
        } else if ($(this).hasClass('next')){
            $('#move_now').data('now', move_now + 1);
        }
        move = $('#move_now').data('now');
        $('#move_controls button.active').removeClass('active');
        $(this).addClass('active');
        output_calendar(move, months);
    });
    // 表示期間
    $('#period_controls button').click(function () {
        var move = null;
        var months = 12;
        if ($('#move_controls button.active').data('move')){
            move = $('#move_controls button.active').data('move');
        }
        months = $(this).data('months');
        $('#period_controls button.active').removeClass('active');
        $(this).addClass('active');
        output_calendar(move, months);
    });
    // Add Money Data
    $("#Add_Money_Submit").click(function(){
        $.ajax({
            url: "#",
            type: "POST",
            data: $("form#Add_Money_Form").serialize(),
            success: function(json){
                var move = $('#move_now').data('now');
                var months = 12;
                months = $('#period_controls button.active').data('months');
                output_calendar(move, months);
            },
            error: function(){
            }
        });
        $('#Add_Money').modal('hide');
    });
    // Update Money Data
    $("#Update_Money_Submit").click(function(){
        $.ajax({
            url: "#",
            type: "POST",
            data: $("form#Update_Money_Form").serialize(),
            success: function(json){
                var move = $('#move_now').data('now');
                var months = 12;
                months = $('#period_controls button.active').data('months');
                output_calendar(move, months);
            },
            error: function(){
            }
        });
        $('#Update_Money').modal('hide');
    });
    // Delete Money Data
    $("#Delete_Money_Submit").click(function(){
        $.ajax({
            url: "#",
            type: "POST",
            data: $("form#Delete_Money_Form").serialize(),
            success: function(json){
                var move = $('#move_now').data('now');
                var months = 12;
                months = $('#period_controls button.active').data('months');
                output_calendar(move, months);
            },
            error: function(){
            }
        });
        $('#Update_Money').modal('hide');
    });
    $("select#AddSelectItem").change(function () {
        var jsonurl = '/ajax/get_item/' + $(this).val() + '/';
        $.getJSON(jsonurl,function(json){
            if (json.default_ammount){
                $('input#AddInputAmmount').val(json.default_ammount);
            }
        });
    });
    $("select#SelectItem").change(function () {
        var jsonurl = '/ajax/get_item/' + $(this).val() + '/';
        $.getJSON(jsonurl,function(json){
            if (json.default_ammount){
                $('input#InputAmmount').val(json.default_ammount);
            }
        });
    });
    $('#Add_Money').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var date = button.data('date');
        var modal = $(this);
        modal.find('.modal-body input#AddInputDate').val(date);
    });
    $('#Update_Money').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var momey_id = button.data('momey_id');
        var modal = $(this);
        var get_itemcategory_url = '/ajax/get_money/' + momey_id + '/';
        $.getJSON(get_itemcategory_url, {
            start:$.now()
        },function(json){
            modal.find('.modal-body input#EditMoneyID').val(json.money_id);
            modal.find('.modal-body input#DeleteMoneyID').val(json.money_id);
            modal.find('.modal-body input#InputDate').val(json.date);
            modal.find('.modal-body select#SelectItem').val(json.item_id);
            modal.find('.modal-body input#InputAmmount').val(json.ammount);
            modal.find('.modal-body input#InputSummary').val(json.summary);
        });
    });
});
function output_calendar(move, months){
    $('#moneys').empty();
    $('.year').empty();
    $('#moneys').append('<thead><tr><th>#</th></tr></thead><tbody></tbody><tfoot><tr><th></th></tr></tfoot>');
    var start_date_year = moment().year();
    if (months) {
        period_months = months;
        if (months == 1){
            start_date_month = moment(moment().add(1, 'months')).month();
        } else if (months == 3){
            start_date_month = moment().month();
        } else if (months == 12){
            start_date_month = 1;
        } else {
            start_date_month = 1;
        }
    } else {
        start_date_month = 1;
        period_months = 12;
    }
    var start_date = String(start_date_year) + '-' + String(start_date_month) + '-1';
    moment_start_date = moment(start_date, "YYYY-MM-DD");
    if (move === null){
        moment_start_date = moment(moment_start_date);
    } else {
        moment_start_date = moment(moment_start_date).add(move*period_months, 'months');
    }
    $('.year').append(moment_start_date.year() + '年');
    for (var i=0; i<period_months; i++) {
        $('#moneys thead tr').append('<th>' + String(moment(moment_start_date).add(i, 'months').month() + 1) + '月</th>');
        $('#moneys tfoot tr').append('<th>' + String(moment(moment_start_date).add(i, 'months').month() + 1) + '月</th>');
    }
    for (var j=0; j<31; j++) {
        string_day = j + 1;
        if (string_day < 10){
            string_day = '0' + String(string_day);
        } else {
            string_day = String(string_day)
        }
        $('#moneys tbody').append('<tr id="day_row_' + string_day + '"><th>' + string_day + '日</th></tr>');
        for (var k=0; k<period_months; k++) {
            moment_start_date_month = moment(moment_start_date).month()+k+1;
            if (moment_start_date_month < 10){
                moment_start_date_month = '0' + String(moment_start_date_month);
            }
            if (moment(String(moment_start_date.year()) + '-' + String(moment_start_date_month) + '-' + string_day, "YYYY-MM-DD").isValid() === true){
                var cellclass = '';
                if (moment(String(moment_start_date.year()) + '-' + String(moment_start_date_month) + '-' + string_day).format('YYYY-MM') == moment().format('YYYY-MM') || moment(String(moment_start_date.year()) + '-' + String(moment_start_date_month) + '-' + string_day).format('YYYY-DD') == moment().format('YYYY-DD')){
                    cellclass = ' bg-info';
                }
                $('#day_row_' + string_day).append('<td class="cell_' + String(moment(String(moment_start_date.year()) + '-' + String(moment_start_date_month) + '-' + string_day).format('YYYY-MM-DD')) + cellclass + '"><p><button class="btn btn-info btn-sm btn-block" data-toggle="modal" data-target="#Add_Money" data-date="' + String(moment(String(moment_start_date.year()) + '-' + String(moment_start_date_month) + '-' + string_day).format('YYYY-MM-DD')) + '"><i class="fa fa-plus"></i></button></p></td>');
            } else {
                $('#day_row_' + string_day).append('<td></td>');
            }
        }
    }
    get_money(moment_start_date.year(), moment_start_date.month()+1, period_months);
}
function get_money(year, month, period_months){
    var get_money_url = '/ajax/get_moneys/' + year + '/' + month + '/1/' + period_months + '/';
    $.getJSON(get_money_url, {
        start:$.now()
    },function(json){
        $.each(json, function(i, data){
            if (data.date){
                var the_date = String(moment(data.date).format('YYYY-MM-DD'));
                var ammountclass = '';
                var ammounticon = '';
                var balanceclass = '';
                var summarybr = '';
                if (data.ammount < 0) {
                    ammountclass = 'text-danger';
                }
                if (data.balance < 0) {
                    balanceclass = 'text-danger';
                }
                if (data.summary) {
                    summarybr = '<br /><i class="fa fa-question-circle"></i>';
                }
                var ammount = separate(data.ammount);
                var balance = separate(data.balance);
                if (!$('.cell_child_' + the_date)[0]){
                $('.cell_' + the_date).append('<table class="table table-bordered table-condensed table-hover cell_child_' + the_date + '"></table>');
                }
                $('.cell_child_' + the_date).append('<tr class="money_' + data.money_id + '" data-toggle="modal" data-target="#Update_Money" data-momey_id="' + data.money_id + '"><td><strong class="' + ammountclass + '">' + ammount + '</strong></td><td><span>' + data.item + summarybr + data.summary + '</span></td><td><strong class="' + balanceclass + '">' + balance + '</strong></td></tr>');
            }
        });
    });
}
function separate(num){
    return String(num).replace( /(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
