# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Iterable, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.bigquery_storage_v1.types import arrow
from google.cloud.bigquery_storage_v1.types import avro
from google.cloud.bigquery_storage_v1.types import storage
from google.cloud.bigquery_storage_v1.types import stream
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import BigQueryReadTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import BigQueryReadGrpcTransport
from .transports.grpc_asyncio import BigQueryReadGrpcAsyncIOTransport


class BigQueryReadClientMeta(type):
    """Metaclass for the BigQueryRead client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[BigQueryReadTransport]]
    _transport_registry["grpc"] = BigQueryReadGrpcTransport
    _transport_registry["grpc_asyncio"] = BigQueryReadGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[BigQueryReadTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class BigQueryReadClient(metaclass=BigQueryReadClientMeta):
    """BigQuery Read API.
    The Read API can be used to read data from BigQuery.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "bigquerystorage.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BigQueryReadTransport:
        """Return the transport used by the client instance.

        Returns:
            BigQueryReadTransport: The transport used by the client instance.
        """
        return self._transport

    @staticmethod
    def read_session_path(project: str, location: str, session: str,) -> str:
        """Return a fully-qualified read_session string."""
        return "projects/{project}/locations/{location}/sessions/{session}".format(
            project=project, location=location, session=session,
        )

    @staticmethod
    def parse_read_session_path(path: str) -> Dict[str, str]:
        """Parse a read_session path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/sessions/(?P<session>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def read_stream_path(
        project: str, location: str, session: str, stream: str,
    ) -> str:
        """Return a fully-qualified read_stream string."""
        return "projects/{project}/locations/{location}/sessions/{session}/streams/{stream}".format(
            project=project, location=location, session=session, stream=stream,
        )

    @staticmethod
    def parse_read_stream_path(path: str) -> Dict[str, str]:
        """Parse a read_stream path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/sessions/(?P<session>.+?)/streams/(?P<stream>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def table_path(project: str, dataset: str, table: str,) -> str:
        """Return a fully-qualified table string."""
        return "projects/{project}/datasets/{dataset}/tables/{table}".format(
            project=project, dataset=dataset, table=table,
        )

    @staticmethod
    def parse_table_path(path: str) -> Dict[str, str]:
        """Parse a table path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)/tables/(?P<table>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Return a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Return a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Return a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Return a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Return a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, BigQueryReadTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the big query read client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BigQueryReadTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (client_options_lib.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, BigQueryReadTransport):
            # transport is a BigQueryReadTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                ssl_channel_credentials=ssl_credentials,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_read_session(
        self,
        request: storage.CreateReadSessionRequest = None,
        *,
        parent: str = None,
        read_session: stream.ReadSession = None,
        max_stream_count: int = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> stream.ReadSession:
        r"""Creates a new read session. A read session divides
        the contents of a BigQuery table into one or more
        streams, which can then be used to read data from the
        table. The read session also specifies properties of the
        data to be read, such as a list of columns or a push-
        down filter describing the rows to be returned.

        A particular row can be read by at most one stream. When
        the caller has reached the end of each stream in the
        session, then all the data in the table has been read.

        Data is assigned to each stream such that roughly the
        same number of rows can be read from each stream.
        Because the server-side unit for assigning data is
        collections of rows, the API does not guarantee that
        each stream will return the same number or rows.
        Additionally, the limits are enforced based on the
        number of pre-filtered rows, so some filters can lead to
        lopsided assignments.

        Read sessions automatically expire 24 hours after they
        are created and do not require manual clean-up by the
        caller.

        Args:
            request (:class:`~.storage.CreateReadSessionRequest`):
                The request object. Request message for
                `CreateReadSession`.
            parent (:class:`str`):
                Required. The request project that owns the session, in
                the form of ``projects/{project_id}``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            read_session (:class:`~.stream.ReadSession`):
                Required. Session to be created.
                This corresponds to the ``read_session`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            max_stream_count (:class:`int`):
                Max initial number of streams. If
                unset or zero, the server will provide a
                value of streams so as to produce
                reasonable throughput. Must be non-
                negative. The number of streams may be
                lower than the requested number,
                depending on the amount parallelism that
                is reasonable for the table. Error will
                be returned if the max count is greater
                than the current system max limit of
                1,000.

                Streams must be read starting from
                offset 0.
                This corresponds to the ``max_stream_count`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.stream.ReadSession:
                Information about the ReadSession.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, read_session, max_stream_count])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.CreateReadSessionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.CreateReadSessionRequest):
            request = storage.CreateReadSessionRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if read_session is not None:
                request.read_session = read_session
            if max_stream_count is not None:
                request.max_stream_count = max_stream_count

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_read_session]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("read_session.table", request.read_session.table),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def read_rows(
        self,
        request: storage.ReadRowsRequest = None,
        *,
        read_stream: str = None,
        offset: int = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[storage.ReadRowsResponse]:
        r"""Reads rows from the stream in the format prescribed
        by the ReadSession. Each response contains one or more
        table rows, up to a maximum of 100 MiB per response;
        read requests which attempt to read individual rows
        larger than 100 MiB will fail.

        Each request also returns a set of stream statistics
        reflecting the current state of the stream.

        Args:
            request (:class:`~.storage.ReadRowsRequest`):
                The request object. Request message for `ReadRows`.
            read_stream (:class:`str`):
                Required. Stream to read rows from.
                This corresponds to the ``read_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            offset (:class:`int`):
                The offset requested must be less
                than the last row read from Read.
                Requesting a larger offset is undefined.
                If not specified, start reading from
                offset zero.
                This corresponds to the ``offset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[~.storage.ReadRowsResponse]:
                Response from calling ``ReadRows`` may include row data,
                progress and throttling information.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([read_stream, offset])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ReadRowsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ReadRowsRequest):
            request = storage.ReadRowsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if read_stream is not None:
                request.read_stream = read_stream
            if offset is not None:
                request.offset = offset

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.read_rows]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("read_stream", request.read_stream),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def split_read_stream(
        self,
        request: storage.SplitReadStreamRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.SplitReadStreamResponse:
        r"""Splits a given ``ReadStream`` into two ``ReadStream`` objects.
        These ``ReadStream`` objects are referred to as the primary and
        the residual streams of the split. The original ``ReadStream``
        can still be read from in the same manner as before. Both of the
        returned ``ReadStream`` objects can also be read from, and the
        rows returned by both child streams will be the same as the rows
        read from the original stream.

        Moreover, the two child streams will be allocated back-to-back
        in the original ``ReadStream``. Concretely, it is guaranteed
        that for streams original, primary, and residual, that
        original[0-j] = primary[0-j] and original[j-n] = residual[0-m]
        once the streams have been read to completion.

        Args:
            request (:class:`~.storage.SplitReadStreamRequest`):
                The request object. Request message for
                `SplitReadStream`.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.storage.SplitReadStreamResponse:
                Response message for ``SplitReadStream``.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.SplitReadStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.SplitReadStreamRequest):
            request = storage.SplitReadStreamRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.split_read_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-storage",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigQueryReadClient",)
