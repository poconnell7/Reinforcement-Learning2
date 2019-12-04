# Reinforcement Learning - Machines teaching themselves (to play games)


## Reinforcement Learning is an active area of research and an important tool in Machine Learning, but is one of the less well understood techniques in the field of Data Science.

### This project explores Reinforcement Learning by creating an algorithm that teaches itself to play a game. In this case the game is Tic-Tac-Toe.

#### Some of the important features of Reinforcement Learning:
- Interacting with its environment
- Maximizing some reward
- Learning by itself i.e. it is not told what steps to take to succeed.

#### There are a couple of things that distinguish Reinforcement Learning from other types of Machine Learning, such as Supervised and Unsupervised Learning:
- Trial and Error Search
- Delayed Reward

#### Reinforcement Algorithms must also balance 
- Exploration
      and
- Exploitation

#### All of these features of Reinforcement Learning can be investigated in an algorithm that learns to play the simple game of Tic-Tac-Toe 

##### The Reinforcement Learning algorithm adjusts its playing strategy as it plays multiple games. It learns to optimize its win rate by learning which moves leads to the most victories against its current opponent. 

##### The game used for this demonstration is Tic-Tac-Toe:
- A 3x3 grid game
- Two players alternate taking turns
- The first player to get 3 boxes in a "row" wins. The 3 cells can be:
 - vertical,
 - horizontal, or 
 - diagonal

Another, non-learning algorithm, (NegaMax) was implemented to play Tic-Tac-Toe. This will play against the Reinforcement algorithm, allowing the latter to learn as it plays.

The NegaMax algorithm can be adjusted (using depth of search lookahead) to make it either a very strong player, or a very weak player. This allows the testing of the different strategies the Reinforcement algorithm learns to play against opponents of different strengths.

#### The graph below shows the win (green) and loss (red) rate per 100 games for the Reinforcement algorithm over 10,000 games while playing against a relatively weak (search depth of 2) opponent.

<img src="Screen Shot 2019-02-08 Win Loss rate for Reinforcement Algorithm per 100 games played Learning 0_2 Depth 2 10_000 games Graph only.png" width="1000" height="400"/>

### Conclusion
The Reinforcement algorithm learns to play the game by itself and its performance exceeds that of the NegaMax algorithm after playing 2,000 games.

Note that this machine learning algorithm does need an external big data source. In this case it generates all the needed data, 10,000 games, by itself.

