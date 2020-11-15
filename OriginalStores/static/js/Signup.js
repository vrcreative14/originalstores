
var isFormValid = true


function checkPassword(){
    debugger;
    let password = document.getElementById('password');
    let cpassword = document.getElementById('cpassword');
    if (password.value != ''){
    document.getElementById('passwordLabel').style.display = 'none'; 
    document.getElementById('cPasswordLabel').style.display = 'none'; 
    document.getElementById('password').disabled = false; 
    }  
    else{
        document.getElementById('passwordLabel').style.display = 'inline'; 
    }
    cpassword.disabled = false;
  
}

function checkConfirmPassword(){
    debugger;
    let password = document.getElementById('password');
    let cpassword = document.getElementById('cpassword');
    console.log(cpassword.value)
    if(password.value == cpassword.value){
    //     document.getElementById('cPasswordLabel').style.display = 'none';
    //     document.getElementById('signupSubmit').style.pointerEvents='auto';
    //     document.getElementById('signupSubmit').disabled=false;
    showMessage('confirm_pass',false);
   }
    else{
        // let button = document.getElementById('signupSubmit');
        // document.getElementById('cPasswordLabel').style.display = 'block';
        // console.log(button);
        // button.style.pointerEvents='none';
        showMessage('confirm_pass',true);
        //document.getElementsByClassName('submitButton').style.='none';
    }
}

function Signup() {
    debugger;
  validateSignupForm();
  console.log(email, mobile_no, first_name)
  if(!isFormValid)
   return false;
  var first_name = document.getElementById('first_name').value
  var last_name = document.getElementById('last_name').value
  var password = document.getElementById('password').value
  var cpassword = document.getElementById('cpassword').value
  var email = document.getElementById('emailInput').value
  var mobile_no = document.getElementById('mobile_no').value
  if (mobile_no=='' || mobile_no==undefined)
         mobile_no=null
    fetch('http://127.0.0.1:8000/api/seller/register/',{ 
    method : 'POST',
    headers: {
      'Accept': "application/json, text/plain, */*",
      'Content-Type': 'application/json',     
      'Accept-Encoding':'gzip,deflate,br',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      "user": {
        "email": email,
        "password": password,
        "phone": mobile_no
      },
      "first_name": first_name,
      "last_name": last_name
    })
  }
    )
      .then(function(response) {
        if(!response.ok){
          console.log(response)
           if(response.status == 400 || response.statusText == 'Bad Request'){
             let msg = 'Email Id or Phone Number already exists'
             document.getElementById('msg-heading').innerText = msg;            
             document.getElementById('msg-heading').className = 'errormsg';
             document.getElementById('msg-heading').style.display = 'block';
           }
          throw Error(response.statusText)
        }
        else{
            response.json()
            console.log(response)
             let msg = 'You have been Registered Successfully'
             document.getElementById('modalmsg').innerText = msg;            
             document.getElementById('sellermodal').style.display = 'block';
             document.getElementById('msg-heading').style.display = 'none';
             if(mobile_no == ''){
             document.getElementById('phoneVerification').display='none';
             document.getElementById('phoneVerification').display='none';
             }
        }       
      })
      .then(data => console.log(data))
      .catch(error => console.log(error))
  }

const validateSignupForm = () => {     
    CheckName();
    validateEmail();
    checkPassword();       
    validateMobileno();
    checkConfirmPassword();       
}

const CheckMandatoryFields = () =>{
    
    
}

function checkMobileno(){
    let phone = document.getElementById('emailInput').value;
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    console.log(regex.test(String(email).toLowerCase()));

    if(regex.test(String(email).toLowerCase()))
    {
        showMessage('email',false)
    }
    else
    {        
        showMessage('email',true)
         //document.getElementById('invalidEmailLabel').style.display='block';
    }
   
}

function validateEmail() {
    let email = document.getElementById('emailInput').value;
    // if(email != undefined && email !='')
    //     return
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    console.log(regex.test(String(email).toLowerCase()));
    
    if(regex.test(String(email).toLowerCase()))
    {
        showMessage('email',false)       
    }
    else
    {        
        showMessage('email',true)
        isFormValid=false;
         //document.getElementById('invalidEmailLabel').style.display='block';
    }
}

const validateMobileno = () =>{
    debugger;
    enteredMobile = document.getElementById('mobile_no').value;
    // if (enteredMobile == undefined || enteredMobile == '')
    //   showMessage('mobileno',true)
    var regex = /^\d{10}$/;
    if( regex.test(String(enteredMobile).toLowerCase()))
         showMessage('mobileno', false)
    else
         showMessage('mobileno', true) 
}

// const giveMsgforPassword = () => {
//     document.getElementById('passwordLabel').style.display
// }

const CheckName = () => {
    first_name = document.getElementById('first_name').value
    if(first_name != undefined && first_name!='')
      showMessage('first_name',false)
    else
      showMessage('first_name',true)
}


function showMessage(formField,isError){

    switch(formField){
        case 'first_name':
            if(isError)
                document.getElementById('enterNameLabel').style.display = 'inline';                      
            else
                document.getElementById('enterNameLabel').style.display = 'none';                    
            break;
        
        case 'email':
            if(isError)
                document.getElementById('invalidEmailLabel').style.display = 'inline';                      
            else
                document.getElementById('invalidEmailLabel').style.display = 'none';                    
            break;

        case 'password':
            if(document.getElementById('password').value == ''){
                document.getElementById('passwordLabel').style.display = 'inline';  
                break;
            } 
            if(isError)
                document.getElementById('passwordLabel').style.display = 'inline';            
            else
                document.getElementById('passwordLabel').style.display = 'none';            
            break;

        case 'mobileno':
           if(isError)
               document.getElementById('invalidPhoneLabel').style.display = 'inline';            
           else
               document.getElementById('invalidPhoneLabel').style.display = 'none';                     
            break;

        case 'confirm_pass':       
        if(document.getElementById('cpassword').value == '')
            document.getElementById('cPasswordLabel').innerText = 'Please confirm Password';  
        else
        document.getElementById('cPasswordLabel').innerText = 'Passwords not matching';  
        
                if(isError)
                    document.getElementById('cPasswordLabel').style.display = 'inline';            
                else
                    document.getElementById('cPasswordLabel').style.display = 'none';            
                break;

    }
    let button = document.getElementById('signupSubmit');
    if(isError){
        //document.getElementById('cPasswordLabel').style.display = 'none';
       
        //document.getElementById('signupSubmit').disabled=false;
       
        //document.getElementById('cPasswordLabel').style.display = 'block';
        //console.log(button);
        //button.style.pointerEvents='none';
        button.disabled = true;
    }
    else{
        //document.getElementById('signupSubmit').style.pointerEvents='auto';
        button.disabled = false;
    }
}

var phoneOTP = ''
var emailOTP = ''

const onChangeEmailOTP = () => {

}

const CheckEmailOTP = () => {
    let otpLength = emailOTP.length;
    let inputs = document.getElementsByClassName('verifyOTP email');
    switch(otpLength){
        case 1 : disableOTPInputs(5, 1)

    }
}

const disableOTPInputs = (from, to) => {
        for(let i= from; i>=to; from--){

        }
}