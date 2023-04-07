function UpdateProductDetails() {
    debugger
    let productType = document.querySelector('#select-prodtype').value
    let tagList = []
    let list = []
    switch (productType) {
        case 'Fashion & Clothing':
            //let list = ['Shirts & T-Shirts','Trousers & Jeans','']
            //let dict = {Men : ['Shirts & T-Shirts','Trousers & Jeans','Suitings','Ethnic Wear','Wollens'], Women:['Sarees']}
            //let list = ['Product Name','Colour','Fabric','Sizes Available','Number of Pockets', , '']
            let list1 = ["Men's Wear", "Women's Wear", "Kid's Wear"]
            AddTags(list1, 'Clothing & Fashion')
            break;
        case 'Home Appliances':
            //let list = ['Television','Speakers','Air-Conditioners','Lightings','Washing-Machine','','Mixers & Grinders']
            //let list = ['Product Name','Colour','Body Material','Power Consumption','Number of Pockets', 'Adequate Seasons', '']
            let list2 = ['Air Conditioners', 'Washing Machine', 'Mixers & Grinders', 'Vaccum Cleaners', 'Room Heaters', 'Fans', 'Desert Coolers', 'Blenders', 'Others']
                //list2.concat(tagList)
            AddTags(list2, 'Home Appliances')
            break;
        case 'Fabrics & Household':
            break;
        case 'Gift Items':
            break;
        case 'Electrical tools & machinery':
            break;
        case 'Mobile Phones':
            break;
        case 'Mobile Phone Accessories':
            let list = ['Product Name', 'Colour', 'Material', 'Number of Ports', '', '', '']
            break;
        case 'Sports Items':
            break;
        case 'Footwear':
            break;
        default:
            break;
    }
}

function UpdateSubCategory() {
    debugger
    let productType = document.querySelector('#select_category').selectedOptions[0].value
    let sub_category_list = []
    switch (productType) {
        case 'Fashion & Clothing':
            sub_category_list = ["Men's Wear", "Women's Wear", "Boys Wear", "Girls Wear"]
            break;
        case 'Home Appliances':
            sub_category_list = ['Air Conditioners', 'Washing Machine', 'Refrigerators', 'Mixers & Grinders', 'Vaccum Cleaners', 'Room Heaters', 'Fans', 'Desert Coolers', 'Blenders', 'Others']
            break;
        case 'Kitchen Essentials':
            sub_category_list = ["Utensils", "Heating & Cooking", "Tools", "Crockery", "Cutlery"]
            break;
        case 'Home Decor & Handicrafts':
            sub_category_list = ["Curtains", "Bed Sheets", "Table Cover"]
            break;
        case 'Groceries':
            sub_category_list = ["Pulses", "Spices", "Grains", "Dry Fruits", "Packaged Food"]
            break;
        case 'Electronic Devices':
            sub_category_list = ["Television", "Speakers", "Lighting"]
            break;
        case 'Personal Care':
            sub_category_list = ["Oral Hygiene", "Hair Care", "Bath Essentials"]
            break;
        case 'Computers & Laptops':
            sub_category_list = ["Laptops", "Desktops"]
            break;
        case 'Mobile Phones':
            sub_category_list = ["Feature Phones", "Smart Phones", "Tablets"]
            break;

    }
    AppendCategory(sub_category_list, 'select_subcategory')
}

function AppendCategory(list, dropdown_id) {
    var options = []
    options.push(`<option value=''>Select Product SubCategory</option>`)
    for (item in list) {
        options.push(`<option value="${list[item]}">${list[item]}</option>`)
    }
    document.querySelector(`#${dropdown_id}`).innerHTML = options.join();
}

