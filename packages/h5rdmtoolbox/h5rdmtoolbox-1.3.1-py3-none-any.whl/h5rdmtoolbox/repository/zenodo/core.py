import abc
import json
import logging
import pathlib
import time
import warnings
from typing import Union, List, Callable, Iterable, Dict

import appdirs
import requests

from .metadata import Metadata
from .tokens import get_api_token
from ..interface import RepositoryInterface

logger = logging.getLogger('h5rdmtoolbox')

__all__ = ['Metadata']


class AbstractZenodoInterface(RepositoryInterface, abc.ABC):
    """Interface for Zenodo.
    """
    depositions_url = None
    rec_url = None

    def __init__(self,
                 rec_id: Union[int, None]):
        """Initialize the ZenodoInterface.

        Parameters
        ----------
        rec_id : int or None
            The rec_id of the deposit. If None, a new deposit will be created.
            If a rec_id is passed, the deposit must exist.

        """
        if self.depositions_url is None:
            raise ValueError('The depositions_url must be set.')
        if rec_id is None:
            # create a new deposit (with new rec_id and without metadata!)
            r = requests.post(
                self.depositions_url,
                json={},
                params={"access_token": self.access_token},
                headers={"Content-Type": "application/json"}
            )
            r.raise_for_status()
            rec_id = r.json()['id']

        self.rec_id = rec_id
        if not self.exists():
            raise ValueError(f'The deposit with rec_id {rec_id} does not exist. '
                             f'To create a new one, please pass rec_id=None.')

        assert self.rec_id is not None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} (id={self.rec_id}, url={self.depositions_url})"

    @abc.abstractmethod
    def get_metadata(self) -> Dict:
        """Return metadata"""

    @abc.abstractmethod
    def get(self, raise_for_status: bool):
        """Get the deposit (json) data."""

    def get_doi(self) -> str:
        """Get the DOI of the deposit."""
        doi = self.json()['metadata'].get('doi', None)
        if doi is None:
            return self.json()['metadata']['prereserve_doi']['doi']
        return doi

    def exists(self) -> bool:
        """Check if the deposit exists on Zenodo."""
        r = self.get(raise_for_status=False)
        if r.status_code == 404:
            return False
        return True

    def is_published(self) -> bool:
        """Check if the deposit is published."""
        return self.json()['submitted']

    submitted = is_published  # alias

    def get(self, raise_for_status: bool = False) -> requests.Response:
        """Get the deposit (json) data."""

        warnings.warn("get() method is deprecated. Use json() instead.", DeprecationWarning)

        def _fetch(token):
            return requests.get(f"{self.depositions_url}/{self.rec_id}", params={"access_token": token})

        r = _fetch(self.access_token)
        while r.status_code == 429:
            logger.info(f"Too many requests message: {r.json()}. Sleep for 60 seconds and try again.")
            time.sleep(60)
            r = _fetch()

        while r.status_code == 500:
            logger.info(f"Internal error: {r.json()}. Sleep for 60 seconds and try again.")
            time.sleep(60)
            r = _fetch()

        if raise_for_status:
            r.raise_for_status()
        return r

    def json(self, raise_for_status: bool = False):
        """Get the deposit (json) data."""

        def _fetch(token):
            return requests.get(f"{self.depositions_url}/{self.rec_id}", params={"access_token": token})

        r = _fetch(self.access_token)
        while r.status_code == 429:
            logger.info(f"Too many requests message: {r.json()}. Sleep for 60 seconds and try again.")
            time.sleep(60)
            r = _fetch()

        while r.status_code == 500:
            logger.info(f"Internal error: {r.json()}. Sleep for 60 seconds and try again.")
            time.sleep(60)
            r = _fetch()

        if raise_for_status:
            r.raise_for_status()
        return r.json()

    def download_files(self,
                       target_folder: Union[str, pathlib.Path] = None,
                       suffix: Union[str, List[str], None] = None) -> List[pathlib.Path]:
        """Download all (!) files from Zenodo. You may specify one or multiple suffixes to only download certain files.

        Parameters
        ----------
        target_folder : str or pathlib.Path, optional
            The target folder, by default None
        suffix: Union[str, List[str], None], optional=None
            Specify a suffix to only download certain files

        Returns
        -------
        List[pathlib.Path]
            A list of all downloaded files.
        """
        if suffix is None:
            return [self.download_file(filename, target_folder=target_folder) for filename in self.get_filenames()]
        if isinstance(suffix, str):
            suffix = [suffix]
        return [self.download_file(filename, target_folder=target_folder) for filename in self.get_filenames() if
                filename.endswith(tuple(suffix))]

    def download_file(self,
                      filename: str,
                      target_folder: Union[str, pathlib.Path] = None) -> pathlib.Path:
        """Download a single file from Zenodo.

        Parameters
        ----------
        filename : str
            The filename to download
        target_folder : Union[str, pathlib.Path], optional
            The target folder, by default None
            If None, the file will be downloaded to the default folder, which is in
            the user data directory of the h5rdmtoolbox package.

        Returns
        -------
        pathlib.Path
            The path to the downloaded file.
        """
        if target_folder is None:
            target_folder = pathlib.Path(appdirs.user_data_dir('h5rdmtoolbox')) / 'zenodo_downloads' / str(
                self.rec_id)
            target_folder.mkdir(exist_ok=True, parents=True)
        else:
            logger.debug(f'A target folder was specified. Downloading file to this folder: {target_folder}')
            target_folder = pathlib.Path(target_folder)
        data = self.json()
        for f in data['files']:
            fname = f.get('filename') or f['key']
            if fname == filename:
                target_filename = target_folder / fname
                logger.debug(f'Downloading file "{fname}" to "{target_filename}"')

                if data['submitted']:
                    url = f'{self.rec_url}/{data["id"]}/files/{filename}'
                else:
                    url = f'{self.rec_url}/{data["id"]}/draft/files/{filename}'
                r = requests.get(url, params={'access_token': self.access_token})
                if r.ok:
                    # r.json()['links']['content']
                    _content_response = requests.get(r.json()['links']['content'],
                                                     params={'access_token': self.access_token})
                    if _content_response.ok:
                        with open(target_filename, 'wb') as file:
                            file.write(_content_response.content)
                    else:
                        raise requests.HTTPError(f'Could not download file "{filename}" from Zenodo. '
                                                 f'Status code: {_content_response.status_code}')
                else:
                    raise requests.HTTPError(f'Could not download file "{filename}" from Zenodo. '
                                             f'Status code: {r.status_code}')

                return target_filename
        raise KeyError(f'File "{filename}" not found in deposit "{self.rec_id}"')

    def delete(self) -> requests.Response:
        """Delete the deposit."""
        r = requests.delete(f"{self.depositions_url}/{self.rec_id}", params={"access_token": self.access_token})
        if r.status_code == 405:
            logger.error(f'Only unpublished records can be deleted. Record "{self.rec_id}" is published.')
        return r


