from rooms_shared_services.src.settings.pricing.base import PriceMarginSettings
from pydantic_settings import SettingsConfigDict


class HalmarPriceMarginSettings(PriceMarginSettings):
    model_config = SettingsConfigDict(env_prefix="halmar_")
    