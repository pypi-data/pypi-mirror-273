import dotenv
def get_envconf():
    dotenv_file = dotenv.find_dotenv('env.conf')
    return dotenv_file


