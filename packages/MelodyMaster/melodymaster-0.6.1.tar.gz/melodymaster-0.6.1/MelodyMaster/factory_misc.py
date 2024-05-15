from dataclass_factory import Factory

from MelodyMaster.factory import FactorySchemas
from MelodyMaster.schemas.artists import ArtistInfo
from MelodyMaster.schemas.artists import ArtistV3
from MelodyMaster.schemas.attributes import ArtistAttribute
from MelodyMaster.schemas.models import (
    SongSection,
    VideoSection,
    RelatedSection,
    LyricsSection,
    BeaconDataLyricsSection,
    ArtistSection,
    MatchModel,
)
from MelodyMaster.schemas.models import TrackInfo
from MelodyMaster.schemas.models import YoutubeData
from MelodyMaster.schemas.models import ResponseTrack


FACTORY_TRACK = Factory(
    schemas={
        TrackInfo: FactorySchemas.FACTORY_TRACK_SCHEMA,
        SongSection: FactorySchemas.FACTORY_SONG_SECTION_SCHEMA,
        VideoSection: FactorySchemas.FACTORY_VIDEO_SECTION_SCHEMA,
        LyricsSection: FactorySchemas.FACTORY_LYRICS_SECTION,
        BeaconDataLyricsSection: FactorySchemas.FACTORY_BEACON_DATA_LYRICS_SECTION,
        ArtistSection: FactorySchemas.FACTORY_ARTIST_SECTION,
        MatchModel: FactorySchemas.FACTORY_MATCH,
        RelatedSection: FactorySchemas.FACTORY_RELATED_SECTION_SCHEMA,
        YoutubeData: FactorySchemas.FACTORY_YOUTUBE_TRACK_SCHEMA,
        ResponseTrack: FactorySchemas.FACTORY_RESPONSE_TRACK_SCHEMA,
    },
    debug_path=True,
)

FACTORY_ARTIST = Factory(
    schemas={
        ArtistAttribute: FactorySchemas.FACTORY_ATTRIBUTES_ARTIST,
        ArtistV3: FactorySchemas.FACTORY_ARTIST_V2,
        ArtistInfo: FactorySchemas.FACTORY_ARTIST_SCHEMA,
    },
    debug_path=True,
)
