$(document).ready(function () {
	var url = window.location;
    $('ul.navbar-nav a').filter(function() {
         return this.href == url;
    }).parent().addClass('active').siblings().removeClass('active');
});