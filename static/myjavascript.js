document.cookie = JSON.stringify({})


function gonext(){
    document.getElementById("user-detail").style.display = "block";
    document.getElementById("item-detail").style.display = "none";
    $('#item-list').val(document.cookie);
}


function phonenumber(inputtxt)
{
      var phoneno = /^\d{10}$/;
      if(inputtxt.value.match(phoneno))
      {
          return true;
      }
      else
      {
         alert("Not a valid Phone Number");
         return false;
      }
}

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  if (evt.type == 'click'){
      // Get all elements with class="tablinks" and remove the class "active"
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      evt.currentTarget.className += " active";
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";

  if(tabName=='myorder'){
      myorder();
  }
}


function  item_snippet() {
    var term = $('#itemname').val();
    var category_filter = $('#category_list').val();
    if (category_filter === undefined || category_filter ==0) {
        category_filter = 0;
    }
    if (term === undefined || term == '') {
        term = 'all';
    }
    var url_str = '/adminpanel/items_snippet/' + category_filter + '/' + term
    $.ajax({
        url: url_str,
        type: 'GET'
    }).done(function (resp) {
        var items_ul = $('#items-ul');
        items_ul.empty();
        items_ul.append(resp.html);
    })
}

function set_units(id, units){
    unit_list = units.split('/');
    select_unit_dropdown = $('#unit-'+id);
    select_unit_dropdown.empty();
    select_unit_dropdown.append($('<option>', {value:'', text:'Select Unit'}));
    for(i=0;i<unit_list.length;i++){
        select_unit_dropdown.append($('<option>', {value:unit_list[i], text:unit_list[i]}));
    }
}

function change_unit(clicked_unit, select_id) {
    event.preventDefault();
    var a = clicked_unit.value;
    document.getElementById(select_id).selecteIndexd = clicked_unit.options.selectedIndex;
    console.log(a);
    return true;
}

function set_subitem(id, subitems){
    unit_list = subitems.split('/');
    select_unit_dropdown = $('#subitemlist-'+id);
    select_unit_dropdown.empty();
    select_unit_dropdown.append($('<option>', {value:'', text:'Choice your item'}));
    for(i=0;i<unit_list.length;i++){
        select_unit_dropdown.append($('<option>', {value:unit_list[i], text:unit_list[i]}));
    }
}

function change_subitem(clicked_subitem, select_id) {
    event.preventDefault();
    var a = clicked_subitem.value;
    document.getElementById(select_id).selectedIndex = clicked_subitem.options.selectedIndex;
    console.log(a);
    return true;
}

function set_default_units(units_list) {
    select_unit_dropdown = $('#unit-dropdown')
    for(i=0;i<units_list.length;i++){
        select_unit_dropdown.append($('<option>', {value:units_list[i], text:units_list[i]}));
    }
}

function add_item_cart(item_id) {
    var item_dict = {};
    var itemname = $('#itemname-'+item_id);

    item_dict['name'] = itemname.val();
    var hindiname = $('#hindiname-'+item_id).val();

    if (hindiname != undefined){
        item_dict['hindiname'] = hindiname;
    }
    var item_img = $('#itemimg-'+item_id).val();
    if (item_img != undefined){
        item_dict['img_url'] = item_img
    }

    var quantity = $('#quantity-'+item_id).val();
    if (quantity == "") {
        alert("Please enter Quantity.");
        return false;
    }
    if (quantity != undefined){
        item_dict['quantity'] = quantity
    }
    var new_item = $('#new-item-'+item_id).val();
    if (new_item != undefined){
        item_dict['new_item'] = true;
        var comment = $('#comment-'+item_id).val();
        if (comment == undefined){
            comment = ''
        }
        item_dict['comment'] = comment;
    }

    item_dict['id'] = item_id;

    var unit = $('#unit-'+item_id).val();
    if (unit != undefined){
        item_dict['unit'] = unit;
    }

    var subitem = $('#subitemlist-'+item_id).val();
    if (subitem != undefined){
        item_dict['subitem'] = subitem
    }

    var cookies_data = JSON.parse(document.cookie.split(';')[0]);
    if (subitem){
        var item_key = item_id + '_'+ subitem
    }
    else{
        var item_key = item_id
    }

    cookies_data[item_key] = item_dict;
    document.cookie = JSON.stringify(cookies_data);

    var check = document.getElementById('item-check-'+ item_id);
    check.classList.remove('hidden');

    var add_btn = document.getElementById('item-add-update-'+item_id);
    add_btn.innerText = 'Update';
}

function remove_item(item_id, item_key) {
    var cookie_data = JSON.parse(document.cookie.split(';')[0]);
    delete cookie_data[item_key];
    document.cookie = JSON.stringify(cookie_data);
    var elem = document.querySelector('#order-row-'+item_key);
    elem.parentNode.removeChild(elem);
    document.getElementById('quantity-'+item_id).selectedIndex=0;
    document.getElementById('unit-'+item_id).selectIndex=0;
    $('#item-add-update-'+item_id).text('Add');
    document.getElementById('item-check-'+ item_id).classList.add('hidden');
}

function edit_item(item_id, item_key) {
    var quantity = parseInt(prompt('Enter Quantity'));
    if (quantity == null || Number.isNaN(quantity) || quantity == "") {
        alert('Please enter valid quantity.');
    }
    else{
        var cookie_data = JSON.parse(document.cookie.split(';')[0]);
        cookie_data[item_key]['quantity'] = quantity;
        document.cookie = JSON.stringify(cookie_data);
        document.getElementById("edit-quantity-"+ item_key).innerHTML = quantity;
    }
}

