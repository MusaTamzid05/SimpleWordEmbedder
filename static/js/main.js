

$(document).ready(() => {
    const path = window.location.pathname;
    $(".nav-btn").removeClass("active");

    if(path === "/") 
        $(".nav-btn.home").addClass("active");
    else
        $(".nav-btn.generate").addClass("active");

    $("#train-button").click(() => {
        const corpusName = $("#data-selection").find(":selected").val();
        const epochCount = $("#epoch-count").val();

        const params = {
            "corpusName"  : corpusName,
            "epochCount" : epochCount
        };




        fetch("http://localhost:5000/train",{
            method: "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify(params)

        })
            .then(res => res.json())
            .then(data => {
                console.log(data);
            })
            .catch(err => console.log(err));

    })


});
