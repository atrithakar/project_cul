import codecs
from common_variables import DEFAULT_URL

def change_reg(link: str) -> None:
    '''
    Changes the registry link in the configuration file.

    Args:
        link (str): The new registry link to be set. If "default", it resets to the default BASE_URL.

    Returns:
        None

    Raises:
        None
    '''
    if link == "default":
        with codecs.open('.cul/cul_config.txt', 'w', encoding='utf-8') as f:
            f.write(DEFAULT_URL)
            print("Registry link set to default")
            return
        
    with codecs.open('.cul/cul_config.txt', 'w', encoding='utf-8') as f:
        f.write(link)
        print(f"Registry link changed to {link}")