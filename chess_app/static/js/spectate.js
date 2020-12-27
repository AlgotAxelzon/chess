
function copyToClipboard(element_id) {
    if (element_id == "play") copy = "http://chess.axelzon.com/play/" + page_match_id; 
    else if (element_id == "spectate") copy = "http://chess.axelzon.com/spectate/" + page_match_id; 
    navigator.clipboard.writeText(copy);
}

function drawBoard(board) {
    // Clear board
    $(".square").each(function() {
        $(this).css("background-image", "");
    });
    // Draw pieces
    $.each(board.positions, function(key, data) {
        pieceType = data.type.toLowerCase();
        pieceColor = data.color == "white" ? "l" : "d";
        url = `/static/img/Chess_${pieceType + pieceColor}t45.svg`;
        $("#" + key).css("background-image", `url(${url})`);
    });
}

function changeBoard(changes) {
    $(".from").removeClass("from");
    $(".to").removeClass("to");
    // Draw pieces
    $.each(changes, function(key, data) {
        if (data == "empty") {
            $("#" + key).css("background-image", "none");
            $("#" + key).attr("hasPiece", "false");
        } else if (data == "from") {
            $("#" + key).css("background-image", "none");
            $("#" + key).addClass("from");
            $("#" + key).attr("hasPiece", "false");
        } else {
            if (data.hasOwnProperty("to")) {
                $("#" + key).addClass("to");
            }
            pieceType = data.type.toLowerCase();
            pieceColor = data.color == "white" ? "l" : "d";
            url = `/static/img/Chess_${pieceType + pieceColor}t45.svg`;
            $("#" + key).css("background-image", `url(${url})`);
            $("#" + key).attr("hasPiece", "true");
        }
    });
}


$(document).ready(function() {
    var socket = io();
    page_match_id = window.location.pathname.split("/")[2];
    console.log(page_match_id);

    socket.on("connect", function() {
        socket.emit("spectateMatch", {"match_id": page_match_id});
    });

    socket.on("joinedSpectate", function(data) {
        match = JSON.parse(data.match);
        drawBoard(match.board);
        // TODO: updatePlayers(match.players, match.spectators);
    });
    
    socket.on("updateBoard", function(data) {
        changeBoard(data.changed);
    });
});
