# Nano MQTT bridge
This tool listens for confirmed blocks via websocket connection to a [Nano Node](https://docs.nano.org/integration-guides/websockets/) and republish them on a MQTT broker.

Only send blocks are published; for each block are published two messages on the following topics, where A is the sender Nano address and B is the recipient Nano address:
```
- nano/A/send
- nano/B/receive
```

This is an example of message published on a topic `nano/#/send`:
```json
{
   "amount":1313000000000000000000000000,
   "hash":"1332CB85224E211E64CAAA791DFFE81C5956184C186159097F1E1096D27AAD92",
   "recipient":"nano_39aqzw9o5o5pj3jpejgz1gze1g81ems335jaqoq5j3ustqqj3q5kws7q3jh5"
}
```

This is an example of message published on a topic `nano/#/receive`:
```json
{
   "amount":1313000000000000000000000000,
   "hash":"1332CB85224E211E64CAAA791DFFE81C5956184C186159097F1E1096D27AAD92",
   "sender":"nano_34prihdxwz3u4ps8qjnn14p7ujyewkoxkwyxm3u665it8rg5rdqw84qrypzk"
}
```

In these examples the Nano amount and the block hash are the same, because they both refer to [this send block](https://nanocrawler.cc/explorer/block/1332CB85224E211E64CAAA791DFFE81C5956184C186159097F1E1096D27AAD92).

Note that Nano protocol requires a send block and a receive block to fulfill a transaction, however in most cases there's no need to wait for the receive block, as the send block cannot be reversed and the transaction can stay in a pending state for an indefinite period of time.

This tool ignores the receive transactions, but consider a transaction as received as soon the send block are confirmed.
