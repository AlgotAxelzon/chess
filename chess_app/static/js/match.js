
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

clickSquare = "";
isDragging = false;
fromSquare = "";
toSquare = "";
toSquareOldUrl = "";
draggedUrl = "";


$(document).ready(function() {
    $(".follow").hide();
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
        changeBoard(data.changed);
    });

    socket.on("revertMove", function() {
        $("#" + toSquare).css("background-image", toSquareOldUrl);
        $("#" + fromSquare).css("background-image", draggedUrl);
    });
    
    $(document).mousemove(function(e) {
        if (isDragging) {
            $(".follow").offset({
                left: e.pageX - width/2,
                top: e.pageY - width/2
            });
        }
    });

    $(".square").click(function(){
        clickSquare = $(this).attr("id");
        hasPiece = $(this).attr("hasPiece");
        if (hasPiece == "true" && !isDragging) {
            width = $(this).width();
            draggedUrl = $(this).css("background-image");
            srcUrl = "/static" + draggedUrl.split("\"")[1].split("static")[1].split("svg")[0] + "svg";
            $(".follow").attr("src", srcUrl);
            $(".follow").css("width", width);
            $(".follow").show();
            $(this).css("border", "solid black 2px");
            $(this).css("background-image", "none");
            isDragging = true;
            fromSquare = clickSquare;
        } else if (isDragging) {
            $(".follow").hide();
            $("#" + fromSquare).css("border", "none");
            isDragging = false;
            toSquare = clickSquare;
            move = fromSquare + toSquare;
            toSquareOldUrl = $(this).css("background-image");
            $(this).css("background-image", draggedUrl);
            if (clickSquare != fromSquare) {
                socket.emit("move", {"move": move, "match_id": page_match_id});
            }
        }
    });
});