function UpdateProductIdentity() {
    debugger
    let productSubcategory = document.querySelector('#select_subcategory').selectedOptions[0].value
    let prod_identity_list = []
    switch (productSubcategory) {
        case "Men's Wear":
        case "Boys Wear":
            prod_identity_list = ['T-Shirts', 'Formal Shirts', 'Casual Shirts', 'Blazors', 'Jackets', 'Trousers', 'Chinos', 'Caps', 'Sports Shoes']
            break;
        case "Women's Wear":
        case "Girls Wear":
            prod_identity_list = ['T-Shirts', 'Formal Shirts', 'Casual Shirts', 'Blazors', 'Jackets', 'Trousers', 'Chinos', 'Caps', 'Sports Shoes']
            break;
        case 'Utensils':
            prod_identity_list = ['Stoves', 'Washing Machine', 'Refrigerators', 'Mixers & Grinders', 'Vaccum Cleaners', 'Room Heaters', 'Fans', 'Desert Coolers', 'Blenders', 'Others']
            break;
        case 'Kitchen Essentials':
            prod_identity_list = ["Utensils", "Heating & Cooking", "Tools", "Crockery", "Cutlery"]
            break;
        case 'Oral':
        case 'Oral Hygiene':
            prod_identity_list = ["Toothbrush", "Toothpaste", "Mouthwash"]
            break;
        case 'Hair Care':
        case 'Hair':
            prod_identity_list = ["Shampoo", "Conditioner", "Hair Oil", "Hair Cream"]
            break;
        case 'General Hygiene':
        case 'General':
            prod_identity_list = ["Hand Sanitizer", "Hand Wash", "Soaps"]
            break;


    }
    AppendCategory(prod_identity_list, 'select_identity')
}


