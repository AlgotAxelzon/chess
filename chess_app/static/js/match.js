
function copyToClipboard(element_id) {
    if (element_id == "play") copy = window.location.hostname + "/play/" + page_match_id; 
    else if (element_id == "spectate") copy = window.location.hostname + "/spectate/" + page_match_id; 
    navigator.clipboard.writeText(copy);
}

function drawBoard(board) {
    // Clear board
    $(".square").each(function() {
        $(this).css("background-image", "");
        $(this).attr("hasPiece", "false");
    });
    // Draw pieces
    $.each(board.positions, function(key, data) {
        pieceType = data.type.toLowerCase();
        pieceColor = data.color == "white" ? "l" : "d";
        url = `/static/img/Chess_${pieceType + pieceColor}t45.svg`;
        $("#" + key).css("background-image", `url(${url})`);
        $("#" + key).attr("hasPiece", "true");
    });
}

clickSquare = "";
isDragging = false;
fromSquare = "";
toSquare = "";


$(document).ready(function() {
    var socket = io();
    page_match_id = window.location.pathname.split("/")[2];
    console.log(page_match_id);
    
    socket.on("connect", function() {
        socket.emit("playMatch", {"match_id": page_match_id});
    });

    socket.on("joinedPlay", function(data) {
        match = JSON.parse(data.match);
        drawBoard(match.board);
        // TODO: updatePlayers(match.players, match.spectators);
    });

    socket.on("toSpectate", function(data) {
        match_id = data.match_id;
        window.location.replace("/spectate/" + match_id);
    });

    socket.on("updateBoard", function(data) {
        match = JSON.parse(data.match);
        drawBoard(match.board);
    });
    
    $(document).mousemove(function(e) {
        if (isDragging) {
            $(".follow").offset({
                left: e.pageX,
                top: e.pageY
            });
        }
    });

    $(".square").click(function(){
        clickSquare = $(this).attr("id");
        hasPiece = $(this).attr("hasPiece");
        if (hasPiece == "true" && !isDragging) {
            isDragging = true;
            fromSquare = clickSquare;
            // TODO: remove piece from clickSquare, put on cursor
        } else if (isDragging) {
            // TODO: Place dragging piece on clickSquare
            isDragging = false;
            toSquare = clickSquare;
            move = fromSquare + toSquare;
            if (clickSquare != fromSquare) {
                socket.emit("move", {"move": move, "match_id": page_match_id});
                console.log("move: " + move);
            }
            fromSquare = "";
            toSquare = "";
        }
    });
});
