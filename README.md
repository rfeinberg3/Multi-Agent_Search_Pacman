# Multi-Agent Search in Pacman
![pacman_multi_agent](https://github.com/rfeinberg3/Multi-Agent_Search_Pacman/assets/95943957/2da3d117-8a5f-4dbb-977d-3118bf1b1478)

## Introduction

This repository contains the implementation of various search agents for the classic Pacman game. The project focuses on designing both Pacman and ghost agents using minimax and expectimax search algorithms, along with custom evaluation functions.

## Problems Solved

1. **Reflex Agent Improvement**:
    - Enhanced the provided ReflexAgent to make smarter decisions by considering both food and ghost locations.
    - Improved performance on different layouts, particularly the `testClassic` and `mediumClassic`.

2. **Minimax Search**:
    - Implemented a MinimaxAgent that uses adversarial search to optimize Pacman's moves.
    - Ensured the agent works with multiple ghosts and arbitrary search depths.
    - Correctly expanded the game tree and evaluated leaf nodes using a provided evaluation function.

3. **Alpha-Beta Pruning**:
    - Developed an AlphaBetaAgent to optimize the minimax search by pruning branches that do not affect the final decision.
    - Achieved speed improvements, enabling deeper searches within a reasonable time frame.

4. **Expectimax Search**:
    - Created an ExpectimaxAgent to model the probabilistic behavior of non-optimal ghost agents.
    - Implemented an algorithm that evaluates the expected utility of actions, assuming ghosts choose actions uniformly at random.

5. **Custom Evaluation Function**:
    - Designed a betterEvaluationFunction to evaluate game states for Pacman.
    - Ensured the function improved Pacman's performance in clearing layouts and achieving higher scores.

## Project Structure

- `multiAgents.py`: Contains the implementation of all multi-agent search agents. **Implemented!**
- `pacman.py`: Main file to run Pacman games and describe the GameState type. **Support File**
- `game.py`: Describes the logic of the Pacman world, including supporting types like AgentState, Agent, Direction, and Grid. **Support File**
- `util.py`: Provides useful data structures for implementing search algorithms. **Support File**

## Running the Project

This program need python version 3.6 to run. This is available on Windows (and possibly Linux), but not Mac. See `requirements.txt`.

### Playing Pacman

To play a game of classic Pacman:

```bash
python pacman.py
```

To run the provided ReflexAgent:

```bash
python pacman.py -p ReflexAgent
```

### Using the Autograder

The project includes an autograder to test your implementation. Run the autograder for all questions with:

```bash
python autograder.py
```

Run the autograder for a specific question:

```bash
python autograder.py -q q2
```

Run the autograder for a specific test:

```bash
python autograder.py -t test_cases/q2/0-small-tree
```

Use the `--graphics` flag to force graphics display or `--no-graphics` to disable it.


## Acknowledgements

This project is based on the Pacman AI projects developed at UC Berkeley.
