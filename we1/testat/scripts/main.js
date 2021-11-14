import {HANDS, getRankings, evaluateHand, isConnected} from './game-service.js';

// Constants / Configs
const DELAY_MS = 2000;

const HAND = {
    SCISSORS: HANDS[0],
    STONE: HANDS[1],
    PAPER: HANDS[2],
    FOUNTAIN: HANDS[3],
    MATCH: HANDS[4],
};

const STATE = {
    HOME: 'home',
    PLAYER_HAND: 'player_hand',
    SYSTEM_HAND: 'system_hand',
    WAITING: 'waiting',
};

const RESULT_LOOKUP = {
    '-1': 'Gewonnen',
    0: 'Unentschieden',
    1: 'Verloren',
};

// Model / State
let activeState = STATE.HOME;
let username = null;
let systemHand = null;
let gameHistory = [];

// View
const domHome = document.querySelector('#home');
const domHomeSwitchButton = document.querySelector('#home-switch-button');
const domHomeRanking = document.querySelector('#home-ranking');
const domHomeForm = document.querySelector('#home-form');
const domHomeFormName = document.querySelector('#home-form-name');

const domGame = document.querySelector('#game');
const domGameUsername = document.querySelector('#game-username');
const domGameHandScissors = document.querySelector('#game-hand-scissors');
const domGameHandStone = document.querySelector('#game-hand-stone');
const domGameHandPaper = document.querySelector('#game-hand-paper');
const domGameHandFountain = document.querySelector('#game-hand-fountain');
const domGameHandMatch = document.querySelector('#game-hand-match');
const domGameStatus = document.querySelector('#game-status');
const domGameSystemHand = document.querySelector('#game-system-hand');
const domGameSwitchButton = document.querySelector('#game-switch-button');
const domGameHistory = document.querySelector('#game-history');

function homeRankingElementHTMLString(ranking) {
    return `<li>${ranking.rank}. Rang mit ${ranking.wins} Siegen : ${ranking.players.join(', ')}</li>`;
}

function gameHistoryRowHTMLString(ranking) {
    return `<tr>
                <td>${RESULT_LOOKUP[ranking.gameEval]}</td>
                <td>${ranking.playerHand}</td>
                <td>${ranking.systemHand}</td>
            </tr>`;
}

function disableGameButtons() {
    domGameSwitchButton.disabled = true;
    domGameHandScissors.disabled = true;
    domGameHandStone.disabled = true;
    domGameHandPaper.disabled = true;
    domGameHandFountain.disabled = true;
    domGameHandMatch.disabled = true;
}

function enableGameButtons() {
    domGameSwitchButton.disabled = false;
    domGameHandScissors.disabled = false;
    domGameHandStone.disabled = false;
    domGameHandPaper.disabled = false;
    domGameHandFountain.disabled = false;
    domGameHandMatch.disabled = false;
}

function updateHomeRanking() {
    getRankings((ranking) => {
        if (activeState === STATE.HOME) {
            if (ranking.length === 0) {
                domHomeRanking.innerHTML = '<li>Keine Einträge vorhanden.</li>';
            } else {
                domHomeRanking.innerHTML = ranking.slice(0, 9).map(homeRankingElementHTMLString).join('');
            }
        }
    });
}

function updateGameHistory() {
    const header = `<tr>
                        <th>Resultat</th>
                        <th>Spieler</th>
                        <th>Gegner</th>
                    </tr>`;
    domGameHistory.innerHTML = header + gameHistory.map(gameHistoryRowHTMLString).join('');
}

function updateViewStateHome() {
    updateHomeRanking();
    domHomeFormName.value = '';
}

function updateViewStatePlayerHand() {
    enableGameButtons();
    domGameUsername.textContent = username;
    domGameStatus.textContent = 'Du bist dran...';
    domGameSystemHand.textContent = '';
    updateGameHistory();
}

function updateViewStateSystemHand() {
    disableGameButtons();
    domGameStatus.textContent = 'Computer wählt eine Hand...';
    updateGameHistory();
}

function updateViewStateWaiting() {
    disableGameButtons();
    domGameStatus.textContent = 'Nächste Runde startet gleich';
    domGameSystemHand.textContent = `Computer Hand: ${systemHand}`;
    updateGameHistory();
}

function updateView() {
    if (activeState === STATE.HOME) {
        domHome.classList.remove('hidden');
        domGame.classList.add('hidden');
    } else {
        domHome.classList.add('hidden');
        domGame.classList.remove('hidden');
    }
    if (activeState === STATE.HOME) {
        updateViewStateHome();
    } else if (activeState === STATE.PLAYER_HAND) {
        updateViewStatePlayerHand();
    } else if (activeState === STATE.SYSTEM_HAND) {
        updateViewStateSystemHand();
    } else if (activeState === STATE.WAITING) {
        updateViewStateWaiting();
    }
}

// Controller
function startGame() {
    username = domHomeFormName.value;
    activeState = STATE.PLAYER_HAND;
    updateView();
}

function stopGame() {
    activeState = STATE.HOME;
    username = null;
    gameHistory = [];
    updateView();
}

function chooseHand(hand) {
    activeState = STATE.SYSTEM_HAND;
    updateView();
    evaluateHand(username, hand, (result) => {
        systemHand = result.systemHand;
        gameHistory.push(result);
        activeState = STATE.WAITING;
        updateView();
        setTimeout(() => {
            systemHand = null;
            activeState = STATE.PLAYER_HAND;
            updateView();
        }, DELAY_MS);
    });
}

domHomeSwitchButton.onclick = () => {
    isConnected();
};

domHomeForm.onsubmit = () => {
    startGame();
    // to stop page from reloading
    return false;
};

domGameSwitchButton.onclick = () => {
    stopGame();
};

domGameHandScissors.onclick = () => {
    chooseHand(HAND.SCISSORS);
};

domGameHandStone.onclick = () => {
    chooseHand(HAND.STONE);
};

domGameHandPaper.onclick = () => {
    chooseHand(HAND.PAPER);
};

domGameHandFountain.onclick = () => {
    chooseHand(HAND.FOUNTAIN);
};

domGameHandMatch.onclick = () => {
    chooseHand(HAND.MATCH);
};

// Init
updateView();
