from pyasic.miners.makes import ePICMake


class BlockMiner520i(ePICMake):
    raw_model = "BlockMiner 520i"
    expected_chips = 124
    expected_fans = 4


class BlockMiner720i(ePICMake):
    raw_model = "BlockMiner 720i"
    expected_chips = 180
    expected_fans = 4
