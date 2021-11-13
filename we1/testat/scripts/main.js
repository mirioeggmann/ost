import {
    HANDS,
    setConnected,
    isConnected,
    getRankings,
    evaluateHand,
    RESULT_WIN,
    RESULT_TIE,
    RESULT_LOSE,
} from './game-service.js';

// Model / State
const libGameService = {
    HANDS,
    setConnected,
    isConnected,
    getRankings,
    evaluateHand,
};

const stateMain = 0;
const stateChooseMove = 1;
const stateBattle = 2;
const stateTimeout = 3;

const gameDelay = 1500;

const resultGermanTranslation = {
    [RESULT_WIN]: 'Gewonnen',
    [RESULT_TIE]: 'Unentschieden',
    [RESULT_LOSE]: 'Verloren',
};

// View
const domHome = document.getElementById('home');
const domHomeSwitchButton = document.getElementById('home-switch-button');
const domHomeRanking = document.getElementById('home-ranking');
const domHomeForm = document.getElementById('home-form');
const domHomeFormName = document.getElementById('home-form-name');

const domGame = document.getElementById('game');
const domGameUsername = document.getElementById('game-username');
const domGameHand = document.getElementById('game-hand');
const domGameStatus = document.getElementById('game-status');
const domGameEnemyHand = document.getElementById('game-enemy-hand');
const domGameSwitchButton = document.getElementById('game-switch-button');
const domGameHistory = document.getElementById('game-history');

function homeRankingHTMLString(ranking) {
    return `<li>${ranking.rank}. Rang mit ${ranking.wins} Siegen : ${ranking.players.join(', ')}</li>`;
}

function createGameScoreboardEntryNode(ranking) {
    const node = document.createElement('tr');

    const result = document.createElement('td');
    const userHand = document.createElement('td');
    const enemyHand = document.createElement('td');

    result.dataset.gameEval = ranking.gameEval;

    result.textContent = resultGermanTranslation[ranking.gameEval];
    userHand.textContent = ranking.playerHand;
    enemyHand.textContent = ranking.systemHand;

    node.appendChild(result);
    node.appendChild(userHand);
    node.appendChild(enemyHand);

    return node;
}

function createUserChoiceButton(name) {
    const node = document.createElement('button');

    node.classList.add('big-button');
    node.textContent = name;
    node.dataset.choiceName = name;

    return node;
}

// Controller
class StonePaperScissorGame {
    constructor(gameService) {
        this.gameService = gameService;
        this.state = stateMain;
        this.username = null;
        this.choice_buttons = [];
        this.user_choice = null;
        this.enemy_choice = null;
        this.game_eval = null;
        this.game_history = [];

        this.selected_choice_dom_button = null;

        // mode switch button
        domHomeSwitchButton.onclick = () => {
            this.toggleMode();
        };

        // start page username form submit
        domHomeForm.onsubmit = () => {
            this.playGame(domHomeFormName.value);
            return false; // don't reload page
        };

        // game page back button
        domGameSwitchButton.onclick = () => {
            this.exitGame();
        };

        // inject user choice buttons into the user choice container div
        for (let i = 0; i < this.gameService.HANDS.length; i++) {
            const choice = this.gameService.HANDS[i];
            const choiceButton = createUserChoiceButton(choice);
            this.choice_buttons.push(choiceButton);
            domGameHand.appendChild(choiceButton);
        }

        // listen for bubbling click events
        domGameHand.onclick = (event) => {
            if (event.target.nodeName === 'BUTTON') {
                this.chooseMove(event.target.dataset.choiceName);
            }
        };

        this.updateView();
    }

    playGame(username) {
        if (this.state !== stateMain) {
            throw new Error('Invalider Spielzustand!');
        }

        this.state = stateChooseMove;
        this.username = username;
        this.updateView();
    }

    exitGame() {
        if (this.state !== stateChooseMove) {
            throw new Error('Invalider Spielzustand!');
        }

        this.state = stateMain;
        this.username = null;
        this.game_history = [];
        this.updateView();
    }

    chooseMove(choice) {
        if (this.state !== stateChooseMove) {
            throw new Error('Invalider Spielzustand!');
        }

        this.user_choice = choice;

        // change into battle mode until the enemy has choosen his move
        this.state = stateBattle;
        this.updateView();

        this.gameService.evaluateHand(this.username, choice, (result) => {
            this.enemy_choice = result.systemHand;
            this.game_eval = result.gameEval;
            this.game_history.push(result);

            this.state = stateTimeout;
            this.updateView();

            setTimeout(() => {
                this.user_choice = null;
                this.enemy_choice = null;
                this.game_eval = null;
                this.selected_choice_dom_button = null;

                this.state = stateChooseMove;
                this.updateView();
            }, gameDelay);
        });
    }

