const DELAY_MS = 750;

const playerStats = {};

function getRankingsFromPlayerStats(stats) {
    const playerNames = Object.keys(stats);

    // compute the ranking
    let ranking = [];
    for (let i = 0; i < playerNames.length; i++) {
        const playerName = playerNames[i];
        const playerInfo = stats[playerName];

        if (ranking[playerInfo.win] === undefined) {
            ranking[playerInfo.win] = {rank: null, wins: playerInfo.win, players: [playerInfo.user]};
        } else {
            ranking[playerInfo.win].players.push(playerInfo.user);
        }
    }

    // remove holes from ranking array
    ranking = ranking.filter((element) => element !== null);

    // sort by win amount
    ranking.sort((lhs, rhs) => rhs.wins - lhs.wins);

    // set rank property
    for (let i = 0; i < ranking.length; i++) {
        ranking[i].rank = i + 1;
    }

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
    const rankingsArray = getRankingsFromPlayerStats(playerStats);
    setTimeout(() => rankingsCallbackHandlerFn(rankingsArray), DELAY_MS);
}

export const RESULT_WIN = -1;
export const RESULT_TIE = 0;
export const RESULT_LOSE = 1;
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

function updateLocalRanking(playerName, gameEval) {
    // initialize a record for the player
    if (playerStats[playerName] === undefined) {
        playerStats[playerName] = {
            user: playerName,
            win: 0,
            lost: 0,
        };
    }

    // update scoreboard
    if (gameEval === RESULT_WIN) {
        playerStats[playerName].win++;
    } else if (gameEval === RESULT_LOSE) {
        playerStats[playerName].lost++;
    }
}

export async function evaluateHand(playerName, playerHand, gameRecordHandlerCallbackFn) {
    const systemHand = HANDS[Math.floor(Math.random() * HANDS.length)];
    const gameEval = getGameEval(playerHand, systemHand);
    updateLocalRanking(playerName, gameEval);
    setTimeout(() => gameRecordHandlerCallbackFn({playerHand, systemHand, gameEval}), DELAY_MS);
}
