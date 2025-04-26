import json
import logging
import azure.functions as func
from sentence_transformers import SentenceTransformer

# Load the efficient model for embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Process HTTP request based on route"""
    
    # Get the route from the request
    route = req.route_params.get('route', '')

    logging.info("HTTP request received by sentence transformer for route: %s",route)
    
    if route == '.well-known/ready':
      return _show_ready_()
    
    return  _create_embedding_(req.get_json())
    
def _create_embedding_(data):
    '''Generate embeddings for the provided string or string array'''
    try:
        texts = data.get("texts", [])

        if isinstance(texts, str):  # Convert single string to a list
            texts = [texts]

        elif not texts or not isinstance(texts, list):  # Handle invalid input
            return func.HttpResponse(
                json.dumps({"error": "Invalid input format. 'texts' must be a list or a single string."}),
                status_code=400,
                mimetype="application/json"
            )

        # Generate embeddings using the SentenceTransformer model
        embeddings = model.encode(texts)

        # Return embeddings as a JSON response
        return func.HttpResponse(
            json.dumps({"embeddings": embeddings.tolist()}),  # Serialize the dict to JSON
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error("Error occurred: %s",str(e))
        
    return func.HttpResponse(
        json.dumps({"error": "An error occurred while processing the request."}),
        status_code=500,
        mimetype="application/json"
    )

def _show_ready_():
    '''Health check endpoint'''

    return func.HttpResponse(
        body="Service is ready and reachable.",
        status_code=200,
        mimetype="text/plain"
    )