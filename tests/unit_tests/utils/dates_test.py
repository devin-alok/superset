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
import time
from datetime import datetime, timedelta, timezone

from superset.utils.dates import datetime_to_epoch, now_as_float


def test_datetime_to_epoch_naive() -> None:
    assert datetime_to_epoch(datetime(1970, 1, 1)) == 0
    assert datetime_to_epoch(datetime(2020, 1, 1, 12, 0, 0)) == 1577880000000.0


def test_datetime_to_epoch_utc_aware() -> None:
    dttm = datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert datetime_to_epoch(dttm) == 1577880000000.0
    assert datetime_to_epoch(dttm) == datetime_to_epoch(dttm.replace(tzinfo=None))


def test_datetime_to_epoch_non_utc_aware() -> None:
    ist = timezone(timedelta(hours=5, minutes=30))
    dttm = datetime(2020, 1, 1, 17, 30, 0, tzinfo=ist)
    utc_equivalent = datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert datetime_to_epoch(dttm) == datetime_to_epoch(utc_equivalent)
    assert datetime_to_epoch(dttm) == 1577880000000.0


def test_now_as_float() -> None:
    result = now_as_float()
    assert isinstance(result, float)
    assert abs(result - time.time() * 1000) < 5000
