# WHOT AI

Whot is a Nigerian card game played with a special deck of cards.   
Players take turns to play by matching the shape (suit) or the number of the current call card. The first player to play all their cards wins.

Official game documentation: [https://en.wikipedia.org/wiki/Whot!](https://en.wikipedia.org/wiki/Whot!)

This project was a fun way to create a computer player for the command line version of the game created in java. Here is the link to the java project if you would like to play the game: [WHOT](https://github.com/rheedhar/WHOT)

**Note**: Since this is a learning project, this model was not added to the java game due to constraints with hosting a large model.


## Data Generation
The data generation code is located in `generate_data.py` . Training data was created by:
- Generating all possible 4-card hand combinations from a 54-card deck
- Adding 5 million additional random game scenarios with special rules
- Total dataset: about 22 million rows

## Model Training
The model was trained using a random forest algorithm

**Model inputs** 
- Player's cards (4 cards)
- Current call card
- Special game states (i.e. if a pick two, pick three, general market, or whot is in effect based on the current state of the game)
- Requested suit (i.e. when a whot card is played and player requests a specific suit from the next player)

**Model Output**
- Action to take (card to play or go to market)

## Running the Code

if you are interested in running the code please follow the steps below.

### Requirements
- Open your terminal and clone this repo to a location on your computer
```
git clone https://github.com/rheedhar/WHOT-AI.git
```
- Install the project dependencies
```
pip install -r requirements.txt
```
### Creating the Dataset
- In the data folder, create a new folder called dataset.
- Uncomment the last line of code in `generate_data.py`

- Run the file
```
python generate_data.py
```

### Training the Model
I already trained the model and you are welcome to download it from here: [Google Drive](https://drive.google.com/drive/folders/1gqC86EvmaSQ01ghwOfMFKwUsz8cP5RLY?usp=drive_link)

**Note:** If you would like to retrain the model, due to the large dataset size, you may need to use a cloud provider or reduce the data size in `generate_data.py` otherwise, it takes forever to run on a personal computer.

- In the src folder create a new folder called models
- If you are using the pretrained model, save the downloads in `src/models/`.
- If you are retraining, you need to run the `whot_model.ipynb` file


### Running the API
- Start the uvicorn server
```
uvicorn src.main:app --reload
```

### Making Predictions

Send a POST request to `http://localhost:8000/predict`:

Example Request
```json
{
    "card_1": "circle 7",
    "card_2": "star 1",
    "card_3": "triangle 5",
    "card_4": "cross 10",
    "call_card": "square 7",
    "requested_suit": "NONE",
    "special_state": "NONE"
}
```

Example Response:
```json
{
    "action": "circle 7"
}
```

For local testing, due to the large size of the models, I recommend reducing the dataset size in `generate_data.py` and retraining

