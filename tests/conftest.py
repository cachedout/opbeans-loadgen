# -*- coding: utf-8 -*-

# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations

"""
Tests for the Openbeans Load Generator
"""
import os
import pytest
import dyno.app

@pytest.fixture
def default_environment(monkeypatch):
    """
    Set up default variables to produce a functional
    test environment
    """
    monkeypatch.setenv("OPBEANS_URLS", "opbeans-python:http://opbeans-python:3000")
    monkeypatch.setenv("OPBEANS_RPMS", "opbeans-python:500")
    monkeypatch.setenv("OPBEANS_RLS", "opbeans-python:500")

@pytest.fixture(scope="session")
def app():
    """
    This overrides the app() function to initialize the pytest-flask
    plugin
    """
    dyno_app = dyno.app.create_app()
    return dyno_app

@pytest.fixture
def scenarios():
    """
    This fixture calculates the scenarios present in the application
    """
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    fixture_path = os.path.join(cur_dir, "../scenarios")
    scenario_files = os.listdir(fixture_path)
    scenarios = [scenario.replace('.py', '') for scenario in scenario_files]
    return scenarios

@pytest.fixture
def procfile():
    """
    Provide a procfile stub for use in tests
    """
    return "python: "
    "OPBEANS_BASE_URL=http://opbeans-python:3000 "
    "OPBEANS_NAME=opbeans-python molotov "
    "-v --duration 500 --delay 0.120 "
    "--uvloop molotov_scenarios.py"


@pytest.fixture
def job_status():
    return {
            'python': {
                'url': 'http://opbeans-python:3000',
                'name': 'opbeans-python',
                'running': False,
                'p': None}
            }

