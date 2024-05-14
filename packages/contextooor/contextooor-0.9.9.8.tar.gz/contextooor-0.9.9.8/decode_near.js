const borsh = require('borsh');
const nearAPI = require('near-api-js');
const {transactions} = nearAPI;

const base64 = require('base64-js');

function decodeTransaction(encodedTx) {
    const txBuffer = base64.toByteArray(encodedTx);
    const transaction = borsh.deserialize(transactions.SCHEMA.Transaction, txBuffer);
    return transaction;
}

const encodedTx = "EQAAAGRhdnlqb25lcy50ZXN0bmV0ACaDxiBTp9kQxrzNthh62vSUMhSR5dpNESO6UGbHy+nmBwAAAAAAAAARAAAAdGVxdWlsYTIwLnRlc3RuZXS2iuUYet0GQlk9+TZ4/5TkPP4M8rpGQ749LzkYk+YEvQEAAAADAABAsrrJ4BkeAgAAAAAAAA==";
const transaction = decodeTransaction(encodedTx);
console.log(transaction);