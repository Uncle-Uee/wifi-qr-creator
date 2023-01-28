from PIL import Image
import wifi_qrcode_generator


def create_qr_code_image(ssid: str, hidden: bool, authentication: str, password: str) -> Image.Image:
    """Generate Wi-Fi QR code for given parameters
        :ssid str: SSID
        :hidden bool: Specify if the network is hidden
        :authentication_type str: Specify the authentication type. Supported types: WPA, WEP, nopass
        :password Optional[str]: Password. Not required if authentication type is nopass
        :rtype Image
    """
    return wifi_qrcode_generator.wifi_qrcode(ssid, hidden, authentication, password)
