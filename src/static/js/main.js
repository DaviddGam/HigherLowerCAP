let score = 0;
let highScore = localStorage.getItem("highScore") || 0;
const scoreEl = document.getElementById("score");
const resultEl = document.getElementById("result");

let currentPlayers = {};  // {player1: {}, player2: {}}

// Mostrar el highscore en pantalla
function renderHighScore() {
    let hsEl = document.getElementById("highscore");
    if (!hsEl) {
        hsEl = document.createElement("div");
        hsEl.id = "highscore";
        document.querySelector(".score-board").appendChild(hsEl);
    }
    hsEl.innerText = `Récord: ${highScore}`;
}

// Cargar dos jugadores iniciales
async function loadInitialPlayers() {
    const res = await fetch("/get_players");
    const data = await res.json();
    currentPlayers = data;
    renderPlayers();
    renderHighScore();
}

// Cargar solo un nuevo player2
async function loadNextPlayer() {
    const res = await fetch(`/get_players?exclude=${currentPlayers.player1.id}`);
    const data = await res.json();
    currentPlayers.player2 = data.player2;
    renderPlayers();
}

// Mostrar jugadores en pantalla
function renderPlayers() {
    // Player 1
    const p1Img = document.getElementById("player1").querySelector("img");
    document.getElementById("name1").innerText = currentPlayers.player1.name;
    document.getElementById("goals1").innerText = `Goles: ${currentPlayers.player1.goals}`;
    p1Img.src = `/static/images/${currentPlayers.player1.id}.jpg`;

    // Player 2
    const p2Img = document.getElementById("player2").querySelector("img");
    document.getElementById("name2").innerText = currentPlayers.player2.name;
    document.getElementById("goals2").innerText = `Goles: ?`;
    p2Img.src = `/static/images/${currentPlayers.player2.id}.jpg`;

    p2Img.classList.remove("flip");
}

// Verificar la predicción
function checkGuess(guess) {
    const g1 = currentPlayers.player1.goals;
    const g2 = currentPlayers.player2.goals;

    const p2Img = document.getElementById("player2").querySelector("img");
    document.getElementById("goals2").innerText = `Goles: ${g2}`;
    p2Img.classList.add("flip");

    if ((guess === "higher" && g2 > g1) || 
        (guess === "lower" && g2 < g1) || 
        (g2 === g1)) {
        
        score++;
        scoreEl.innerText = score;
        resultEl.innerText = "✅ Correcto!";

        // Preparar siguiente ronda
        currentPlayers.player1 = currentPlayers.player2;
        setTimeout(loadNextPlayer, 800);
    } else {
        resultEl.innerText = `❌ Incorrecto! Era ${g2}`;

        // Actualizar highscore solo al perder
        if (score > highScore) {
            highScore = score;
            localStorage.setItem("highScore", highScore);
        }

        score = 0;
        scoreEl.innerText = score;
        renderHighScore();

        setTimeout(loadInitialPlayers, 1000);
    }
}

// Event listeners
document.getElementById("higher").addEventListener("click", () => checkGuess("higher"));
document.getElementById("lower").addEventListener("click", () => checkGuess("lower"));

// Cargar primera ronda
loadInitialPlayers();
