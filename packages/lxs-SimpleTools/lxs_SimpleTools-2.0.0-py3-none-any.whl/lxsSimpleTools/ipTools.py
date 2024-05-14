import socket
import ipaddress


class IPUtils:
    @staticmethod
    def get_local_ip():
        """获取本机IP地址。"""
        ip = socket.gethostbyname(socket.gethostname())
        return ip

    @staticmethod
    def is_valid_ip(ip):
        """检查IP地址是否合法。"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_network(ip):
        """提取IP地址中的网络部分。"""
        network = ipaddress.ip_network(ip, strict=False)
        return str(network.network_address)

    @staticmethod
    def get_host(ip):
        """提取IP地址中的主机部分。"""
        network = ipaddress.ip_network(ip, strict=False)
        return str(network.hosts())

    @staticmethod
    def is_same_network(ip1, ip2):
        """检查两个IP地址是否在同一个网络中。"""
        network1 = ipaddress.ip_network(ip1, strict=False)
        network2 = ipaddress.ip_network(ip2, strict=False)
        return network1.network_address == network2.network_address

    @staticmethod
    def ipv4_to_hex(ip):
        """将IPv4地址转换为十六进制表示。"""
        hex_ip = socket.inet_aton(ip).hex()
        return hex_ip

    @staticmethod
    def hex_to_ipv4(hex_ip):
        """将十六进制表示的IPv4地址转换为标准表示。"""
        ip = socket.inet_ntoa(bytes.fromhex(hex_ip))
        return ip

    @staticmethod
    def is_private_ip(ip):
        """检查IP地址是否为私有地址。"""
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private

    @staticmethod
    def is_public_ip(ip):
        """检查IP地址是否为公网地址。"""
        ip_obj = ipaddress.ip_address(ip)
        return not ip_obj.is_private

    @staticmethod
    def reverse_dns_lookup(ip):
        """获取IP地址的反向解析（域名）。"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except socket.herror:
            return None
