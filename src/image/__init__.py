import requests


class ImageServer:
    BASE_URL = "https://images.evetech.net"

    def get_character_portrait(self, character_id, size) -> bytes:
        """
        Get a character's portrait from the image server.

        :param character_id: The character ID of the character to get the portrait for.
        :param size: The size of the portrait to get. Valid values are 32, 64, 128, 256, 512 and 1024.
        :return: The image data in bytes.

        ## Doctest
        ### Get a character's portrait
        >>> image_server = ImageServer()
        >>> image_server.get_character_portrait(2112008192, 32) # doctest: +ELLIPSIS
        b'...'

        ### Get a character's portrait and save it to a file
        >>> image_server = ImageServer()
        >>> with open('portrait.png', 'wb') as portrait_file:
        ...     portrait_file.write(image_server.get_character_portrait(2112008192, 32))
        977
        >>> import os
        >>> os.path.isfile('portrait.png')
        True
        """
        url = f"{self.BASE_URL}/characters/{character_id}/portrait?size={size}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.content
