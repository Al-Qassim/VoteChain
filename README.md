# VoteChain
Open Source BlockChain-based election management web application

Despite the digital age we live in, elections are still conducted with paper in most parts of the world. That is because elections require serious security requirements that, until the last decade, digital systems didn't have the right tools to meet those requirements. Blockchain and zk-SNARK are modern tools that make it possible for the electronic systems to meet the elections requirements (other than the **safe input device**  requirement). In this project, we developed the classical basics for such a system; all essential components, from users managing their polls to displaying results, are present. Future development would include the integration of this web app with the Ethereum blockchain.

## Context

This project was submitted as the final project to the CS50x (2024) UniTech Iraq course, made by: 
* Alqassim Ali
* Hadeel Saad
* Zahraa Muafaq
* Reem Zeyad

## Features:
* Anyone (or any election commission) can create a poll.
* All polls are public (users can see what polls are run by other users).
* Poll results will be published on the election deadline automatically, and the poll creator can stop the poll earlier, and the results will be published.
* Currently there is only support for one voting system:
    * **Plurality** (https://cs50.harvard.edu/x/2024/psets/3/plurality/).

    Future updates may include supporting the following systems:
    * **Runoff** (https://cs50.harvard.edu/x/2024/psets/3/runoff/).
    * **Tideman** (https://cs50.harvard.edu/x/2024/psets/3/tideman/).
* Only support simple candidates voting (The Party List System will be supported in future updates).   
* Users can delete their polls.
* Voters can vote more than once, and only the last vote will be counted. This ensures **coercion resistance**.
* Users can reset their passwords.
* Users need not have an account to be able to view the polls.
* Users need not have an account to be able to vote; they only need a valid voting key.
* Upon creating a poll, users can download the voting keys in a CSV file. 

## Election System Requirements
Any election system should guarantee the following security requirement:
* **Correct execution**: correctly processes the votes according to some pre-defined rules and returns the correct result.
* **Censorship resistance**: all eligible voters can participate and have their vote counted, even if that is against the will of big player. 
* **Privacy**: You should not be able to tell which candidate someone specific voted for, or even if they voted at all. The main benefit is to avoid potential social problems among the votes (the people).
* **Coercion resistance**: You should not be able to prove to someone else how you voted, even if you want to. This also eliminates vote selling.
* **Safe input devices**: The voters devices (computers and self-phones) should be secure from hacking.

Note: Right now, these requirements are not all met by the current application. Specifically, there is no guarantee for the (censorship resistance) and (correct execution) since the corrupt election committee can easily manipulate the database and, ultimately, the results. 

## How it works currently:

Let's go through an example of an election from start to finish:

* User X creates a new poll according to the voting systems available.
* User X wants n voters to participate in the poll; this is necessarily because most elections require certain eligibility requirements to participate.
* User X will generate n pairs of public/secret keys and send each public key to each voter. For the sake of clarity, let's use the term (voting keys) instead of "public key, since the voters will use them to encrypt their voting ballot. Here you should note that this app is not responsible for distributing the voting keys. 
* Of course, user X should not let anyone know the secret keys (private), not even the voters, and each voter should not let other people know what their public keys are.
* Each voter specifies the candidate he will vote for and encrypts his index, i.e., candidate index, with the voting key he got from user X. Note here that the encrypting is done on the client side (front end).
* Finally, the voter simply casts it, i.e., casts the encrypted voting ballot, to user X (or to the blockchain, if the blockchain was used).
* Upon receiving the encrypted ballot, user X uses all private keys he has trying to decrypt the voting ballots.
* When the poll ends, either at the deadline or when user X stops it, the results will be calculated and published. Anyone will be able to view the voting results.
* If blockchain is used, user X is further required to generate a zk proof for the results and publish it.

The image below illustrates the process. Note: Since the blockchain is not integrated with the app yet, skip the steps of signature, blockchain, and zk proof.

![image](static/images/how%20it%20works%20digram.png)

## Blockchain Integration

The two main technologies that will meet all the requirements above are:
* **BlockChain** (specifically the Ethereum blockchain) (TODO)
* **zk-SNARK** (Zero-Knowledge Proofs) (TODO)

The main resource so far for the security system of the app will be based on this article by Vitalik Buterin: https://vitalik.eth.limo/general/2021/05/25/voting2.html

Essentially, the election starts with the election commission generating public key and private key pairs for every voter; voters will encrypt their voting ballot with their public key, which guarantees **privacy**. Voters will be able to change their vote; only the last vote will be counted. This ensures **coercion resistance**. Then they publish their encrypted voting ballot to the Ethereum blockchain; this guarantees **censorship resistance** since no one can alter the blockchain or prevent others from writing to the blockchain. When the election deadline comes, the commission reads the encrypted ballots from the blockchain and decrypts them using private keys. The results will be calculated according to the chosen election system, and a zk-SNARK proof is generated for the results. The purpose of zk-SNARK is that it guarantees that the commission **did the calculations correctly** with no manipulations. Finally, the results and the zk-SNARK will be published to the public.

The blockchain feature is not implemented yet. 

## Database Structure

The database contains several tables; the following are the tables and columns it contains (I know, I know; it can be improved):

* polls:
    * poll_id
    * user_id
    * title
    * description
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
    * signature_private_key 
    * signature_public_key
    * date (registration date)