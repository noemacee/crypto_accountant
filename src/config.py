PAGE_SIZE = 100


WALLET_ADDRESSES = [
    "0x035b6530ef09e227ca9f92efb66df12d0da9fface35ecd53b53a918c7d4eaa75",
]

important_addresses = {
    "sequencer": "0x01176a1bd84444c89232ec27754698e5d2e7e1a7f1539f12027f28b23ec9f3d8",
}


address_to_contract_alias = { # Used for 'from_alias' and 'to_alias' columns
    # Ekubo
    "0x00000005dd3d2f4429af886cd1a3b08289dbcea99a294197e9eb43b0e0325b4b": "Ekubo Core",
    "0x02e0af29598b407c8716b17f6d2795eca1b471413fa03fb145a5e33722184067": "Ekubo Positions",
    "0x07b696af58c967c1b14c9dde0ace001720635a660a8e90c565ea459345318b30": "Ekubo Positions NFT",
    # Nostra
    "0x073f6addc9339de9822cab4dac8c9431779c09077f02ba7bc36904ea342dd9eb": "Nostra CDP Manager / Deferred Batch Call Adapter",
    "0x059a943ca214c10234b9a3b61c558ac20c005127d183b86a99a8f3c60a08b4ff": "Nostra Interest Rate Model",
    "0x1bcfcb651e98317dc042cb34d0e0226c7f83bca309b6c54d8f0df6ee4e5f721": "Nostra Flash Loan Adapter",
    # AVNU
    "0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f": "AVNU Exchange",
    "0x0360fb3a51bd291e5db0892b6249918a5689bc61760adcb350fe39cd725e1d22": "AVNU Fee Collector",
    "0x0759c955b1cfddb8fcab93fddb0da1902d55bfe98bc4605ecb8cd4c635bc085b": "AVNU Elite Role NFT",
    # Starknet
    "0x01176a1bd84444c89232ec27754698e5d2e7e1a7f1539f12027f28b23ec9f3d8": "StarkWare: Sequencer",
}


address_to_protocol = { # Used for 'DeFi Deposit' and 'DeFi Withdrawal' descriptions.
    # Ekubo
    "0x00000005dd3d2f4429af886cd1a3b08289dbcea99a294197e9eb43b0e0325b4b": "Ekubo",
    "0x02e0af29598b407c8716b17f6d2795eca1b471413fa03fb145a5e33722184067": "Ekubo",
    "0x07b696af58c967c1b14c9dde0ace001720635a660a8e90c565ea459345318b30": "Ekubo",
    # Immutable EKUBO contracts
    "0x0199741822c2dc722f6f605204f35e56dbc23bceed54818168c4c49e4fb8737e": "Ekubo",  # Router V3.0.13
    "0x04505a9f06f2bd639b6601f37a4dc0908bb70e8e0e0c34b1220827d64f4fc066": "Ekubo",  # Router V3.0.3
    "0x03266fe47923e1500aec0fa973df8093b5850bbce8dcd0666d3f47298b4b806e": "Ekubo",  # Router V2.0.1
    "0x010c7eb57cbfeb18bde525912c1b6e9a7ebb4f692e0576af1ba7be8b3b9a70f6": "Ekubo",  # Router V2
    "0x01b6f560def289b32e2a7b0920909615531a4d9d5636ca509045843559dc23d5": "Ekubo",  #
    "0x064bdb4094881140bc39340146c5fcc5a187a98aec5a53f448ac702e5de5067e": "Ekubo",  #
    "0x0013e25867b6eef62703735aa4cfa7754e72f4e94a56c9d3d9ad8ebe86cee4aa": "Ekubo",  #
    "0x006f55e718ae592b22117c3e3b557b6b2b5f827ddcd7e6fdebd1a4ce7462c93e": "Ekubo",  #
    "0x00f2e9a400ba65b13255ef2792612b45d5a20a7a7cf211ffb3f485445022ef72": "Ekubo",  #
    "0x04946fb4ad5237d97bbb1256eba2080c4fe1de156da6a7f83e3b4823bb6d7da1": "Ekubo",  #
    # Nostra
    "0x073f6addc9339de9822cab4dac8c9431779c09077f02ba7bc36904ea342dd9eb": "Nostra",
    "0x059a943ca214c10234b9a3b61c558ac20c005127d183b86a99a8f3c60a08b4ff": "Nostra",
    "0x1bcfcb651e98317dc042cb34d0e0226c7f83bca309b6c54d8f0df6ee4e5f721": "Nostra",
    "0x04327da17a67e92dcd37619b927a7ee962c92a951dc42f78598c54bf77db467a": "Nostra",
    "0x0476e3589c53f1f0223cfe5129c80a03a9f7d32a69f7d9da2b6f70686bf685dc": "Nostra",
    # AVNU
    "0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f": "AVNU",
    "0x0360fb3a51bd291e5db0892b6249918a5689bc61760adcb350fe39cd725e1d22": "AVNU",
    "0x0759c955b1cfddb8fcab93fddb0da1902d55bfe98bc4605ecb8cd4c635bc085b": "AVNU",
    # Starknet
    "0x01176a1bd84444c89232ec27754698e5d2e7e1a7f1539f12027f28b23ec9f3d8": "Starknet",

    # Binance
    "0x0213c67ed78bc280887234fe5ed5e77272465317978ae86c25a71531d9332a2d": "Binance",
}


