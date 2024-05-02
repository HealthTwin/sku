window.onload = function () {
  const div = document.querySelector('.img-scale-contact');
  div.style.left = '0%';
  div.style.opacity = '1';
  const div2 = document.querySelector('.moving-div');
  if (window.innerWidth > 800) {
    div2.style.left = '-5%';
  } else {
    div2.style.left = '0%';
  }
  div2.style.opacity = '1';
};

function myMap() {
  var mapProp = {
    center: new google.maps.LatLng(51.508742, -0.120850),
    zoom: 5,
  };
  var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}