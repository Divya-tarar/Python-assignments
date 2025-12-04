# Name = Divya
# Date = 22/11/25
# Project = Gradebook analyzer

import csv
def main_menu():
    print("Welcome to Gradebook Analyzer")
    print("choose an option:")
    print("1. Enter marks manually")
    print("2. load marks from  a CSV file")
    print("3. Exit")
    
def get_manual_marks():
    """
    Ask the user to enter student names and marks manually:
    Returns a dictionary like:{"Alice":78, "Bob":92}
    """
    marks = {}
    try:
        n = int(input("How many students do you want to enter?"))
    except ValueError:
        print("please enter a valid number. Returning to main menu.")
        return marks
    for i in range(1, n + 1):
        print(f"\nstudents {i}:")
        name = input(" Enter student name: ").strip()

        while True:
            try:
                score = float(input(" Enter marks (0-100): "))
                if 0 <= score <=100:
                    break
                else:
                    print(" Marks must be between 0 and 100. Try again.")
            except ValueError:
                print(" Please enetr a valid number for marks.")
    marks[name] = score
            
    print("\nManual data entry complete!")
    return marks
def load_marks_from_csv():
    """
    Ask the user for a CSV file name and load names & marks.
    The CSV file should have columns: Name,Marks
    Return a dictionary like: {"Alice":78, "Bob":92}
    """
    marks={}
    filename = input("Enter CSV file name (e.g., students,csv):").strip()
    try:
        with open(filename, mode='r',newline="")as file:
            reader = csv.DictReader(file)
            for row in reader:
                name=row.get("Namme","").strip()
                score_str = row.get("Marks","").strip()

                if not name:
                    continue

                try:
                    score = float(score_str)
                except ValueError:
                    print(f"could not convert marks for student '{name}'.skipping.")
                    continue

                marks[name] = score
        print("\nCSV file loaded successfully!")
    except FileNotFoundError:
        print("File not found.Please make sure the file is in the same folder as gradebook.py")
    except Exception as e:
        print("An error occurred while reading the CSV file:",e)
    return marks
def main():
    marks={}
    while True:
        main_menu()
        choice = input("Enter your choice(1-3): ").strip()
        if choice == "1":
            mmarks = get_manual_marks()
            print("\nCuurent marks data (manual):")
            print(marks)
        elif choice =="2":
            marks = load_marks_from_csv()
            print("\nCurrent marks data (from CSV):")
            print(marks)
        elif choice == "3":
            print("Exiting GradeBook Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1,2, or 3.")
if __name__ == "__main__":
    main()
                  

            
            
    
    

    
        
                


          