const AddTags = (event, list, category) => {
    let div = document.createElement('div');
    debugger
    // var elem = document.getElementById('product_details_div');
    // if (elem.childElementCount > 0)
    //     elem.parentNode.removeChild(elem);

    div.className = 'fields';
    div.id = 'product_details'
    switch (category) {
        case 'Clothing & Fashion':
            let category_div = document.createElement('div');
            category_div.className = 'fields';
            category_div.id = 'product_details'
            var tag = ` <div><div class="required inline field"> <label class="formLabel">Select the type of Clothing</label>
            </div>
          `
            debugger
            list.forEach(function(item) {
                tag += `
                  <div class="ui radio checkbox" style="margin-top:10px;margin-right:25px;">
                    <input id="clothing_category" name="clothing_category" type="radio" class="subcategory" value="${item}" onclick="UpdateForm2()">
                    <label class="formLabel">${item}</label>
                    </div>                 
                 `
            });
            tag += `</div>`
            category_div.innerHTML = tag
            document.querySelector('#product_details_div').appendChild(category_div)
            break;
        case 'Home Appliances':

            var tag = ` <div><div class="required inline field"> <label class="formLabel">Select the type of Home Appliance</label>
            </div>
          `
            debugger
            list.forEach(function(item) {
                tag += `
                  <div class="ui radio checkbox" style="margin-top:10px;margin-right:25px;">
                    <input id="appliances_category" name="appliances_category" type="radio" class="subcategory" value="${item}" onclick="UpdateForm2()">
                    <label class="formLabel">${item}</label>
                    </div>                 
                 `
            });
            tag += `</div>`
            div.innerHTML = tag
            document.querySelector('#product_details_div').appendChild(div)

            break;

        case "Men's Wear":
        case "Kid's Wear":
        case "Women's Wear":
            var elem = document.getElementById('product_moredetails');
            if (elem != null)
                elem.parentNode.removeChild(elem);

            var elem2 = document.getElementById('sizes_available');
            if (elem2 != null)
                elem2.parentNode.removeChild(elem2);

            const clothing_type_div = document.createElement('div');
            div.className = ' fields';
            clothing_type_div.id = 'product_moredetails'
            var tag = `<div class="four wide required field"> <label class="formLabel">Select the type of ${category} </label>
            <span id="article_errorLabel" class="ui left pointing red basic label promptLabel">Mention Product Colors</span>                                            `
            tag += `
            <select id="select_garment" class="ui dropdown" onchange="UpdateForm3()" id="article">`

            list.forEach(function(items) {
                let type = Object.keys(items)[0]
                tag += `<label>${type}</label>`
                let i = 0
                for (var key in items) {
                    for (let j = 0; j < items[key].length; j++) {
                        tag += `<option id="" value="${items[key][i]}" onchange="UpdateForm3()">${items[key][i]}</option>`
                        i++
                    }
                }
            });
            tag += `</select>
          </div>
          </div>`
                //document.querySelector('#product_details_div').appendChild(tag)
                //document.querySelector('#product_details_form > div').appendChild(tag)

            let specs = ['Fabric Used', 'Number Of Pockets']
            specs.forEach(function(item) {
                switch (item) {
                    case 'Fabric Used':
                        tag += `
                <div id="add_fabric_div">
                <div class="fields">
                <div class="six wide field">
                <div class="required  field">                
                <label>${item}</label>  
                <span id="fabricerrorLabel" class="ui bottom pointing red basic label promptLabel">Grament Fabric is required</span>                                                                  
                </div>
                <input type="text" class="fabric">                
                </div>              
                <div class="four wide field">
                <div class="required field">
                <label>Percentage out of total</label> 
                <span id="fabricpercentageerrorLabel" class="ui bottom pointing red basic label promptLabel">Fabric % is required</span>                                                                  
                </div>   
                <input type="text" class="percentage" style="width:100px;">
                </div>
                <div class="two wide field">
                <label>Add Fabric</label>              
                <button class="small ui blue compact icon button" onclick="AddTags([],'AddFabric')">
                <i class="plus icon"></i>
                </button>
                </div>                             
               `
                        break;
                    case 'Number Of Pockets':
                        tag += `
                <div class="one wide field"></div>
                <div class="ten wide field">
                <div class="inline field">       
                <label>${item}</label>                                
                <input type="text" value="1" text="1" id="no_of_pockets" maxlength="2" placeholder="1" onkeypress="return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))" maxlength="10" style="width: 55px;">                          
           
               
                <button class="small ui blue compact icon button" onclick="plusminusValue('no_of_pockets','+')">
                <i class="plus icon"></i>
                </button>

                <button class="medium ui blue compact icon button" onclick="plusminusValue('no_of_pockets','-')">
                <i class="minus icon"></i>
                </button>
                </div>
                
                </div>
                </div>
                </div>`
                        break;
                }
            });
            //tag += `<button class="ui button successBtn">Save Product</button>`
            clothing_type_div.innerHTML = tag
            document.querySelector('#product_details_div2').appendChild(clothing_type_div)
            const div2 = document.createElement('div');
            div2.className = "four wide field"
            div2.id = "sizes_available"
            tag = `
          <div class="inline required field">
          <label>Sizes Available </label>
          <span id="colorserrorLabel" class="ui left pointing red basic label promptLabel">Select the sizes available</span>                                            
          </div>
          <select id="available_sizes" name="availableSizes"  multiple="" class="ui fluid dropdown">                         
              <option value="all"> All sizes available</option>    
              <option value="S">Small</option>
              <option value="M">Medium</option>
              <option value="L">Large</option>
              <option value="XL">XL</option>
              <option value="XXL">XXL</option>
              <option value="XXXL"> XXXL</option>                                                            
          </select>`
            div2.innerHTML = tag
            document.querySelector('#appearance_details').appendChild(div2)
            $('#available_sizes').dropdown()
            break;
        case 'Shirts':
            var elem = document.getElementById('garment_moredetails');
            if (elem != null)
                elem.parentNode.removeChild(elem);
            // const div = document.createElement('div');
            div.className = 'inline fields';
            div.id = 'garment_moredetails'
            var tag = ''
            list.forEach(function(item) {
                tag += `<div class="four wide field">
            <label>${item}</label>
            <div class="inline field">           
            <input type="text">
            </div>`
            });
            div.innerHTML = tag
            document.querySelector('#product_moredetails').appendChild(div)
            break;

        case 'AddFabric':
            let parentDiv = document.querySelector('#add_material_div')
            if (parentDiv.childElementCount >= 10) {
                break;
            }
            div.className = 'fields';
            div.id = ''
            var tag = ''
            tag += `           
            <div class="five wide field">
            <label>Fabric Used</label>                        
            <input type="text" class="fabric">                
            </div>  

            <div class="two wide field">
            <label>Percentage out of total</label>    
            <input type="text" class="percentage" style="width:100px;">
            </div>  
            <div class="four wide field">
            <label>Remove</label>
            <button class="small ui blue compact icon button" onclick="RemoveTags([],'Fabric',this)">
            <i class="minus icon"></i>
            </button>         
            `
            div.innerHTML = tag
            parentDiv.appendChild(div)
            break;
        case 'Air Conditioners':
            var elem = document.getElementById('appliance_moredetails');
            if (elem != null)
                elem.parentNode.removeChild(elem);
            // const div = document.createElement('div');
            div.className = 'inline fields';
            div.id = 'appliance_moredetails'
            var tag = ''
            list.forEach(function(item) {
                tag += `<div class="four wide field">
            <label>${item}</label>
            <div class="inline field">           
            <input type="text">
            </div>`
            });
            div.innerHTML = tag
            document.querySelector('#product_moredetails').appendChild(div)
            break;

        case 'Others':
            var tag = ''
            tag += `<div class="inline field"><div class="four wide field">
            <input type="text"/>
            </div></div>`
            div.innerHTML = tag
            document.querySelector('#product_moredetails').appendChild(div)
            break;

    }
}

