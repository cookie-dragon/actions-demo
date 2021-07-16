#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython   : language_level=2
# @Time    : 2020/4/1 10:21 上午
# @Author  : Cooky Long
# @File    : pyshell
import os
import commands
import time

from sqlalchemy import event, create_engine, Column, TEXT, BOOLEAN, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine


class IpCheck(object):
    @staticmethod
    def find_first(string, str):
        return string.find(str)

    @staticmethod
    def find_last(string, str):
        last_position = -1
        while True:
            position = string.find(str, last_position + 1)
            if position == -1:
                return last_position
            last_position = position

    @staticmethod
    def ipv4_to_int(value):
        rst = 0
        if IpCheck.check_ipv4(value):
            parts = value.split('.')
            for i in range(4):
                rst = rst + int(parts[i]) * pow(256, 3 - i)
        return rst

    @staticmethod
    def int_to_ipv4(value):
        fields = [0 for i in range(4)]
        fields[0] = value // pow(256, 3)
        fields[1] = (value - pow(256, 3) * fields[0]) // pow(256, 2)
        fields[2] = (value - pow(256, 3) * fields[0] - pow(256, 2) * fields[1]) // 256
        fields[3] = value - pow(256, 3) * fields[0] - pow(256, 2) * fields[1] - 256 * fields[2]
        return str(fields[0]) + '.' + str(fields[1]) + '.' + str(fields[2]) + '.' + str(fields[3])

    @staticmethod
    def check_ipv4(value):
        parts = value.split('.')
        if len(parts) == 4 and all(x.isdigit() for x in parts):
            numbers = list(int(x) for x in parts)
            return all(0 <= num < 256 for num in numbers)
        return False

    @staticmethod
    def check_netmask(value):
        if IpCheck.check_ipv4(value):
            i = IpCheck.ipv4_to_int(value)
            b_str = bin(i).replace('0b', '')
            pos_last_1 = IpCheck.find_last(b_str, '1')
            pos_first_0 = IpCheck.find_first(b_str, '0')
            if pos_last_1 < pos_first_0:
                return True
            else:
                return False
        else:
            return False


engine = create_engine('sqlite:///identifier.sqlite?check_same_thread=False')
Base = declarative_base()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class STNetworkIface(Base):
    __tablename__ = 'config_network_iface'
    iface = Column(TEXT, nullable=False, unique=True, primary_key=True)
    mode = Column(TEXT, nullable=False, default='off')
    address = Column(TEXT)
    netmask = Column(TEXT)
    gateway = Column(TEXT)
    wlan_ssid = Column(TEXT)
    wlan_psk = Column(TEXT)
    gateway_dhcp_start = Column(TEXT)
    gateway_dhcp_end = Column(TEXT)
    property_code = Column(TEXT)


class STNetworkRouteAddNet(Base):
    __tablename__ = 'config_network_route_add_net'
    id = Column(INTEGER, nullable=False, unique=True, primary_key=True)
    netaddress = Column(TEXT, nullable=False)
    netmask = Column(TEXT, nullable=False)
    localgateway = Column(TEXT, nullable=False)


class STNetworkIfaceDefault(Base):
    __tablename__ = 'config_network_iface_default'
    iface = Column(TEXT, nullable=False, unique=True, primary_key=True)
    mode = Column(TEXT, nullable=False, default='off')
    address = Column(TEXT)
    netmask = Column(TEXT)
    gateway = Column(TEXT)
    wlan_ssid = Column(TEXT)
    wlan_psk = Column(TEXT)
    gateway_dhcp_start = Column(TEXT)
    gateway_dhcp_end = Column(TEXT)
    property_code = Column(TEXT)


class STDictNetworkInterfaceProperty(Base):
    __tablename__ = 'dict_network_interface_property'
    property_code = Column(TEXT, nullable=False, unique=True, primary_key=True)
    ifacetyp = Column(TEXT, nullable=False)
    mode = Column(TEXT, nullable=False)
    vpn = Column(BOOLEAN, nullable=False)
    eth_inet = Column(TEXT)
    gateway_dhcp = Column(BOOLEAN)


class STSwitch(Base):
    __tablename__ = 'config_switch'
    key = Column(TEXT, nullable=False, unique=True, primary_key=True)
    value = Column(TEXT)


class STDictHtlinkWlanpowergpioProperty(Base):
    __tablename__ = 'dict_htlink_wlanpowergpio_property'
    model = Column(TEXT, nullable=False, unique=True, primary_key=True)
    gpio = Column(TEXT, nullable=False)


