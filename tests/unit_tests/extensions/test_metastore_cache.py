# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from typing import Any

import pytest
from flask import Flask

from superset.extensions.metastore_cache import SupersetMetastoreCache
from superset.key_value.types import JsonKeyValueCodec, PickleKeyValueCodec


def _build(app: Flask, config: dict[str, Any]) -> SupersetMetastoreCache:
    cache = SupersetMetastoreCache.factory(app, config, [], {})
    assert isinstance(cache, SupersetMetastoreCache)
    return cache


def test_factory_defaults_to_json_codec(app: Flask) -> None:
    with app.app_context():
        cache = _build(app, {"CACHE_TYPE": "SupersetMetastoreCache"})
    assert isinstance(cache.codec, JsonKeyValueCodec)


def test_factory_pickle_requires_explicit_opt_in(
    app: Flask, caplog: pytest.LogCaptureFixture
) -> None:
    with app.app_context(), caplog.at_level("WARNING"):
        app.debug = False
        cache = _build(
            app,
            {"CACHE_TYPE": "SupersetMetastoreCache", "CODEC": PickleKeyValueCodec()},
        )
    assert isinstance(cache.codec, PickleKeyValueCodec)
    assert any(
        "PickleKeyValueCodec" in record.message and "CODEC" in record.message
        for record in caplog.records
    )
