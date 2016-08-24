# vi: ts=4 expandtab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3, as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
This supports rendering output format for netifrc that is used in gentoo.

https://wiki.gentoo.org/wiki/Netifrc
"""

import os
import re

from . import renderer

from cloudinit import util


def _make_header(sep='#'):
    lines = [
        "Created by cloud-init on instance boot automatically, do not edit.",
        "",
    ]
    for i in range(0, len(lines)):
        if lines[i]:
            lines[i] = sep + " " + lines[i]
        else:
            lines[i] = sep
    return "\n".join(lines)


def _is_default_route(route):
    if route['network'] == '::' and route['netmask'] == 0:
        return True
    if route['network'] == '0.0.0.0' and route['netmask'] == '0.0.0.0':
        return True
    return False


def _quote_value(value):
    if re.search(r"\s", value):
        # This doesn't handle complex cases...
        if value.startswith('"') and value.endswith('"'):
            return value
        else:
            return '"%s"' % value
    else:
        return value


def _create_network_symlink(interface_name, target):
    file_path = os.path.join(target, 'etc/init.d/net.{name}'.format(
        name=interface_name))
    if not util.is_link(file_path):
        util.sym_link('/etc/init.d/net.lo', file_path)


class Renderer(renderer.Renderer):
    """Renders network information in a /etc/network/interfaces format."""

    def __init__(self, config=None):
        if not config:
            config = {}
        self.conf_dir = config.get('confd_dir', 'etc/conf.d/')
        self.dns_path = config.get('dns_path', 'etc/resolv.conf')

    @classmethod
    def _render_netifrc_conf(cls, network_state):
        """Given state, return /etc/conf.d/net + contents"""
        # [
        #  {
        #   'mac_address': 'fa:16:3e:00:10:ee',
        #   'name': 'eth0',
        #   'mtu': None,
        #   'type': 'physical',
        #   'subnets': [{'type': 'dhcp4'}]
        #  },
        #  {
        #   'address': '10.0.1.3',
        #   'type': 'nameserver'
        #  }
        # ]

        contents = {}
        return contents

    def render_network_state(self, target, network_state):
        base_confd_dir = os.path.join(target, self.conf_dir)

        self._render_netifrc_conf(network_state)
        # for iface in network_state.iter_interfaces():
        #    _create_network_symlink(iface['name'], target)
