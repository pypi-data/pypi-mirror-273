const nearAPI = require('near-api-js');
const { connect, transactions, utils, keyStores } = nearAPI;
const path = require('path');
const os = require('os');


const credentialsPath = path.join(os.homedir(), '.near-credentials');
const keyStore = new keyStores.UnencryptedFileSystemKeyStore(credentialsPath);
// Configuration for NEAR blockchain connection
const config = {
    networkId: "testnet",
    keyStore: keyStore, // For this example, we'll use an in-memory keystore
    nodeUrl: "https://rpc.testnet.near.org",
    walletUrl: "https://wallet.testnet.near.org",
    helperUrl: "https://helper.testnet.near.org",
    explorerUrl: "https://explorer.testnet.near.org",
};

// Function to create and serialize a transfer transaction
async function createTransferTransaction(senderAccountId, receiverAccountId, amount) {
    // Connect to NEAR
    const near = await connect(config);
    const senderAccount = await near.account(senderAccountId);

    // Get the public key and nonce for the transaction
    const publicKey = (await senderAccount.getAccessKeys())[0].public_key; // Using the first access key for simplicity
    const nonce = 7;
    const recentBlockHash = utils.serialize.base_decode((await senderAccount.connection.provider.block({ finality: 'final' })).header.hash);

    // Create the transaction with a transfer action
    const actions = [transactions.transfer(amount)];
    const transaction = transactions.createTransaction(
        senderAccountId,
        utils.PublicKey.fromString(publicKey),
        receiverAccountId,
        nonce,
        actions,
        recentBlockHash
    );

    // Serialize the transaction
    return utils.serialize.serialize(transactions.SCHEMA.Transaction, transaction);
}

// Function to encode and log the serialized transaction
async function encodeTransaction() {
    const senderAccountId = 'davyjones.testnet'; // Replace with actual sender account ID
    const receiverAccountId = 'tequila20.testnet'; // Replace with actual receiver account ID
    const amount = utils.format.parseNearAmount('0.01'); // Sending 1 NEAR

    // Create and serialize the transaction
    const serializedTx = await createTransferTransaction(senderAccountId, receiverAccountId, amount);

    // Encode to Base64
    const encodedTxBase64 = Buffer.from(serializedTx).toString('base64');
    console.log('Encoded Transaction (Base64):', encodedTxBase64);
}

encodeTransaction().catch(console.error);