const UpdateForm2 = () => {
    debugger
    //var subcategories = document.getElementsByClassName('subcategory').value
    let clothing_categories = document.getElementsByName('clothing_category')
    for (let i = 0; i < clothing_categories.length; i++) {
        if (clothing_categories[i].checked == true) {
            var clothing_category = clothing_categories[i].value
        }
    }
    let list = []
    switch (clothing_category) {
        case "Men's Wear":
            list = [
                { Shirts: ['Formal Shirts', 'Casual Shirts', 'Party Wear Shirts'] },
                { Trousers: ["Formal Trousers", "Chinos", "Jeans"] },
                { Ethnic: ["Kurta", 'Pyjama', 'Sadri', 'Kurta-Pyjama', 'Sherwani', 'Others'] },
            ]
            AddTags(list, "Men's Wear")
            break;
        case "Women's Wear":
            list = [
                { Ethnic: ['Sarees', 'Kurtas', 'Plazo', "Shawls & Dupattas"] }, { Accessories: ["Watches", "Bangles"] },
                { Casual: ['Jeans', 'Tops', 'Shirts', 'T-Shirts', 'leggings', 'Blazers', 'Jackets', 'Coats', 'Others'] },
            ]
            AddTags(list, "Women's Wear")
            break;

        case "Kid's Wear":
            list = [
                { GirlsCasual: ['T-Shirts', 'Tops', 'Dresses', 'Lowers'] },
                { BoysCasual: ['Shirts', 'Others'] },
            ]
            AddTags(list, "Kid's Wear")
            break;
        case "Blenders":
        case "Mixers & Grinders":
            break;
        case "Air Conditioners":
            list = [
                { Type: ['Window AC', 'Split AC', 'Central AC', 'Portable AC', 'Others'] },
                { Capacity: ['0.8 ton', '1.0 ton', '1.5 ton', '2.0 ton', 'Others'] },
                { EnergyRating: ['1', '2', '3', '4', '5'] },
                { EnergyConsumption: [] }
            ]
            AddTags(list, "Air Conditioners")
            break;
        case "Washing Machine":
            break;
        case "Fans":
        case "Coolers":
            break;
    }
}

