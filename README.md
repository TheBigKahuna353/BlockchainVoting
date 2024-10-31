# Voting System using a blockchain

This project is a Python-based blockchain voting system designed to securely record and verify votes while ensuring data integrity and transparency. Each voter is assigned a unique voter_id upon registration, which is used for casting votes on the blockchain. Votes are stored as individual transactions within blocks, and nodes validate blocks to maintain consistency across the network. By leveraging blockchain’s decentralized and immutable structure, the system prevents tampering, enables easy auditing of votes, and ensures that each voter can only vote once
 
# Privacy

Users register to receive a unique voter_id, which acts as their private identifier and should remain confidential. No personal information is required, ensuring that all votes are anonymous and privacy is preserved.

# Security

The blockchain structure ensures data integrity and resistance to tampering. Once a vote is recorded on a block, it cannot be altered, and the chain provides a transparent audit trail. Each node participates in verifying new transactions and blocks, promoting a decentralized approach to security.

# Downfalls

This project is designed for small-scale use, so it has a few limitations:

- Limited Scalability: Currently, only one user registration can be processed at a time. Each registration requires network-wide block validation, so if another user tries to register while a registration block is still being mined, their registration attempt will fail. This limitation would become more problematic in larger networks.
- Potential Single Points of Failure: While decentralized, the network relies on a few nodes, which could impact reliability if any node goes offline.

This prototype is a foundation for understanding blockchain voting mechanics, with room for future scaling improvements and enhanced robustness.


# TODO
## networking
- abstract P2P into P2P and P2PNode (make P2P a standalone library?)
- more error/timeout catching, get rid of while not self.server_connected to take into account server errors

## Blockchain