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
    document.getElementById(select_id).selectedIndex = clicked_unit.options.selectedIndex;
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
    item_dict['hindiname'] = $('#hindiname-'+item_id).val();
    item_dict['img_url'] = $('#itemimg-'+item_id).val();

    var quantity = $('#quantity-'+item_id).val();
    item_dict['quantity'] = quantity
    if (quantity == "") {
        alert("Please enter Quantity.");
        return false;
    }
    item_dict['unit'] = $('#unit-'+item_id).val();

    var cookies_data = JSON.parse(document.cookie.split(';')[0]);
    cookies_data[item_id] = item_dict;
    document.cookie = JSON.stringify(cookies_data);

    var check = document.getElementById('item-check-'+ item_id);
    check.classList.remove('hidden');

    var add_btn = document.getElementById('item-add-update-'+item_id);
    add_btn.innerText = 'Update';

}

function myorder() {
    var item_row_html;
    var item_order_list = $('#item_order_list');
    var cookie_data = JSON.parse(document.cookie.split(';')[0]);
    item_order_list.empty();
    for(item_id in cookie_data){
        item_data = cookie_data[item_id];

        item_row_html = '<div class="row item-list-row">\n' +
            '        <div class="fit_img col-md-3 col-xs-3 col-sm-3">\n' +
            '            <img src="' + item_data['img_url'] + '" width="50px" height="50px">\n' +
            '        </div>\n' +
            '        <div class="col-md-9 col-xs-9 col-sm-9">\n' +
            '            <div class="">' + item_data['name'] + '</div>\n' +
            '            <div>' +  item_data['hindiname'] + '</div>\n' +
            '            <div>' +  item_data['quantity'] + item_data['unit'] + '</div>\n' +
            '            <div>close</div>\n' +
            '        </div>\n' +
            '    </div>'
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