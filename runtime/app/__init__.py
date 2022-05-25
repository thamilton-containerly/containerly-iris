import logging
import os
import numpy as np
from joblib import load

MODEL_LOCATION = os.getenv('MODEL_LOCATION')

def model_predict(data):
    # Convert into nd-array
    try:
        data = np.array(data).reshape(1, -1)
        model = load(MODEL_LOCATION)
        pred = model.predict(data)[0]
        return pred
    except Exception as e:
        raise e

def run_service(request, **kwargs):
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.INFO)

    LOGGER.info("Got type: %s", type(request))
    LOGGER.info("Got service: %s", request)

    vector = [
        int(request["sepal_length_cm"]),
        int(request["sepal_width_cm"]),
        int(request["petal_length_cm"]),
        int(request["petal_width_cm"])
    ]
    response = {
        "class": model_predict(vector)
    }

    LOGGER.info("Got service: %s", response)

    return response
