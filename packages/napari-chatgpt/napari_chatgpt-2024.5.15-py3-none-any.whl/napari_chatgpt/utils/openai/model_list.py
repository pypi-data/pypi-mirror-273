import traceback

from arbol import asection, aprint

from napari_chatgpt.utils.api_keys.api_key import set_api_key




def get_openai_model_list(filter: str = 'gpt', verbose: bool = False) -> list:
    """
    Get the list of all OpenAI ChatGPT models.

    Parameters
    ----------
    filter : str
        Filter to apply to the list of models.
    verbose : bool
        Verbosity flag.

    Returns
    -------
    list
        List of models.

    """

    with asection(f"Enumerating all OpenAI ChatGPT models:"):

        # Ensure that the OpenAI API key is set:
        set_api_key('OpenAI')

        # Local imports to avoid issues:
        from openai import OpenAI

        try:
            # Model list to populate:
            model_list = []

            # Instantiate API entry point
            client = OpenAI()

            # Goes through models and populate the list:
            for model in client.models.list().data:
                model_id = model.id

                # only keep models that match the filter:
                if filter in model_id:
                    model_list.append(model_id)
                    if verbose:
                        aprint(model_id)

            return model_list

        except Exception as e:
            # Error message:
            aprint(f"Error: {type(e).__name__} with message: '{str(e)}' occured while trying to get the list of OpenAI models. ")
            # print stacktrace:
            traceback.print_exc()

            return []