class ZenodoSandboxDeposit(AbstractZenodoInterface):
    """Interface to Zenodo's testing (sandbox) api. API TOKEN needed.

    Note: Metadata can always be changed, without publishing a new version!

    Examples
    --------
    new repo:
    >>> repo = ZenodoSandboxDeposit(rec_id=None)
    new version:
    >>> repo = ZenodoSandboxDeposit(rec_id=12345)
    >>> new_repo = repo.new_version()
    >>> new_repo.discard()


    """
    depositions_url = 'https://sandbox.zenodo.org/api/deposit/depositions'
    rec_url = "https://sandbox.zenodo.org/api/records"

    def get_metadata(self) -> Dict:
        return self.json()['metadata']
        # return Metadata(**self.json()['metadata'])

    def set_metadata(self, metadata: Union[Dict, Metadata]):
        """update the metadata of the deposit"""
        if isinstance(metadata, dict):
            metadata = Metadata(**metadata)
        else:
            if not isinstance(metadata, Metadata):
                raise TypeError('The metadata must be of type Metadata, not {type(metadata)}')
        r = requests.put(
            self.json()['links']['latest_draft'],
            data=json.dumps(dict(metadata=metadata.model_dump(exclude_none=True))),
            params={"access_token": self.access_token},
            # headers={"Content-Type": "application/json"}
        )
        if r.status_code == 400:
            logger.critical(f"Bad request message: {r.json()}")
        r.raise_for_status()

    def unlock(self):
        """unlock the deposit. To lock it call publish()"""
        r = requests.post(self.json()['links']['edit'],
                          params={'access_token': self.access_token})
        if r.status_code == 400:
            print(f'Cannot publish data. This might be because metadata is missing. Check on the website, which '
                  f'fields are required!')
        r.raise_for_status()

    def new_version(self):
        self.unlock()
        jdata = self.json()
        r = requests.post(jdata['links']['newversion'],
                          params={'access_token': self.access_token})
        r.raise_for_status()
        latest_draft = r.json()['links']['latest_draft']
        _id = latest_draft.split('/')[-1]
        self.rec_id = _id
        return self

    def discard(self):
        """Discard the latest action, e.g. creating a new version"""
        jdata = self.json()
        r = requests.post(jdata['links']['discard'],
                          params={'access_token': self.access_token})
        r.raise_for_status()

    def publish(self) -> requests.Response:
        """Be careful. The record cannot be deleted afterwards!"""
        print(self.json()['links']['publish'])
        r = requests.post(self.json()['links']['publish'],
                          # data=json.dumps({'publication_date': '2024-03-03', 'version': '1.2.3'}),
                          params={'access_token': self.access_token})
        r.raise_for_status()

    @property
    def access_token(self):
        """Return current access token for the Zenodo API."""
        return get_api_token(sandbox=True)

    def get_filenames(self, suffix=None) -> Iterable[str]:
        """Get a list of all filenames. If suffix is given, only filenames
        with this suffix are returned."""
        file_dict = {f['filename']: f for f in self.json()['files']}
        if suffix is not None:
            remove = []
            for f in file_dict:
                if f.endswith(suffix):
                    remove.append(f)
            for r in remove:
                file_dict.pop(r)
        return file_dict

    def upload_file(self, filename, overwrite: bool = False):
        """Add a file to the deposit. If the filename already exists, it can
        be overwritten with overwrite=True"""
        filename = pathlib.Path(filename)
        if not filename.exists():
            raise FileNotFoundError(f'File "{filename}" does not exist.')

        existing_filenames = self.get_filenames()
        if not overwrite:
            # we need to check if the file already exists
            if filename.name in existing_filenames:
                logger.debug(f'Overwriting file "{filename}" in deposit "{self.rec_id}"')
                warnings.warn(f'Filename "{filename}" already exists in deposit. Skipping..."', UserWarning)
                return

        # get file id
        if filename.name in existing_filenames:
            file_id = existing_filenames[filename.name]['id']
            url = f"{self.depositions_url}/{self.rec_id}/files/{file_id}"
            logger.debug(f'requests.delete(url={url}, ...)')
            r = requests.delete(url=url,
                                params={'access_token': self.access_token})
            r.raise_for_status()
        # else:
        #     url = self.json()['links']['files']
        #     logger.debug(f'requests.delete(url={url}, ...)')
        #     r = requests.delete(url=url,
        #                         params={'access_token': self.access_token})
        #     r.raise_for_status()

        # bucket_url = self.json()["links"]["bucket"]
        # if filename.name in existing_filenames:
        #     # delete the file first
        #     url = f"{self.depositions_url}/{self.rec_id}/files/{file_id}"
        #     logger.debug(f'requests.delete(url={url}, ...)')
        #     r = requests.delete(url=url,
        #                         params={'access_token': self.access_token})
        #     r.raise_for_status()

        # https://developers.zenodo.org/?python#quickstart-upload
        bucket_url = self.json()["links"]["bucket"]
        logger.debug(f'adding file "{filename}" to deposit "{self.rec_id}"')
        with open(filename, "rb") as fp:
            r = requests.put(f"{bucket_url}/{filename.name}",
                             data=fp,
                             params={"access_token": self.access_token},
                             )
            if r.status_code == 403:
                logger.critical(f"Access denied message: {r.json()}. This could be because the record is published. "
                                f"You can only modify metadata.")
            r.raise_for_status()


