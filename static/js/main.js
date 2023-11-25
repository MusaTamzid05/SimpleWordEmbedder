

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

    });

    setInterval(() => {
        fetch("http://localhost:5000/current_model_info",{
            method: "GET",
            headers : {
                "Content-Type" : "application/json"
            },

        })
            .then(res => res.json())
            .then(data => {
                if(data.length == 0)
                    return;

                const epochTable = "epoch-table";
                $("#" + epochTable).remove();

                let tableContent = `<table id=${epochTable}>`;

                data.forEach((epochData) => {
                    const name = epochData["name"];
                    const epochCount = epochData["epochs"];
                    const loss = epochData["loss"];

                    tableContent +=  `<tr><td>Model name ${name}</td><td>Epochs ${epochCount}</td><td>Loss ${loss}</td></tr>`;
                });

                tableContent += "</table>";

                $("#epoch-info").append(tableContent);
            })
            .catch(err => console.log(err));

    }, 1000);

    $("#generate-button").click(() => {
        const modelName = $("#model-name").find(":selected").val();
        const userInput = $("#generate-input").val();
        const wordCount = $("#word-count").val();

        const params = {
            "modelName" : modelName,
            "userInput" : userInput,
            "wordCount" : wordCount
        };

        console.log(params);

        fetch("http://localhost:5000/generate_text",{
            method: "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify(params)

        })
            .then(res => res.json())
            .then(data => {
                $("#generated-text").text(data["result"])
            })
            .catch(err => console.log(err));



    })

    


});
