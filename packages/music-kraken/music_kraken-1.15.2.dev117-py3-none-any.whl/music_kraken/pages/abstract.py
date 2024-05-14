import logging
import random
import re
from copy import copy
from pathlib import Path
from typing import Optional, Union, Type, Dict, Set, List, Tuple, TypedDict
from string import Formatter
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

from ..connection import Connection
from ..objects import (
    Song,
    Source,
    Album,
    Artist,
    Target,
    DatabaseObject,
    Options,
    Collection,
    Label,
)
from ..utils.enums.source import SourcePages
from ..utils.enums.album import AlbumType
from ..audio import write_metadata_to_target, correct_codec
from ..utils.config import main_settings
from ..utils.support_classes.query import Query
from ..utils.support_classes.download_result import DownloadResult
from ..utils.string_processing import fit_to_file_system
from ..utils import trace, output, BColors

INDEPENDENT_DB_OBJECTS = Union[Label, Album, Artist, Song]
INDEPENDENT_DB_TYPES = Union[Type[Song], Type[Album], Type[Artist], Type[Label]]

@dataclass
class FetchOptions:
    download_all: bool = False
    album_type_blacklist: Set[AlbumType] = field(default_factory=lambda: set(AlbumType(a) for a in main_settings["album_type_blacklist"]))

@dataclass
class DownloadOptions:
    download_all: bool = False
    album_type_blacklist: Set[AlbumType] = field(default_factory=lambda: set(AlbumType(a) for a in main_settings["album_type_blacklist"]))

    process_audio_if_found: bool = False
    process_metadata_if_found: bool = True

class NamingDict(dict):
    CUSTOM_KEYS: Dict[str, str] = {
        "label": "label.name",
        "artist": "artist.name",
        "song": "song.title",
        "isrc": "song.isrc",
        "album": "album.title",
        "album_type": "album.album_type_string"
    }

    def __init__(self, values: dict, object_mappings: Dict[str, DatabaseObject] = None):
        self.object_mappings: Dict[str, DatabaseObject] = object_mappings or dict()

        super().__init__(values)
        self["audio_format"] = main_settings["audio_format"]

    def add_object(self, music_object: DatabaseObject):
        self.object_mappings[type(music_object).__name__.lower()] = music_object

    def copy(self) -> dict:
        return type(self)(super().copy(), self.object_mappings.copy())

    def __getitem__(self, key: str) -> str:
        return fit_to_file_system(super().__getitem__(key))

    def default_value_for_name(self, name: str) -> str:
        return f'Various {name.replace("_", " ").title()}'

    def __missing__(self, key: str) -> str:
        if "." not in key:
            if key not in self.CUSTOM_KEYS:
                return self.default_value_for_name(key)

            key = self.CUSTOM_KEYS[key]

        frag_list = key.split(".")

        object_name = frag_list[0].strip().lower()
        attribute_name = frag_list[-1].strip().lower()

        if object_name not in self.object_mappings:
            return self.default_value_for_name(attribute_name)

        music_object = self.object_mappings[object_name]
        try:
            value = getattr(music_object, attribute_name)
            if value is None:
                return self.default_value_for_name(attribute_name)

            return str(value)

        except AttributeError:
            return self.default_value_for_name(attribute_name)