## These are a mix of various maps : to remove
addresses2exchanges_map = {
    # Ekubo
    "0x04505a9f06f2bd639b6601f37a4dc0908bb70e8e0e0c34b1220827d64f4fc066": "Ekubo",  # Unknown Address to understand
    # Nostra
    "0x040784ffdde08057a5957e64ed360c0ae4e04117b6d8e351c6bb912c09c5cbf5": "Nostra",  # Unknown Address to understand
    "0x01a2de9f2895ac4e6cb80c11ecc07ce8062a4ae883f64cb2b1dc6724b85e897d": "Nostra",  # Strk/Eth Degen
    # AVNU
    "0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f": "AVNU",  # AVNU Exchange address.
}


# Pool contracts data

address_to_pool = {# Used for "Nostra" in 'counterparty_name' column
    # Nostra : https://docs.nostra.finance/pools/deployed-contracts
    "0x068400056dccee818caa7e8a2c305f9a60d255145bac22d6c5c9bf9e2e046b71": "STRK/ETH",
    "0x07ae43abf704f4981094a4f3457d1abe6b176844f6cdfbb39c0544a635ef56b0": "STRK/USDC",
    "0x00c318445d5a5096e2ad086452d5c97f65a9d28cafe343345e0fa70da0841295": "USDC/USDT",
    "0x05ef8800d242c5d5e218605d6a10e81449529d4144185f95bf4b8fb669424516": "ETH/USDC",
    "0x052b136b37a7e6ea52ce1647fb5edc64efe23d449fc1561d9994a9f8feaa6753": "ETH/USDT",
    "0x05ae9c593b2bef20a8d69ae7abf1e6da551481f9efd83d03a9f05b6d7c9a78ec": "LORDS/ETH",
    "0x0285aa1c4bbeef8a183fb7245f096ddc4c99c6b2fedd1c1af52a634c83842804": "WBTC/ETH",
    "0x33c4141c8eb6ab8e7506c6f09c1a64b0995c9a5fa2ba6fa827845535b942786": "BRRR/ETH",
    "0x13e7962df51aba2afedbc1c86b0b61d36410f97fc75cb8f51e525559bef49f6": "STRONK/STRK",
    "0x0344653508c3b8831d6826712004f5bcff9d7a9a8fe720ba8e8b6005fb23c04d": "TONY/STRK",
    "0x05737b6463e8aab45d9237180ac68515a49fa3e0656f06b5831c15c69af83332": "AKU/STRK",
    "0x07d24fc0949e9579cb6e08bb65ffe39fd5dd78a47ad2e4eb52e49b97c2cd26db": "PAL/STRK",
    "0x076def79cc9a3a375779c163ad12996f99fbeb4acd68d7041529159bde897160": "nstSTRK/STRK",
    "0x03f8c9062f1bfe45f82cd70ed97ff053bc5836783ec66adfe3288eb1b43aa83b": "ETH/UNO",
    "0x03d51776d3ce07c211d5dbdf40a9333ec6d6d3a0b2853de1d6706f9ea3b88d45": "STRK/UNO",
    "0x01a2de9f2895ac4e6cb80c11ecc07ce8062a4ae883f64cb2b1dc6724b85e897d": "STRK/ETH (Degen)",
    "0x042543c7d220465bd3f8f42314b51f4f3a61d58de3770523b281da61dbf27c8a": "STRK/USDC (Degen)",
    "0x05e03162008d76cf645fe53c6c13a7a5fce745e8991c6ffe94400d60e44c210a": "ETH/USDC (Degen)",
    "0x01583919ffd78e87fa28fdf6b6a805fe3ddf52f754a63721dcd4c258211129a6": "WBTC/ETH (Degen)",
    "0x0577521a1f005bd663d0fa7f37f0dbac4d7f55b98791d280b158346d9551ff2b": "wstETH/ETH",
    "0x0362ec0c49a9c8f2d322d0ba6a8ec1214b9e4f7e80a17d462ec2585362547d95": "USDC/DAI",
    "0x05458b28f32b5f6e635895063ec0fe85c5a3864d257c4ae293edd5f66acf988d": "zUSDC/USDC",
    "0x07f232e7857effe04f7351e9bb2f1ebc2589bacca3380ae84efcc22067c1436e": "NSTR/USDC",
}


