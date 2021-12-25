
const socket = new WebSocket('ws://localhost:8000/ws/gamebot/' + room_code)
socket.onopen = function(e){
    console.log("Socket Connected");
}

socket.onmessage = function(e){
    var data = JSON.parse(e.data)
    console.log("message received")
    if(data.payload.type === 'botMove') {
        console.log('botMove');
        makebotMove(data.payload.game_squares_value, data.payload.game_isKing, data.payload.turn, data.payload.redScore, data.payload.blackScore);
    }
}

socket.onclose = function(e){
    console.log("Socket Disconnected");
}

/* Game State Data */

const board = game_squares;

/* Cached Variables */

/* Parse piece ID's and return index of place on board */
let findPiece = function (pieceId) {
    let parsed = parseInt(pieceId);
    return board.indexOf(parsed);
};

/* DOM References */
const cells = document.querySelectorAll("td");
let redPieces = document.querySelectorAll("p");
let blackPieces = document.querySelectorAll("span")
const redUserText = document.querySelectorAll(".red-user-text");
const blackUserText = document.querySelectorAll(".black-user-text");
const divider = document.querySelector("#divider")

/* Player Profiles */
let playerPieces;

/* Selected Piece Properties */
let selectedPiece = {
    pieceId: -1,
    indexOfBoardPiece: -1,
    isKing: false,
    seventhSpace: false,
    ninthSpace: false,
    fourteenthSpace: false,
    eighteenthSpace: false,
    minusSeventhSpace: false,
    minusNinthSpace: false,
    minusFourteenthSpace: false,
    minusEighteenthSpace: false
}

/* Event Listeners */

/* Initialize Event Listeners on Pieces */

function makebotMove(game_squares, isKing, _turn, red_score, black_score)
{
    turn = _turn;
    redScore = red_score;
    blackScore = black_score;
    document.getElementById("redscore").innerHTML = `${redScore}`;
    document.getElementById("blackscore").innerHTML = `${blackScore}`;
    console.log(game_squares)
    for(i=0;i<64;i++)
    {
        if(game_squares[i] != null)
        {
            if(game_squares[i] < 12)
            {
                if(isKing[i])
                    cells[i].innerHTML = `<p class="red-piece king" id="${game_squares[i]}"></p>`;
                else
                    cells[i].innerHTML = `<p class="red-piece" id="${game_squares[i]}"></p>`; 
            }
            else if(game_squares[i] > 11)
            {
                if(isKing[i])
                    cells[i].innerHTML = `<span class="black-piece king" id="${game_squares[i]}"></span>`;
                else
                    cells[i].innerHTML = `<span class="black-piece" id="${game_squares[i]}"></span>`;
            }
        }
        else
        {
            cells[i].innerHTML = ``;
        }
    }
    redPieces = document.querySelectorAll("p");
    blackPieces = document.querySelectorAll("span");
    givePiecesEventListeners();
}

function givePiecesEventListeners() {
    if (turn) {
        for (let i = 0; i < redPieces.length; i++) {
            redPieces[i].addEventListener("click", getPlayerPieces);
        }
    }
    // } else {
    //     for (let i = 0; i < blackPieces.length; i++) {
    //         blackPieces[i].addEventListener("click", getPlayerPieces);
    //     }
    // }
}

/* Logic */

/* Holds number of remaining player pieces */
function getPlayerPieces() {
    if (turn) {
        playerPieces = redPieces;
    } else {
        playerPieces = blackPieces;
    }
    removeCellonclick();
    resetBorders();
}

/* Removes possible moves from old selected piece */
function removeCellonclick() {
    for (let i = 0; i < cells.length; i++) {
        cells[i].removeAttribute("onclick");
    }
}

/* Resets borders to default */
function resetBorders() {
    for (let i = 0; i < playerPieces.length; i++) {
        playerPieces[i].style.border = "1px solid white";
    }
    resetSelectedPieceProperties();
    getSelectedPiece();
}

