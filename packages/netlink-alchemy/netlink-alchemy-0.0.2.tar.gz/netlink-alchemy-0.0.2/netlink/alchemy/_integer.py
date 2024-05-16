from sqlalchemy import SmallInteger, Integer, BigInteger
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, MEDIUMINT, INTEGER, BIGINT

TinyInteger = SmallInteger()
TinyInteger = TinyInteger.with_variant(Integer, "sqlite")
TinyInteger = TinyInteger.with_variant(TINYINT(), "mysql")
TinyInteger = TinyInteger.with_variant(TINYINT(), "mariadb")

UnsignedTinyInteger = SmallInteger()
UnsignedTinyInteger = UnsignedTinyInteger.with_variant(Integer, "sqlite")
UnsignedTinyInteger = UnsignedTinyInteger.with_variant(TINYINT(unsigned=True), "mysql")
UnsignedTinyInteger = UnsignedTinyInteger.with_variant(TINYINT(unsigned=True), "mariadb")

UnsignedSmallInteger = SmallInteger()
UnsignedSmallInteger = UnsignedSmallInteger.with_variant(Integer, "sqlite")
UnsignedSmallInteger = UnsignedSmallInteger.with_variant(SMALLINT(unsigned=True), "mysql")
UnsignedSmallInteger = UnsignedSmallInteger.with_variant(SMALLINT(unsigned=True), "mariadb")

MediumInteger = Integer()
MediumInteger = MediumInteger.with_variant(Integer, "sqlite")
MediumInteger = MediumInteger.with_variant(MEDIUMINT(), "mysql")
MediumInteger = MediumInteger.with_variant(MEDIUMINT(), "mariadb")

UnsignedMediumInteger = Integer()
UnsignedMediumInteger = UnsignedMediumInteger.with_variant(Integer, "sqlite")
UnsignedMediumInteger = UnsignedMediumInteger.with_variant(MEDIUMINT(unsigned=True), "mysql")
UnsignedMediumInteger = UnsignedMediumInteger.with_variant(MEDIUMINT(unsigned=True), "mariadb")

UnsignedInteger = Integer()
UnsignedInteger = UnsignedInteger.with_variant(INTEGER(unsigned=True), "mysql")
UnsignedInteger = UnsignedInteger.with_variant(INTEGER(unsigned=True), "mariadb")

UnsignedBigInteger = BigInteger()
UnsignedBigInteger = UnsignedBigInteger.with_variant(Integer, "sqlite")
UnsignedBigInteger = UnsignedBigInteger.with_variant(BIGINT(unsigned=True), "mysql")
UnsignedBigInteger = UnsignedBigInteger.with_variant(BIGINT(unsigned=True), "mariadb")
