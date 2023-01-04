# Decline Analysis Tool

## Summary


A windows application made to speed up the process of decline analysis by allowing a user to interact with the graph. Program allows the user to select points and create a best fit on the data. This is an improvement over existing software solutions which require manually typing in decline parameters to complete a curve fit

## Examples of Functionality

The main application is divided into several sections.

	- Toolbars: Access additional functionality
	- Select Well: Pick a well name that will be displayed in the graphs
	- Plots: A plot of Production vs Cumulative Production is shown on the left. A plot of Production vs Time is shown on the right
	- Options: Commonly used functionality is placed as buttons for easy access
	- Results: The production values based on the current decline  

![Menus](/Document/Screenshot/menus.png)


### Load Data

After running the program as described in the How to Run section below.

When the file menu is opened data can be imported either from a save file or imported from excel. 

Select Import from Excel. In the popup window select a CSV with well production data

![Open Excel](/Document/Screenshot/open_excel.png)

On the import window select the type of data in each column of the excel sheet from the top drop down row. If necessary select the unit type from the second row of dropdown boxes

Select Import to import the well data

![Import Data](/Document/Screenshot/import_excel.png)


### Create a Decline

Select a well from the LHS and then use the mouse to circle the points to complete a best fit on. The best fit will be calculated and a best fit line will be placed. 

![Creating Decline](/Document/Screenshot/selecting_points.png)

The line can then be adjusted by dragging on the ends of the best fit to move it into place. Or a new set of points can be selected by pressing the Best Fit From Selection Button

![Adjusting Decline](/Document/Screenshot/adjust_decline.png)

The parameters of the decline are shown on the results window below

If multiple fluids were imported for each well the drop down box below the plot can be changed to do a decline for other fluids


### Saving a File

A file can be saved with the declines using a custom Decline Analysis (.da) file format.

A file is saved using the File -> Save menu. The file can then be reopened using File -> Open

![Saved File](/Document/Screenshot/save_file.png)

## How to Run

Clone the git repository using the following command

```
git clone https://github.com/gcrookes/DeclineAnalysis.git
```

Run the file Main.py in the src folder