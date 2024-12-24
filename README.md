# VoteChain
BlockChain-based election management web application

Despite the digital age we live in, elections are still conducted with paper in most parts of the world. That is because elections require serious security requirments that, until the last decade, digital systems didn't have the right tools to meet those requirments. Blockchain and zk snark are modern tools that makes to posible for the electronic systems to meet the elections requirments (other that the **safe input device** requirment). In this project, we developed the classical basics for such system, all essencial components from users maneging thier polls to displaying results are present. Future development would include the integration of this web app with the etherium blockchain.

## Context

This porject wes submitted as the final project to the CS50x (2024) UniTech Iraq course, made by: 
* Alqassim Ali
* Hadeel Saad
* Zahraa Muafaq
* Reem Zeyad

## Features:
* Any one (or any election commission) can create a poll.
* all polls are public (users can see what polls are run by other users).
* polls results will be published on the election deadline automatically, and poll creator can stop the poll earlier and the results will be published.
* Corrently there is only a support for one voting systems:
    * **Plurality** (https://cs50.harvard.edu/x/2024/psets/3/plurality/).

    future updates may include supporting the following systems:
    * **Runoff** (https://cs50.harvard.edu/x/2024/psets/3/runoff/).
    * **Tideman** (https://cs50.harvard.edu/x/2024/psets/3/tideman/).
* only support simple candedates voting (The Party List System will be supported in the future).   
* users can delete their polls.
* voters can vote more than once, and only the last vote will be counted. This ensure **coercion resistance**.
* users can reset there passwords.
* users need not to have an account to be able to view the polls.
* users need not to have an account to be able to vote, they only need a valid voting key.

## Election System Requirments
Any election system should guarantee the following security requirement:
* **Correct execution**: correctly processes the votes according to some pre-defined rules, and returns the correct result.
* **Censorship resistance**: all eligible voters can participate and have their vote counted, even if that is against the will of big player. 
* **Privacy**: you should not be able to tell which candidate someone specific voted for, or even if they voted at all. The main benefit is to avoid potionial social problems among the votes (the people).
* **Coercion resistance**: you should not be able to prove to someone else how you voted, even if you want to. This also eliminate vote selling.
* **Safe input devices**: the voters device (computers and self-phones) should be secure from hacking.

Note: right now, these requirments are not all met by the current application. Spicifcly, there is no guarantee for the (censorship resistance) and (correct execution) since the currapt election commity can easily manipulate the database, and ultimatly, the results. 

## How it works Currently:

Let's go through an example of an election from start to finish:

* User X creates a new poll according to the voting systems available. Let's call it the "2024 United States Presidential Election" with three candidates (Trump, Kamala, Robart).
* User X wants n voters to participate in the poll, this is neccessarly because most elections require certian eligability requirments to participate.
* User X will generate n pairs of public/secret keys and send each public key to each voter. for the sake of clearty, let's use the term (voting keys) instead of the (public key), since the voters will use them to encrypte there voting ballot. Here you should note that this app is not responsable to destripute the voting keys. 
* of course, user X should not let anyone know the secret keys (private), not even the voters, and each voter should not let other people know what is their public keys.
* each voter specifies the candidate he will vote for, and encrypts his index, i.e. candidate index, with the voting key he got from user X. Note here that the encrypting is done in the clinte side (front end)
* Finally, the voter simply casts it, i.e. casts the encrypted voting ballot, to user X (or to the blockchain, if the blockchain was used).
* apon reciving the encypted ballot, user X uses all private keys he has tring to decrypte the voting ballots.
* when the poll ends, eather at the deadline or when user x stops it, the results will be calculated and published. Anyone will be able to view the voting results.
* if blockchain is used, user X is further required to generate a zk proof for the results and publish it.

The image below illustrate the process. Note, since the blockchain is not integrated with the app yet, skip the steps of signiture, blockchain, and zk proof.

![image](static/images/how%20it%20works%20digram.png)

## BlockChain integration

the two main technologies that will meet all the requirments above are:
* **BlockChain** (specicly the etherium blockchain) (TODO)
* **zk snark** (Zero knowlage proofs) (TODO)

The main resource so far for the security system of the app will be based on this artical by vitalik buterin: https://vitalik.eth.limo/general/2021/05/25/voting2.html

Essentially, the election starts with the election commission generating public key and private key pairs for every voter, voters will encrypt their voting ballot with their public key, which guarantees **privacy**. Voters will be able to change their vote, only the last vote will be counted, this ensure **coercion resistance**. Then they publish their encrypted voting ballot to the Ethereum blockchain, this guarantees **censorship resistance** since no one can alter the blockchain or prevent others from writing to the blockchain. When the election deadline comes, the commission reads the encrypted ballots from the blockchain and decrypts them using private keys. The results will be calculated according to the chosen election system, and a zk snark proof is generated for the results, the perpose of zk snark is that it guarantees that the commission **did the calculations correctly** with no manipulations. Finally, the results and the zksnark will be published to the public.

The blockchain feature is not implemented yet. 

## Database Structure

the database contains several tables, the following are the tables and columns it contain (I know I know, it can be improved):

* polls:
    * poll_id
    * user_id
    * title
    * discription
    * deadline
    * voting_system
    * number_of_voters
    * zkproof
    * results (win or draw)
    * finish (bool)
    * winner (candidate name(s))

* candidates
    * candidate_index (from 1 to n, where n is the number of candidates)
    * candidate_name
    * poll_id
            
* votes
    * vote_id 
    * poll_id
    * voting_ballot (text)
    * ballot_encryption_key (voter's public key)
    * ballot_decryption_key (voter's private key)

* users
    * user_id 
    * username 
    * hash_password 
    * phone_number 
    * signiture_private_key 
    * signiture_public_key
    * date (registration date)