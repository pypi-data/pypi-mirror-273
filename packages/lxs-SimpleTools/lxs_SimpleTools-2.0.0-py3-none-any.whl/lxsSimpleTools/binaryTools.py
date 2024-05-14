class NumberConverter:
    @staticmethod
    def decimal_to_binary(decimal_number):
        """将十进制转换为二进制"""
        return bin(decimal_number)

    @staticmethod
    def decimal_to_octal(decimal_number):
        """将十进制转换为八进制"""
        return oct(decimal_number)

    @staticmethod
    def decimal_to_hexadecimal(decimal_number):
        """将十进制转换为十六进制"""
        return hex(decimal_number)

    @staticmethod
    def binary_to_decimal(binary_number):
        """将二进制转换为十进制"""
        return int(binary_number, 2)

    @staticmethod
    def binary_to_octal(binary_number):
        """将二进制转换为八进制"""
        decimal_number = int(binary_number, 2)
        return oct(decimal_number)

    @staticmethod
    def binary_to_hexadecimal(binary_number):
        """将二进制转换为十六进制"""
        decimal_number = int(binary_number, 2)
        return hex(decimal_number)

    @staticmethod
    def octal_to_decimal(octal_number):
        """将八进制转换为十进制"""
        return int(octal_number, 8)

    @staticmethod
    def octal_to_binary(octal_number):
        """将八进制转换为二进制"""
        decimal_number = int(octal_number, 8)
        return bin(decimal_number)

    @staticmethod
    def octal_to_hexadecimal(octal_number):
        """将八进制转换为十六进制"""
        decimal_number = int(octal_number, 8)
        return hex(decimal_number)

    @staticmethod
    def hexadecimal_to_decimal(hexadecimal_number):
        """将十六进制转换为十进制"""
        return int(hexadecimal_number, 16)

    @staticmethod
    def hexadecimal_to_binary(hexadecimal_number):
        """将十六进制转换为二进制"""
        decimal_number = int(hexadecimal_number, 16)
        return bin(decimal_number)

    @staticmethod
    def hexadecimal_to_octal(hexadecimal_number):
        """将十六进制转换为八进制"""
        decimal_number = int(hexadecimal_number, 16)
        return oct(decimal_number)
