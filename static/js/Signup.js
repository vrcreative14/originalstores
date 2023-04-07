var isFormValid = true


function checkPassword() {
    debugger;
    let password = document.getElementById('password');
    let regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/
    if (regex.test(String(password))) {
        //showMessage('mobileno', false)
        isFormValid = true;
        return true;
    } else {
        //showMessage('mobileno', true)
        isFormValid = false;
        return false
    }
    if (password.value != '') {
        document.getElementById('passwordLabel').style.display = 'none';
        document.getElementById('password').disabled = false;
    } else {
        document.getElementById('passwordLabel').style.display = 'inline';
    }
}

const Register = () => {
    validateSignupForm();
    if (!isFormValid)
        return false;
    var name = document.getElementById('name').value
    var password = document.getElementById('password').value
    var email = document.getElementById('emailInput').value
    var mobile_no = document.getElementById('mobile_no').value
    var otp = document.getElementsByClassName('verifyOTP')


    if (email == undefined || email == '')
        email = null



    var jsonbody = JSON.stringify({
        "name": name,
        "email": email,
        "pw": password,
        "mobile": mobile_no,
        "otp": otpvalue
    })
    postJSON('/api/register/', jsonbody)
}


// const postJSON = (url, jsonBody) => {

//     fetch(url,{ 
//         method : 'POST',
//         headers: {
//         'Accept': "application/json, text/plain, */*",
//         'Content-Type': 'application/json',     
//         'Accept-Encoding':'gzip,deflate,br',      
//         },
//         body: jsonBody
//     }
//   )
//         .then(response => {
//             if(!response.ok){
//             console.log(response)
//             response.text().then(text => {
//                 DisplayMessage('','Some Error Occurred. Please try again after some time.', false)
//             })
//             // if(response.status == 400 || response.statusText == 'Bad Request'){
//             //     let msg = 'Email Id or Phone Number already exists'
//             //     document.getElementById('msg-heading').innerText = msg;            
//             //     document.getElementById('msg-heading').className = 'errormsg';
//             //     document.getElementById('msg-heading').style.display = 'block';
//             // }
//             //throw Error(response.statusText)
//             }
//             else{
//                  return response.json()
//                 // console.log(response)
//                 // let msg = 'You have been Registered Successfully'
//                 // OpenMobileVerification()
//                 //  document.getElementById('modalmsg').innerText = msg;            
//                 //  document.getElementById('sellermodal').style.display = 'block';
//                 //  document.getElementById('msg-heading').style.display = 'none';
//                 //  if(mobile_no == ''){
//                 //  document.getElementById('phoneVerification').display='none';
//                 //  document.getElementById('phoneVerification').display='none';
//                 //  }
//             }       
//         })
//         .then(data => {
//             console.log(data)
//             ShowResult(data);
//         })
//         .catch(error => console.log(error))
// }

// const ShowResult = (data) => {
//     var detail = data.detail
//         switch(data.detail){
//             case 'An SMS with an OTP(One Time Password) has been sent <br/> to your Mobile number':                
//                 OpenMobileVerification();
//                 DisplayMessage('',data.detail,data.status)
//                 document.querySelector('#mobileField').classList.add('hidden')
//                 document.querySelector('#signupBtn').classList.add('hidden')
//                // OpenSignupForm()
//                 break;

//             case 'Either phone or otp was not received':
//                 DisplayMessage('Required Data missing',data.detail,data.status)
//                 break;

//             case 'User registered successfully':
//                 //DisplayMessage('Required Data missing',data.detail,data.status)
//                 document.getElementById('otpVerificationDiv').style.display = 'none';    
//                 $('.ui.modal').modal('show');
//                 setTimeout(() => {  window.open('/','_self') }, 3000);

//             case 'OTP matched':
//                // document.getElementById('otpmatchedIcon').style.display = 'inline';

//                 DisplayMessage('','Excellent! OTP Matched',data.status)
//                 OpenSignupForm()
//                 document.querySelector('#signupBtn').classList.remove('hidden')
//                 document.querySelector('#changemobileBtn').classList.remove('hidden')
//                 document.querySelector('#otpVerificationDiv').classList.add('hidden')
//                 document.querySelector('#otpVerificationDiv').classList.add('hidden')
//                 document.querySelector('#invalidPhoneLabel').classList.remove('red')
//                 document.querySelector('#invalidPhoneLabel').classList.add('green')
//                 document.querySelector('#invalidPhoneLabel').style.display = 'inline'
//                 document.querySelector('#invalidPhoneLabel').innerText = 'Verified through OTP'
//                 window.scrollBy(0, -300);

