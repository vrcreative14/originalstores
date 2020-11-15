

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            //Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//const csrftoken=getCookie('csrftoken');


var x = document.getElementById("demo");
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
    debugger;
    getLocation();
    fetchLocationName(position);
  x.placeholder = "Latitude: " + position.coords.latitude +
  "<br>Longitude: " + position.coords.longitude;
}

function fetchLocationName(position){
    fetch('http://apis.mapmyindia.com/advancedmaps/v1/99gsfvaspt7kg4nz13g3hg1bvsvkx48j/rev_geocode?lat=position.coords.latitude&lng=position.coords.longitude',{
        method:'GET',
        headers:{
            
            'X-CSRFToken':csrftoken,
        },
    })
    .then(response => response.json())
    .then(function(data){
        console.log(data)
    })
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
 }

/* Set the width of the side navigation to 0 */
function closeNav() {
document.getElementById("mySidenav").style.width = "0";
}
//fetchStores();
//getLocation();
function fetchStores() {
var wrapper = document.getElementById('storeListDiv')
//wrapper.innerHTML=''
 console.log('fetching....')
  fetch('http://127.0.0.1:8000/api/store-list/', {
      method:'GET',              
  }) 
  .then(response => response.json())
  .then(function(data){
      console.log(data)
       var list=data
       for(let i in list){
           var title =`<span class="title">${list[i].shopName}</span>`
           console.log(title)
           console.log(list[i].imgPath)
           try{
           var desc= `
           <div>
                   <div style="background-image: url(${list[i].imgPath});" class="productDesc" alt="hello">                   
                   </div>
                   <a href="#"> ${title}</a>
                   </div>
           `
          wrapper.innerHTML+=desc
           }

           catch{
               continue;
           }
       }
  })
}


var slideIndex = 1;
//showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
showSlides(slideIndex += n);
}

//Thumbnail image controls
function currentSlide(n) {
showSlides(slideIndex = n);
}

function showSlides(n) {
var i;
var slides = document.getElementsByClassName("mySlides");
var dots = document.getElementsByClassName("dot");  
if (n > slides.length) {slideIndex = 1}
if (n < 1) {slideIndex = slides.length}
for (i = 0; i < slides.length; i++) {
   slides[i].style.display = "none";
}
for (i = 0; i < dots.length; i++) {
   dots[i].className = dots[i].className.replace(" active", "");
}
slides[slideIndex-1].style.display = "block";
dots[slideIndex-1].className += " active";  
}

var docWidth = document.documentElement.offsetWidth;

[].forEach.call(
   document.querySelector('*'),
   function(e1) {
       if (e1.offsetWidth > docWidth){
           console.log(e1);
       }
   }
);

function autoSlide(n){
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
 
    for(i=0; i<slides.length; i++){
        slides[i].style.display="none";
    }
    slideIndex++;
    if(slideIndex > slides.length) {slideIndex = 1}
    for(i=0;i<dots.length;i++){
        dots[i].className = dots[i].className.replace("active","");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
    setTimeout(showSlides, 2000); //change image every 2 seconds
}






