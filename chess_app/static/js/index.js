function startGame() {
    socket.emit("createMatch");
}

function practice() {
    socket.emit("createPractice");
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
    })
}

var socket = io();

$(document).ready(function() {

    socket.on("connect", function() {
        socket.emit("join");
    });

    socket.on("disconnect", function() {
        socket.emit("leave");
    });

    socket.on("matchCreated", function(data) {
        match_id = data.match_id;
        window.location.replace("/play/" + match_id);
    });

    socket.on("practiceCreated", function(data) {
        practice_id = data.practice_id
        window.location.replace("/practice/" + practice_id);
    });
});
