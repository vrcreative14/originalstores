function checkGSTIN(gstin) {
    var regex = '\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}'
    if (regex.test(String(gstin))) {
        return true
    } else
        return false
}

function CheckGSTINEntry(value) {
    debugger
    if (value == "1")
        document.querySelector('.gstinEntry').classList.remove('hidden')
    else
        document.querySelector('.gstinEntry').classList.add('hidden')
}


const SaveSellerInfo = () => {
    let status = ValidateSellerInfo()
    if (status == false)
        return
    const list = ["firstname", "middlename", "lastname", "primaryemail", "primarymobile", "secondaryemail", "secondarymobile"]
    debugger
    //var user = getCookie('user')
    var dict = {};
    dict[""]
    for (let i = 0; i < list.length; i++) {
        dict[list[i]] = document.getElementById(list[i]).value
    }
    jsonBody = JSON.stringify(dict)
    getID(postJSONAuth, "/api/seller/register/", jsonBody);
    //document.querySelector('.showMessage').style.display = 'block'
}


const SaveStoreInfo = () => {

    let status = ValidateStoreInfo()
    if (status == false)
        return
    const list = ["shopname", "state", "city", "pincode", "latitude", "longitude", "productcategory", "storecategory", "address", "landmark", "gstin"]
    debugger
    var dict = {};
    var product_category = []
    var store_category = []
    for (let i = 0; i < list.length; i++) {
        //  let a = document.getElementById(list[i])
        //  array.push(a.value)
        if (list[i] == "productcategory" || list[i] == "storecategory") {
            let count = document.getElementById(list[i]).options.length
            for (let j = 0; j < count; j++) {
                if (document.getElementById(list[i]).options[j].selected) {
                    if (list[i] == "productcategory")
                        product_category.push(document.getElementById(list[i]).options[j].value)
                    else
                        store_category.push(document.getElementById(list[i]).options[j].value)
                }
            }
            dict[list[i]] = list[i] == "productcategory" ? product_category : store_category
            continue
        }
        dict[list[i]] = document.getElementById(list[i]).value
    }
    if (document.querySelector('input[name="is_gst_registered"]:checked').value == '1')
        dict["is_gst_registered"] = true
    else
        dict["is_gst_registered"] = false

    jsonBody = JSON.stringify(dict)
    debugger
    getID(postJSONAuth, "/api/store/create/", jsonBody);
}


const SaveStoreDetails = () => {
    debugger
    let status = ValidateStoreInfo()
    if (status == false)
        return

    const list = ["shopname", "state", "city", "pincode", "latitude", "longitude", "productcategory", "storecategory", "storeimage", "address", "is_gst_registered", "gstin"]
    debugger
    var user = getCookie('user')
    var seller = getCookie('seller')
    var dict = {
        "user": user,
        "seller": seller
    };
    dict[""]
    for (let i = 0; i < list.length; i++) {
        //  let a = document.getElementById(list[i])
        //  array.push(a.value)    
        dict[list[i]] = document.getElementById(list[i]).value
    }
    jsonBody = JSON.stringify(dict)
    postJSON('/api/store/details/', jsonBody)
}

function FetchFillLocation(event) {
    document.getElementById('currentEvent').value = event.target.id
    var locatebutton = document.querySelector('#detect-location')
    if (locatebutton != null)
        locatebutton.classList.add('loading')
    getLocation()
    let location = document.getElementById('saveLocation').value
    if (location != "")
        FillAddress(location)
        //DisplayMessage('', 'Not able to detect location at this time' ,false)
}

function FillAddress(data) {
    let address = data["houseNumber"] + " " + data["street"] + " " + data["subLocality"]
    if (document.getElementById('address') == null)
        return
    document.getElementById('address').value = address
    document.getElementById('city').value = data["city"]
    document.getElementById('pincode').value = data["pincode"]
    document.getElementById('state').value = data["state"]
    document.getElementById('landmark').value = data["poi"]

    var locatebutton = document.querySelector('#detect-location')
    if (locatebutton != null)
        locatebutton.classList.remove('loading')
    document.querySelector('#locationmessage').style.display = 'inline'
}

