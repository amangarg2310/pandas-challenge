#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# In[4]:


print('')
print('Player Count')
print('..................')
print('')
   
# Use the length of list of screen names "SN", for total players.
total_players = len(purchase_data["SN"].value_counts())

# Create a data frame with total players named player count
player_count = pd.DataFrame({"Total Players":[total_players]})
player_count


# In[5]:


print('')
print('Purchasing Analysis (Total)')
print('..................')
print('')

# Calculations for unique items, average price, purchase count, and revenue
number_of_unique_items = len((purchase_data["Item ID"]).unique())
average_price = (purchase_data["Price"]).mean()
number_of_purchases = (purchase_data["Purchase ID"]).count()
total_revenue = (purchase_data["Price"]).sum()

# Create data frame with obtained values
summary_df = pd.DataFrame({"Number of Unique Items":[number_of_unique_items],
                           "Average Price":[average_price], 
                           "Number of Purchases": [number_of_purchases], 
                           "Total Revenue": [total_revenue]})
# Format with currency style
summary_df.style.format({'Average Price':"${:,.2f}",
                         'Total Revenue': '${:,.2f}'})


# In[6]:


print('')
print('Gender (Demographics)')
print('..................')
print('')


# Group purchase_data by Gender
gender_stats = purchase_data.groupby("Gender")

# Count the total of screen names "SN" by gender; use nunique to get number of unique items in list instead of LEN & UNIQUE
total_count_gender = gender_stats.nunique()["SN"]
total_count_gender
#total_count_gender

# Total count by gender and divivde by total players 
percentage_of_players = total_count_gender / total_players * 100

total_count_gender.head(10)

# Create data frame with obtained values
gender_demographics = pd.DataFrame({"Percentage of Players": percentage_of_players, "Total Count": total_count_gender})

# Format the values sorted by total count in descending order, and two decimal places for the percentage
gender_demographics.style.format({"Percentage of Players":"{:.2f}%"})


# In[7]:


print('')
print('Purchasing Analysis (Gender)')
print('..................')
print('')



# Count the total purchases by gender 
purchase_count = gender_stats["Purchase ID"].count()

# Average purchase prices by gender
avg_purchase_price = gender_stats["Price"].mean()

# Average purchase total by gender 
avg_purchase_total = gender_stats["Price"].sum()

# Average purchase total by gender divivded by purchase count by unique shoppers
avg_purchase_per_person = avg_purchase_total/total_count_gender

# Create data frame with obtained values 
gender_demos = pd.DataFrame({"Purchase Count": purchase_count, 
                                    "Average Purchase Price": avg_purchase_price,
                                    "Average Purchase Value":avg_purchase_total,
                                    "Avg Purchase Total per Person": avg_purchase_per_person})

# Format with currency style
gender_demos.style.format({"Average Purchase Value":"${:,.2f}",
                                  "Average Purchase Price":"${:,.2f}",
                                  "Avg Purchase Total per Person":"${:,.2f}"})


# In[8]:


# Establish bins for ages
bins = [0, 9, 14, 19, 24, 29, 34, 39, 200]
group = ["<10", "10 to 14", "15 to 19", "20 to 24", "25 to 29", "30 to 34", "35 to 39", "40+"]

# Segment and sort age values into bins established above
purchase_data["Age Group"] = pd.cut(purchase_data["Age"], bins, labels=group)
purchase_data.head(10)

# Create new data frame with the added "Age Group" and group it
age_grouped_df = purchase_data.groupby("Age Group")


# In[9]:


print('')
print('Age Demographics')
print('..................')
print('')


# Count total players by age category
total_count_age = age_grouped_df["SN"].nunique()
total_count_age

# Calculate percentages by age category 
percentage_by_age = (total_count_age/total_players) * 100

# Create data frame with obtained values
age_demo_summary = pd.DataFrame({"Percentage of Players": percentage_by_age, "Total Count": total_count_age})

# Format the data frame with no index name in the corner
age_demo_summary.index.name = None

# Format percentage with two decimal places 
age_demo_summary.style.format({"Percentage of Players":"{:,.2f}%"})


# In[14]:


print('')
print('Top Spenders (by Age)')
print('..................')
print('')


# Count purchases by age group
purchase_count_age = age_grouped_df["Purchase ID"].count()

# Obtain average purchase price by age group 
avg_purchase_price_age = age_grouped_df["Price"].mean()

# Calculate total purchase value by age group 
total_purchase_value = age_grouped_df["Price"].sum()

# Calculate the average purchase per person in the age group 
avg_purchase_per_person_age = total_purchase_value/total_count_age

# Create data frame with obtained values
age_demographics_summary = pd.DataFrame({"Purchase Count": purchase_count_age,
                                 "Average Purchase Price": avg_purchase_price_age,
                                 "Total Purchase Value":total_purchase_value,
                                 "Average Purchase Total per Person": avg_purchase_per_person_age})

# Format the data frame with no index name in the corner
age_demographics_summary.index.name = None

# Format with currency style
age_demographics_summary.style.format({"Average Purchase Price":"${:,.2f}",
                               "Total Purchase Value":"${:,.2f}",
                               "Average Purchase Total per Person":"${:,.2f}"})


# In[11]:


print('')
print('Most Popular Items')
print('..................')
print('')


# Group purchase data by screen names
spender_stats = purchase_data.groupby("SN")

# Count the total purchases by name
purchase_count_spender = spender_stats["Purchase ID"].count()

# Calculate the average purchase by name 
avg_purchase_price_spender = spender_stats["Price"].mean()

# Calculate purchase total 
purchase_total_spender = spender_stats["Price"].sum()

# Create data frame with obtained values
top_spenders = pd.DataFrame({"Purchase Count": purchase_count_spender,
                             "Average Purchase Price": avg_purchase_price_spender,
                             "Total Purchase Value":purchase_total_spender})

# Sort in descending order to obtain top 5 spender names 
formatted_spenders = top_spenders.sort_values(["Total Purchase Value"], ascending=False).head()

# Format with currency style
formatted_spenders.style.format({"Average Purchase Total":"${:,.2f}",
                                 "Average Purchase Price":"${:,.2f}", 
                                 "Total Purchase Value":"${:,.2f}"})


# In[15]:


# Create new data frame with related items information 
popular_items_df = purchase_data[["Item ID", "Item Name", "Price"]]
popular_items_df

# Group the item data by item id and item name 
popular_item_stats = popular_items_df.groupby(["Item ID","Item Name"])

# Count the number of times an item has been purchased 
purchase_count_item = popular_item_stats["Price"].count()

# Calculate the purchase value per item 
purchase_value = popular_item_stats["Price"].sum() 

# Find individual item price
item_price = purchase_value/purchase_count_item

# Create data frame with obtained values
most_popular_items = pd.DataFrame({"Purchase Count": purchase_count_item, 
                                   "Item Price": item_price,
                                   "Total Purchase Value":purchase_value})

# Sort in descending order to obtain top spender names and provide top 5 item names
popular_formatted = most_popular_items.sort_values(["Purchase Count"], ascending=False).head()

# Format with currency style
popular_formatted.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# In[16]:


print('')
print('Most Profitable Items')
print('..................')
print('')


# Take the most_popular items data frame and change the sorting to find highest total purchase value
popular_formatted = most_popular_items.sort_values(["Total Purchase Value"],
                                                   ascending=False).head()
# Format with currency style
popular_formatted.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# In[ ]:




