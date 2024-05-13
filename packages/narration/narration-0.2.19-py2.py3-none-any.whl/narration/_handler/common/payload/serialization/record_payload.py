import logging
from typing import Dict, Any, Type, List

import msgspec

from narration._handler.common.payload.payload import LogRecordPayload, PayloadType
from narration._handler.common.payload.serialization.generic import (
    to_log_record_native_type,
    from_log_record_native_type,
)


class NarrationTransport(msgspec.Struct):
    payloads: List[LogRecordPayload]


def _enc_hook(obj: Any) -> Any:
    if isinstance(obj, logging.LogRecord):
        # Convert LogRecord -> Dict
        return to_log_record_native_type(record=obj)

    # Raise a TypeError for other types
    raise TypeError(f"Objects of type {type(obj)} are not supported")


def _dec_hook(typ: Type, obj: Any) -> Any:
    if typ is logging.LogRecord:
        # Convert Dict -> LogRecord
        return from_log_record_native_type(obj)

    # Raise a TypeError for other types
    raise TypeError(f"Objects of type {typ} are not supported")


_encoder = msgspec.msgpack.Encoder(enc_hook=_enc_hook)
_decoder = msgspec.msgpack.Decoder(NarrationTransport, dec_hook=_dec_hook)


def to_transport_payload(payloads: List[PayloadType] = None) -> NarrationTransport:
    return NarrationTransport(payloads=payloads)


def to_record_payload(transport_payload: Dict = None) -> List[PayloadType]:
    return transport_payload.payloads


def to_binary_payload(data: Dict = None) -> bytes:
    # 2x or better speed up than msgpack library: https://jcristharif.com/msgspec/benchmarks.html
    if data is None:
        data = {}
    return _encoder.encode(data)


def to_unbinary_payload(data: bytes = None) -> Dict:
    return _decoder.decode(data)