/* Resets selected piece properties */
function resetSelectedPieceProperties() {
    selectedPiece.pieceId = -1;
    selectedPiece.pieceId = -1;
    selectedPiece.isKing = false;
    selectedPiece.seventhSpace = false;
    selectedPiece.ninthSpace = false;
    selectedPiece.fourteenthSpace = false;
    selectedPiece.eighteenthSpace = false;
    selectedPiece.minusSeventhSpace = false;
    selectedPiece.minusNinthSpace = false;
    selectedPiece.minusFourteenthSpace = false;
    selectedPiece.minusEighteenthSpace = false;
}

/* Gets ID and index of the board cell where piece is located */
function getSelectedPiece() {
    selectedPiece.pieceId = parseInt(event.target.id);
    selectedPiece.indexOfBoardPiece = findPiece(selectedPiece.pieceId);
    isPieceKing();
}

/* Checks if selected piece is Kinged */
function isPieceKing() {
    if (document.getElementById(selectedPiece.pieceId).classList.contains("king")) {
        selectedPiece.isKing = true;
    } else {
        selectedPiece.isKing = false;
    }
    getAvailableSpaces();
}

/* Gets the available moves for the selected piece */
function getAvailableSpaces() {
    if (board[selectedPiece.indexOfBoardPiece + 7] === null && 
        cells[selectedPiece.indexOfBoardPiece + 7].classList.contains("noPieceHere") !== true) {
        selectedPiece.seventhSpace = true;
    }
    if (board[selectedPiece.indexOfBoardPiece + 9] === null && 
        cells[selectedPiece.indexOfBoardPiece + 9].classList.contains("noPieceHere") !== true) {
        selectedPiece.ninthSpace = true;
    }
    if (board[selectedPiece.indexOfBoardPiece - 7] === null && 
        cells[selectedPiece.indexOfBoardPiece - 7].classList.contains("noPieceHere") !== true) {
        selectedPiece.minusSeventhSpace = true;
    }
    if (board[selectedPiece.indexOfBoardPiece - 9] === null && 
        cells[selectedPiece.indexOfBoardPiece - 9].classList.contains("noPieceHere") !== true) {
        selectedPiece.minusNinthSpace = true;
    }
    checkAvailableJumpSpaces();
}

/* Gets the moves selected pieces can make */
function checkAvailableJumpSpaces() {
    if (turn) {
        if (board[selectedPiece.indexOfBoardPiece + 14] === null 
        && cells[selectedPiece.indexOfBoardPiece + 14].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece + 7] >= 12) {
            selectedPiece.fourteenthSpace = true;
        }
        if (board[selectedPiece.indexOfBoardPiece + 18] === null 
        && cells[selectedPiece.indexOfBoardPiece + 18].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece + 9] >= 12) {
            selectedPiece.eighteenthSpace = true;
        }
        if (board[selectedPiece.indexOfBoardPiece - 14] === null 
        && cells[selectedPiece.indexOfBoardPiece - 14].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece - 7] >= 12) {
            selectedPiece.minusFourteenthSpace = true;
        }
        if (board[selectedPiece.indexOfBoardPiece - 18] === null 
        && cells[selectedPiece.indexOfBoardPiece - 18].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece - 9] >= 12) {
            selectedPiece.minusEighteenthSpace = true;
        }
    } else {
        if (board[selectedPiece.indexOfBoardPiece + 14] === null 
        && cells[selectedPiece.indexOfBoardPiece + 14].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece + 7] < 12 && board[selectedPiece.indexOfBoardPiece + 7] !== null) {
            selectedPiece.fourteenthSpace = true;
        }
        if (board[selectedPiece.indexOfBoardPiece + 18] === null 
        && cells[selectedPiece.indexOfBoardPiece + 18].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece + 9] < 12 && board[selectedPiece.indexOfBoardPiece + 9] !== null) {
            selectedPiece.eighteenthSpace = true;
        }
        if (board[selectedPiece.indexOfBoardPiece - 14] === null && cells[selectedPiece.indexOfBoardPiece - 14].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece - 7] < 12 
        && board[selectedPiece.indexOfBoardPiece - 7] !== null) {
            selectedPiece.minusFourteenthSpace = true;
        }
        if (board[selectedPiece.indexOfBoardPiece - 18] === null && cells[selectedPiece.indexOfBoardPiece - 18].classList.contains("noPieceHere") !== true
        && board[selectedPiece.indexOfBoardPiece - 9] < 12
        && board[selectedPiece.indexOfBoardPiece - 9] !== null) {
            selectedPiece.minusEighteenthSpace = true;
        }
    }
    checkPieceConditions();
}

