# from the ~/website/__init__.py folder, import the create_app function
from website import create_app

# get the create_app() function in __init__.py, and use that to create the application
app = create_app();

# main file
if __name__ == "__main__":
    # run the application, allow debugging
    app.run(debug=True);
