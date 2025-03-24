
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
// create board with starting pieces
let res = getState();
for(let k = 0; k < 64; k++){
    let div = document.createElement("div");
    div.id = "pos" + k;
    document.getElementById("board").appendChild(div);
    div.onclick = async () => {
        let id_string = ""+div.id
        let res = await makeMove(div.id);
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
    for(let k = 0; k < 64; k++){
        let div = document.getElementById("pos" + k);
        let color = board[k];
        if(possible_moves.includes(k)){
            div.style.backgroundColor = "yellow";
        } else {
            div.style.backgroundColor = "green";
        }
        if(color == "X"){
            placePiece(div.id, "black");
        }
        if(color == "O"){
            placePiece(div.id, "white");
        }
    }
}