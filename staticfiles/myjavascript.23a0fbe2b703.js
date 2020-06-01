function  item_snippet() {
    var term = $('#itemname').val();
    var category_filter = $('#category-select').val();
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

function set_default_units(units_list){
    select_unit_dropdown = $('#unit-dropdown')
    for(i=0;i<units_list.length;i++){
        select_unit_dropdown.append($('<option>', {value:units_list[i], text:units_list[i]}));
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



        $("document").ready(function() {
            set_default_units();
            item_snippet();
        });

        function gonext(){
            document.cookie = JSON.stringify(item_list_dict);
            document.getElementById("user-detail").style.display = "block";
            document.getElementById("item-detail").style.display = "none";
            $('#item-list').val(document.cookie);
        }

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