const UpdateForm3 = () => {
    let selected_garment = document.getElementById('select_garment').value
    let list = []
    switch (selected_garment) {
        case "Shirts":
            list = ['Fabric', 'No of Pockets']
                //AddTags(list,'Shirts')
            break;
        case "Trousers":

            break;
        case 'Others':
            AddTags([], 'Others')
            break;
    }
    console.log('checked')
}

const RemoveTags = (list, category, elem) => {
    debugger
    switch (category) {
        case 'Fabric':
            document.querySelector('#add_material_div').removeChild(elem.parentNode.parentNode);
            break;
        case '':
            break;
    }
}

const plusminusValue = (elem, operation) => {
    let num = document.getElementById(elem).value
    debugger
    switch (operation) {
        case '+':
            if (elem.toString().includes("pockets") && parseInt(num) >= 99)
                break;
            num = parseInt(num) + 1
            document.getElementById(elem).value = num
            break;

        case '-':
            if (parseInt(num) <= 0)
                break;
            num = parseInt(num) - 1
            document.getElementById(elem).value = num
            break;
    }
}

function isNumberKey(txt, evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode == 46) {
        //Check if the text already contains the . character
        if (txt.value.indexOf('.') === -1) {
            return true;
        } else {
            return false;
        }
    } else {
        if (charCode > 31 &&
            (charCode < 48 || charCode > 57))
            return false;
    }
    return true;
}

function SaveProduct() {

    var dict = {};
    category = document.querySelector('#select_category').value
    category = "Fashion & Clothing"
    switch (category) {
        case 'Fashion & Clothing':
            var inputs = document.getElementById('product_details_form').querySelectorAll('input')
                // for (let i = 0; i < inputs.length; i++) {
                //let element_id = inputs[i].id
            let prod = ['name', 'image', 'image_rear', '', 'img_path', 'brand_name', 'price', 'store', 'category', 'garment_details']
            let prod_details = ['specific_name', 'colors', 'material', 'is_discounted', 'discount', 'description', 'subcategory', 'neck_design', 'design_pattern', 'sizes_available']
            let required_fields = ['primary_color', 'material', 'description', 'quantity', 'origin_country', 'manufacturer_name']
            let material = ''
            let percent = ''

            for (item in required_fields) {
                if (required_fields[item] == 'material') {
                    // if (document.getElementById(required_fields[item]).value == '') {

                    // }
                    let composition = document.querySelector('#add_material_div').children
                    for (let i = 0; i < composition.length; i++) {
                        //material = document.querySelector('#add_material_div').children[i].querySelector('.material').value
                        //percent = document.querySelector('#add_material_div').children[i].querySelector('.percentage').value
                        material = composition[i].querySelector('.material')
                        if (material == null)
                            material = composition[i].querySelector('.fabric').value
                        else
                            material = composition[i].querySelector('.material').value
                        percent = composition[i].querySelector('.percentage')
                        if (percent != null)
                            percent = composition[i].querySelector('.percentage').value

                        dict['material'] += material + ':' + percent + ','
                    }
                    continue
                }
                dict[required_fields[item]] = document.getElementById(required_fields[item]).value
            }
            //dict['product_id'] = '226001754380733'
            dict['product_id'] = document.querySelector('#product_id').value
            dict['article'] = ''
            getID(postJSONAuth, 'api/product/details/add/', JSON.stringify(dict))
                // }
            break;
        case 'Home Appliances':
            break;
    }
    let jsonBody = JSON.stringify(dict)
        //getID(postJSONAuth, 'product/add/', jsonBody)
}

function OpenNextStep(step) {
    debugger;
    //let stepid = step + '_step';
    let tabid = step + '_tab';
    let disabled_steps = document.getElementsByClassName('disabled step')
    disabled_steps[0].classList.add('active')
    disabled_steps[0].classList.remove('disabled')
        // disabled_steps[0].classList.add('active')
    let active_steps = document.getElementsByClassName('active step')
    active_steps[0].classList.add('disabled')
    active_steps[0].classList.remove('active')

    //active_steps[0].classList.add('disabled')
    // let link = tabName + 'Link'
    // document.getElementById(link).classList.add('active')
    var a = document.querySelector('.ui.tab.active')
    if (a !== null)
        document.querySelector('.ui.tab.active').classList.remove('active');

    document.querySelector(`[id=${CSS.escape(tabid)}]`).classList.add('active');
}

