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
const domGameHandSchere = document.getElementById('game-hand-schere');
const domGameHandStein = document.getElementById('game-hand-stein');
const domGameHandPapier = document.getElementById('game-hand-papier');
const domGameHandBrunnen = document.getElementById('game-hand-brunnen');
const domGameHandStreichholz = document.getElementById('game-hand-streichholz');
const domGameStatus = document.getElementById('game-status');
const domGameEnemyHand = document.getElementById('game-enemy-hand');
const domGameSwitchButton = document.getElementById('game-switch-button');
const domGameHistory = document.getElementById('game-history');

function homeRankingElementHTMLString(ranking) {
    return `<li>${ranking.rank}. Rang mit ${ranking.wins} Siegen : ${ranking.players.join(', ')}</li>`;
}

function gameHistoryRowHTMLString(ranking) {
    return `<tr>
                <td>${resultGermanTranslation[ranking.gameEval]}</td>
                <td>${ranking.playerHand}</td>
                <td>${ranking.systemHand}</td>
            </tr>`;
}

// Controller
class Game {
    constructor(gameService) {
        this.gameService = gameService;
        this.state = stateMain;
        this.username = null;
        this.enemy_choice = null;
        this.game_history = [];

        // start page username form submit
        domHomeForm.onsubmit = () => {
            this.playGame(domHomeFormName.value);
            return false; // don't reload page
        };

        // game page back button
        domGameSwitchButton.onclick = () => {
            this.exitGame();
        };

        domGameHandSchere.onclick = () => {
            this.chooseMove('Schere');
        };

        domGameHandStein.onclick = () => {
            this.chooseMove('Stein');
        };

        domGameHandPapier.onclick = () => {
            this.chooseMove('Papier');
        };

        domGameHandBrunnen.onclick = () => {
            this.chooseMove('Brunnen');
        };

        domGameHandStreichholz.onclick = () => {
            this.chooseMove('Streichholz');
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

        // change into battle mode until the enemy has choosen his move
        this.state = stateBattle;
        this.updateView();

        this.gameService.evaluateHand(this.username, choice, (result) => {
            this.enemy_choice = result.systemHand;
            this.game_history.push(result);

            this.state = stateTimeout;
            this.updateView();

            setTimeout(() => {
                this.enemy_choice = null;

                this.state = stateChooseMove;
                this.updateView();
            }, gameDelay);
        });
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
                domGameHandSchere.disabled = false;
                domGameHandStein.disabled = false;
                domGameHandPapier.disabled = false;
                domGameHandBrunnen.disabled = false;
                domGameHandStreichholz.disabled = false;

                domGameUsername.textContent = this.username;
                domGameStatus.textContent = 'Du bist am Zug...';
                domGameEnemyHand.textContent = '??';

                this.updateGameScoreboard();
                break;
            }
            case stateBattle: {
                domGameSwitchButton.disabled = true;
                domGameHandSchere.disabled = true;
                domGameHandStein.disabled = true;
                domGameHandPapier.disabled = true;
                domGameHandBrunnen.disabled = true;
                domGameHandStreichholz.disabled = true;

                domGameStatus.textContent = 'Gegner ist am Zug...';
                this.updateGameScoreboard();
                break;
            }
            case stateTimeout: {
                domGameSwitchButton.disabled = true;
                domGameHandSchere.disabled = true;
                domGameHandStein.disabled = true;
                domGameHandPapier.disabled = true;
                domGameHandBrunnen.disabled = true;
                domGameHandStreichholz.disabled = true;

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
                    domHomeRanking.innerHTML = '<li>Keine Einträge vorhanden.</li>';
                } else {
                    domHomeRanking.innerHTML = ranking.slice(0, 9).map(homeRankingElementHTMLString).join('');
                }
            }
        });
    }

    updateGameScoreboard() {
        const header = `<tr>
                            <th>Resultat</th>
                            <th>Spieler</th>
                            <th>Gegner</th>
                        </tr>`;
        domGameHistory.innerHTML = header + this.game_history.map(gameHistoryRowHTMLString).join('');
    }
}

const game = new Game(libGameService);
game.updateView();
