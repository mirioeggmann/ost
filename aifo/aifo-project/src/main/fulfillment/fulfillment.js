'use strict';

const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const rp = require('request-promise');
const admin = require('firebase-admin');

process.env.DEBUG = 'dialogflow:debug';

admin.initializeApp(functions.config().firebase);
const db = admin.firestore();

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
    const agent = new WebhookClient({ request, response });
    console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
    console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

    // TODO in future take and safe in db
    function convertCurrencyHandler(agent) {
        const currencyFrom = agent.parameters.currencyFrom;
        const currencyTo = agent.parameters.currencyTo;
        const amount = JSON.stringify(agent.parameters.amount);

        const requestOptions = {
            method: 'GET',
            uri: 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion',
            qs: {'symbol': currencyFrom, 'convert': currencyTo, 'amount': amount},
            headers: {'X-CMC_PRO_API_KEY': '6bb28d89-de08-405e-9c40-65d767fb737f'},
            json: true,
            gzip: true
        };

        return rp(requestOptions).then(response => {
            console.log('API call response:', response);
            console.log(response.data.quote[currencyTo].price);
            let price = response.data.quote[currencyTo].price;
            agent.add(`According to Coinmarketap ${amount} ${currencyFrom} will get you ${price} ${currencyTo}`);
        }).catch((err) => {
            console.log('API call error:', err.message);
            agent.add(`Error occured`);
        });
    }

    function depositCurrencyHandler(agent) {
        const email = agent.parameters.email;
        const currency = agent.parameters.currency;
        const amount = agent.parameters.amount;

        const currencyRef = db.collection('portfolio').doc(email).collection('currency').doc(currency);
        balance: firebase.firestore.FieldValue.increment(amount)
        return currencyRef.get()
            .then(doc => {
                let balance = JSON.stringify(doc.data().balance);
                let newBalance = parseFloat(balance) + parseFloat(amount);
                return currencyRef
                    .set({balance: newBalance})
                    .then(() => agent.add(`deposited ${amount} ${currency}`))
                    .catch(() => agent.add(`deposit failed.`));
            }).catch((err) => {
                console.log(err);
                agent.add(`Error occured fetching value of ${currency}`);
            });
    }

    function withdrawCurrencyHandler(agent) {
        const email = agent.parameters.email;
        const currency = agent.parameters.currency;
        const amount = agent.parameters.amount;

        return db.collection('portfolio').doc(email).collection('currency').doc(currency).get()
            .then(doc => {
                let balance = JSON.stringify(doc.data().balance);
                if (parseFloat(balance) >= parseFloat(amount)) {
                    let newBalance = parseFloat(balance) - parseFloat(amount);
                    return db.collection('portfolio').doc(email).collection('currency').doc(currency)
                        .set({balance: newBalance}).then(() => {
                            agent.add(`withdraw ${amount} ${currency} from ${email}`);
                        }).catch(() => {
                            agent.add(`withdraw failed.`);
                        });
                } else {
                    agent.add(`Balance: ${balance} cannot witdraw ${amount}`);
                }
            }).catch((err) => {
                console.log(err);
                agent.add(`Error occured fetching the current value of ${currency}`);
            });
    }

    function createPortfolioHandler(agent) {
        const email = agent.parameters.email;

        const btcDoc = db.collection('portfolio').doc(email).collection('currency').doc('BTC');
        const ethDoc = db.collection('portfolio').doc(email).collection('currency').doc('ETH');
        const xlmDoc = db.collection('portfolio').doc(email).collection('currency').doc('XLM');
        const adaDoc = db.collection('portfolio').doc(email).collection('currency').doc('ADA');
        const eurDoc = db.collection('portfolio').doc(email).collection('currency').doc('EUR');
        const usdDoc = db.collection('portfolio').doc(email).collection('currency').doc('USD');
        console.log('test1');
        agent.add(`created portfolio`);
        console.log('test2');
        return btcDoc
            .set({balance: 0})
            .then(() => {
                return ethDoc.set({balance: 0});
            })
            .then(() => {
                return xlmDoc.set({balance: 0});
            })
            .then(() => {
                return adaDoc.set({balance: 0});
            })
            .then(() => {
                return eurDoc.set({balance: 0});
            })
            .then(() => {
                return usdDoc.set({balance: 0});
            })
            .then(() => {
                console.log('test3');
            })
            .catch(() => {
                console.log('failed');
            });
    }

    function listPortfolioHandler(agent) {
        const email = agent.parameters.email;

        const currencyCol = db.collection('portfolio').doc(email).collection('currency');
        let balances = '';

        return currencyCol
            .get()
            .then((docs) => {
                console.log('test2');
                return docs.forEach((doc) => {
                    console.log('test3');
                    balances = balances + doc.id + ': ' + JSON.stringify(doc.data().balance) + ' \n';
                    console.log(balances);
                });
            }).then(() => {
                agent.add(balances);
            });
    }

    function fallback(agent) {
        agent.add(`I didn't understand`);
        agent.add(`I'm sorry, can you try again?`);
    }

    let intentMap = new Map();
    intentMap.set('currency.deposit', depositCurrencyHandler);
    intentMap.set('currency.withdraw', withdrawCurrencyHandler);
    intentMap.set('currency.convert', convertCurrencyHandler);
    intentMap.set('portfolio.create', createPortfolioHandler);
    intentMap.set('portfolio.list',listPortfolioHandler);
    intentMap.set('Default Fallback Intent', fallback);
    agent.handleRequest(intentMap);
});