/* Changes direction of movement if piece is King */
function checkPieceConditions() {
    if (selectedPiece.isKing) {
        givePieceBorder();
    } else {
        if (turn) {
            selectedPiece.minusSeventhSpace = false;
            selectedPiece.minusNinthSpace = false;
            selectedPiece.minusFourteenthSpace = false;
            selectedPiece.minusEighteenthSpace = false;
        } else {
            selectedPiece.seventhSpace = false;
            selectedPiece.ninthSpace = false;
            selectedPiece.fourteenthSpace = false;
            selectedPiece.eighteenthSpace = false;
        }
        givePieceBorder();
    }
}

/* Gives active piece green border */
function givePieceBorder() {
    if (selectedPiece.seventhSpace || selectedPiece.ninthSpace || selectedPiece.fourteenthSpace || selectedPiece.eighteenthSpace
    || selectedPiece.minusSeventhSpace || selectedPiece.minusNinthSpace || selectedPiece.minusFourteenthSpace || selectedPiece.minusEighteenthSpace) {
        document.getElementById(selectedPiece.pieceId).style.border = "3px solid green";
        giveCellsClick();
    } else {
        return;
    }
}

/* Gives cells on the board a 'click' based on possible moves */
function giveCellsClick() {
    if (selectedPiece.seventhSpace) {
        cells[selectedPiece.indexOfBoardPiece + 7].setAttribute("onclick", "makeMove(7)");
    }
    if (selectedPiece.ninthSpace) {
        cells[selectedPiece.indexOfBoardPiece + 9].setAttribute("onclick", "makeMove(9)");
    }
    if (selectedPiece.fourteenthSpace) {
        cells[selectedPiece.indexOfBoardPiece + 14].setAttribute("onclick", "makeMove(14)");
    }
    if (selectedPiece.eighteenthSpace) {
        cells[selectedPiece.indexOfBoardPiece + 18].setAttribute("onclick", "makeMove(18)");
    }
    if (selectedPiece.minusSeventhSpace) {
        cells[selectedPiece.indexOfBoardPiece - 7].setAttribute("onclick", "makeMove(-7)");
    }
    if (selectedPiece.minusNinthSpace) {
        cells[selectedPiece.indexOfBoardPiece - 9].setAttribute("onclick", "makeMove(-9)");
    }
    if (selectedPiece.minusFourteenthSpace) {
        cells[selectedPiece.indexOfBoardPiece - 14].setAttribute("onclick", "makeMove(-14)");
    }
    if (selectedPiece.minusEighteenthSpace) {
        cells[selectedPiece.indexOfBoardPiece - 18].setAttribute("onclick", "makeMove(-18)");
    }
}

/* When cell is clicked */

/* Makes move to space that was clicked */
function makeMove(number) {
    var data = {
        'type': 'move',
        'selectedPiece' : selectedPiece,
        'turn' : turn,
        'number' : number,
        'board': board,
        'redScore': redScore,
        'blackScore': blackScore
    }

    socket.send(JSON.stringify({
        data
    }));

    document.getElementById(selectedPiece.pieceId).remove();
    cells[selectedPiece.indexOfBoardPiece].innerHTML = "";
    if (turn) {
        if (selectedPiece.isKing) {
            cells[selectedPiece.indexOfBoardPiece + number].innerHTML = `<p class="red-piece king" id="${selectedPiece.pieceId}"></p>`;
            redPieces = document.querySelectorAll("p");
        } else {
            cells[selectedPiece.indexOfBoardPiece + number].innerHTML = `<p class="red-piece" id="${selectedPiece.pieceId}"></p>`;
            redPieces = document.querySelectorAll("p");
        }
    } else {
        if (selectedPiece.isKing) {
            cells[selectedPiece.indexOfBoardPiece + number].innerHTML = `<span class="black-piece king" id="${selectedPiece.pieceId}"></span>`;
            blackPieces = document.querySelectorAll("span");
        } else {
            cells[selectedPiece.indexOfBoardPiece + number].innerHTML = `<span class="black-piece" id="${selectedPiece.pieceId}"></span>`;
            blackPieces = document.querySelectorAll("span");
        }
    }

    let indexOfPiece = selectedPiece.indexOfBoardPiece
    if (number === 14 || number === -14 || number === 18 || number === -18) {
        changeData(indexOfPiece, indexOfPiece + number, indexOfPiece + number / 2);
    } else {
        changeData(indexOfPiece, indexOfPiece + number);
    }
}