class STAutoDefaultRouteInfo(Base):
    __tablename__ = 'auto_default_route_info'
    destination = Column(TEXT, nullable=False)
    gateway = Column(TEXT, nullable=False)
    genmask = Column(TEXT, nullable=False)
    flags = Column(TEXT, nullable=False)
    metric = Column(INTEGER, nullable=False)
    ref = Column(INTEGER, nullable=False)
    use = Column(INTEGER, nullable=False)
    iface = Column(TEXT, nullable=False, unique=True, primary_key=True)

    def __init__(self, destination, gateway, genmask, flags, metric, ref, use, iface):
        self.destination = destination
        self.gateway = gateway
        self.genmask = genmask
        self.flags = flags
        self.metric = metric
        self.ref = ref
        self.use = use
        self.iface = iface

    def __str__(self):
        return self.destination + ',' + self.gateway + ',' + self.genmask + ',' + self.flags + ',' + str(
            self.metric) + ',' + str(self.ref) + ',' + str(self.use) + ',' + self.iface


class Config(object):

    @staticmethod
    def iswifideviceonpower():
        return_code, output = commands.getstatusoutput('lsusb')
        if return_code == 0:
            if output.find('0bda:8179') != -1:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def iscardconnected(card):
        return_code, output = commands.getstatusoutput('ip addr show ' + card)
        if return_code == 0:
            if output and output != '':
                return True
            else:
                return False
        else:
            return False

    def startwifidevice(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        devicemodelRow = session.query(STSwitch).filter_by(key='devicemodel').first()
        if devicemodelRow:
            devicemodel = devicemodelRow.value
            gpioRow = session.query(STDictHtlinkWlanpowergpioProperty).filter_by(model=devicemodel).first()
            if gpioRow:
                gpio = gpioRow.gpio
            else:
                gpio = None
        else:
            gpio = None

        if gpio:
            os.system('gpio_test ' + gpio + ' 1')
        else:
            gpios = []
            gpioRows = session.query(STDictHtlinkWlanpowergpioProperty).all()
            for gpioRow in gpioRows:
                gpios.append(gpioRow.gpio)
            gpios = list(set(gpios))
            for gpio in gpios:
                os.system('gpio_test ' + gpio + ' 1')

        os.system('insmod /lib/modules/3.2.0/8188eu.ko')
        for i in range(3):
            time.sleep(1)
            if Config.iswifideviceonpower():
                return True
        return False

    def startdhcpserver(self, abpath_udhcpd_conf):
        if os.path.exists(abpath_udhcpd_conf):
            os.system('udhcpd -f ' + abpath_udhcpd_conf + ' &')

    __abpath_interfaces = '/etc/network/interfaces'
    # __abpath_interfaces = 'pyshell2/interfaces'
    __abpath_wpa_supplicant_conf = '/etc/wpa_supplicant.conf'
    # __abpath_wpa_supplicant_conf = 'pyshell2/wpa_supplicant.conf'
    __abpath_hostapd_conf = '/etc/hostapd.conf'
    # __abpath_hostapd_conf = 'pyshell2/hostapd.conf'

    __vpn_bridge_name = 'br-vpn'

    def __config_init_interfaces(self):
        interfaces_lines = [
            '# ' + self.__abpath_interfaces + ' -- configuration file for ifup(8), ifdown(8)' + os.linesep,
            os.linesep,
            '# The loopback interface' + os.linesep + 'auto lo' + os.linesep + 'iface lo inet loopback' + os.linesep
        ]

        with open(self.__abpath_interfaces, 'w+') as f:
            f.writelines(interfaces_lines)

    def __config_vpn(self, networkConfigRow):
        interfaces_lines = [os.linesep]
        interfaces_lines.append('iface ' + self.__vpn_bridge_name + ' inet static' + os.linesep +
                                '\taddress ' + networkConfigRow[0].address + os.linesep +
                                '\tnetmask ' + networkConfigRow[0].netmask + os.linesep +
                                '\tgateway ' + networkConfigRow[0].gateway + os.linesep)
        with open(self.__abpath_interfaces, 'a+') as f:
            f.writelines(interfaces_lines)

    def __gateway_wlan(self, isConfig, networkConfigRow):
        abpath_udhcpd_conf = 'udhcpd_' + networkConfigRow[0].iface + '.conf'
        if isConfig:
            interfaces_lines = [os.linesep]
            interfaces_lines.append(
                'iface ' + networkConfigRow[0].iface + ' inet static' + os.linesep)
            interfaces_lines.append('\taddress ' + networkConfigRow[0].address + os.linesep +
                                    '\tnetmask ' + networkConfigRow[0].netmask + os.linesep +
                                    '\tgateway ' + networkConfigRow[0].gateway + os.linesep)
            with open(self.__abpath_interfaces, 'a+') as f:
                f.writelines(interfaces_lines)

            hostapd_conf_line = [
                '##### hostapd configuration file ##############################################' + os.linesep,
                'interface=' + networkConfigRow[0].iface + os.linesep,
                'logger_syslog=-1' + os.linesep,
                'logger_syslog_level=2' + os.linesep,
                'logger_stdout=-1' + os.linesep,
                'logger_stdout_level=2' + os.linesep,
                'dump_file=/tmp/hostapd.dump' + os.linesep,
                'ctrl_interface=/var/run/hostapd' + os.linesep,
                'ctrl_interface_group=0' + os.linesep,
                '##### IEEE 802.11 related configuration #######################################' + os.linesep,
                'ssid=' + networkConfigRow[0].wlan_ssid + os.linesep,
                'hw_mode=g' + os.linesep,
                'channel=6' + os.linesep,
                'beacon_int=100' + os.linesep,
                'dtim_period=2' + os.linesep,
                'max_num_sta=255' + os.linesep,
                'rts_threshold=2347' + os.linesep,
                'fragm_threshold=2346' + os.linesep,
                'macaddr_acl=0' + os.linesep,
                'auth_algs=3' + os.linesep,
                'ignore_broadcast_ssid=0' + os.linesep,
                'wmm_enabled=1' + os.linesep,
                'wmm_ac_bk_cwmin=4' + os.linesep,
                'wmm_ac_bk_cwmax=10' + os.linesep,
                'wmm_ac_bk_aifs=7' + os.linesep,
                'wmm_ac_bk_txop_limit=0' + os.linesep,
                'wmm_ac_bk_acm=0' + os.linesep,
                'wmm_ac_be_aifs=3' + os.linesep,
                'wmm_ac_be_cwmin=4' + os.linesep,
                'wmm_ac_be_cwmax=10' + os.linesep,
                'wmm_ac_be_txop_limit=0' + os.linesep,
                'wmm_ac_be_acm=0' + os.linesep,
                'wmm_ac_vi_aifs=2' + os.linesep,
                'wmm_ac_vi_cwmin=3' + os.linesep,
                'wmm_ac_vi_cwmax=4' + os.linesep,
                'wmm_ac_vi_txop_limit=94' + os.linesep,
                'wmm_ac_vi_acm=0' + os.linesep,
                'wmm_ac_vo_aifs=2' + os.linesep,
                'wmm_ac_vo_cwmin=2' + os.linesep,
                'wmm_ac_vo_cwmax=3' + os.linesep,
                'wmm_ac_vo_txop_limit=47' + os.linesep,
                'wmm_ac_vo_acm=0' + os.linesep,
                '##### IEEE 802.11n related configuration ######################################' + os.linesep,
                'ht_capab=[SHORT-GI-20][SHORT-GI-40][HT40]' + os.linesep,
                '##### IEEE 802.1X-2004 related configuration ##################################' + os.linesep,
                'eapol_key_index_workaround=0' + os.linesep,
                '##### Integrated EAP server ###################################################' + os.linesep,
                'eap_server=0' + os.linesep,
                '##### RADIUS client configuration #############################################' + os.linesep,
                'own_ip_addr=127.0.0.1' + os.linesep,
                '##### WPA/IEEE 802.11i configuration ##########################################' + os.linesep,
                'wpa=2' + os.linesep,
                'wpa_passphrase=' + networkConfigRow[0].wlan_psk + os.linesep,
                'wpa_key_mgmt=WPA-PSK' + os.linesep,
                'wpa_pairwise=CCMP' + os.linesep,
            ]
            with open(self.__abpath_hostapd_conf, 'w+') as f:
                f.writelines(hostapd_conf_line)

            udhcpd_conf_lines = ['interface ' + networkConfigRow[0].iface + os.linesep,
                                 'option subnet ' + networkConfigRow[0].netmask + os.linesep,
                                 'opt router ' + networkConfigRow[0].gateway + os.linesep,
                                 'opt dns 114.114.114.114 114.114.115.115' + os.linesep,
                                 'start ' + networkConfigRow[0].gateway_dhcp_start + os.linesep,
                                 'end ' + networkConfigRow[0].gateway_dhcp_end + os.linesep,
                                 'max_leases ' + str(
                                     IpCheck.ipv4_to_int(
                                         networkConfigRow[0].gateway_dhcp_end) - IpCheck.ipv4_to_int(
                                         networkConfigRow[0].gateway_dhcp_start) + 1) + os.linesep,
                                 ]
            with open(abpath_udhcpd_conf, 'w+') as f:
                f.writelines(udhcpd_conf_lines)
        else:
            if self.startwifidevice():
                os.system('hostapd ' + self.__abpath_hostapd_conf + ' -B')
                os.system('ifup ' + networkConfigRow[0].iface)
                time.sleep(3)
                os.system('route del default')
                self.startdhcpserver(abpath_udhcpd_conf)

    def __gateway_eth(self, isConfig, networkConfigRow):
        abpath_udhcpd_conf = 'udhcpd_' + networkConfigRow[0].iface + '.conf'
        if isConfig:
            interfaces_lines = [os.linesep]
            interfaces_lines.append(
                'iface ' + networkConfigRow[0].iface + ' inet static' + os.linesep)
            interfaces_lines.append('\taddress ' + networkConfigRow[0].address + os.linesep +
                                    '\tnetmask ' + networkConfigRow[0].netmask + os.linesep +
                                    '\tgateway ' + networkConfigRow[0].gateway + os.linesep)
            with open(self.__abpath_interfaces, 'a+') as f:
                f.writelines(interfaces_lines)

            if networkConfigRow.STDictNetworkInterfaceProperty.gateway_dhcp:
                udhcpd_conf_lines = ['interface ' + networkConfigRow[0].iface + os.linesep,
                                     'option subnet ' + networkConfigRow[0].netmask + os.linesep,
                                     'opt router ' + networkConfigRow[0].gateway + os.linesep,
                                     'opt dns 114.114.114.114 114.114.115.115' + os.linesep,
                                     'start ' + networkConfigRow[0].gateway_dhcp_start + os.linesep,
                                     'end ' + networkConfigRow[0].gateway_dhcp_end + os.linesep,
                                     'max_leases ' + str(
                                         IpCheck.ipv4_to_int(
                                             networkConfigRow[0].gateway_dhcp_end) - IpCheck.ipv4_to_int(
                                             networkConfigRow[0].gateway_dhcp_start) + 1) + os.linesep,
                                     ]
                with open(abpath_udhcpd_conf, 'w+') as f:
                    f.writelines(udhcpd_conf_lines)
        else:
            # os.system('ifdown ' + networkConfigRow[0].iface)
            # time.sleep(1)
            os.system('ifup ' + networkConfigRow[0].iface)
            time.sleep(3)
            for i in range(3):
                if Config.iscardconnected(networkConfigRow[0].iface):
                    os.system('route del default')
                    if networkConfigRow.STDictNetworkInterfaceProperty.gateway_dhcp:
                        self.startdhcpserver(abpath_udhcpd_conf)
                    break
                else:
                    time.sleep(1)

    def __vice_pppd(self, isConfig, networkConfigRow):
        if isConfig:
            pass
        else:
            os.system('yiyuan_4g')
            time.sleep(5)
            self.addDefaultRouterIntoDB()
            time.sleep(1)
            os.system('route del default')

    def __vice_wlan(self, isConfig, networkConfigRow):
        if isConfig:
            interfaces_lines = [os.linesep]
            interfaces_lines.append('iface ' + networkConfigRow[0].iface + ' inet dhcp' + os.linesep +
                                    '\twireless_mode managed' + os.linesep +
                                    '\twireless_essid any' + os.linesep +
                                    '\twpa-driver wext' + os.linesep +
                                    '\twpa-conf ' + self.__abpath_wpa_supplicant_conf + os.linesep)
            with open(self.__abpath_interfaces, 'a+') as f:
                f.writelines(interfaces_lines)

            wpa_supplicant_conf_lines = ['ctrl_interface=/var/run/wpa_supplicant' + os.linesep +
                                         'ctrl_interface_group=0' + os.linesep +
                                         'update_config=1' + os.linesep +
                                         os.linesep,
                                         ]
            with open(self.__abpath_wpa_supplicant_conf, 'w+') as f:
                f.writelines(wpa_supplicant_conf_lines)
            if networkConfigRow[0].wlan_psk and len(networkConfigRow[0].wlan_psk) > 0:
                os.system(
                    'wpa_passphrase \"' + networkConfigRow[0].wlan_ssid + '\" \"' + networkConfigRow[
                        0].wlan_psk + '\" >> ' + self.__abpath_wpa_supplicant_conf)
            else:
                wpa_supplicant_conf_lines_add = ['network={' + os.linesep +
                                                 '\tssid=\"' + networkConfigRow[0].wlan_ssid + '\"' + os.linesep +
                                                 '\tkey_mgmt=NONE' + os.linesep +
                                                 '}' +
                                                 os.linesep]
                with open(self.__abpath_wpa_supplicant_conf, 'a+') as f:
                    f.writelines(wpa_supplicant_conf_lines_add)
        else:
            if self.startwifidevice():
                os.system('ifconfig ' + networkConfigRow[0].iface + ' up')
                os.system(
                    'wpa_supplicant -i' + networkConfigRow[
                        0].iface + ' -c ' + self.__abpath_wpa_supplicant_conf + ' -B')
                os.system('udhcpc -i ' + networkConfigRow[0].iface + ' -B &')
                time.sleep(5)
                self.addDefaultRouterIntoDB()
                time.sleep(1)
                os.system('route del default')

    def __vice_eth(self, isConfig, networkConfigRow):
        if isConfig:
            interfaces_lines = [os.linesep]
            interfaces_lines.append(
                'iface ' + networkConfigRow[
                    0].iface + ' inet ' + networkConfigRow.STDictNetworkInterfaceProperty.eth_inet + os.linesep)
            if networkConfigRow.STDictNetworkInterfaceProperty.eth_inet == 'static':
                interfaces_lines.append('\taddress ' + networkConfigRow[0].address + os.linesep +
                                        '\tnetmask ' + networkConfigRow[0].netmask + os.linesep +
                                        '\tgateway ' + networkConfigRow[0].gateway + os.linesep)
            with open(self.__abpath_interfaces, 'a+') as f:
                f.writelines(interfaces_lines)
        else:
            # os.system('ifdown ' + networkConfigRow[0].iface)
            # time.sleep(1)
            os.system('ifup ' + networkConfigRow[0].iface)
            time.sleep(5)
            self.addDefaultRouterIntoDB()
            time.sleep(1)
            os.system('route del default')

    def __main_pppd(self, isConfig, networkConfigRow):
        if isConfig:
            pass
        else:
            os.system('yiyuan_4g')
            time.sleep(5)
            self.addDefaultRouterIntoDB()
            time.sleep(1)
            os.system('iptables -t nat -A POSTROUTING -o ' + networkConfigRow[0].iface + ' -j MASQUERADE')

    def __main_wlan(self, isConfig, networkConfigRow):
        if isConfig:
            interfaces_lines = [os.linesep]
            interfaces_lines.append('iface ' + networkConfigRow[0].iface + ' inet dhcp' + os.linesep +
                                    '\twireless_mode managed' + os.linesep +
                                    '\twireless_essid any' + os.linesep +
                                    '\twpa-driver wext' + os.linesep +
                                    '\twpa-conf ' + self.__abpath_wpa_supplicant_conf + os.linesep)
            with open(self.__abpath_interfaces, 'a+') as f:
                f.writelines(interfaces_lines)

            wpa_supplicant_conf_lines = ['ctrl_interface=/var/run/wpa_supplicant' + os.linesep +
                                         'ctrl_interface_group=0' + os.linesep +
                                         'update_config=1' + os.linesep +
                                         os.linesep,
                                         ]
            with open(self.__abpath_wpa_supplicant_conf, 'w+') as f:
                f.writelines(wpa_supplicant_conf_lines)
            if networkConfigRow[0].wlan_psk and len(networkConfigRow[0].wlan_psk) > 0:
                os.system(
                    'wpa_passphrase \"' + networkConfigRow[0].wlan_ssid + '\" \"' + networkConfigRow[
                        0].wlan_psk + '\" >> ' + self.__abpath_wpa_supplicant_conf)
            else:
                wpa_supplicant_conf_lines_add = ['network={' + os.linesep +
                                                 '\tssid=\"' + networkConfigRow[0].wlan_ssid + '\"' + os.linesep +
                                                 '\tkey_mgmt=NONE' + os.linesep +
                                                 '}' +
                                                 os.linesep]
                with open(self.__abpath_wpa_supplicant_conf, 'a+') as f:
                    f.writelines(wpa_supplicant_conf_lines_add)
        else:
            if self.startwifidevice():
                os.system('ifconfig ' + networkConfigRow[0].iface + ' up')
                os.system(
                    'wpa_supplicant -i' + networkConfigRow[
                        0].iface + ' -c ' + self.__abpath_wpa_supplicant_conf + ' -B')
                os.system('udhcpc -i ' + networkConfigRow[0].iface + ' -B &')
                time.sleep(5)
                self.addDefaultRouterIntoDB()
                time.sleep(1)
                os.system(
                    'iptables -t nat -A POSTROUTING -o ' + networkConfigRow[0].iface + ' -j MASQUERADE')

    def __main_eth(self, isConfig, networkConfigRow):
        if isConfig:
            interfaces_lines = [os.linesep]
            interfaces_lines.append(
                'iface ' + networkConfigRow[
                    0].iface + ' inet ' + networkConfigRow.STDictNetworkInterfaceProperty.eth_inet + os.linesep)
            if networkConfigRow.STDictNetworkInterfaceProperty.eth_inet == 'static':
                interfaces_lines.append('\taddress ' + networkConfigRow[0].address + os.linesep +
                                        '\tnetmask ' + networkConfigRow[0].netmask + os.linesep +
                                        '\tgateway ' + networkConfigRow[0].gateway + os.linesep)
            with open(self.__abpath_interfaces, 'a+') as f:
                f.writelines(interfaces_lines)
        else:
            # os.system('ifdown ' + networkConfigRow[0].iface)
            # time.sleep(1)
            os.system('ifup ' + networkConfigRow[0].iface)
            time.sleep(5)
            self.addDefaultRouterIntoDB()
            time.sleep(1)
            os.system('iptables -t nat -A POSTROUTING -o ' + networkConfigRow[0].iface + ' -j MASQUERADE')

    def __route_add_net(self, isConfig, networkConfigRouteAddNetRow):
        if isConfig:
            pass
        else:
            time.sleep(1)
            cmd = 'route add -net ' + networkConfigRouteAddNetRow.netaddress + ' netmask ' + networkConfigRouteAddNetRow.netmask + ' gw ' + networkConfigRouteAddNetRow.localgateway
            os.system('echo \"' + cmd + '\" >> routeUG.sh')
            os.system(cmd)

    def run(self, isConfig=True):
        Session = sessionmaker(bind=engine)
        session = Session()
        switch_check = session.query(STSwitch).filter_by(key='check').first()
        if switch_check and (switch_check.value == '1'):
            networkConfigRows = session.query(STNetworkIface, STDictNetworkInterfaceProperty).outerjoin(
                STDictNetworkInterfaceProperty,
                STDictNetworkInterfaceProperty.property_code == STNetworkIface.property_code).all()
            networkConfigRouteAddNetRows = session.query(STNetworkRouteAddNet).all()

            if isConfig:
                self.__config_init_interfaces()

                switch_vpn = session.query(STSwitch).filter_by(key='vpn').first()
                if switch_vpn and switch_vpn.value != None:
                    for networkConfigRow in networkConfigRows:
                        if networkConfigRow.STNetworkIface.iface == switch_vpn.value:
                            self.__config_vpn(networkConfigRow)
                            break

            for networkConfigRow in networkConfigRows:
                if networkConfigRow.STNetworkIface.mode == 'gateway':
                    if networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'wlan':
                        self.__gateway_wlan(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'eth':
                        self.__gateway_eth(isConfig, networkConfigRow)

            for networkConfigRow in networkConfigRows:
                if networkConfigRow.STNetworkIface.mode == 'vice':
                    if networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'pppd':
                        self.__vice_pppd(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'wlan':
                        self.__vice_wlan(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'eth':
                        self.__vice_eth(isConfig, networkConfigRow)

            for networkConfigRow in networkConfigRows:
                if networkConfigRow.STNetworkIface.mode == 'main':
                    if networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'pppd':
                        self.__main_pppd(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'wlan':
                        self.__main_wlan(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'eth':
                        self.__main_eth(isConfig, networkConfigRow)
                    break

            os.system('echo \"#!/bin/sh\" > routeUG.sh')
            for networkConfigRouteAddNetRow in networkConfigRouteAddNetRows:
                self.__route_add_net(isConfig, networkConfigRouteAddNetRow)
            os.system('chmod +x routeUG.sh')

        else:
            networkConfigRows = session.query(STNetworkIfaceDefault, STDictNetworkInterfaceProperty).outerjoin(
                STDictNetworkInterfaceProperty,
                STDictNetworkInterfaceProperty.property_code == STNetworkIfaceDefault.property_code).all()

            if isConfig:
                self.__config_init_interfaces()
            else:
                self.run(isConfig=True)

            for networkConfigRow in networkConfigRows:
                if networkConfigRow.STNetworkIfaceDefault.mode == 'gateway':
                    if networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'wlan':
                        self.__gateway_wlan(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'eth':
                        self.__gateway_eth(isConfig, networkConfigRow)

            for networkConfigRow in networkConfigRows:
                if networkConfigRow.STNetworkIfaceDefault.mode == 'vice':
                    if networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'pppd':
                        self.__vice_pppd(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'wlan':
                        self.__vice_wlan(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'eth':
                        self.__vice_eth(isConfig, networkConfigRow)

            for networkConfigRow in networkConfigRows:
                if networkConfigRow.STNetworkIfaceDefault.mode == 'main':
                    if networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'pppd':
                        self.__main_pppd(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'wlan':
                        self.__main_wlan(isConfig, networkConfigRow)
                    elif networkConfigRow.STDictNetworkInterfaceProperty.ifacetyp == 'eth':
                        self.__main_eth(isConfig, networkConfigRow)
                    break

        print 'Finish!!!!!!!!!!'

    def getRouters(self):
        p = os.popen('route -n')
        lines = p.readlines()

        routers = []
        realData = False
        for line in lines:
            line_str_list = line.split()
            if line_str_list[0] == 'Destination':
                realData = True
                continue
            if realData:
                routers.append(
                    STAutoDefaultRouteInfo(line_str_list[0], line_str_list[1], line_str_list[2], line_str_list[3],
                                           line_str_list[4], line_str_list[5], line_str_list[6], line_str_list[7]))

        return routers

    def getDefaultRouter(self):
        routers = self.getRouters()
        trashDefCount = 0
        defRouter = None
        for router in routers:
            if router.destination == '0.0.0.0':
                if defRouter != None:
                    trashDefCount = trashDefCount + 1
                defRouter = router

        for i in range(trashDefCount):
            os.system('route del default')
            time.sleep(3)

        return defRouter

    def addDefaultRouterIntoDB(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        defRouter = self.getDefaultRouter()
        if defRouter is not None:
            defRouterInDB = session.query(STAutoDefaultRouteInfo).filter_by(iface=defRouter.iface).first()
            if defRouterInDB != None:
                defRouterInDB.destination = defRouter.destination
                defRouterInDB.gateway = defRouter.gateway
                defRouterInDB.genmask = defRouter.genmask
                defRouterInDB.flags = defRouter.flags
                defRouterInDB.metric = defRouter.metric
                defRouterInDB.ref = defRouter.ref
                defRouterInDB.use = defRouter.use
                session.commit()
            else:
                session.add(defRouter)
                session.commit()

    def monitorDefaultRouter(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        mainiface = session.query(STNetworkIface).filter_by(mode='main').first().iface  # 肯定有
        defRouterInDB = session.query(STAutoDefaultRouteInfo).filter_by(iface=mainiface).first()  # 不一定有
        if defRouterInDB != None:
            mainifacegw = defRouterInDB.gateway  # 肯定有
            defRouter = self.getDefaultRouter()  # 不一定有
            if defRouter != None:
                if defRouter.iface == mainiface:
                    defRouterInDB.destination = defRouter.destination
                    defRouterInDB.gateway = defRouter.gateway
                    defRouterInDB.genmask = defRouter.genmask
                    defRouterInDB.flags = defRouter.flags
                    defRouterInDB.metric = defRouter.metric
                    defRouterInDB.ref = defRouter.ref
                    defRouterInDB.use = defRouter.use
                    session.commit()
                else:  # 如果默认路由不是当前主出口
                    os.system('route del default')
                    time.sleep(1)
                    os.system('route add default gw ' + mainifacegw)
            else:  # 如果没有默认路由
                os.system('route add default gw ' + mainifacegw)
