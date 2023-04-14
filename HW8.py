# Your name: Raina Gebara 
# Your student id: 
# Your email:
# List who you have worked with on this homework: Emily Libman and Julia Coffman

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    #print(cursor)

    
    cursor.execute("""
        SELECT r.name, c.category, b.building, r.rating 
        FROM restaurants r 
        JOIN categories c ON r.category_id = c.id 
        JOIN buildings b ON r.building_id = b.id
    """)

    results = cursor.fetchall()

    #print(names)    
    data = {}
    
    for row in results:
        #print(row)
        name = row[0]
        category = row[1]
        building = row[2]
        rating = row[3]
        
        data[name] = {'category': category, 'building': building, 'rating': rating}
    
    conn.close()

    return data

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.category, COUNT(r.name) 
        FROM restaurants r 
        JOIN categories c ON r.category_id = c.id 
        GROUP BY c.category
    """)

    results = cursor.fetchall()

    data = {}
    #print(results)
    for row in results:
        #print(row)
        category = row[0]
        num = row[1]

        data[category] = num
    
    print(data)
    conn.close()

    # plot the bar chart
    plt.bar(data.keys(), data.values())
    plt.title('Number of Restaurants by Category')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.show()

    return data


def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.name 
        FROM restaurants r 
        JOIN buildings b ON r.building_id = b.id 
        WHERE b.building = ? 
        ORDER BY r.rating DESC
    """, (building_num,))

    results = cursor.fetchall()

    restaurant = [row[0] for row in results]
    conn.close()

    print(restaurant)
    return restaurant

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    import sqlite3
import matplotlib.pyplot as plt

def get_highest_rating(db):
    # Connect to the database
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Get the highest-rated restaurant category and its average rating
    cur.execute("""
        SELECT categories.category, AVG(restaurants.rating)
        FROM restaurants
        JOIN categories ON restaurants.category_id = categories.id
        GROUP BY categories.category
        ORDER BY AVG(restaurants.rating) DESC
        LIMIT 1
    """)
    highest_cat, avg_cat_rating = cur.fetchone()

    # Get the building with the highest-rated restaurants and its average rating
    cur.execute("""
        SELECT buildings.building, AVG(restaurants.rating)
        FROM restaurants
        JOIN buildings ON restaurants.building_id = buildings.id
        GROUP BY buildings.building
        ORDER BY AVG(restaurants.rating) DESC
        LIMIT 1
    """)
    highest_building, avg_building_rating = cur.fetchone()

    # Close the database connection

    # Plot the bar charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Plot the bar chart for restaurant categories
    cur.execute("""
        SELECT categories.category, AVG(restaurants.rating)
        FROM restaurants
        JOIN categories ON restaurants.category_id = categories.id
        GROUP BY categories.category
        ORDER BY AVG(restaurants.rating) DESC
    """)
    data = cur.fetchall()
    categories, ratings = zip(*data)
    ax1.bar(categories, ratings)
    ax1.set_title("Restaurant Categories by Average Rating")
    ax1.set_xlabel("Category")
    ax1.set_ylabel("Average Rating")
    ax1.tick_params(axis="x", rotation=90)

    # Plot the bar chart for buildings
    cur.execute("""
        SELECT buildings.building, AVG(restaurants.rating)
        FROM restaurants
        JOIN buildings ON restaurants.building_id = buildings.id
        GROUP BY buildings.building
        ORDER BY AVG(restaurants.rating) DESC
    """)
    data = cur.fetchall()
    buildings, ratings = zip(*data)
    ax2.bar(buildings, ratings)
    ax2.set_title("Buildings by Average Rating")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Average Rating")
    ax2.tick_params(axis="x", rotation=90)

    # Show the plot
    plt.show()

    # Return the results as a list of tuples
    #print([(highest_cat, avg_cat_rating), (highest_building, avg_building_rating)])
    return [(highest_cat, avg_cat_rating), (highest_building, avg_building_rating)]


#Try calling your functions here
def main():
    # load_rest_data("South_U_Restaurants.db")
    # plot_rest_categories("South_U_Restaurants.db")
    #find_rest_in_building(1140, 'South_U_Restaurants.db')
    get_highest_rating("South_U_Restaurants.db")
    

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

#     def test_get_highest_rating(self):
#         highest_rating = get_highest_rating('South_U_Restaurants.db')
#         self.assertEqual(highest_rating, self.highest_rating)

# if __name__ == '__main__':
#     main()
#     unittest.main(verbosity=2)
