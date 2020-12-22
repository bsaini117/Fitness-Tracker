import re
import requests
import sys
import matplotlib.pyplot as plt
import pandas as pd
from argparse import ArgumentParser
from bs4 import BeautifulSoup



class FitnessSolutionReport:
    """Calls class FitnessSolutionReport"""
    
    
    
    def __init__(self, age, gender, weight, height, objective, how_often):
        """
        Creates attributes and stores the information from the parameters 
        Args: 
            age (int): The user's age
            gender (str): The user's gender
            weight (float): The user's weight in kilograms
            height (float): The user's height in centimeters
            objective (str): Whether the user wants to gain, maintain, or lose weight
            how_often (int): How many days the user wants to work out (minimum of 3 and maximum of 6)
        """
        self.age = age
        self.gender = gender
        self.weight = weight
        self.height = height
        self.objective = objective
        self.how_often = how_often
        
    
        
    def DataframeConverter(self, url, days):
        """
        Scrapes data from the given URL, converts it into a Pandas dataframe, and returns it
        Args: 
            url: The URL of the website from which the data is going to be scraped
            days (int): Amount of days user wants to workout (pulled from WorkoutRegime)
        Returns: Updated dataframe based on the input of the the user and the corresponding website with the fitness regime
        """
        
        res = requests.get(url)
        soup = BeautifulSoup(res.content,'lxml')
        table = soup.find_all('table', class_='InnerTable')
        
        l = []
        
        for i in range(days):
            innerTables = table[i].find_all('p')
            exercise = table[i].find_all('a')
            td = table[i].find_all('td')
            names, timers, reps, Sets = 2, 9, 10, 11
            
            for i in range(len(innerTables)):
                    day = {}
                    day["Muscle"] = innerTables[i].text
                    try:
                        day["Exercise Name"] = exercise[names].text
                    except:
                        day["Exercise Name"] = exercise[2].text
                    try:
                        day["Timer"] = td[timers].text.replace(' ','').replace('\n','')
                    except:
                        day["Timer"] = td[9].text.replace(' ','').replace('\n','')
                    try:
                        day["Reps"] = td[reps].text.replace(' ','').replace('\n','')
                    except:
                        day["Reps"] = td[10].text.replace(' ','').replace('\n','')
                    try:
                        day["Sets"] = td[Sets].text.replace(' ','').replace('\n','') 
                    except:
                        day["Sets"] = td[11].text.replace(' ','').replace('\n','') 
                        
                    day["Track"] = "NaN"

                    names += 4
                    timers += 7
                    reps +=7
                    Sets += 7

                    l.append(day)
                    
        df = pd.DataFrame(l)
        return df
              
       
    
    def CalorieCalculator(self, age, gender, weight, height):
        """
        Calculates the number of calories a person should have daily and BMI depending on user inputs
        Args:
            age (int): The user's age
            gender (str): The user's gender
            weight (float): The user's weight in kilograms
            height (float): The user's height in centimeters
        Side Effects:
            Prints dataframe featuring BMR, BMI, and weight status
        """

        l = []
        d_ret = {}
        p_bmi = (self.weight / (self.height * self.height)) * int(703)

        if gender == "female":
            weight = 10 * float(self.weight)
            height = 6.25 * float(self.height)
            age = 5 * int(self.age)
            bmr = ((weight + height) - age) + 5

        elif gender == "male":
            weight = 10 * float(self.weight)
            height = 6.25 * float(self.height)
            age = 5 * int(self.age)
            bmr = ((weight + height) - age) - 161

        if p_bmi < 18.5:
            weightStatus = "Underweight"
        elif p_bmi > 18.5 and p_bmi < 25:
            weightStatus = "Normal weight"
        elif p_bmi > 25:
            weightStatus = "Overweight"

        d_ret["BMR"] = bmr
        d_ret["BMI"] = p_bmi
        d_ret["Weight Status"] = weightStatus

        l.append(d_ret)
        df = pd.DataFrame(l)
        print(df)
    
    
       
    def WorkoutRegime(self):
        """
        Provides user with workout regime based on their objective and how often they want to workout.
        Args:
            Filename: Path to the file
        Side Effects: 
            Calls DataframeConverter() function
            Adds column to dataframe specifying days using df.index()
            Prints a workout that is catered to the user's preferences 
        """
        
        #FOR WORKING OUT THREE DAYS

        if self.how_often == 3:
            
            if self.objective == "maintain":

                url = "https://www.jefit.com/routines/72415/wedding-thicc"
                df = self.DataframeConverter(url, 3)
                df.index = ['Day 1', ' ', ' ', ' ' , ' ' , ' ', 'Day 2' ,' ' , ' ', ' ', ' ' , ' ' , 'Day 3' , ' ' , ' ' , ' ' , ' ', ' ', ' ' , ' '] 
                print(df)

            elif self.objective == "gain":

                url = "https://www.jefit.com/routines/199187/5x5-split-routine-3-day"
                df = self.DataframeConverter(url, 3)
                df.index = ['Day 1', ' ', ' ', ' ' , 'Day 2' ,' ' , ' ', ' ',  'Day 3' , ' ' , ' ' , ' ' , ' ' ] 
                print(df)

            elif self.objective == "lose":

                url = "https://www.jefit.com/routines/86376/3-day-for-running"
                df = self.DataframeConverter(url, 3)
                df.index = ['Day 1', ' ', ' ', ' ' , ' ', ' ', ' ' ,' ', ' ','Day 2' ,' ' , ' ', ' ', ' ', ' ', ' ' ,' ', ' ', ' ' ,  'Day 3' , ' ' , ' ' , ' ' , ' ' , ' ', ' ', ' ' ,' ', ' ', ' ' ] 
                print(df)

        #FOR WORKING OUT FOUR DAYS

        if self.how_often == 4:
            
            if self.objective == "maintain":

                url = "https://www.jefit.com/routines/70021/masunas-baseball-off-season-program-weeks-1-4"
                df = self.DataframeConverter(url, 4)
                df.index = ['Monday', ' ', ' ', ' ' , ' ' , ' ', 'Tuesday' ,' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' ,' ' , ' ' , 'Thursday' , ' ' , ' ' , ' ', ' ', ' ' ,'Friday' , ' ' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' ,' '] 
                print(df)

            elif self.objective == "gain":
                url = "https://www.jefit.com/routines/195547/hipertrofia-de-todo-el-cuerpo"
                df = self.DataframeConverter(url, 4)
                df.index = ['Monday', ' ', ' ', ' ' , ' ' , ' ', 'Tuesday' ,' ' , ' ', ' ', ' ' , ' ' ,  'Thursday' , ' ' , ' ' , ' ', ' ', ' ' ,'Friday' , ' ' , ' ' , ' ' , ' ', ' '] 
                print(df)

            elif self.objective == "lose":
                url = "https://www.jefit.com/routines/112064/lean-and-large"
                df = self.DataframeConverter(url, 4)
                df.index = ['Day 1', ' ', ' ', ' ' , ' ' , ' ', 'Day 2' ,' ' , ' ', ' ', ' ' , ' ' , ' ',  'Day 3' , ' ' , ' ' , ' ', ' ', ' ' ,'Day 4' , ' ' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' '] 
                print(df)

        #FOR WORKING OUT FIVE DAYS

        if self.how_often == 5:
            
            if self.objective == "maintain":

                url = "https://www.jefit.com/routines/101459/bikini-prep-schedule-4"
                df = self.DataframeConverter(url, 5)
                df.index = ['Monday', ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , 'Tuesday' ,' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ' ,' ','Wednesday' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ', 'Thursday' , ' ' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' , 'Friday ' , ' ' , ' ' , ' ' , ' ' ,' ', ' ', ' '] 
                print(df)

            elif self.objective == "gain":

                url = "https://www.jefit.com/routines/195713/scovs-routine"
                df = self.DataframeConverter(url, 5)
                df.index = ['Monday', ' ', ' ', ' ' , ' ' , ' ' , ' ' , 'Tuesday' ,' ' , ' ', ' ','Wednesday' , ' ' , ' ' , ' ', 'Thursday' , ' ' , ' ' , ' ' , ' ' , 'Friday ' , ' ' , ' ' , ' ']
                print(df)

            elif self.objective == "lose":

                url = "https://jefit.com/routines/107113/rajata-workout"
                df = self.DataframeConverter(url, 5)
                df.index = ['Monday', ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ' ,' ', ' ',' ',' ',' ', 'Tuesday' ,' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' ,'Wednesday' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ', ' ', 'Thursday' , ' ' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' ,' ', ' ', ' ', ' ', 'Friday ']
                print(df)         

        #FOR WORKING OUT SIX DAYS

        if self.how_often == 6:

            if self.objective == "maintain":

                url = "https://www.jefit.com/routines/33778/swimming-and-strength-101"
                df = self.DataframeConverter(url, 6)
                df.index = ['Day 1', 'Day 2', ' ', ' ' , ' ' , ' ' , 'Day 3' , 'Day 4' , 'Day 5' , ' ' , ' ' , ' ' , ' ' ,''] 
                print(df)

            elif self.objective == "gain":

                url = "https://www.jefit.com/routines/111830/6-day-push-pull-leg-workout-for-body-recomposition"
                df = self.DataframeConverter(url, 6)
                df.index = ['Monday', ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , 'Tuesday' ,' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , 'Wednesday' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , 'Thursday' , ' ' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' , 'Friday ' , ' ' , ' ' , ' ' , ' ' ,' ', ' ', ' ' , ' ' , ' ' , ' ' , 'Saturday' , ' ' , ' ' , ' ' , ' ' , ' ', ' ',' ', ' ', ' '] 
                print(df)

            elif self.objective == "lose":

                url = "https://www.jefit.com/routines/103151/fat-loss-workout"
                df = self.DataframeConverter(url, 6)
                df.index = ['Monday', ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , ' ' , ' ', 'Tuesday' ,' ' , ' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , 'Wednesday' , ' ' , ' ' , ' ', ' ', ' ' , ' ' , ' ' , 'Thursday' , ' ' , ' ' , ' ' , ' ', ' ', ' ' , 'Friday ' , ' ' , ' ' , ' ' , ' ' ,' ', ' ', ' ' , ' ' , ' ' , ' ' , ' ' , 'Saturday' , ' ' , ' ' , ' ' , ' ' , ' ', ' ',' ', ' ', ' ' , ' ' , ' '] 
                print(df)
    
    
    
    def DietPlan(self, objective):
        """
            Scrapes diet tables from provided URLS and displays them in pandas Dataframe
            Args:
                objective (str): a string containing the objective
            Side Effects: 
                    Makes output easier to see by printing dashed line
                    Prints part of output text in bold, then prints out heading with necessary information
                    Prints out dataframe
                    Prints new lines for organizational purposes
        """
        
        if self.objective == "lose":
            url = 'https://www.myfooddata.com/articles/gourmet-low-carb-high-protein-weight-loss-meal-plans.php'
            num_of_tables = 11
        elif self.objective == "gain":
            url = 'https://myfooddata.com/articles/budget-weight-gain-meal-plans.php'
            num_of_tables = 7
        else:
            output = 'To maintain your caloric intake, please consume the recommend number of calories provided by the Calorie Calculator.'
            return output
        
        res = requests.get(url)
        soup = BeautifulSoup(res.content)
        table = soup.find_all('div', class_='dayplan')
        head = soup.find_all('h2')
        dfs = pd.read_html(url)
        
        #Headings
        
        tableCounter = 0
        for i in range(num_of_tables):
            print('-' * 60)
            print('\033[1m' + head[i].text[: 5] + ' ' + head[i].text[5:])
            print('-' * 60)
            
            # Inner Headings
            
            innerTable = table[i].find_all('strong')
            for j in range(len(innerTable)):
                print('\033[1m' + innerTable[j].text)
                print(dfs[tableCounter])
                tableCounter += 1
                print('\n')
            print('\n\n')



    def WeightManage(self, weight, objective):
        """
            Plots a graph expressing how much weight the user would gain/lose/maintain over 4 weeks
            Args:
                weight (float): The user's weight in kilograms
                objective (str): Whether the user wants to gain, maintain, or lose weight
            Side Effects:
                Shows graph output
        """
        
        if self.objective == 'lose':
            lbl = 'Weight Lost from Cardio'
            weight = [self.weight, self.weight-2, self.weight-4, self.weight-6]
        elif self.objective == 'gain':
            lbl = 'Weight Gained from Calories'
            weight = [self.weight, self.weight+2, self.weight+4, self.weight+6]
        elif self.objective == 'maintain':
            lbl = 'Weight Maintained from Calories'
            weight = [self.weight, self.weight, self.weight, self.weight]
        
        weeks = [1, 2, 3, 4]
        
        plt.xlabel('Weeks')
        plt.ylabel('Weight (kg)')

        plt.plot(weeks, weight, label=lbl)
        plt.grid()
        plt.legend()
        plt.show()



    def FitnessResources(self, filename):
        """
        To obtain author and URL information of fitness resources from file and organize them into a dataframe
        Args:
            filename: Path to file
        Side Effects: Prints out a magazine that is taken from the website and stored the r dictionary
        """
        r = []
        with open(filename, 'r', encoding = "utf-8") as f:
            for line in f:
                resources = r"^(https?:\/\/(www\.)?[a-zA-Z]{1,256}.[a-zA-Z0-9()]{1,6}\b([a-zA-Z0-9()/]*))"
                url = re.search(resources, line) 
                a = r"^(([A-Za-z]+),\s+([A-Za-z]+)\s[A-Za-z].)"
                author = re.search(a, line)

            if resources:
                print("url.group() : ", url.group())
                print("url.group(1) : ", url.group(1))
                print("url.group(2) : ", url.group(2))
            else:
                print("No match!")
            
            if a:
                print("author.group() : ", author.group())
                print("author.group(1) : ", author.group(1))
                print("author.group(2) : ", author.group(2))
            else:
                print("No match!")
        
        Magazines = pd.DataFrame( 
        { 'Author of Magazine' : author , 'Website Link' : url }) 
    
        print(Magazines)


    
def parse_args(my_args_list):
    parser = ArgumentParser(description= "A comprehensive fitness report")   
    parser.add_argument('age', type = int, help="Age of the user")
    parser.add_argument('weight', type = float, help="Weight of the user (kg)")
    parser.add_argument('gender', type = str, help="Gender of the user (male/female)")
    parser.add_argument('height', type = float, help="Height of the user (cm)")
    parser.add_argument('objective', type = str, help ="User's goal to lose, mantain or gain weight")
    parser.add_argument('how_often', type = int, help ="How many days the user wants to spend attaining their goal (3-6)", choices=range(3,7))
    
    args = parser.parse_args()
    return args    

if __name__ == '__main__':
    print(sys.argv)
    args = parse_args(sys.argv[1:])
    print(FitnessSolutionReport(args.age, args.weight, args.gender, args.height, args.objective, args.how_often))
