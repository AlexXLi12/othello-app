// create board with starting pieces
let resetButton = document.getElementById("reset");
resetButton.onclick = resetGame;


let res = getState();
for(let k = 0; k < 64; k++){
    let div = document.createElement("div");
    div.id = "pos" + k;
    document.getElementById("board").appendChild(div);
    div.onclick = async () => {
        let res = await makeMove(div.id);
        renderBoard(res.board, []);
        if (res.winner != null) {
            let winner;
            if (res.winner == "X") {
                winner = "black";
                alert("Winner is: black");
            } else if (res.winner == "O") {
                alert("Winner is: white");
                winner = "white";
            } else {
                alert("Tie!");
            }
        }
        // get engine move
        res = await getEngineMove();
        console.log(res);
        console.log('rendering engine move');
        renderBoard(res.board, res.possible_moves);
        if (res.winner != null) {
            let winner;
            if (res.winner == "X") {
                winner = "black";
                alert("Winner is: black");
            } else if (res.winner == "O") {
                alert("Winner is: white");
                winner = "white";
            } else {
                alert("Tie!");
            }
        }
        player_turn = res.to_move;
        if (player_turn == "O"){
            document.getElementById("player-turn").innerText = "white";
        } else {
            document.getElementById("player-turn").innerText = "black";
        }
    }
}

res.then((data) => {
    renderBoard(data.board, data.possible_moves);
    if (data.to_move == "O"){
        document.getElementById("player-turn").innerText = "white";
    } else {
        document.getElementById("player-turn").innerText = "black";
    }
}, (error) => {
    console.log(error);
});

async function getState() {
    let response = await fetch("http://localhost:5000/state", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    let data = await response.json();
    return data;
}

async function getEngineMove() {
    let response = await fetch("http://localhost:5000/engine", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });
    let data = await response.json();
    return data;
}

async function makeMove(position) {
    let response = await fetch("http://localhost:5000/move?pos=" + position, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            position: position
        })
    });
    let data = await response.json();
    console.log(data);
    return data;
}

function placePiece(position, color) {
    let div = document.getElementById(position);
    div.innerHTML = "<img src='static/images/"+ color +".png'>";
}

function renderBoard(board, possible_moves) {
    let blackScore = 0;
    let whiteScore = 0;
    for (let k = 0; k < 64; k++) {
        let div = document.getElementById("pos" + k);
        let color = board[k];
        // Remove any existing classes
        div.classList.remove("possible-move", "default-tile");

        // Add classes based on the board state
        if (possible_moves.includes(k)) {
            div.classList.add("possible-move");
        } else {
            div.classList.add("default-tile");
        }
        if (color == "X") {
            placePiece(div.id, "black");
            blackScore++;
        } else if (color == "O") {
            placePiece(div.id, "white");
            whiteScore++;
        } else {
            div.innerHTML = "";
        }
    }
    document.getElementById("black-score").innerText = blackScore;
    document.getElementById("white-score").innerText = whiteScore;
}

async function resetGame() {
    let response = await fetch("http://localhost:5000/reset", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });
    let data = await response.json();
    console.log(data);
    renderBoard(data.board, data.possible_moves);
    if (data.to_move == "O"){
            document.getElementById("player-turn").innerText = "white";
    } else {
        document.getElementById("player-turn").innerText = "black";
    }
}