#


address_to_debt_token = {
    # Nostra : https://docs.nostra.finance/lend-and-borrow/deployed-contracts/money-market-mainnet
    "0x0491480f21299223b9ce770f23a2c383437f9fbf57abc2ac952e9af8cdb12c97": "WBTC",
    "0x00ba3037d968790ac486f70acaa9a1cab10cf5843bb85c986624b4d0e5a82e74": "ETH",
    "0x063d69ae657bd2f40337c39bf35a870ac27ddf91e6623c2f52529db4c1619a51": "USDC",
    "0x066037c083c33330a8460a65e4748ceec275bbf5f28aa71b686cbc0010e12597": "DAIv0",
    "0x024e9b0d6bc79e111e6872bb1ada2a874c25712cf08dfc5bcf0de008a7cca55f": "UDST",
    "0x0348cc417fc877a7868a66510e8e0d0f3f351f5e6b0886a86b652fcb30a3d1fb": "wstETH",
    "0x035778d24792bbebcf7651146896df5f787641af9e2a3db06480a637fbc9fff8": "LORDS",
    "0x001258eae3eae5002125bebf062d611a772e8aea3a1879b64a19f363ebd00947": "STRK",
    "0x0292be6baee291a148006db984f200dbdb34b12fb2136c70bfe88649c12d934b": "nstSTRK",
    "0x04b036839a8769c04144cc47415c64b083a2b26e4a7daa53c07f6042a0d35792": "UNO",
    "0x03e0576565c1b51fcac3b402eb002447f21e97abb5da7011c0a2e0b465136814": "NSTR",
    "0x06726ec97bae4e28efa8993a8e0853bd4bad0bd71de44c23a1cd651b026b00e7": "DAI",
    "0x073fa792a8ad45303db3651c34176dc419bee98bfe45791ab12f884201a90ae2": "EKUBO",
}


