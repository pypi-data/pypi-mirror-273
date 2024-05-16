# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from ..adapters.gem_rest import prepared_gem_messages, formatted_gem_output


gemini_key              = environ.get("GOOGLE_API_KEY","")


def gemini_get_client(**kwargs):
    client = None
    try:
        import google.generativeai as genai
        client = genai.GenerativeModel(model_name= kwargs['model_name'] if kwargs['model_name'] else 'gemini-1.5-flash'
            # defaults to os.environ.get("GOOGLE_API_KEY")
        )
    except ImportError:
        print("google-generativeai package is not installed")

    return client


def gemini_content(client, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    client.config(**kwargs)
    response = client.generate_content("What is the meaning of life?")
    return response.text


if __name__ == "__main__":
    print("you launched main.")