import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("placement_data.csv")

print("\nPlacement Data\n")
print(data)

# Highest Salary
highest_salary = data["Salary_LPA"].max()
print("\nHighest Salary:", highest_salary, "LPA")

# Average Salary
average_salary = data["Salary_LPA"].mean()
print("Average Salary:", round(average_salary,2), "LPA")

# Company-wise Selection
company_count = data[data["Placed"]=="Yes"].groupby("Company").size()

print("\nCompany-wise Selection Count")
print(company_count)

# Department-wise Placement Rate
dept_total = data.groupby("Department").size()
dept_placed = data[data["Placed"]=="Yes"].groupby("Department").size()

placement_rate = (dept_placed / dept_total) * 100

print("\nDepartment-wise Placement Rate")
print(placement_rate)

# Bar Chart Company Selection
company_count.plot(kind="bar", title="Company-wise Selection Count")
plt.xlabel("Company")
plt.ylabel("Students Selected")
plt.show()

# Bar Chart Department Placement
placement_rate.plot(kind="bar", title="Department-wise Placement Rate")
plt.xlabel("Department")
plt.ylabel("Placement Percentage")
plt.show()