localStorage.setItem("lastname", "Smith");

function myorder() {
    var item_row_html;
    var item_order_list = $('#item_order_list');
    var cookie_data = JSON.parse(document.cookie.split(';')[0]);
    item_order_list.empty();
    for(item_id in cookie_data){
        item_data = cookie_data[item_id];
        if (item_data['new_item'] != undefined){
            item_row_html = '<div id="order-row-'+ item_id +'" class="row item-list-row form-group">\n' +
            '        <div class="fit_img col-md-2 col-xs-2 col-sm-3">\n' +
            '        </div>\n' +
            '        <div class="col-md-8 col-xs-8 col-sm-7">\n' +
            '            <div class="row">' +
            '                <div class="col-sm-12 col-md-12 col-xs-12">' +
            '                   <div class="item-name">' + item_data['name'] + '</div>\n' +
            '                   <div class="item-hindi-name m5-bottom">' + item_data['comment'] + '</div>\n' +
            '                </div>' +
            '            </div>'+
            '        </div>\n' +
            '        <div class="col-md-1 col-sm-1 col-xs-1">' +
            '        '+
            '        </div>'+
            '        <div class="col-md-1 col-sm-1 col-xs-1" style="cursor: pointer; z-index: 5" onclick="remove_item('+ item_data['id'] +',' + item_id + ')">' +
            '           <div class="icon-trash" style="float: left">\n' +
            '           <div class="trash-lid" style="background-color: blue"></div>\n' +
            '           <div class="trash-container" style="background-color: blue"></div>\n' +
            '           <div class="trash-line-1"></div>\n' +
            '           <div class="trash-line-2"></div>\n' +
            '           <div class="trash-line-3"></div>\n' +
            '        </div>'+
            '    </div>'
        }
        else {
            item_row_html = '<div id="order-row-'+ item_id +'" class="row item-list-row form-group">\n' +
            '        <div class="fit_img col-md-2 col-xs-2 col-sm-3">\n' +
            '            <img src="' + item_data['img_url'] + '" width="150px" height="150px">\n' +
            '        </div>\n' +
            '        <div class="col-md-8 col-xs-8 col-sm-7">\n' +
            '            <div class="row">' +
            '                <div class="col-sm-12 col-md-12 col-xs-12">' +
            '                   <div class="item-name">' + item_data['name'] + '</div>\n' +
            '                   <div class="item-hindi-name m5-bottom">' +  item_data['hindiname'] + '</div>\n' +
            '                   <div id="edit-quantity-'+ item_id +'" style="display: inline-block; font-size: 20px">' +  item_data['quantity'] +' </div>' +
            '                   <div style="display: inline-block; font-size: 20px">' + item_data['unit'] + '</div>\n' +
            '                 </div>' +
            '            </div>'+
            '        </div>\n' +
            '        <div class="col-md-1 col-sm-1 col-xs-1">' +
            '           <i class="fa fa-edit" style="font-size:30px" onclick="edit_item('+ item_data['id'] +',' +item_data['id'] + ')"></i>'+
            '        </div>'+
            '        <div class="col-md-1 col-sm-1 col-xs-1" style="cursor: pointer; z-index: 5" onclick="remove_item('+ item_data['id'] +',' + item_id + ')">' +
            '           <div class="icon-trash" style="float: left">\n' +
            '           <div class="trash-lid" style="background-color: blue"></div>\n' +
            '           <div class="trash-container" style="background-color: blue"></div>\n' +
            '           <div class="trash-line-1"></div>\n' +
            '           <div class="trash-line-2"></div>\n' +
            '           <div class="trash-line-3"></div>\n' +
            '        </div>'+
            '    </div>'
        }
        item_order_list.append(item_row_html);
        console.log(cookie_data[item_id]);
    }
}














/*
* <script>
        var item_count = 0
        var item_list_dict = {}
        function addItem() {
            var itemname= $('#itemname').val()
            var unit = $('#unit-dropdown').val()
            var quantity = $('#itemquantity').val()
            $('#itemList').append('<tr><td>'+itemname +'</td><td>'+quantity+unit+'</td></tr>')
            item_count = item_count + 1
            item_list_dict[item_count] = {'name':itemname, 'quantity': quantity, 'unit': unit}
            $('#itemname').val('')
            $('#itemquantity').val('')
            set_default_units()
        }




        $("document").ready(function() {
            set_default_units();
            item_snippet();
        });



        $(function() {
            $("#itemname").autocomplete({
                source: function (request, response) {
                     $.ajax({
                         url: "/adminpanel/getItems/",
                         type: "GET",
                         data: request,
                             dataType: "JSON",
                             minLength: 2,
                         success: function (data) {
                             if (Array.isArray(data) && data.length){
                                 response($.map(data, function (el) {
                                     return {
                                         label: el.name,
                                         value: el.unit
                                     };
                                }));

                             }else {
                                 set_default_units()
                             }

                         }
                     });
                },
                select: function (event, ui) {
                    this.value = ui.item.label;
                    unitautoselect(ui.item.value)
                    event.preventDefault();
                }
            });
            function unitautoselect(units) {
                units_list = units.split(',')
                select_unit_dropdown = $('#unit-dropdown')
                select_unit_dropdown.find('option').remove()
                for(i=0;i<units_list.length;i++){
                    select_unit_dropdown.append($('<option>', {value:units_list[i], text:units_list[i]}));
                }

            }
        });
    </script>
* */