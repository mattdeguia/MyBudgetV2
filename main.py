# import the class to create the actual app
from website import create_app
app = create_app();

# run the application
if __name__ == "__main__":
    app.run(debug=True);