/* Changes board state data on back end */
function changeData(indexOfBoardPiece, modifiedIndex, removePiece) {
    board[indexOfBoardPiece] = null;
    board[modifiedIndex] = parseInt(selectedPiece.pieceId);
    if (turn && selectedPiece.pieceId < 12 && modifiedIndex >= 57) {
        document.getElementById(selectedPiece.pieceId).classList.add("king")
    }
    if (turn === false && selectedPiece.pieceId >= 12 && modifiedIndex <= 7) {
        document.getElementById(selectedPiece.pieceId).classList.add("king");
    }
    if (removePiece) {
        board[removePiece] = null;
        if (turn && selectedPiece.pieceId < 12) {
            cells[removePiece].innerHTML = "";
            blackScore--
        }
        if (turn === false && selectedPiece.pieceId >= 12) {
            cells[removePiece].innerHTML = "";
            redScore--
        }
    }
    resetSelectedPieceProperties();
    removeCellonclick();
    removeEventListeners();
}

/* Removes the 'onClick' event listeners for pieces */
function removeEventListeners() {
    if (turn) {
        for (let i = 0; i < redPieces.length; i++) {
            redPieces[i].removeEventListener("click", getPlayerPieces);
        }
    } else {
        for (let i = 0; i < blackPieces.length; i++) {
            blackPieces[i].removeEventListener("click", getPlayerPieces);
        }
    }
    checkForWin();
}

/* Checks for a win */
function checkForWin() {
    if (blackScore === 0) {
        divider.style.display = "none";
        for (let i = 0; i < redTurnText.length; i++) {
            redTurnText[i].style.color = "black";
            blackTurntext[i].style.display = "none";
            redTurnText[i].textContent = "RED WINS!";
            var data = {
                'type': 'endgame',
                'result': 'R'
            }
            socket.send(JSON.stringify({
                data
            }));
        }
    } else if (redScore === 0) {
        divider.style.display = "none";
        for (let i = 0; i < blackTurntext.length; i++) {            
            blackTurntext[i].style.color = "black";
            redTurnText[i].style.display = "none";
            blackTurntext[i].textContent = "BLACK WINS!";
            var data = {
                'type' : 'endgame',
                'result' : 'B'
            }
            socket.send(JSON.stringify({
                data
            }));
        }
    } else {
        var data = {
            'type' : 'state',
            'board' : board,
            'turn' : !turn,
            'redScore' : redScore,
            'blackScore' : blackScore
        }
        socket.send(JSON.stringify({
            data
        }));
        changePlayer();
    }
}

/* Swaps active player */
function changePlayer() {
    if (turn) {
        turn = false;
        for (let i = 0; i < redUserText.length; i++) {
            redUserText[i].style.color = "lightGrey";
            blackUserText[i].style.color = "black";
            blackUserText[i].textContent = `Black's Turn Remaining Pieces: ${blackScore}`
        }
    } else {
        turn = true;
        for (let i = 0; i < blackUserText.length; i++) {
            blackUserText[i].style.color = "lightGrey";
            redUserText[i].style.color = "red";
            redUserText[i].textContent = `Red's Turn Remaining Pieces: ${redScore}`
        }
    }
    givePiecesEventListeners();
}

givePiecesEventListeners();