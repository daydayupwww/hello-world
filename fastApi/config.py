from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    STATIC_DIR : str = "static"
    STATIC_URL : str = "/static"
    TEMPLATES_DIR : str = "front_end/templates"
    DEBUG_MOOD : bool = True
    SHOW_CONSTANTS :str = "this is config"

    class Config:
        env_file = (".env", ".ev.prod",".env")

config = Settings()
print(config.SHOW_CONSTANTS)