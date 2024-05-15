import hashlib
import json
from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar, Iterator, List

from pydantic import BaseModel, Field

# For more details on the serialisation spec, head over to
# https://github.com/LedgerHQ/app-ethereum/blob/apr/feature/eip712/doc/ethapp.adoc#eip712-filtering


@dataclass
class EIP712BaseMapper:
    chain_id: int
    contract_address: str
    schema: dict
    display_name: str
    TYPE_PREFIX: ClassVar[int]

    @cached_property
    def type_prefix_hash(self) -> str:
        return self.TYPE_PREFIX.to_bytes(1, byteorder="big").hex()

    @cached_property
    def chain_id_hash(self) -> str:
        return self.chain_id.to_bytes(8, byteorder="big").hex()

    @cached_property
    def contract_address_hash(self) -> str:
        return self.contract_address[2:].lower()

    @cached_property
    def schema_hash(self) -> str:
        # Remove all spaces and new lines from the json schema
        schema_str = json.dumps(self.schema, separators=(",", ":"), indent=None)
        return hashlib.sha224(schema_str.encode("utf-8")).hexdigest()

    @cached_property
    def display_name_hash(self) -> str:
        return self.display_name.encode("utf-8").hex()

    @cached_property
    def additional_hash(self) -> str:
        return ""

    @cached_property
    def identifier(self) -> str:
        return (
            f"{self.type_prefix_hash}"
            f"{self.chain_id_hash}"
            f"{self.contract_address_hash}"
            f"{self.schema_hash}"
            f"{self.additional_hash}"
            f"{self.display_name_hash}"
        )


@dataclass
class EIP712FieldMapper(EIP712BaseMapper):
    field_path: str
    TYPE_PREFIX: ClassVar[int] = 72

    @property
    def additional_hash(self) -> str:
        return self.field_path.encode("utf-8").hex()


@dataclass
class EIP712MessageNameMapper(EIP712BaseMapper):
    field_mappers_count: int
    TYPE_PREFIX: ClassVar[int] = 183

    @property
    def additional_hash(self) -> str:
        return self.field_mappers_count.to_bytes(1, byteorder="big").hex()


class EIP712Field(BaseModel):
    path: str
    label: str

    def mapper(self, **mapper_data) -> EIP712FieldMapper:
        return EIP712FieldMapper(
            field_path=self.path, display_name=self.label, **mapper_data
        )


class EIP712Mapper(BaseModel):
    label: str
    fields: List[EIP712Field]

    def mappers(self, **mapper_data) -> Iterator[EIP712BaseMapper]:
        yield EIP712MessageNameMapper(
            field_mappers_count=len(self.fields),
            display_name=self.label,
            **mapper_data,
        )
        for field in self.fields:
            yield field.mapper(**mapper_data)


class EIP712MessageDescriptor(BaseModel):
    schema_: dict = Field(alias="schema")
    mapper: EIP712Mapper

    def mappers(self, **mapper_data) -> Iterator[EIP712BaseMapper]:
        return self.mapper.mappers(schema=self.schema_, **mapper_data)

    @classmethod
    def from_schema(cls, schema: dict):
        """Given a schema, generate a new message descriptor"""
        filtered_schema: dict = {
            type_name: type_fields
            for type_name, type_fields in schema.items()
            if type_name != "EIP712Domain"
        }
        all_type_names = {
            type_field["type"]
            for type_fields in filtered_schema.values()
            for type_field in type_fields
        }
        top_level_type_name = next(
            type_name
            for type_name in filtered_schema.keys()
            if type_name not in all_type_names
        )

        def _get_name_list(schema: dict, target_type_name: str) -> List[str]:
            """Recursively generate the list of fields to reach an object with a basic type"""
            for type_fields in schema[target_type_name]:
                name_list = [type_fields["name"]]
                short_type = type_fields["type"].removesuffix("[]")
                if short_type != type_fields["type"]:
                    name_list.append("[]")
                if short_type in schema:
                    for recursive_name_list in _get_name_list(
                        schema=schema, target_type_name=short_type
                    ):
                        yield name_list + recursive_name_list
                else:
                    yield name_list

        mapper_fields = []
        for name_list in _get_name_list(
            schema=schema, target_type_name=top_level_type_name
        ):
            field_label = f"{top_level_type_name} {' '.join(name_list)}"
            field_path = f"{'.'.join(name_list)}"
            mapper_fields.append(EIP712Field(path=field_path, label=field_label))

        mapper = EIP712Mapper(label=top_level_type_name, fields=mapper_fields)
        return cls(schema=schema, mapper=mapper)


class EIP712ContractDescriptor(BaseModel):
    address: str
    name: str = Field(alias="contractName")
    messages: List[EIP712MessageDescriptor]

    def mappers(self, **mapper_data) -> Iterator[EIP712BaseMapper]:
        for message in self.messages:
            for mapper in message.mappers(contract_address=self.address, **mapper_data):
                yield mapper

    def add_message(self, schema: dict):
        message = EIP712MessageDescriptor.from_schema(schema=schema)
        self.messages.append(message)


class EIP712DAppDescriptor(BaseModel):
    blockchain_name: str = Field(alias="blockchainName")
    chain_id: int = Field(alias="chainId")
    name: str
    contracts: List[EIP712ContractDescriptor]

    def mappers(self) -> Iterator[EIP712BaseMapper]:
        for contract in self.contracts:
            for mapper in contract.mappers(chain_id=self.chain_id):
                yield mapper

    def add_message(self, target_contract: EIP712ContractDescriptor, schema: dict):
        contract = next(
            (c for c in self.contracts if c.address == target_contract.address), None
        )
        if not contract:
            contract = target_contract
            self.contracts.append(contract)
        contract.add_message(schema=schema)
