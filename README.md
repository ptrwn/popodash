# popodash
App for tracking trends in alcohol consumption behaviour. Provides generic overviews of all parties and detailed descriptions for a party or a period. 

## data structure
1. Each party is meant to be one event that has:
    - start dt and end dt;
    - at least one location, a pub crawl is counted as a sigle party;
    - at least one user;
    - at least one item.

2. Each user is connected to at least 1 party. A user within a party has:
    - join and leave dt (default to party start and end dt);
    - at least 1 item. An item can be shared between several users within a party.

3. Each item:
    - is either a food or a drink;
    - has name and abv for drinks;
    - name and abv are properties of an item;
    - can be ordered in one location at a time;
    - volume and price are properties of an item in a specific location;

#### think on
- Shoud it be possible for a user to have more that 1 start-end dts within a party? Usecase: I join a party, have a couple of drinks, then leave for a couple of hours to walk the dog, then come back and stay till the end. Reasoning: double-check for shared items. 
- Should there be processing for food-and-drink combos? 