    toggleMode() {
        if (this.state === stateMain) {
            const isOnline = this.gameService.isConnected();
            this.gameService.setConnected(!isOnline);
            this.updateView();
        }
    }

    updateView() {
        // hide or show relevant game pages
        if (this.state === stateMain) {
            domHome.classList.remove('hidden');
            domGame.classList.add('hidden');
        } else {
            domHome.classList.add('hidden');
            domGame.classList.remove('hidden');
        }

        switch (this.state) {
            case stateMain: {
                this.updateRanking();

                // update mode toggle button message
                if (this.gameService.isConnected()) {
                    domHomeSwitchButton.textContent = 'Wechsel zur Lokal';
                } else {
                    domHomeSwitchButton.textContent = 'Wechsel zur Server';
                }

                domHomeFormName.value = '';

                break;
            }
            case stateChooseMove: {
                domGameSwitchButton.disabled = false;

                for (let i = 0; i < this.choice_buttons.length; i++) {
                    const button = this.choice_buttons[i];
                    button.disabled = false;
                    button.classList.remove('selected_by_user', 'winning_choice', 'tie_choice', 'lost_choice');
                }

                domGameEnemyHand.classList.remove('winning_choice', 'tie_choice', 'lost_choice');

                domGameUsername.textContent = this.username;
                domGameStatus.textContent = 'Du bist am Zug...';
                domGameEnemyHand.textContent = '??';
                this.updateGameScoreboard();
                break;
            }
            case stateBattle: {
                for (let i = 0; i < this.choice_buttons.length; i++) {
                    const button = this.choice_buttons[i];
                    button.disabled = true;

                    if (button.dataset.choiceName === this.user_choice) {
                        button.classList.add('selected_by_user');
                        this.selected_choice_dom_button = button;
                    }
                }
                domGameSwitchButton.disabled = true;

                domGameStatus.textContent = 'Gegner ist am Zug...';
                this.updateGameScoreboard();
                break;
            }
            case stateTimeout: {
                for (let i = 0; i < this.choice_buttons.length; i++) {
                    const button = this.choice_buttons[i];
                    button.disabled = true;
                }
                domGameSwitchButton.disabled = true;

                this.selected_choice_dom_button.classList.remove('selected_by_user');

                switch (this.game_eval) {
                    case RESULT_WIN: { // won
                        this.selected_choice_dom_button.classList.add('winning_choice');
                        domGameEnemyHand.classList.add('lost_choice');
                        break;
                    }
                    case RESULT_TIE: { // tie
                        this.selected_choice_dom_button.classList.add('tie_choice');
                        domGameEnemyHand.classList.add('tie_choice');
                        break;
                    }
                    case RESULT_LOSE: { // lost
                        this.selected_choice_dom_button.classList.add('lost_choice');
                        domGameEnemyHand.classList.add('winning_choice');
                        break;
                    }
                    default: {
                        throw new Error('unexpected value');
                    }
                }

                domGameStatus.textContent = 'Nächste Runde beginnt in Kürze';
                domGameEnemyHand.textContent = this.enemy_choice;
                this.updateGameScoreboard();
                break;
            }
            default: {
                throw new Error('unexpected state');
            }
        }
    }

    updateRanking() {
        this.gameService.getRankings((ranking) => {
            if (this.state === stateMain) {
                if (ranking.length === 0) {
                    domHomeRanking.innerHTML = `<li>Keine Einträge vorhanden.</li>`;
                } else {
                    domHomeRanking.innerHTML = ranking.slice(0, 9).map(homeRankingHTMLString).join('');
                }
            }
        });
    }

    updateGameScoreboard() {
        // remove all the previous entries, except for the table header
        // TODO
        while (domGameHistory.childElementCount > 1) {
            domGameHistory.removeChild(domGameHistory.lastElementChild);
        }

        // insert new entries
        for (let i = 0; i < this.game_history.length; i++) {
            const result = this.game_history[i];
            const resultDomNode = createGameScoreboardEntryNode(result);
            domGameHistory.appendChild(resultDomNode);
        }
    }
}

// wait for the document to be ready
document.addEventListener('DOMContentLoaded', () => {
    const game = new StonePaperScissorGame(libGameService);
    game.updateView();
});
