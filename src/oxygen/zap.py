import json
import xml.etree.ElementTree as ETree

from collections import defaultdict

from robot.api import logger

from .base_handler import BaseHandler
from .errors import SubprocessException, ZAProxyHandlerException
from .utils import run_command_line, validate_path


class ZAProxyHandler(BaseHandler):
    def run_zap(self, result_file, command, check_return_code=False, **env):
        '''Run Zed Attack Proxy security testing tool specified with
        ``command``.

        See documentation for other arguments in \`Run Gatling\`.
        '''
        try:
            output = run_command_line(command, check_return_code, **env)
        except SubprocessException as e:
            raise ZAProxyHandlerException(e)
        logger.info(output)
        logger.info('Result file: {}'.format(result_file))
        return result_file

    def cli(self):
        cli_interface = self.DEFAULT_CLI.copy()
        cli_interface[('--accepted-risk-level',)] = {
            'help': 'Set accepted risk level',
            'type': int
        }
        cli_interface[('--required-confidence-level',)] = {
            'help': 'Set required confidence level',
            'type': int
        }
        return cli_interface

    def parse_results(self, result_file, accepted_risk_level=None,
                      required_confidence_level=None):
        if accepted_risk_level is not None:
            self._config['accepted_risk_level'] = accepted_risk_level
        if required_confidence_level is not None:
            self._config['required_confidence_level'] = \
                required_confidence_level
        zap_dict = self._read_results(validate_path(result_file).resolve())
        return self._parse_zap_dict(zap_dict)

    def _read_results(self, file_name):
        with open(file_name) as test_file:
            result_contents = test_file.read()

        try:
            json_dict = self._xml_to_dict(ETree.XML(result_contents))
            if 'OWASPZAPReport' in json_dict.keys():
                json_dict = json_dict['OWASPZAPReport']
        except:
            print('Oxygen: Loading {} as XML failed, falling '
                  'back to JSON.'.format(file_name))
            json_dict = json.loads(result_contents)
        return json_dict

    def _xml_to_dict(self, xml):
        d = {xml.tag: {} if xml.attrib else None}
        children = list(xml)
        if children:
            dd = defaultdict(list)
            for dc in map(self._xml_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {xml.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if xml.attrib:
            d[xml.tag].update(('@' + k, v) for k, v in xml.attrib.items())
        if xml.text:
            text = xml.text.strip()
            if children or xml.attrib:
                if text:
                  d[xml.tag]['#text'] = text
            else:
                d[xml.tag] = text
        return d


    def _parse_zap_dict(self, zap_dict):
        zap_version = self._get_parameter(zap_dict, 'version', 'Unknown ZAProxy Version')
        zap_run_date = self._get_parameter(zap_dict, 'generated', 'Unknown ZAProxy Run Time')

        return_dict = {}
        return_dict['name'] = 'Oxygen ZAProxy Report ({}, {})'.format(
            zap_version,
            zap_run_date,
        )

        zap_sites = zap_dict.get('site', [])

        return_dict['tags'] = self._tags
        return_dict['suites'] = []

        for zap_site in zap_sites:
            parsed_site = self._parse_zap_site_dict(zap_site)
            return_dict['suites'].append(parsed_site)

        return return_dict


    def _parse_zap_site_dict(self, zap_site_dict):
        site_name = self._get_parameter(zap_site_dict, 'name', 'Unknown Site Name')

        return_dict = {}
        return_dict['name'] = 'Site: {}'.format(site_name)
        return_dict['tests'] = []

        zap_alerts = zap_site_dict.get('alerts', [])
        zap_alerts = zap_alerts or []

        if isinstance(zap_alerts, dict):
            zap_alerts = zap_alerts.get('alertitem', [])
        if not isinstance(zap_alerts, list):
            zap_alerts = [zap_alerts]
        for zap_alert in zap_alerts:
            parsed_alert = self._parse_zap_alert_dict(zap_alert)
            return_dict['tests'].append(parsed_alert)

        return return_dict


    def _parse_zap_alert_dict(self, zap_alert_dict):
        plugin_id = zap_alert_dict.get('pluginid', '[Unknown Plugin ID]')
        alert_name = zap_alert_dict.get('name', 'Unknown Alert Name')
        zap_instances = zap_alert_dict.get('instances', [])
        tags = []

        return_dict = {}
        return_dict['name'] = '{} {}'.format(plugin_id, alert_name)
        return_dict['tags'] = tags
        return_dict['keywords'] = []

        considered_risk = self._is_considered_risk(zap_alert_dict)
        is_confident = self._is_considered_confident(zap_alert_dict)

        if isinstance(zap_instances, dict):
            zap_instances = zap_instances.get('instance', None)
            if not isinstance(zap_instances, list):
                zap_instances = filter(None, [zap_instances])

        for zap_instance in zap_instances:
            parsed_instance = self._parse_zap_instance(zap_instance,
                                                       considered_risk,
                                                       is_confident,
            )
            return_dict['keywords'].append(parsed_instance)

        return return_dict


    def _is_considered_risk(self, zap_alert_dict):
        risk_level = zap_alert_dict.get('riskcode', -1)
        risk_level = int(risk_level)

        if risk_level < 0:
            risk_level = 3

        acceptable_risk = self._get_treshold_risk_level()
        considered_risk = (risk_level >= acceptable_risk)

        return considered_risk


    def _is_considered_confident(self, zap_alert_dict):
        confidence_level = zap_alert_dict.get('confidence', -1)
        confidence_level = int(confidence_level)

        if confidence_level < 0:
            confidence_level = 3

        required_confidence = self._get_required_confidence_level()
        is_confident = (confidence_level >= required_confidence)

        return is_confident


    def _parse_zap_instance(self, zap_instance_dict, risk, confident):
        zap_uri = zap_instance_dict.get('uri', '[Unknown Target URI]')
        zap_method = zap_instance_dict.get('method', '[Unknown HTTP Method]')
        zap_param = zap_instance_dict.get('param', '[Unknown Target Parameter]')
        zap_evidence = zap_instance_dict.get('evidence', '[No Evidence Provided]')

        return_dict = {}
        return_dict['name'] = '{} {}: {}'.format(zap_method, zap_uri, zap_param)
        return_dict['pass'] = not (risk and confident)
        return_dict['elapsed'] = 0.0
        return_dict['messages'] = []
        return_dict['messages'].append('Evidence: {}'.format(zap_evidence))

        return return_dict


    def _get_parameter(self, zap_dict, name, default_text):
        special_name = '@' + name

        return_value = zap_dict.get(name, None)
        if not return_value:
            return_value = zap_dict.get(special_name, default_text)

        return return_value


    def _get_treshold_risk_level(self):
        risk_level = self._config.get('accepted_risk_level', None)

        if risk_level is None:
            print('No acceptable risk level configured, defaulting to 0')
            return 0

        risk_level = int(risk_level)

        if risk_level > 3:
            print('Risk level is configured too high, maximizing at 3')
            return 3

        return risk_level


    def _get_required_confidence_level(self):
        confidence_level = self._config.get('required_confidence_level', None)

        if confidence_level is None:
            print('No required confidence level configured, defaulting to 0')
            return 0

        confidence_level = int(confidence_level)

        if confidence_level > 3:
            print('Confidence level is configured too high, maximizing at 3')
            return 3

        return confidence_level