class Page:
    """
    This is an abstract class, laying out the 
    functionality for every other class fetching something
    """

    SOURCE_TYPE: SourcePages
    LOGGER = logging.getLogger("this shouldn't be used")

    # set this to true, if all song details can also be fetched by fetching album details
    NO_ADDITIONAL_DATA_FROM_SONG = False

    def __init__(self, download_options: DownloadOptions = None, fetch_options: FetchOptions = None):
        self.download_options: DownloadOptions = download_options or DownloadOptions()
        self.fetch_options: FetchOptions = fetch_options or FetchOptions()

    def _search_regex(self, pattern, string, default=None, fatal=True, flags=0, group=None):
        """
        Perform a regex search on the given string, using a single or a list of
        patterns returning the first matching group.
        In case of failure return a default value or raise a WARNING or a
        RegexNotFoundError, depending on fatal, specifying the field name.
        """

        if isinstance(pattern, str):
            mobj = re.search(pattern, string, flags)
        else:
            for p in pattern:
                mobj = re.search(p, string, flags)
                if mobj:
                    break

        if mobj:
            if group is None:
                # return the first matching group
                return next(g for g in mobj.groups() if g is not None)
            elif isinstance(group, (list, tuple)):
                return tuple(mobj.group(g) for g in group)
            else:
                return mobj.group(group)

        return default

    def get_source_type(self, source: Source) -> Optional[Type[DatabaseObject]]:
        return None

    def get_soup_from_response(self, r: requests.Response) -> BeautifulSoup:
        return BeautifulSoup(r.content, "html.parser")

    # to search stuff
    def search(self, query: Query) -> List[DatabaseObject]:
        music_object = query.music_object

        search_functions = {
            Song: self.song_search,
            Album: self.album_search,
            Artist: self.artist_search,
            Label: self.label_search
        }

        if type(music_object) in search_functions:
            r = search_functions[type(music_object)](music_object)
            if r is not None and len(r) > 0:
                return r

        r = []
        for default_query in query.default_search:
            for single_option in self.general_search(default_query):
                r.append(single_option)

        return r

    def general_search(self, search_query: str) -> List[DatabaseObject]:
        return []

    def label_search(self, label: Label) -> List[Label]:
        return []

    def artist_search(self, artist: Artist) -> List[Artist]:
        return []

    def album_search(self, album: Album) -> List[Album]:
        return []

    def song_search(self, song: Song) -> List[Song]:
        return []

    def fetch_details(
        self, 
        music_object: DatabaseObject, 
        stop_at_level: int = 1,
    ) -> DatabaseObject:
        """
        when a music object with lacking data is passed in, it returns
        the SAME object **(no copy)** with more detailed data.
        If you for example put in, an album, it fetches the tracklist

        :param music_object:
        :param stop_at_level: 
        This says the depth of the level the scraper will recurse to.
        If this is for example set to 2, then the levels could be:
        1. Level: the album
        2. Level: every song of the album + every artist of the album
        If no additional requests are needed to get the data one level below the supposed stop level
        this gets ignored
        :return detailed_music_object: IT MODIFIES THE INPUT OBJ
        """
        # creating a new object, of the same type
        new_music_object: Optional[DatabaseObject] = None
        fetched_from_url: List[str] = []

        # only certain database objects, have a source list
        if isinstance(music_object, INDEPENDENT_DB_OBJECTS):
            source: Source
            for source in music_object.source_collection.get_sources(self.SOURCE_TYPE):
                if music_object.already_fetched_from(source.hash_url):
                    continue

                tmp = self.fetch_object_from_source(
                    source=source,
                    enforce_type=type(music_object),
                    stop_at_level=stop_at_level,
                    type_string=type(music_object).__name__,
                    entity_string=music_object.option_string,
                )

                if new_music_object is None:
                    new_music_object = tmp
                else:
                    new_music_object.merge(tmp)
                fetched_from_url.append(source.hash_url)

        if new_music_object is not None:
            music_object.merge(new_music_object)

        music_object.mark_as_fetched(*fetched_from_url)
        return music_object

    def fetch_object_from_source(
        self, 
        source: Source, 
        stop_at_level: int = 2,
        enforce_type: Type[DatabaseObject] = None, 
        type_string: str = "",
        entity_string: str = "",
    ) -> Optional[DatabaseObject]:

        obj_type = self.get_source_type(source)

        if obj_type is None:
            return None

        if enforce_type != obj_type and enforce_type is not None:
            self.LOGGER.warning(f"Object type isn't type to enforce: {enforce_type}, {obj_type}")
            return None

        music_object: DatabaseObject = None

        fetch_map = {
            Song: self.fetch_song,
            Album: self.fetch_album,
            Artist: self.fetch_artist,
            Label: self.fetch_label
        }

        if obj_type in fetch_map:
            music_object = fetch_map[obj_type](source, stop_at_level=stop_at_level)
        else:
            self.LOGGER.warning(f"Can't fetch details of type: {obj_type}")
            return None

        if stop_at_level > 0:
            trace(f"fetching {type_string} [{entity_string}] [stop_at_level={stop_at_level}]")

            collection: Collection
            for collection_str in music_object.DOWNWARDS_COLLECTION_STRING_ATTRIBUTES:
                collection = music_object.__getattribute__(collection_str)

                for sub_element in collection:
                    sub_element.merge(
                        self.fetch_details(sub_element, stop_at_level=stop_at_level - 1))

        return music_object

    def fetch_song(self, source: Source, stop_at_level: int = 1) -> Song:
        return Song()

    def fetch_album(self, source: Source, stop_at_level: int = 1) -> Album:
        return Album()

    def fetch_artist(self, source: Source, stop_at_level: int = 1) -> Artist:
        return Artist()

    def fetch_label(self, source: Source, stop_at_level: int = 1) -> Label:
        return Label()

    def download(
        self, 
        music_object: DatabaseObject, 
        genre: str, 
    ) -> DownloadResult:
        naming_dict: NamingDict = NamingDict({"genre": genre})

        def fill_naming_objects(naming_music_object: DatabaseObject):
            nonlocal naming_dict

            for collection_name in naming_music_object.UPWARDS_COLLECTION_STRING_ATTRIBUTES:
                collection: Collection = getattr(naming_music_object, collection_name)

                if collection.empty:
                    continue
                
                dom_ordered_music_object: DatabaseObject = collection[0]
                naming_dict.add_object(dom_ordered_music_object)
                return fill_naming_objects(dom_ordered_music_object)

        fill_naming_objects(music_object)

        return self._download(music_object, naming_dict)

    def _download(
        self, 
        music_object: DatabaseObject, 
        naming_dict: NamingDict, 
        **kwargs
    ) -> DownloadResult:
        if isinstance(music_object, Song):
            output(f"Downloading {music_object.option_string} to:", color=BColors.BOLD)
        else:
            output(f"Downloading {music_object.option_string}...", color=BColors.BOLD)

        # Skips all releases, that are defined in shared.ALBUM_TYPE_BLACKLIST, if download_all is False
        if isinstance(music_object, Album):
            if not self.download_options.download_all and music_object.album_type in self.download_options.album_type_blacklist:
                return DownloadResult()

        if not (isinstance(music_object, Song) and self.NO_ADDITIONAL_DATA_FROM_SONG):
            self.fetch_details(music_object=music_object, stop_at_level=1)

        if isinstance(music_object, Album):
            music_object.update_tracksort()
            
        naming_dict.add_object(music_object)

        if isinstance(music_object, Song):
            return self._download_song(music_object, naming_dict)

        download_result: DownloadResult = DownloadResult()

        for collection_name in music_object.DOWNWARDS_COLLECTION_STRING_ATTRIBUTES:
            collection: Collection = getattr(music_object, collection_name)

            sub_ordered_music_object: DatabaseObject
            for sub_ordered_music_object in collection:
                download_result.merge(self._download(sub_ordered_music_object, naming_dict.copy()))

        return download_result

    def _download_song(self, song: Song, naming_dict: NamingDict):
        song.compile()
        if "genre" not in naming_dict and song.genre is not None:
            naming_dict["genre"] = song.genre

        if song.genre is None:
            song.genre = naming_dict["genre"]

        path_parts = Formatter().parse(main_settings["download_path"])
        file_parts = Formatter().parse(main_settings["download_file"])
        new_target = Target(
            relative_to_music_dir=True,
            file_path=Path(
                main_settings["download_path"].format(**{part[1]: naming_dict[part[1]] for part in path_parts}),
                main_settings["download_file"].format(**{part[1]: naming_dict[part[1]] for part in file_parts})
            )
        )

        if song.target_collection.empty:
            song.target_collection.append(new_target)

        r = DownloadResult(1)
        temp_target: Target = Target.temp(file_extension=main_settings["audio_format"])

        found_on_disc = False
        target: Target
        for target in song.target_collection:
            current_exists = target.exists

            if current_exists:
                output(f'- {target.file_path} {BColors.OKGREEN.value}[already exists]', color=BColors.GREY)
                target.copy_content(temp_target)
                found_on_disc = True

                r.found_on_disk += 1
                r.add_target(target)
            else:
                output(f'- {target.file_path}', color=BColors.GREY)

        if not song.source_collection.has_source_page(self.SOURCE_TYPE):
            return DownloadResult(error_message=f"No {self.__class__.__name__} source found for {song.option_string}.")

        sources = song.source_collection.get_sources(self.SOURCE_TYPE)

        skip_intervals = []
        if not found_on_disc:
            for source in sources:
                r = self.download_song_to_target(source=source, target=temp_target, desc="downloading")

                if not r.is_fatal_error:
                    skip_intervals = self.get_skip_intervals(song, source)
                    break
        
        if temp_target.exists:
            r.merge(self._post_process_targets(
                song=song, 
                temp_target=temp_target,
                interval_list=skip_intervals,
                found_on_disc=found_on_disc,
            ))

        return r

    def _post_process_targets(self, song: Song, temp_target: Target, interval_list: List, found_on_disc: bool) -> DownloadResult:
        if not found_on_disc or self.download_options.process_audio_if_found:
            correct_codec(temp_target, interval_list=interval_list)

        self.post_process_hook(song, temp_target)

        if not found_on_disc or self.download_options.process_metadata_if_found:
            write_metadata_to_target(song.metadata, temp_target, song)

        r = DownloadResult()

        target: Target
        for target in song.target_collection:
            if temp_target is not target:
                temp_target.copy_content(target)
            r.add_target(target)

        temp_target.delete()
        r.sponsor_segments += len(interval_list)

        return r

    def get_skip_intervals(self, song: Song, source: Source) -> List[Tuple[float, float]]:
        return []

    def post_process_hook(self, song: Song, temp_target: Target, **kwargs):
        pass

    def download_song_to_target(self, source: Source, target: Target, desc: str = None) -> DownloadResult:
        return DownloadResult()