function ProceedStep2(value) {
    //UpdateForm1()
    if (!ValidateProductInfo(value)) {
        DisplayMessage('Required Fields Missing', 'Complete the form below to proceed', false)

    }
}

function process(id) {
    debugger
    const file = document.querySelector(`#${id}`).files[0];
    if (file.type == "image/jpeg" || file.type == "image/jpg" || file.type == "image/png") {
        if (!file) return;
        const reader = new FileReader();
        reader.readAsDataURL(file);
        let list = ["small_thumbnail", "thumbnail", "large"]
        reader.onload = function(event) {
            const imgElement = document.createElement("img");
            imgElement.src = event.target.result;
            // document.querySelector("#input").src = event.target.result;
            imgElement.onload = function(e) {
                let errorMsg = ''
                    //document.querySelector('#resolution').innerHTML = e.target.width+'&times'+e.target.height; 
                if (e.target.width < 600) {

                    errorMsg = '<li>Image Width should not be less than 600 px</li>'
                }
                if (e.target.height < 900) {
                    errorMsg += '<li>Image Height should not be less than 900 px</li>'
                }
                if (errorMsg != '') {
                    document.querySelector(`#${id}_errorLabel`).classList.remove('hidden')
                    document.querySelector(`#${id}_errorLabel`).innerHTML = errorMsg
                    DisplayMessage('Invalid Image File', errorMsg, false)
                    document.querySelector(`#${id}`).value = null
                    return
                } else {
                    document.querySelector(`#${id}_errorLabel`).classList.add('hidden')
                    document.querySelector(`#${id}_errorLabel`).innerHTML = errorMsg
                    document.querySelector('.showMessage').style.display = 'none'
                }
                let MAX_HEIGHT
                let srcEncoded
                let given_height = e.target.height
                let given_width = e.target.width
                for (item in list) {
                    switch (list[item]) {
                        case "thumbnail":
                            MAX_HEIGHT = 300
                            debugger
                            srcEncoded = ResizeImage(e, MAX_HEIGHT, true)
                            document.querySelector(`#output_${id}`).src = srcEncoded;
                            document.getElementById('image_handler').value = id

                            var blobBin = atob(srcEncoded.split(',')[1]);
                            var array = [];
                            for (var i = 0; i < blobBin.length; i++) {
                                array.push(blobBin.charCodeAt(i));
                            }
                            var file = new Blob([new Uint8Array(array)], { type: 'image/png' });

                            document.querySelector('#product_image_front_thumb').setAttribute('value', file)
                            break;
                        case "large":
                            MAX_HEIGHT = 500
                            srcEncoded = ResizeImage(e, MAX_HEIGHT)
                            document.querySelector('#modal_preview').src = srcEncoded;
                            break;
                    }
                }
                // document.querySelector("a.ui.image").classList.remove('hidden')
                //document.querySelector('#modal_preview').src = srcEncoded;
                $('.ui.modal').modal('show');
                document.querySelector('#preview_modal').classList.add('active');
            };
        };
    } else {
        DisplayMessage('Invalid Image File', 'Allowed types are JPG/JPEG Or PNG', false)
        return false
    }
}

function ResizeImage(event, MAX_HEIGHT, is_thumbnail = false) {
    const canvas = document.createElement("canvas");
    //const MAX_HEIGHT = 200;
    let given_width = event.target.width
    let given_height = event.target.height
    if (is_thumbnail) {
        canvas.width = 300
        canvas.height = 350
    } else {
        if (given_height > 350 || given_width > 300) {
            const scaleSize = MAX_HEIGHT / given_height;
            canvas.width = given_width * scaleSize;
            canvas.height = MAX_HEIGHT;
        } else {
            canvas.width = given_width
            canvas.height = given_height
        }
    }
    const ctx = canvas.getContext("2d");
    ctx.drawImage(event.target, 0, 0, canvas.width, canvas.height);
    const srcEncoded = ctx.canvas.toDataURL(event.target, "image/jpeg");
    return srcEncoded
        // you can send srcEncoded to the server
}

