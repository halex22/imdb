$(document).ready(
    console.log("What would we do with the drunken sailor ?")    
)


function updateFavArtist(x, add) {
    const endpointURL = $("#endpoint").val();
    const token = $("input").val();
    const artistID = $("#artist_id").val();
    const afterMSG  = add ? "Artist added to favorites" : "Artist remove from favorites";

    const requestData = {
        "artist_info": artistID
    }

    if (!add) {
        requestData["delete"] = true;
    }
    
    $.ajax({
        type: "POST",
        url: endpointURL,
        headers: {'X-CSRFToken': token},
        data: requestData,
        success: (res) => {
            console.log(res);
            $(x).hide(); // hide the clicked button
            $("#after-msg").text(afterMSG);
        },
        error: (res) => {
            alert("An error acourred. Please try again.");
        }        
    })
};
