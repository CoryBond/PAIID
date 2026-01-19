from io import BytesIO
import logging
import traceback
import openai
import requests
from imageProviders.ImageProvider import ImageProvider, ImageProviderResult
from PIL import Image


ENGINE_NAME = "Dall-e"


class DalleProvider(ImageProvider):
    """
    NOTE: The dalle-3 model is deprecated and will be shutdown on May 12, 2026. Users are recommended to move to gpt-image-1 or gpt-image-1-mini.
    TODO: Switch to gpt-image-1 or gpt-image-1-mini for the model. Replace the name of this provider.
    STRETCH-GOAL: Have a way for users of the new "OpenAIProvider" to switch between OpenAPI existing models. Make the "default" model less static (or just use what is the default OpenAPI uses.)
    
    Wrapper for calling the Dalle-3 API and getting images (as bytes from it).

    This is a waiting call so it should be threaded.

    Attributes
    ----------
    key(str)
        the API key. See : https://openai.com/blog/dall-e-api-now-available-in-public-beta

    Methods
    -------
    get_image_from_string(prompt)
        Retrieves image from API. Image as bytes. Returns 'None' on failure
    """

    # inherits from Provider
    def __init__(self, key=None):
        super().__init__(key=key, keyname=key)
        self.openAiClient = openai.OpenAI(api_key=key)
        return


    def engine_name(self):
        return ENGINE_NAME


    def get_image_from_string(self, prompt) -> ImageProviderResult:
        logging.info("Generating image for prompt : " + prompt)
        img = None
        errorMessage = None
        try:
            # Select appropriate size from options in
            # res = list(DalleConst.SIZES.value.keys())[0]

            # if height != 0 and width != 0:
            #    for key in DalleConst.SIZES.value:
            #        if key > height or key > width:
            #            res = DalleConst.SIZES.value[key]
            #            break

            response = self.openAiClient.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            url = response.data[0].url
            logging.info("Generated image at : " + url)
            img = requests.get(url).content

        except openai.APIConnectionError as e:
            logging.error(traceback.format_exc())  
            errorMessage = "Unable to contact OpenAI. Internet or provider may be down."
        except openai.AuthenticationError as e:
            logging.error(traceback.format_exc())  
            errorMessage = "Error authenticating with OpenAI. Please check your credentials in '.creds'."
        except openai.RateLimitError as e:
            logging.error(traceback.format_exc())  
            errorMessage = "OpenAI reporting Rate Limiting. Please check your account at openai.com."
        except openai.APITimeoutError as e:
            logging.error(traceback.format_exc())            
            errorMessage = "Timeout contacting OpenAI. Internet or provider may be down."
        except BaseException as e:
            logging.error(traceback.format_exc())  
            errorMessage = str(e)
        
        return { 'img': img, 'errorMessage': errorMessage }
    
