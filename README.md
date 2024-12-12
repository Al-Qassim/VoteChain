# VoteChain
BlockChain-based election management web application

Despite the digital age we live in, elections are still conducted with paper in most parts of the world, that is because digital systems for elections require serious security properties that, until the last decade, didn't have the right tools so be provided. The modern tools that would allow for electronic election are Blockchain and zk snark. 

## Features:
* Any one (or any election commission) can create an elections for his community.
* Elections can be private or public 
* Elections results will be published on the election deadline day only (future update may include the possibility of real time publication of results)
* Support for many voting systems:
    * **Plurality** (https://cs50.harvard.edu/x/2024/psets/3/plurality/)
    * **Runoff** (https://cs50.harvard.edu/x/2024/psets/3/runoff/)
    * **Tideman** (https://cs50.harvard.edu/x/2024/psets/3/tideman/)
* A simple candedates voting (The Party List System will be supported in the future).   

## Election System Requirments
Any election system should garenty the folloing security requirment
*  **Correct execution**: correctly processes the votes according to some pre-defined rules, and returns the correct output.
* **Censorship resistance**: all eligible voters can participate and have their vote counted, even if that is against the will of big player. 
* **Privacy**: you should not be able to tell which candidate someone specific voted for, or even if they voted at all. The main panafit is to avoid potionial social problems among the votes (the people).
* **Coercion resistance**: you should not be able to prove to someone else how you voted, even if you want to. 

## BlockChain integration
the two main technologies that will meet all the requirments above are:
* **BlockChain** (specicly the etherium blockchain) (TODO: link for more informations)
* **zk snark** (Zero knowlage proofs) (TODO: link for more informations)

The main resource so far for the security system of the app will be based on this artical by vitalik buterin: https://vitalik.eth.limo/general/2021/05/25/voting2.html

Essentially, the election starts with the election commission generating public key and private key pairs for every voter, voters will encrypt their voting ballot with their public key, which guarantees privacy. Then they publish their encrypted voting ballot to the Ethereum blockchain, this guarantees censorship resistance since no one can alter the blockchain or prevent others from writing to the blockchain. When the election deadline comes, the commission reads the encrypted ballots from the blockchain and decrypts them using private keys. The results will be calculated according to the chosen election system, and a zk snark proof is generated for the results, the perpose of zk snark is that it guarantees that the commission did the calculations correctly with no manipulations. Finally, the results and the zksnark will be published to the public.

The blockchain feature is not implemented yet, and will be the last feature to be implemented. 

## Database Structure

the database contains several tables, the following are the tables and columns it contain:

```python
db.execute("""
    ceatre table users (
        user_id int primary key,
        username text unique,
        hash_password text,
        phone_number text,
        signiture_private_key text,
        signiture_public_key text 
    )
""")

db.execute("""
    ceatre table elections (
        election_id int primary key,
        discription text,
        deadline text,
        voting_system text,
        zkproof text default null,
        results text default null
    )
""")

db.execute("""
    ceatre table candedates (
        candedate_id int primary key,
        election_id int,
        private_key text,
        public_key text 
    )
""")
```   