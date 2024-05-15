from typing import List, Optional

from pydantic import BaseModel, Field

from MelodyMaster.schemas.base import BaseHrefData, BaseIdTypeHref
from MelodyMaster.schemas.content_version import MetaContentVersion
from MelodyMaster.schemas.photos import ImageModel
from MelodyMaster.schemas.play_params import PlayParams
from MelodyMaster.schemas.urls import UrlDTO


class PlayListRelationshipDTO(BaseModel):
    music_videos: BaseHrefData[List[BaseIdTypeHref]] = Field([], alias="music-videos")
    artists: BaseHrefData[List[BaseIdTypeHref]] = Field([], alias="artists")


class PlayListAttributes(BaseModel):
    has_time_synced_lyrics: bool = Field(..., alias="hasTimeSyncedLyrics")
    album_name: str = Field(..., alias="albumName")
    genre_names: List[str] = Field(..., alias="genreNames")
    track_number: int = Field(..., alias="trackNumber")
    release_date: Optional[str] = Field(None, alias="releaseDate")
    duration_in_millis: Optional[int] = Field(None, alias="durationInMillis")
    is_vocal_attenuation_allowed: bool = Field(..., alias="isVocalAttenuationAllowed")
    is_mastered_for_itunes: bool = Field(..., alias="isMasteredForItunes")
    isrc: str
    artwork: ImageModel
    audio_locale: str = Field(..., alias="audioLocale")
    url: str
    play_params: Optional[PlayParams] = Field(None, alias="playParams")
    disc_number: int = Field(..., alias="discNumber")
    has_credits: bool = Field(..., alias="hasCredits")
    is_apple_digital_master: bool = Field(..., alias="isAppleDigitalMaster")
    has_lyrics: bool = Field(..., alias="hasLyrics")
    audio_traits: List[str] = Field(..., alias="audioTraits")
    name: str
    previews: List[UrlDTO]
    content_rating: Optional[str] = Field(None, alias="contentRating")
    artist_name: str = Field(..., alias="artistName")


class PlayList(BaseIdTypeHref):
    attributes: PlayListAttributes
    relationships: PlayListRelationshipDTO
    meta: MetaContentVersion
