const DELAY_MS = 1000;
const playerStats = {};

function getRankingsFromPlayerStats() {
    const playerNames = Object.keys(playerStats);
    let ranking = [];
    playerNames.forEach((playerName) => {
        const playerInfo = playerStats[playerName];
        if (ranking[playerInfo.win] === undefined) {
            ranking[playerInfo.win] = {
                rank: null,
                wins: playerInfo.win,
                players: [playerInfo.user],
            };
        } else {
            ranking[playerInfo.win].players.push(playerInfo.user);
        }
    });
    ranking = ranking.filter((element) => element !== null);
    ranking.sort((left, right) => right.wins - left.wins);
    ranking.forEach((element, index) => {
        element.rank = index + 1;
    });
    return ranking;
}

export const HANDS = ['Schere', 'Stein', 'Papier', 'Brunnen', 'Streichholz'];

let isConnectedState = false;

export function setConnected(newIsConnected) {
    isConnectedState = Boolean(newIsConnected);
}

export function isConnected() {
    return isConnectedState;
}

export async function getRankings(rankingsCallbackHandlerFn) {
    const rankingsArray = getRankingsFromPlayerStats();
    setTimeout(() => rankingsCallbackHandlerFn(rankingsArray), DELAY_MS);
}

const RESULT_WIN = -1;
const RESULT_TIE = 0;
const RESULT_LOSE = 1;

const evalLookup = {
    Schere: {
        Schere: RESULT_TIE,
        Stein: RESULT_LOSE,
        Papier: RESULT_WIN,
        Brunnen: RESULT_LOSE,
        Streichholz: RESULT_WIN,
    },
    Stein: {
        Schere: RESULT_WIN,
        Stein: RESULT_TIE,
        Papier: RESULT_LOSE,
        Brunnen: RESULT_LOSE,
        Streichholz: RESULT_WIN,
    },
    Papier: {
        Schere: RESULT_LOSE,
        Stein: RESULT_WIN,
        Papier: RESULT_TIE,
        Brunnen: RESULT_WIN,
        Streichholz: RESULT_LOSE,
    },
    Brunnen: {
        Schere: RESULT_WIN,
        Stein: RESULT_WIN,
        Papier: RESULT_LOSE,
        Brunnen: RESULT_TIE,
        Streichholz: RESULT_LOSE,
    },
    Streichholz: {
        Schere: RESULT_LOSE,
        Stein: RESULT_LOSE,
        Papier: RESULT_WIN,
        Brunnen: RESULT_WIN,
        Streichholz: RESULT_TIE,
    },
};

function getGameEval(playerHand, systemHand) {
    return evalLookup[playerHand][systemHand];
}

export async function evaluateHand(playerName, playerHand, gameRecordHandlerCallbackFn) {
    const systemHand = HANDS[Math.floor(Math.random() * HANDS.length)];
    const gameEval = getGameEval(playerHand, systemHand);
    if (playerStats[playerName] === undefined) {
        playerStats[playerName] = {
            user: playerName,
            win: 0,
            lost: 0,
        };
    }
    if (gameEval === RESULT_WIN) {
        playerStats[playerName].win++;
    } else if (gameEval === RESULT_LOSE) {
        playerStats[playerName].lost++;
    }
    setTimeout(() => gameRecordHandlerCallbackFn({playerHand, systemHand, gameEval}), DELAY_MS);
}
