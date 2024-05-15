from pathlib import Path
from typing import List

import pytest

from eip712 import (
    EIP712ContractDescriptor,
    EIP712DAppDescriptor,
    EIP712FieldMapper,
    EIP712MessageNameMapper,
)

TEST_FILE = Path(__file__).parent / "data" / "ether_mail.json"
TEST_IDENTIFIERS = [
    (
        EIP712MessageNameMapper,
        [
            "b7"  # identifier of a name mapper
            "0000000000000005"  # chain id
            "cccccccccccccccccccccccccccccccccccccccc"  # contract address
            "1e3673a051b6a5a6391c56ad7d859bc60cb18244ee8196d79a444d82"  # message schema hash
            "05"  # count of field mappers
            "536e656e64696e672061206d657373616765"  # name to display
        ],
    ),
    (
        EIP712FieldMapper,
        [
            "48"  # identifier of a field mapper
            "0000000000000005"  # chain id
            "cccccccccccccccccccccccccccccccccccccccc"  # contract address
            "1e3673a051b6a5a6391c56ad7d859bc60cb18244ee8196d79a444d82"  # message schema hash
            "66726f6d2e6e616d6553656e646572",  # field path and display name
            "48"  # identifier of a field mapper
            "0000000000000005"  # chain id
            "cccccccccccccccccccccccccccccccccccccccc"  # contract address
            "1e3673a051b6a5a6391c56ad7d859bc60cb18244ee8196d79a444d82"  # message schema hash
            "66726f6d2e77616c6c6574732e5b5d53656e6465722041646472657373",  # field path and display name
            "48"  # identifier of a field mapper
            "0000000000000005"  # chain id
            "cccccccccccccccccccccccccccccccccccccccc"  # contract address
            "1e3673a051b6a5a6391c56ad7d859bc60cb18244ee8196d79a444d82"  # message schema hash
            "746f2e6e616d65526563697069656e74",  # field path and display name
            "48"  # identifier of a field mapper
            "0000000000000005"  # chain id
            "cccccccccccccccccccccccccccccccccccccccc"  # contract address
            "1e3673a051b6a5a6391c56ad7d859bc60cb18244ee8196d79a444d82"  # message schema hash
            "746f2e77616c6c6574732e5b5d526563697069656e742041646472657373",  # field path and display name
            "48"  # identifier of a field mapper
            "0000000000000005"  # chain id
            "cccccccccccccccccccccccccccccccccccccccc"  # contract address
            "1e3673a051b6a5a6391c56ad7d859bc60cb18244ee8196d79a444d82"  # message schema hash
            "636f6e74656e74734d657373616765",  # field path and display name
        ],
    ),
]


@pytest.mark.parametrize(
    "expected_mapping_type, expected_mapping_identifiers", TEST_IDENTIFIERS
)
def test_identifiers(
    expected_mapping_type: str, expected_mapping_identifiers: List[str]
):
    eip712_descriptor = EIP712DAppDescriptor.parse_file(TEST_FILE)
    field_identifiers = [
        mapper.identifier
        for mapper in eip712_descriptor.mappers()
        if type(mapper) is expected_mapping_type
    ]
    assert field_identifiers == expected_mapping_identifiers


