from rooms_shared_services.src.settings.pricing.base import PriceMarginSettings
from pydantic_settings import SettingsConfigDict


class SignalPriceMarginSettings(PriceMarginSettings):
    model_config = SettingsConfigDict(env_prefix="signal_")
    