import time


def generate_with_retry(
    client,
    model,
    contents,
    config=None,
    max_retries=3
):

    for attempt in range(max_retries):

        try:

            if config is not None:

                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )

            else:

                response = client.models.generate_content(
                    model=model,
                    contents=contents
                )

            return response

        except Exception as error:

            error_message = str(error)

            temporary_error = (
                "503" in error_message
                or "429" in error_message
                or "UNAVAILABLE" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            )

            if temporary_error and attempt < max_retries - 1:

                wait_time = 2 ** attempt

                time.sleep(wait_time)

                continue

            raise error