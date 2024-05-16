import logging

from tc66c2mqtt.data_classes import TC66PollData

logger = logging.getLogger(__name__)


def parse_tc66_packet(data: bytes) -> TC66PollData | None:
    """
    https://sigrok.org/wiki/RDTech_TC66C#Protocol_response_format_(%22Poll_data%22)
    """
    pac1: bytes = data[:64]
    logging.debug(f'{pac1=}')
    pac1prefix = pac1[:4]
    if pac1prefix != b'pac1':
        logger.error(f'Invalid prefix {pac1prefix=}')
        return None

    product_name = pac1[4:8].decode('utf-8')  # Product name, e.g.: "TC66"
    version = pac1[8:12].decode('utf-8')  # Version (e.g., 1.14)
    serial = int.from_bytes(pac1[12:16], 'little')

    number_of_runs = int.from_bytes(pac1[44:48], 'little')

    voltage = float(int.from_bytes(pac1[48:52], 'little')) / 10_000
    current = float(int.from_bytes(pac1[52:56], 'little')) / 100_000
    power = float(int.from_bytes(pac1[56:60], 'little')) / 10_000

    # Compare V * A = W ;)
    power_calc = voltage * current
    diff = abs(power - power_calc)
    if diff > 0.0002:
        logger.warning(f'Power calculation diff: {power=}, {power_calc=} ({diff=})')

    # CRC16: pac1[60:64]

    pac2 = data[64:128]
    logging.debug(f'{pac2=}')
    pac2prefix = pac2[:4]
    if pac2prefix != b'pac2':
        logger.error(f'Invalid prefix {pac2prefix=}')
        return None

    resistor = float(int.from_bytes(pac2[4:8], 'little')) / 10

    group0Ah = float(int.from_bytes(pac2[8:12], 'little')) / 1_000
    group0Wh = float(int.from_bytes(pac2[12:16], 'little')) / 1_000

    group1Ah = float(int.from_bytes(pac2[16:20], 'little')) / 1_000
    group1Wh = float(int.from_bytes(pac2[20:24], 'little')) / 1_000

    temperature_sign = int.from_bytes(pac2[24:28], 'little')
    temperature = int.from_bytes(pac2[28:32], 'little')
    if temperature_sign:
        temperature = -temperature

    data_plus = float(int.from_bytes(pac2[32:36], 'little')) / 100
    data_minus = float(int.from_bytes(pac2[36:40], 'little')) / 100

    # pac2[40:60] contains unknown data -> ignore
    # CRC16: pac2[60:64]
    # pac3 = data[128:192] -> All data are unknown
    pac3: bytes = data[128:192]
    logging.debug(f'{pac3=}')
    pac3prefix = pac3[:4]
    if pac3prefix != b'pac3':
        logger.error(f'Invalid prefix {pac3prefix=}')
        return None

    return TC66PollData(
        product_name=product_name,
        version=version,
        serial=serial,
        number_of_runs=number_of_runs,
        #
        voltage=voltage,
        current=current,
        power=power,
        #
        resistor=resistor,
        #
        group0Ah=group0Ah,
        group0Wh=group0Wh,
        group1Ah=group1Ah,
        group1Wh=group1Wh,
        #
        temperature=temperature,
        #
        data_plus=data_plus,
        data_minus=data_minus,
    )