class ZenodoRecord(AbstractZenodoInterface):
    """Interface to Zenodo records."""

    depositions_url = 'https://zenodo.org/api/records'
    rec_url = "https://zenodo.org/api/records"

    @property
    def access_token(self):
        """Get the access token for the Zenodo API. This is needed to upload files."""
        return get_api_token(sandbox=False)

    def get_metadata(self) -> Dict:
        return self.json()['metadata']

    def set_metadata(self, metadata: Metadata):
        """update the metadata of the deposit"""
        if not isinstance(metadata, Metadata):
            raise TypeError('The metadata must be of type Metadata, not {type(metadata)}')
        r = requests.put(
            self.json()['links']['latest_draft'],
            data=json.dumps(dict(metadata=metadata.model_dump(exclude_none=True))),
            params={"access_token": self.access_token},
            # headers={"Content-Type": "application/json"}
        )
        if r.status_code == 400:
            logger.critical(f"Bad request message: {r.json()}")
        r.raise_for_status()

    def upload_file(self, filename, overwrite: bool = False):
        raise RuntimeError(f'The {self.__class__.__name__} does not support file uploads.')

    def upload_hdf_file(self, filename, metamapper: Callable, overwrite: bool = False):
        raise RuntimeError(f'The {self.__class__.__name__} does not support file uploads.')

    def get_filenames(self) -> List[str]:
        """Get a list of all filenames."""
        return [f['key'] for f in self.json()['files']]
