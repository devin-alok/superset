#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from importlib import import_module
from typing import Any


def load_class_from_name(fq_class_name: str) -> Any:
    """
    Given a string representing a fully qualified class name, attempts to load
    the class and return it.

    :param fq_class_name: The fully qualified name of the class to load
    :return: The class object
    :raises ValueError: if the name is not fully qualified or the class is
        not found in the module
    :raises ModuleNotFoundError: if the module cannot be imported
    """
    if not fq_class_name or "." not in fq_class_name:
        raise ValueError(
            f"Invalid fully qualified class name {fq_class_name!r}; "
            "expected 'package.module.ClassName'"
        )

    module_name, class_name = fq_class_name.rsplit(".", 1)

    module = import_module(module_name)
    try:
        return getattr(module, class_name)
    except AttributeError as ex:
        raise ValueError(
            f"Module {module_name!r} has no class named {class_name!r}"
        ) from ex
