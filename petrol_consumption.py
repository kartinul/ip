import pandas as pd
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine, text


FILE_PATH = "petrol_consumption.csv"
CLEAR_SCREEN = False

# MySQL authentication configuration
AUTH = {
    "host": "localhost",
    "user": "root",
    "password": "10915",
    "database": "petrol_db",
}
ENGINE_URI = f"mysql+pymysql://{AUTH['user']}:{AUTH['password']}@{AUTH['host']}"
ENGINE_URI_DB = f"mysql+pymysql://{AUTH['user']}:{AUTH['password']}@{AUTH['host']}/{AUTH['database']}"

dataframe = pd.DataFrame(
    columns=[
        "Petrol_tax",
        "Average_income",
        "Paved_Highways",
        "Population_Driver_licence_percent",
        "Petrol_Consumption",
    ]
)


def initialize_csv():
    global dataframe

    if not os.path.exists(FILE_PATH):
        print("CSV file not found. Creating a new one.")
        dataframe.to_csv(FILE_PATH, index=False)
    else:
        dataframe = pd.read_csv(FILE_PATH)


def save_to_csv():
    global dataframe

    dataframe.to_csv(FILE_PATH, index=False)
    print("Data saved to CSV.")


def add_data():
    global dataframe

    print("\n--- Add Petrol Consumption Data ---")
    petrol_tax = float(input("Enter petrol tax: "))
    avg_income = int(input("Enter average income: "))
    paved_highways = int(input("Enter paved highways: "))
    driver_license_percent = float(input("Enter driver license percentage: "))
    petrol_consumption = int(input("Enter petrol consumption: "))

    new_data = pd.DataFrame(
        {
            "Petrol_tax": [petrol_tax],
            "Average_income": [avg_income],
            "Paved_Highways": [paved_highways],
            "Population_Driver_licence_percent": [driver_license_percent],
            "Petrol_Consumption": [petrol_consumption],
        }
    )

    dataframe = pd.concat([dataframe, new_data], ignore_index=True)
    save_to_csv()


def view_data():
    global dataframe

    print("\n--- View Petrol Consumption Data ---")
    if dataframe.empty:
        print("No data available.")
    else:
        print(dataframe)


def modify_data():
    global dataframe
    view_data()

    idx = int(input("Enter the index of the data to modify: "))
    if idx not in dataframe.index:
        print("Invalid index.")
        return
    print("Modify the fields (leave blank to keep current value):")

    for column in dataframe.columns:
        current_value = dataframe.at[idx, column]
        new_value = input(f"{column} [{current_value}]: ")
        if new_value:
            dataframe.at[idx, column] = (
                float(new_value) if column != "Paved_Highways" else int(new_value)
            )
    save_to_csv()


def delete_data():
    global dataframe
    view_data()

    try:
        idx = int(input("Enter the index of the data to delete: "))
        if idx not in dataframe.index:
            print("Invalid index.")
            return
        dataframe = dataframe.drop(idx).reset_index(drop=True)
        save_to_csv()
    except ValueError:
        print("Invalid input.")


def clear_all_data():
    global dataframe

    dataframe = pd.DataFrame(columns=dataframe.columns)
    save_to_csv()
    print("All data cleared.")


def sort_data():
    global dataframe

    print("\n--- Sort Petrol Consumption Data ---")
    print("1. Petrol Tax\n2. Average Income\n3. Petrol Consumption")
    column_map = {"1": "Petrol_tax", "2": "Average_income", "3": "Petrol_Consumption"}
    choice = input("Sort by (1/2/3): ")
    if choice in column_map:
        dataframe = dataframe.sort_values(
            by=column_map[choice], ascending=True
        ).reset_index(drop=True)
        view_data()
    else:
        print("Invalid choice.")


def view_average_consumption():
    global dataframe

    if dataframe.empty:
        print("No data available.")
        return
    average_consumption = dataframe["Petrol_Consumption"].mean()
    print(f"Average Petrol Consumption: {average_consumption:.2f}")


def setup_database():
    engine = create_engine(ENGINE_URI)

    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {AUTH['database']}"))

    engine = create_engine(ENGINE_URI_DB)

    with engine.connect() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS consumption (
                    Petrol_tax FLOAT,
                    Average_income INT,
                    Paved_Highways INT,
                    Population_Driver_licence_percent FLOAT,
                    Petrol_Consumption INT
                )
            """
            )
        )

    print("Database and table set up successfully.")


def export_to_sql():
    global dataframe

    engine = create_engine(ENGINE_URI_DB)

    dataframe.to_sql(
        "consumption", engine, if_exists="replace", index=False, method="multi"
    )
    print("Data exported to MySQL database.")


def generate_graph():
    global dataframe

    if dataframe.empty:
        print("No data available.")
        return

    print("\n--- Graph Options ---")
    print("1. Bar Graph\n2. Scatter Plot")
    choice = input("Select graph type (1/2): ")
    if choice == "1":
        plt.bar(
            dataframe.index,
            dataframe["Petrol_Consumption"],
            color=["red", "green", "blue", "orange", "purple"],
        )
        plt.title("Petrol Consumption")
        plt.xlabel("Index")
        plt.ylabel("Consumption")
        plt.show()

    elif choice == "2":
        plt.scatter(
            dataframe.index,
            dataframe["Petrol_Consumption"],
            c="blue",
            label="Consumption",
        )
        plt.title("Petrol Consumption (Scatter Plot)")
        plt.xlabel("Index")
        plt.ylabel("Consumption")
        plt.legend()
        plt.show()
    else:
        print("Invalid choice.")


def toggle_clear_screen():
    global CLEAR_SCREEN

    CLEAR_SCREEN = not CLEAR_SCREEN
    print(f"Clear screen feature is now {'enabled' if CLEAR_SCREEN else 'disabled'}.")


def display_menu():
    print("\n--- Petrol Consumption Management System ---")
    print("1. Add Data")
    print("2. View Data")
    print("3. Modify Data")
    print("4. Delete Data")
    print("5. Sort Data")
    print("6. View Average Consumption")
    print("7. Export to SQL")
    print("8. Generate Graph")
    print("9. Clear All Data")
    print("10. Toggle Clear Screen")
    print("11. Exit")


def main():
    initialize_csv()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if CLEAR_SCREEN:
            os.system("cls")

        if choice == "1":
            add_data()
        elif choice == "2":
            view_data()
        elif choice == "3":
            modify_data()
        elif choice == "4":
            delete_data()
        elif choice == "5":
            sort_data()
        elif choice == "6":
            view_average_consumption()
        elif choice == "7":
            export_to_sql()
        elif choice == "8":
            generate_graph()
        elif choice == "9":
            clear_all_data()
        elif choice == "10":
            toggle_clear_screen()
        elif choice == "11":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