function DiscardImage() {
    debugger
    let tag_id = document.getElementById('image_handler').value
    document.getElementById(tag_id).value = null
    document.getElementById('output_' + tag_id).src = null
}

function ValidateImg() {
    debugger
    const file = document.querySelector("#product_image").files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = function(event) {
        const imgElement = document.createElement("img");
        imgElement.src = event.target.result;
        imgElement.onload = function(e) {
            if (e.target.width < 1100 || e.target.width > 2500) {
                console.log('invalid')
            }
            if (e.target.height < 1100 || e.target.height > 2500) {
                console.log('Invalid')
            }
        };
    };
}

function ValidateProductInfo(val) {
    dict = {}
    let requiredFields = ['product_name', 'select_category', 'select_subcategory', 'select_identity', 'product_price', 'product_image_front', 'product_image_rear', 'product_image_side', 'select_store']
    let count = 0
    var formdata = new FormData();
    let selectedStores = []
    let errorLabel = ''
    let productInfo = ''
    let imageName = ''
    let rearImageName = ''
    let side1ImageName = ''
    let img = ''
    for (let field in requiredFields) {
        errorLabel = requiredFields[field] + '_errorLabel'
        if (requiredFields[field] == 'select_store') {
            stores = document.getElementsByName('select_store');
            let store_count = stores.length
            for (let i = 0; i < store_count; i++) {
                if (stores[i].checked) {
                    selectedStores.push(stores[i].value)
                    store_count--;
                }
            }
            if (stores.length > 1) {
                if (store_count == stores.length) {
                    document.getElementById(errorLabel).classList.remove('hidden')
                        //document.getElementById(errorLabel).innerHTML = 'This Field is Required'
                    count++
                    continue
                } else {
                    formdata.append("store_id", selectedStores)
                    document.getElementById(errorLabel).classList.add('hidden')
                }
                continue
            } else {
                store = document.getElementsByName('select_store');
                selectedStores.push(store[0].value)
                formdata.append("store_id", selectedStores)
                continue;
            }
        }
        productInfo = document.getElementById(requiredFields[field]).value
        if (productInfo != null && productInfo !== "") {
            document.getElementById(errorLabel).classList.add('hidden')
            dict[requiredFields[field]] = document.getElementById(requiredFields[field]).value

            switch (requiredFields[field]) {
                case 'product_image_front':
                    img = document.getElementById(requiredFields[field]).value
                    path = img.split('\\')
                    imageName = path[path.length - 1]
                        //imageName = imageName.split('.')
                        //imageName = imageName[imageName.length - 2]
                    formdata.append("image", document.getElementById('product_image_front').files[0], document.getElementById('product_image_front').files[0].name);
                    continue;
                case 'product_image_rear':
                    img = document.getElementById(requiredFields[field]).value
                    path = img.split('\\')
                    rearImageName = path[path.length - 1]
                        //rearImageName = imageName.split('.')
                        //rearImageName = imageName[imageName.length - 2]
                    if (imageName == rearImageName) {
                        document.getElementById(errorLabel).classList.remove('hidden')
                        document.getElementById(errorLabel).innerHTML = 'Rear Image is same as Front Image'
                        OpenMessageBar('Upload different rear image.It is same as front image')
                        count++
                        return false
                    }
                    formdata.append("image_rear", document.getElementById('product_image_rear').files[0], document.getElementById('product_image_rear').files[0].name);
                    continue;
                case 'product_image_side':
                    img = document.getElementById(requiredFields[field]).value
                    path = img.split('\\')
                    side1ImageName = path[path.length - 1]
                        //side1ImageName = imageName.split('.')
                        //side1ImageName = imageName[imageName.length - 2]
                    if (imageName == side1ImageName) {
                        document.getElementById(errorLabel).classList.remove('hidden')
                        document.getElementById(errorLabel).innerHTML = 'Side Image is same as Front Image'
                        OpenMessageBar('Upload different side image.It is same as front image')
                        count++
                        return false
                    }
                    if (rearImageName == side1ImageName) {
                        document.getElementById(errorLabel).classList.remove('hidden')
                        document.getElementById(errorLabel).innerHTML = 'Side Image is same as Rear Image'
                        OpenMessageBar('Upload different side image.It is same as rear image')
                        count++
                        return false
                    }

                    formdata.append("image_side1", document.getElementById('product_image_side').files[0], document.getElementById('product_image_side').files[0].name);
                    continue;
                case 'select_store':
                    store = document.getElementsByName('select_store');
                    selectedStores.push(store.value)
                    formdata.append("store_id", selectedStores)
                    continue;
                default:
                    formdata.append(requiredFields[field], document.getElementById(requiredFields[field]).value);
                    continue;

            }
            // if (requiredFields[field] == 'product_image_front') {
            //     formdata.append("image", document.getElementById('product_image_front').files[0], document.getElementById('product_image_front').files[0].name);
            // } else if (requiredFields[field] == 'product_image_rear') {
            //     formdata.append("image_rear", document.getElementById('product_image_rear').files[0], document.getElementById('product_image_rear').files[0].name);
            // } else if (requiredFields[field] == 'product_image_side') {
            //     formdata.append("image_side1", document.getElementById('product_image_side').files[0], document.getElementById('product_image_side').files[0].name);
            // } else
            //     formdata.append(requiredFields[field], document.getElementById(requiredFields[field]).value);
            // formdata.append("brand_name", ".Raymonds\n\n499\n\n\n \"Duke\"");
            // formdata.append("product_price", "899");

            continue
        } else {
            document.getElementById(errorLabel).classList.remove('hidden')
            document.getElementById(errorLabel).innerHTML = 'This Field is Required'
            count++
        }
    }
    if (count == 0) {
        let jsonBody = JSON.stringify(dict)
        formdata.append("brand_name", document.getElementById('brand_name').value)
        if (val == "")
            getID(AddProduct, 'api/product/add/', formdata)
        else
            getID(AddProduct, `api/product/add/${val}/`, formdata)
        return true
    } else {
        return false
    }
}

