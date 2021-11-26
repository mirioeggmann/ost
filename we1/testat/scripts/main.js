import {HANDS, getRankings, evaluateHand, isConnected} from './game-service.js';

// Constants / Configs
const DELAY_MS = 2000;

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
const domHomeSection = document.querySelector('#home-section');
const domHomeSwitchButton = document.querySelector('#home-switch-button');
const domHomeRankingList = document.querySelector('#home-ranking-list');
const domHomeForm = document.querySelector('#home-form');
const domHomeFormNameInput = document.querySelector('#home-form-name-input');

const domGameSection = document.querySelector('#game-section');
const domGameUsernameParagraph = document.querySelector('#game-username-paragraph');
const domGamePlayerHandDiv = document.querySelector('#game-player-hand-div');
const domGameStatusParagraph = document.querySelector('#game-status-paragraph');
const domGameSystemHandParagraph = document.querySelector('#game-system-hand-paragraph');
const domGameSwitchButton = document.querySelector('#game-switch-button');
const domGameHistoryTable = document.querySelector('#game-history-table');

function homeRankingElementHTMLString(ranking) {
    return `<li>${ranking.rank}. Rang mit ${ranking.wins} Siegen : ${ranking.players.join(', ')}</li>`;
}

function gamePlayerHandButtonHTMLString(playerHand) {
    return `<button>${playerHand}</button>`;
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
    const playerHands = domGamePlayerHandDiv.getElementsByTagName('button');
    for (let i = 0; i < playerHands.length; i++) {
        playerHands[i].disabled = true;
    }
}

function enableGameButtons() {
    domGameSwitchButton.disabled = false;
    const playerHands = domGamePlayerHandDiv.getElementsByTagName('button');
    for (let i = 0; i < playerHands.length; i++) {
        playerHands[i].disabled = false;
    }
}

function updateHomeRankingList() {
    getRankings((ranking) => {
        if (activeState === STATE.HOME) {
            if (ranking.length === 0) {
                domHomeRankingList.innerHTML = '<li>Keine Einträge vorhanden.</li>';
            } else {
                domHomeRankingList.innerHTML = ranking.slice(0, 9).map(homeRankingElementHTMLString).join('');
            }
        }
    });
}

function updateGameHistoryTable() {
    const header = `<tr>
                        <th>Resultat</th>
                        <th>Spieler</th>
                        <th>Gegner</th>
                    </tr>`;
    domGameHistoryTable.innerHTML = header + gameHistory.map(gameHistoryRowHTMLString).join('');
}

function initGamePlayerHandDiv() {
    domGamePlayerHandDiv.innerHTML = HANDS.map(gamePlayerHandButtonHTMLString).join('');
}

function updateViewStateHome() {
    updateHomeRankingList();
    domHomeFormNameInput.value = '';
}

function updateViewStatePlayerHand() {
    enableGameButtons();
    domGameUsernameParagraph.textContent = `${username}! Wähle deine Hand!`;
    domGameStatusParagraph.textContent = 'Du bist dran...';
    domGameSystemHandParagraph.textContent = '';
    updateGameHistoryTable();
}

function updateViewStateSystemHand() {
    disableGameButtons();
    domGameStatusParagraph.textContent = 'Computer wählt eine Hand...';
    updateGameHistoryTable();
}

function updateViewStateWaiting() {
    disableGameButtons();
    domGameStatusParagraph.textContent = 'Nächste Runde startet gleich';
    domGameSystemHandParagraph.textContent = `Computer Hand: ${systemHand}`;
    updateGameHistoryTable();
}

const STATE_ACTION = {
    home: () => updateViewStateHome(),
    player_hand: () => updateViewStatePlayerHand(),
    system_hand: () => updateViewStateSystemHand(),
    waiting: () => updateViewStateWaiting(),
};

function updateView() {
    if (activeState === STATE.HOME) {
        domHomeSection.classList.remove('hidden');
        domGameSection.classList.add('hidden');
    } else {
        domHomeSection.classList.add('hidden');
        domGameSection.classList.remove('hidden');
    }
    STATE_ACTION[activeState]();
}

// Controller
function startGame() {
    username = domHomeFormNameInput.value;
    activeState = STATE.PLAYER_HAND;
    updateView();
}

function stopGame() {
    activeState = STATE.HOME;
    username = null;
    gameHistory = [];
    updateView();
}

function chooseHand(playerHand) {
    activeState = STATE.SYSTEM_HAND;
    updateView();
    evaluateHand(username, playerHand, (result) => {
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

domHomeSwitchButton.addEventListener('click', () => {
    isConnected();
});

domHomeForm.addEventListener('submit', (event) => {
    event.preventDefault();
    startGame();
});

domGameSwitchButton.addEventListener('click', () => {
    stopGame();
});

// Event bubbling for player hands
domGamePlayerHandDiv.addEventListener('click', (event) => {
    const playerHand = event.target.innerHTML;
    chooseHand(playerHand);
});

// Init
updateView();
initGamePlayerHandDiv();