function CheckProductCategory() {
    var category = document.getElementById('store-category').value
    if (category == 'Others') {
        document.querySelector('#describe-category').classList.remove('hidden')
    }

}

const ValidateStoreInfo = () => {
    const list = ["shopname", "state", "city", "pincode", "productcategory", "storecategory", "isgstregistered", "gstin", 'addressLine1']
    var listDup = ["shopname", "state", "city", "pincode", "productcategory", "storecategory", "isgstregistered", "gstin"]
    const optionalList = ['address', 'latitude', 'longitude', 'storeimage']
    var index = 0
    for (let i = 0; i < list.length; i++) {
        let item = list[i]
        if (item == 'isgstregistered') {
            if (document.querySelector('input[name="is_gst_registered"]:checked') == null) {
                document.getElementById('isgstregistered_errorLabel').style.display = 'inline-block'
                continue
            }
            listDup.shift()
            document.getElementById('isgstregistered_errorLabel').style.display = 'none'
            continue
        }
        // if (item == 'is_store_existing') {
        //     if (document.querySelector('input[name="is_store_existing"]:checked') == null) {
        //         document.getElementById('is_store_existing_errorLabel').style.display = 'inline-block'
        //         continue
        //     }
        //     listDup.shift()
        //     document.getElementById('is_store_existing_errorLabel').style.display = 'none'
        //     continue
        // }

        let itemvalue = document.getElementById(item).value
        let itemid = item + "_errorLabel"
        if (itemvalue == undefined || itemvalue == "") {
            if (item == 'gstin') {
                let isGST = document.querySelector('input[name="isgstregistered"]:checked')
                switch (isGST) {
                    case "1":
                        document.getElementById('gstin_errorLabel').style.display = 'inline-block'
                        document.getElementById(itemid).style.display = 'inline-block'
                        break;
                    case "0":
                        document.getElementById('gstin_errorLabel').style.display = 'none'
                        listDup.shift();
                        break;
                    default:
                        document.getElementById('gstin_errorLabel').style.display = 'none'
                        listDup.shift();
                        break;
                }
            }

            if (item == 'addressLine1') {
                if (document.querySelector('input[name="is_store_existing"]:checked') != null) {
                    if (document.querySelector('input[name="is_store_existing"]:checked').value == 1) {
                        document.getElementById('addressLine1_errorLabel').style.display = 'inline-block'
                        continue
                    }
                } else {
                    listDup.shift()
                    continue
                }
            }
            document.getElementById(itemid).style.display = 'inline-block'
        } else {
            listDup.shift()
            document.getElementById(itemid).style.display = 'none'
        }
    }

    if (listDup.length == 0) {
        optionalList.forEach(function(optionalItem) {
            switch (optionalItem) {
                case "latitude" || "longitude":
                    break;

                case "storeimage":

                    break;

            }

        });
        return true;
    } else {
        debugger
        OpenMessageBar('Could not save.Please Enter the required fields')
        return false;
    }
}

