

$(document).ready(() => {
    const path = window.location.pathname;
    $(".nav-btn").removeClass("active");

    if(path === "/") 
        $(".nav-btn.home").addClass("active");
    else
        $(".nav-btn.generate").addClass("active");


});
