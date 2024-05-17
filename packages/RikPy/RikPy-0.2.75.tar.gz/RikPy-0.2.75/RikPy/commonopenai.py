import openai
from .customresponse import CustomResponse
import requests
import json

def OpenAI_generate_response(prompt, openai_key=""):
    
    try:
        # Executes the prompt and returns the response without parsing
        print ("Warming Up the Wisdom Workshop!")
        openai.api_key = openai_key

        print ("Assembling Words of Wisdom!")
        details_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,  # Your prompt goes here
                }
            ]
        )
        
        return CustomResponse(data=details_response, status_code=200)
    
    ## https://platform.openai.com/docs/guides/error-codes/python-library-error-types
    except openai.InternalServerError as e:
        return CustomResponse(data={"error": str(e)}, status_code=400)
    except openai.RateLimitError as e: 
        return CustomResponse(data={"error": str(e)}, status_code=429)
    except openai.BadRequestError as e:
        return CustomResponse(data={"error": str(e)}, status_code=500)
    except openai.APIError as e:
        return CustomResponse(data={"error": str(e)}, status_code=500)
    except Exception as e:
        return CustomResponse(data={"error": str(e)}, status_code=500)
        
def OpenAI_generate_image(image_prompt, number_images=1, quality="standard", size="1024x1024", openai_key=""):
    
    try:
        # Executes the prompt and returns the response without parsing
        
        print ("Sparking the Synapses of Silicon!")
        openai.api_key = openai_key

        print("Summoning Pixels from the Digital Depths!")
        print(image_prompt)
        
        image_response = openai.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            n=number_images,
            quality=quality,
            size=size
        )
        
        #return image_response
        return CustomResponse(data=image_response, status_code=200)
    
    ## https://platform.openai.com/docs/guides/error-codes/python-library-error-types
    except openai.InternalServerError as e:
        return CustomResponse(data={"error": str(e)}, status_code=400)
    except openai.RateLimitError as e: 
        return CustomResponse(data={"error": str(e)}, status_code=429)
    except openai.BadRequestError as e:
        return CustomResponse(data={"error": str(e)}, status_code=500)
    except openai.APIError as e:
        return CustomResponse(data={"error": str(e)}, status_code=500)
    except Exception as e:
        return CustomResponse(data={"error": str(e)}, status_code=500)
    
def OpenAI_generate_image_request(image_prompt, number_images=1, quality="standard", size="1024x1024", openai_key=""):
    try:
        print("Sparking the Synapses of Silicon!")
        url = "https://api.openai.com/v1/images/generations"

        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "dall-e-3",
            "prompt": image_prompt,
            "n": number_images,
            "quality": quality,
            "size": size
        }

        print("Summoning Pixels from the Digital Depths!")
        print(image_prompt)

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_json = response.json()

        if response.status_code != 200: return CustomResponse(data={"error": response_json.get("error", "Unknown error")}, status_code=response.status_code)
        # Extract token usage information from headers
        token_usage = response.headers.get('X-OpenAI-Usage')
        return CustomResponse(data={"response": response_json, "usage": token_usage}, status_code=200)

    except requests.exceptions.RequestException as e:
        return CustomResponse(data={"error": str(e)}, status_code=500)