def test_add_message():
    target_contract = EIP712ContractDescriptor(
        address="0x9757f2d2b135150bbeb65308d4a91804107cd8d6",
        contractName="Rarible ExchangeV2",
        messages=[],
    )

    expected_eip712_dapp = EIP712DAppDescriptor.parse_obj(
        {
            "blockchainName": "ethereum",
            "chainId": 1,
            "contracts": [
                {
                    "address": "0x9757f2d2b135150bbeb65308d4a91804107cd8d6",
                    "contractName": "Rarible ExchangeV2",
                    "messages": [
                        {
                            "mapper": {
                                "fields": [
                                    {"label": "Order maker", "path": "maker"},
                                    {
                                        "label": "Order makeAsset assetType assetClass",
                                        "path": "makeAsset.assetType.assetClass",
                                    },
                                    {
                                        "label": "Order makeAsset assetType data",
                                        "path": "makeAsset.assetType.data",
                                    },
                                    {
                                        "label": "Order makeAsset value",
                                        "path": "makeAsset.value",
                                    },
                                    {"label": "Order taker", "path": "taker"},
                                    {
                                        "label": "Order takeAsset assetType assetClass",
                                        "path": "takeAsset.assetType.assetClass",
                                    },
                                    {
                                        "label": "Order takeAsset assetType data",
                                        "path": "takeAsset.assetType.data",
                                    },
                                    {
                                        "label": "Order takeAsset value",
                                        "path": "takeAsset.value",
                                    },
                                    {"label": "Order salt", "path": "salt"},
                                    {"label": "Order start", "path": "start"},
                                    {"label": "Order end", "path": "end"},
                                    {"label": "Order dataType", "path": "dataType"},
                                    {"label": "Order data", "path": "data"},
                                ],
                                "label": "Order",
                            },
                            "schema": {
                                "Asset": [
                                    {"name": "assetType", "type": "AssetType"},
                                    {"name": "value", "type": "uint256"},
                                ],
                                "AssetType": [
                                    {"name": "assetClass", "type": "bytes4"},
                                    {"name": "data", "type": "bytes"},
                                ],
                                "EIP712Domain": [
                                    {"name": "name", "type": "string"},
                                    {"name": "version", "type": "string"},
                                    {"name": "chainId", "type": "uint256"},
                                    {"name": "verifyingContract", "type": "address"},
                                ],
                                "Order": [
                                    {"name": "maker", "type": "address"},
                                    {"name": "makeAsset", "type": "Asset"},
                                    {"name": "taker", "type": "address"},
                                    {"name": "takeAsset", "type": "Asset"},
                                    {"name": "salt", "type": "uint256"},
                                    {"name": "start", "type": "uint256"},
                                    {"name": "end", "type": "uint256"},
                                    {"name": "dataType", "type": "bytes4"},
                                    {"name": "data", "type": "bytes"},
                                ],
                            },
                        },
                        {
                            "mapper": {
                                "fields": [
                                    {"label": "Mail contents", "path": "contents"},
                                    {"label": "Mail from name", "path": "from.name"},
                                    {
                                        "label": "Mail from wallets [] name",
                                        "path": "from.wallets.[].name",
                                    },
                                    {
                                        "label": "Mail from wallets [] addr",
                                        "path": "from.wallets.[].addr",
                                    },
                                    {"label": "Mail to name", "path": "to.name"},
                                    {
                                        "label": "Mail to wallets [] name",
                                        "path": "to.wallets.[].name",
                                    },
                                    {
                                        "label": "Mail to wallets [] addr",
                                        "path": "to.wallets.[].addr",
                                    },
                                ],
                                "label": "Mail",
                            },
                            "schema": {
                                "EIP712Domain": [
                                    {"name": "chainId", "type": "uint256"},
                                    {"name": "name", "type": "string"},
                                    {"name": "verifyingContract", "type": "address"},
                                    {"name": "version", "type": "string"},
                                ],
                                "Mail": [
                                    {"name": "contents", "type": "string"},
                                    {"name": "from", "type": "Person"},
                                    {"name": "to", "type": "Person"},
                                ],
                                "Person": [
                                    {"name": "name", "type": "string"},
                                    {"name": "wallets", "type": "Wallet[]"},
                                ],
                                "Wallet": [
                                    {"name": "name", "type": "string"},
                                    {"name": "addr", "type": "address"},
                                ],
                            },
                        },
                    ],
                }
            ],
            "name": "Rarible",
        }
    )
    schemas = [m.schema_ for c in expected_eip712_dapp.contracts for m in c.messages]
    eip712_dapp = EIP712DAppDescriptor(
        blockchainName="ethereum", chainId=1, name="Rarible", contracts=[]
    )
    assert expected_eip712_dapp != eip712_dapp
    for schema in schemas:
        eip712_dapp.add_message(target_contract=target_contract, schema=schema)
    assert expected_eip712_dapp == eip712_dapp