//                 break;
//             default:                
//                 DisplayMessage('',data.detail,data.status)

//         }
// }

// const DisplayMessage = (heading,detail, status) =>{
//     if(status==true){

//     document.querySelector('.showMessage').classList.remove('error') ;
//     document.querySelector('.showMessage').classList.add('success') ;
//     }
//     else{

//     document.querySelector('.showMessage').classList.remove('success') ;
//     document.querySelector('.showMessage').classList.add('error') ;
//     }

//     document.querySelector('.showMessage').style.display='block'
//     document.querySelector('.showMessage>div').innerText = heading
//     document.querySelector('.showMessage>p').innerHTML = detail     

// }


const OpenSignupForm = () => {
    let d = document.querySelectorAll('.fields.hidden')
    for (let i = 0; i < d.length; i++) {
        d[i].classList.remove('hidden')
    }
    document.getElementById('mobile_no').readOnly = true
    document.getElementById('')
}

function SendOTP() {
    //validateSignupForm();
    enteredMobile = document.getElementById('mobile_no').value;
    if (validateMobileno(enteredMobile))
        showMessage('mobileno', false)
    else
        showMessage('mobileno', true)
    if (!isFormValid)
        return false;
    // var name = document.getElementById('name').value  
    // var password = document.getElementById('password').value  
    // var email = document.getElementById('emailInput').value
    var mobile_no = document.getElementById('mobile_no').value


    // var signupInfo = JSON.stringify({
    //     "user": {
    //     "email": email,
    //     "password": password,
    //     "phone": mobile_no
    //     },
    //     "first_name": name,   
    // })

    var signupUrl = "/api/seller/register/"

    var otpInfo = JSON.stringify({
        "phone": mobile_no,
    });
    debugger;
    var result = postJSON('/api/send_mobile_otp/', otpInfo)

    //         fetch('http://127.0.0.1:8000/api/send_mobile_otp/',{ 
    //         method : 'POST',
    //         headers: {
    //         'Accept': "application/json, text/plain, */*",
    //         'Content-Type': 'application/json',     
    //         'Accept-Encoding':'gzip,deflate,br',      
    //         },
    //         body: JSON.stringify({
    //         "name":  name,     
    //         "phone": mobile_no,
    //         })
    //     }
    //   )
    //          .then(res =>{
    //             res.clone().json()
    //             console.log(res)
    //          }
    //               )
    //function(response) {
    //     if(!response.ok){
    //     console.log(response)
    //     if(response.status == 400 || response.statusText == 'Bad Request'){

    //     }
    //     switch(response.status){
    //         case 400: 
    //         if(response.statusText == 'Bad Request'){
    //         let msg = 'Email Id or Phone Number already exists'
    //         document.getElementById('msg-heading').innerText = msg;            
    //         document.getElementById('msg-heading').className = 'errormsg';
    //         document.getElementById('msg-heading').style.display = 'block';
    //         }
    //         break;
    //         case 500:
    //             if(response.statusText == 'Internal Server Error'){
    //                 let msg = 'Some Error Occured. Please try again..'
    //                 document.getElementById('msg-heading').innerText = msg;            
    //                 document.getElementById('msg-heading').className = 'errormsg';
    //                 document.getElementById('msg-heading').style.display = 'block';
    //             }
    //             break;

    //     }
    //     throw Error(response.statusText)
    //     }
    //     else{
    //         response.json()
    //         console.log(response)
    //         let msg = 'You have been Registered Successfully'
    //        // OpenMobileVerification()
    //         //  document.getElementById('modalmsg').innerText = msg;            
    //         //  document.getElementById('sellermodal').style.display = 'block';
    //         //  document.getElementById('msg-heading').style.display = 'none';
    //         //  if(mobile_no == ''){
    //         //  document.getElementById('phoneVerification').display='none';
    //         //  document.getElementById('phoneVerification').display='none';
    //         //  }
    //     }       
    // }
    //)
    // .then(data => {
    //     debugger;
    //     console.log('parsed json', data.json())
    //     console.log(response)
    // })
    // .catch(error => console.log(error))
}

const OpenMobileVerification = () => {
    //document.getElementById('signupForm').style.display = 'none'
    document.getElementById('otpVerificationDiv').style.display = 'block'
    document.getElementById('submitMobileBtn').style.display = 'none'
    document.querySelector('#signupBtn').classList.remove('hidden')
        // document.getElementById('emailOptionBtn').style.display = 'none'
}