# ibc = interest bearing collaterals
address_to_ibc_token = {
    # Nostra : https://docs.nostra.finance/lend-and-borrow/deployed-contracts/money-market-mainnet
    "0x05b7d301fa769274f20e89222169c0fad4d846c366440afc160aafadd6f88f0c": "WBTC",
    "0x057146f6409deb4c9fa12866915dd952aa07c1eb2752e451d7f3b042086bdeb8": "ETH",
    "0x05dcd26c25d9d8fd9fc860038dcb6e4d835e524eb8a85213a8cda5b7fff845f6": "USDC",
    "0x04f18ffc850cdfa223a530d7246d3c6fc12a5969e0aa5d4a88f470f5fe6c46e9": "DAIv0",
    "0x0453c4c996f1047d9370f824d68145bd5e7ce12d00437140ad02181e1d11dc83": "UDST",
    "0x009377fdde350e01e0397820ea83ed3b4f05df30bfb8cf8055d62cafa1b2106a": "wstETH",
    "0x0739760bce37f89b6c1e6b1198bb8dc7166b8cf21509032894f912c9d5de9cbd": "LORDS",
    "0x07c2e1e733f28daa23e78be3a4f6c724c0ab06af65f6a95b5e0545215f1abc1b": "STRK",
    "0x067a34ff63ec38d0ccb2817c6d3f01e8b0c4792c77845feb43571092dcf5ebb5": "nstSTRK",
    "0x02a3a9d7bcecc6d3121e3b6180b73c7e8f4c5f81c35a90c8dd457a70a842b723": "UNO",
    "0x046ab56ec0c6a6d42384251c97e9331aa75eb693e05ed8823e2df4de5713e9a4": "NSTR",
    "0x02360bd006d42c1a17d23ebe7ae246a0764dea4ac86201884514f86754ccc7b8": "EKUBO",
}

# ic = interest collaterals
address_to_ic_token = {
    # Nostra : https://docs.nostra.finance/lend-and-borrow/deployed-contracts/money-market-mainnet
    "": "WBTC",
    "": "ETH",
    "": "USDC",
    "": "DAIv0",
    "": "UDST",
    "": "wstETH",
    "": "LORDS",
    "": "STRK",
    "": "nstSTRK",
    "": "UNO",
    "": "NSTR",
    "": "DAI",
    "": "EKUBO",
}



address_to_call_function = {
    "0x83afd3f4caedc6eebf44246fe54e38c95e3179a5ec9ea81740eca5b482d12e": "transfer",
    "0x015511cc3694f64379908437d6d64458dc76d02482052bfb8a5b33a72c054c77": "withdraw",
    "0x02f0b3c5710379609eb5495f1ecd348cb28167711b73609fe565a72734550354": "mint",
    "0x03276861cf5e05d6daf8f352cabb47df623eb10c383ab742fcc7abea94d5c5cc": "swap_exact_tokens_for_tokens",
    "0x01171593aa5bdadda4d6b0efde6cc94ee7649c3163d5efeb19da6c16d63a2a63": "multi_route_swap",
    "0xb758361d5e84380ef1e632f89d8e76a8677dbc3f4b93a4f9d75d2a6048f312": "claim",
    "0x3e8cfd4725c1e28fa4a6e3e468b4fcf75367166b850ac5f04e33ec843e82c1": "burn",
    "0x02cfb12ff9e08412ec5009c65ea06e727119ad948d25c8a8cc2c86fec4adee70": "add_liquidity",
    "0x02e875d1c86df033547c5c7839d8b6e3641de29ee1f708bbce99743b34272ada": "remove_liquidity",
    "0x02e1d93dafae32660a4a76a0fd6f31550f3ddfd6a51c29ef2e055b80afbbd011": "clear_minimum",
    "0x01b64b1b3b690b43b9b514fb81377518f4039cd3e4f4914d8a6bdf01d679fb19": "permissioned_mint (=handle_token_deposits)",
}


exchanges = {
    "Nostra",
    "Ekubo",
    "AVNU",
}