function ValidateSaveAddress() {
    let requiredList = ['addressee_name', 'address_line1', 'address_line2', 'pincode', 'city', 'state']
    let itemValue = ''
    let dict = {}
    for (item in requiredList) {
        if (document.querySelector(`#${requiredList[item]}`) != null) {
            itemValue = document.querySelector(`#${requiredList[item]}`).value
            dict[requiredList[item]] = itemValue
        }
        if (itemValue == null || itemValue == '') {
            DisplayMessage('', 'Required Fields Missing', false)
            OpenMessageBar('Could not save.Please Enter the required fields')
            return null
        }
    }

    return dict;
}

function SetAddressInfo(val) {
    debugger
    let dict = {}
    if (val == '') {
        // getId(postJSONAuth, 'url', jsonBody)
        document.getElementById('is_self_pickup').value = '1'
    } else {
        dict = ValidateSaveAddress()
        if (dict != null) {
            getID(postJSONAuth, '/api/address/save', JSON.stringify(dict))
        }
    }
}
debugger
var discountCheckbox = document.querySelectorAll("input[name=is_discounted]");
if (discountCheckbox != null || discountCheckbox != undefined) {
    for (let i = 0; i < 2; i++) {
        discountCheckbox[i].addEventListener('click', function() {
            if (discountCheckbox[i].value == 1) {
                document.querySelector('#discount_div').classList.remove('hidden')
            } else {
                document.querySelector('#discount_div').classList.add('hidden')
            }
        });
    }
}