const validateSignupForm = () => {
    CheckName();
    let email = document.getElementById('emailInput').value;

    if (validateEmail(email))
        showMessage('email', false)
    else if (email !== '')
        showMessage('email', true)
    checkPassword();
    let enteredMobile = document.getElementById('mobile_no').value;
    if (validateMobileno(enteredMobile))
        showMessage('mobileno', false)
    else
        showMessage('mobileno', true)
        //checkConfirmPassword();       
}

const CheckMandatoryFields = () => {

}

function checkMobileno() {
    let phone = document.getElementById('emailInput').value;
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    console.log(regex.test(String(email).toLowerCase()));

    if (regex.test(String(email).toLowerCase())) {
        showMessage('email', false)
    } else {
        showMessage('email', true)
        isFormValid = false;
        //document.getElementById('invalidEmailLabel').style.display='block';
    }

}


// const giveMsgforPassword = () => {
//     document.getElementById('passwordLabel').style.display
// }

const CheckName = () => {
    first_name = document.getElementById('name').value
    if (first_name != undefined && first_name != '')
        showMessage('first_name', false)
    else {
        showMessage('first_name', true)
        isFormValid = false;
    }
}


function showMessage(formField, isError) {

    switch (formField) {
        case 'first_name':
            if (isError)
                document.getElementById('enterNameLabel').style.display = 'inline';
            else
                document.getElementById('enterNameLabel').style.display = 'none';
            break;

        case 'email':
            if (isError)
                document.getElementById('invalidEmailLabel').style.display = 'inline';
            else
                document.getElementById('invalidEmailLabel').style.display = 'none';
            break;

        case 'password':
            if (document.getElementById('password').value == '') {
                document.getElementById('passwordLabel').style.display = 'inline';
                break;
            }
            if (isError)
                document.getElementById('passwordLabel').style.display = 'inline';
            else
                document.getElementById('passwordLabel').style.display = 'none';
            break;

        case 'mobileno':
            if (isError)
                document.getElementById('invalidPhoneLabel').style.display = 'inline';
            else
                document.getElementById('invalidPhoneLabel').style.display = 'none';
            break;
    }
    // let button = document.getElementById('signupSubmit');
    // if(isError){      

    //     //document.getElementById('signupSubmit').disabled=false;    
    //     //button.style.pointerEvents='none';
    //     button.disabled = true;
    // }
    // else{
    //     //document.getElementById('signupSubmit').style.pointerEvents='auto';
    //     button.disabled = false;
    // }
}

var phoneOTP = ''
var emailOTP = ''

const onChangeEmailOTP = () => {

}

const CheckEmailOTP = () => {
    let otpLength = emailOTP.length;
    let inputs = document.getElementsByClassName('verifyOTP email');
    switch (otpLength) {
        case 1:
            disableOTPInputs(5, 1)

    }
}

const disableOTPInputs = (from, to) => {
    for (let i = from; i >= to; from--) {

    }
}

function ShowPassword() {
    let passwordInput = document.getElementById('password');

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        document.getElementById("showpass").classList.remove("eye");
        document.getElementById("showpass").classList.add('eye', 'slash');
    } else {
        passwordInput.type = "password";
        document.getElementById("showpass").classList.remove('eye', 'slash');
        document.getElementById("showpass").classList.add("eye");
    }
}

var otp1 = document.getElementById("otpMobile1"),
    otp2 = document.getElementById("otpMobile2"),
    otp3 = document.getElementById("otpMobile3"),
    otp4 = document.getElementById("otpMobile4");

if (otp1 !== null)
    otp1.onkeyup = function() {
        if (this.value.length === parseInt(this.attributes["maxlength"].value)) {
            otp2.focus();
        }
    }

if (otp2 !== null)
    otp2.onkeyup = function() {
        if (this.value.length === parseInt(this.attributes["maxlength"].value)) {
            otp3.focus();
        }
    }

if (otp3 !== null)
    otp3.onkeyup = function() {
        if (this.value.length === parseInt(this.attributes["maxlength"].value)) {
            otp4.focus();
        }
    }

const CheckOTP = () => {
    if (otp1.value == undefined || otp2.value == '' || otp3.value == '')
        return;
    var mobile_no = document.getElementById('mobile_no').value
    var otp = document.getElementsByClassName('verifyOTP')
    otpvalue = ""
    for (let i = 0; i <= 3; i++) {
        if (otp[i].value === undefined || otp[i].value === '')
            return;
        otpvalue += otp[i].value
    }

    var jsonbody = JSON.stringify({
        "mobile": mobile_no,
        "otp": otpvalue
    })
    postJSON('/api/validate_mobile_otp/', jsonbody)
}

var OpenEmailInput = () => {
    document.getElementById('')
}