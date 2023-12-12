# code-academy-baigiamasis
This project offers a deep dive into the exciting world of Euroleague basketball, providing users with a wealth of data and insights about ongoing matches and teams. It is an invaluable resource for fans, bettors, and sports analysts who are interested in the Euroleague. Here are the key features:

## Match Statistics:
Access detailed statistics from Euroleague matches.
View team stats, and game outcomes.
Analyze data to understand team strengths, weaknesses, and overall dynamics.

## Predictive Analysis:
Make informed predictions about future matches.
Utilize current season statistics to forecast outcomes.

## Dependencies

List of dependencies required to run this project:

- Python 3.11.4
- crispy-bootstrap4 2023.1
- Django 5.0
- django-crispy-forms 2.1
- django-tinymce 3.6.1
- django-widget-tweaks 1.5.0
- numpy 1.26.2
- pandas 2.1.3
- Pillow 10.1.0
- scikit-learn 1.3.2

## Interactive Team Window with Detailed Statistics
Our platform offers an intuitive and detailed view of each team in the Euroleague. Here's what you can expect in the team window:

Expandable Team Averages and Game Stats
In-Depth Team Averages: Get a comprehensive look at team performance with expandable sections for team averages. This feature provides insights into a team's overall performance across various metrics such as points per game, rebounds, assists, and more.

Game-by-Game Statistics: Dive deeper into each match with expandable game statistics. This section offers detailed data from individual games, allowing users to analyze and understand the team's performance in specific matches.


![gamestats](https://github.com/Aristotlle/code-academy-baigiamasis/assets/62259737/114269c7-ed9d-4fc5-ae3f-ac0cb35f8a65)

## Making Predictions
Intuitive Prediction Interface
Our platform offers a unique feature that allows users to make informed predictions about Euroleague basketball games. Here’s how it works:

Easy-to-Use Prediction View
Select Teams: Navigate to the prediction view where you can easily select a Home team and an Opponent team from the current Euroleague roster.

Leverage Ongoing Stats: The prediction algorithm takes into account the ongoing season's statistics for both teams. This ensures that the predictions are based on the most recent and relevant data.

![predictions](https://github.com/Aristotlle/code-academy-baigiamasis/assets/62259737/70e0dc62-a4de-4193-b1ba-3734ce88f27f)

## Management functions:

```ruby
# To delete all GameStats records:
python manage.py delete_gamestats
```
```ruby
# To populate GameStats from a CSV file:
python manage.py populate_gamestats path/to/your/file.csv
```