const ValidateSaveSellerInfo = () => {
    const list = ["firstname", "lastname", "primaryemail", "primarymobile", "is_physical_store", "is_business_registered"]
    const optional = ["secondaryemail", "secondarymobile"]
    let count = 0
    var dict = {};
    // let itemvalue = ""
    let itemid = ""

    for (let i = 0; i < list.length; i++) {
        let item = list[i]
            // if (itemvalue == undefined || itemvalue == "") {
        switch (item) {
            case "firstname":
            case "lastname":
                itemvalue = document.getElementById(item).value
                itemid = "name_errorLabel"
                if (document.getElementById(item).value == "" || document.getElementById(item).value == undefined) {
                    document.getElementById(itemid).style.display = 'inline-block'
                    count = count + 1
                } else {
                    dict[item] = itemvalue
                    document.getElementById(itemid).style.display = 'none'
                }
                break;
                // case "is_physical_store":
                //     if (document.querySelector('input[name="is_physical_store"]:checked').value == "1")
                //         dict["is_physical_store"] = true
                //     else
                //         dict["is_physical_store"] = false
                //     break;
                // case "is_business_registered":
                //     if (document.querySelector('input[name="is_business_registered"]:checked').value == "1") {
                //         dict["is_business_registered"] = true
                //         dict["business_name"] = document.querySelector('#business_name').value
                //     } else {
                //         dict["is_business_registered"] = false
                //         dict["business_name"] = ""
                //     }

                //     break;
            case 'is_physical_store':
                itemvalue = document.querySelector('input[name="is_physical_store"]:checked')
                if (itemvalue == null) {
                    document.getElementById('is_physical_store_errorLabel').style.display = 'inline-block'
                    count = count + 1
                    break
                } else if (itemvalue.value == 1) {
                    dict["is_physical_store"] = true
                        //dict["business_name"] = document.querySelector('#business_name').value
                } else {
                    dict["is_physical_store"] = false
                        //dict["business_name"] = ""
                }
                document.getElementById('is_physical_store_errorLabel').style.display = 'none'
                break;
            case 'is_business_registered':
                itemvalue = document.querySelector('input[name="is_business_registered"]:checked')
                if (itemvalue == null) {
                    document.getElementById('is_business_registered_errorLabel').style.display = 'inline-block'
                    count = count + 1
                    break
                } else if (itemvalue.value == 1) {
                    let busName = document.querySelector('#business_name').value
                    if (busName == "") {
                        document.querySelector('#business_name_errorLabel').style.display = 'inline-block'
                        count++
                        break
                    }
                    dict["is_business_registered"] = true
                    dict["business_name"] = document.querySelector('#business_name').value
                } else {
                    dict["is_business_registered"] = false
                    dict["business_name"] = ""
                }
                document.getElementById('is_business_registered_errorLabel').style.display = 'none'
                document.querySelector('#business_name_errorLabel').style.display = 'none'
                break;

            default:
                itemvalue = document.getElementById(item).value
                if (document.getElementById(item).value == "" || document.getElementById(item).value == undefined) {
                    itemid = item + "_errorLabel"
                    document.getElementById(itemid).style.display = 'inline-block'
                    count = count + 1
                } else {
                    dict[item] = itemvalue
                    document.getElementById(itemid).style.display = 'none'
                }
                break;
        }

        continue
        // } else {
        //     switch (item) {
        //         case "firstname":
        //         case "lastname":
        //             itemid = "name_errorLabel"
        //             document.getElementById(itemid).style.display = 'inline-block'
        //             count = count + 1
        //             break;
        //         case "is_physical_store":
        //             if (document.querySelector('input[name="is_physical_store"]:checked').value == "1")
        //                 dict["is_physical_store"] = true
        //             else
        //                 dict["is_physical_store"] = false
        //             break;
        //         case "is_business_registered":
        //             if (document.querySelector('input[name="is_business_registered"]:checked').value == "1") {
        //                 dict["is_business_registered"] = true
        //                 dict["business_name"] = document.querySelector('#business_name').value
        //             } else {
        //                 dict["is_business_registered"] = false
        //                 dict["business_name"] = ""
        //             }
        //             break;
        //         default:
        //             itemid = item + "_errorLabel"
        //             document.getElementById(itemid).style.display = 'inline-block'
        //             count = count + 1
        //             break;
        //     }
    }
    if (count === 0) {
        jsonBody = JSON.stringify(dict)
        getID(postJSONAuth, "/api/seller/register/", jsonBody);
    } else {
        OpenMessageBar('Could not save.Please Enter the required fields')
        return false;
    }
}


function CheckStoreAddress(val) {
    debugger
    if (val == 1)
        document.getElementById('addressLine1').classList.add('required')
    else
        document.getElementById('addressLine1').classList.remove('required')
}