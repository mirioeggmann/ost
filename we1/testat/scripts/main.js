import {HANDS, getRankings, evaluateHand, isConnected, setConnected} from './game-service.js';

// Constants / Configs
const DELAY_MS = 2000;

const STATE = {
    HOME: 'home',
    PLAYER_HAND: 'player_hand',
    SYSTEM_HAND: 'system_hand',
    WAITING: 'waiting',
};

const RESULT_SYMBOL_LOOKUP = {
    '-1': '✓',
    0: '=',
    1: '✗',
};

const RESULT_CLASS_LOOKUP = {
    '-1': 'game-history-result-win',
    0: 'game-history-result-tie',
    1: 'game-history-result-lose',
};

const CONNECTED_LOOKUP = {
    true: 'Wechsle zu Lokal',
    false: 'Wechsle zu Server',
};

// Model / State
let activeState = STATE.HOME;
let username = null;
let systemHand = null;
let playerHand = null;
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
const domGamePlayerHandParagraph = document.querySelector('#game-player-hand-paragraph');
const domGameStatusParagraph = document.querySelector('#game-status-paragraph');
const domGameSystemHandParagraph = document.querySelector('#game-system-hand-paragraph');
const domGameSwitchButton = document.querySelector('#game-switch-button');
const domGameHistoryTable = document.querySelector('#game-history-table');

function homeRankingElementHTMLString(ranking) {
    return `<li>${ranking.rank}. Rang mit ${ranking.wins} Siegen : ${ranking.players.join(', ')}</li>`;
}

function gamePlayerHandButtonHTMLString(gameHand) {
    return `<button>${gameHand}</button>`;
}

function gameHistoryRowHTMLString(ranking) {
    return `<tr>
                <td class="${RESULT_CLASS_LOOKUP[ranking.gameEval]}">${RESULT_SYMBOL_LOOKUP[ranking.gameEval]}</td>
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

function countDown() {
    let counter = 2;
    const countdown = setInterval(() => {
        if (counter <= 0) {
            clearInterval(countdown);
        } else {
            domGameStatusParagraph.textContent = `Nächste Runde in ${counter}`;
        }
        counter -= 1;
    }, DELAY_MS / 3);
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
    domGamePlayerHandParagraph.textContent = 'Player Hand: ?';
    domGameStatusParagraph.textContent = 'VS';
    domGameSystemHandParagraph.textContent = 'Computer Hand: ?';
    updateGameHistoryTable();
}

function updateViewStateSystemHand() {
    disableGameButtons();
    domGamePlayerHandParagraph.textContent = `Player Hand: ${playerHand}`;
    updateGameHistoryTable();
}

function updateViewStateWaiting() {
    disableGameButtons();
    domGameSystemHandParagraph.textContent = `Computer Hand: ${systemHand}`;
    countDown();
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

function chooseHand() {
    activeState = STATE.SYSTEM_HAND;
    updateView();
    evaluateHand(username, playerHand, (result) => {
        systemHand = result.systemHand;
        gameHistory.push(result);
        activeState = STATE.WAITING;
        updateView();
        setTimeout(() => {
            systemHand = null;
            playerHand = null;
            activeState = STATE.PLAYER_HAND;
            updateView();
        }, DELAY_MS);
    });
}

function changeMode() {
    setConnected(!isConnected());
    domHomeSwitchButton.textContent = CONNECTED_LOOKUP[isConnected()];
    updateView();
}

domHomeSwitchButton.addEventListener('click', () => {
    changeMode();
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
    playerHand = event.target.innerHTML;
    chooseHand();
});

// Init
updateView();
initGamePlayerHandDiv();
