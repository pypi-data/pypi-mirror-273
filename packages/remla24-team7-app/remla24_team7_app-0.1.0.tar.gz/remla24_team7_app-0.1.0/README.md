# app

This is the repository for the app of Assigment 2. 

The frontend is in the frontend folder and the backend is just `app.py`. 

Entering a URL and clicking "Predict" in the web frontend queries the `app-service` backend, which then communicates with `model-service` to retrieve the prediction. The prediciton is then shown on the website. Make sure to have `model-service` running and configured (`MODEL_SERVICE_URL`) for this backend to work.