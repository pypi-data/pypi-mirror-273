from datetime import datetime
import re
from typing import Dict, Any, Union

from .parse import BaseParser, TLDBaseKeys
from .errors import NotFoundError


class DomainParser:
    _no_match_checks = [
        "no match",
        "not found",
        "no entries found",
        "invalid query",
        "domain name not known",
        "no object found",
        "available for re-registration",
        "object does not exist",
        "domain you requested is not known",
    ]

    def __init__(self, ignore_not_found: bool = False):
        self.ignore_not_found = ignore_not_found

    def parse(self, blob: str, tld: str) -> dict[TLDBaseKeys, Any]:
        if not self.ignore_not_found and any(
            [n in blob.lower() for n in self._no_match_checks]
        ):
            raise NotFoundError("Domain not found!")
        parser = self._init_parser(tld)
        return parser.parse(blob)

    @staticmethod
    def _init_parser(tld: str) -> "TLDParser":
        """
        Retrieves the parser instance which can most accurately extract
        key/value pairs from the whois server output for the given `tld`.

        :param tld: the top level domain
        :return: instance of TLDParser or a TLDParser subclass
        """
        if tld == "ae":
            return RegexAE()
        elif tld == "ar":
            return RegexAR()
        elif tld == "at":
            return RegexAT()
        elif tld == "au":
            return RegexAU()
        elif tld == "aw":
            return RegexAW()
        elif tld == "ax":
            return RegexAX()
        elif tld == "be":
            return RegexBE()
        elif tld == "br":
            return RegexBR()
        elif tld == "by":
            return RegexBY()
        elif tld == "cc":
            return RegexCC()
        elif tld == "ch":
            return RegexCH()
        elif tld == "cl":
            return RegexCL()
        elif tld == "cn":
            return RegexCN()
        elif tld == "cr":
            return RegexCR()
        elif tld == "cz":
            return RegexCZ()
        elif tld == "de":
            return RegexDE()
        elif tld == "dk":
            return RegexDK()
        elif tld == "edu":
            return RegexEDU()
        elif tld == "ee":
            return RegexEE()
        elif tld == "eu":
            return RegexEU()
        elif tld == "fi":
            return RegexFI()
        elif tld == "fr":
            return RegexFR()
        elif tld == "ga":
            return RegexGA()
        elif tld == "ge":
            return RegexGE()
        elif tld == "gg":
            return RegexGG()
        elif tld == "gq":
            return RegexGQ()
        elif tld == "hk":
            return RegexHK()
        elif tld == "hr":
            return RegexHR()
        elif tld == "id":
            return RegexID()
        elif tld == "ie":
            return RegexIE()
        elif tld == "il":
            return RegexIL()
        elif tld == "ir":
            return RegexIR()
        elif tld == "is":
            return RegexIS()
        elif tld == "it":
            return RegexIT()
        elif tld == "jp":
            return RegexJP()
        elif tld == "kg":
            return RegexKG()
        elif tld == "kr":
            return RegexKR()
        elif tld == "kz":
            return RegexKZ()
        elif tld == "li":
            return RegexLI()
        elif tld == "lu":
            return RegexLU()
        elif tld == "lv":
            return RegexLV()
        elif tld == "ma":
            return RegexMA()
        elif tld == "ml":
            return RegexML()
        elif tld == "mx":
            return RegexMX()
        elif tld == "nl":
            return RegexNL()
        elif tld == "no":
            return RegexNO()
        elif tld == "nu":
            return RegexNU()
        elif tld == "nz":
            return RegexNZ()
        elif tld == "om":
            return RegexOM()
        elif tld == "pe":
            return RegexPE()
        elif tld == "pl":
            return RegexPL()
        elif tld == "pt":
            return RegexPT()
        elif tld == "rf":
            return RegexRF()
        elif tld == "ro":
            return RegexRO()
        elif tld == "ru":
            return RegexRU()
        elif tld == "sa":
            return RegexSA()
        elif tld == "se":
            return RegexSE()
        elif tld == "si":
            return RegexSI()
        elif tld == "sk":
            return RegexSK()
        elif tld == "su":
            return RegexSU()
        elif tld == "tk":
            return RegexTK()
        elif tld == "tr":
            return RegexTR()
        elif tld == "tw":
            return RegexTW()
        elif tld == "ua":
            return RegexUA()
        elif tld == "uk":
            return RegexUK()
        elif tld == "uz":
            return RegexUZ()
        elif tld == "ve":
            return RegexVE()

        # The TLDParser can handle all "Generic" and some "Country-Code" TLDs.
        # If the parsed output of lookup is not what you expect or even incorrect,
        # check and modify the existing Regex subclass or create a new one.
        return TLDParser()


class TLDParser(BaseParser):
    base_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain Name: *(.+)",
        TLDBaseKeys.CREATED: r"Creation Date: *(.+)",
        TLDBaseKeys.UPDATED: r"Updated Date: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expir\w+\sDate: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar: *(.+)",
        TLDBaseKeys.REGISTRAR_IANA_ID: r"Registrar IANA ID: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"Registrar URL: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"Registrar Abuse Contact Email: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_PHONE: r"Registrar Abuse Contact Phone: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant Name: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"Registrant Organization: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Registrant Street: *(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"Registrant City: *(.+)",
        TLDBaseKeys.REGISTRANT_STATE: r"Registrant State/Province: *(.+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"Registrant Postal Code: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"Registrant Country: *(.+)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"Registrant Email: *(.+)",
        TLDBaseKeys.REGISTRANT_PHONE: r"Registrant Phone: *(.+)",
        TLDBaseKeys.REGISTRANT_FAX: r"Registrant Fax: *(.+)",
        TLDBaseKeys.DNSSEC: r"DNSSEC: *([\S]+)",
        TLDBaseKeys.STATUS: r"Status: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Name server: *(.+)",
        TLDBaseKeys.ADMIN_NAME: r"Admin Name: (.+)",
        TLDBaseKeys.ADMIN_ID: r"Admin ID: (.+)",
        TLDBaseKeys.ADMIN_ORGANIZATION: r"Admin Organization: (.+)",
        TLDBaseKeys.ADMIN_CITY: r"Admin City: (.*)",
        TLDBaseKeys.ADMIN_ADDRESS: r"Admin Street: (.*)",
        TLDBaseKeys.ADMIN_STATE: r"Admin State/Province: (.*)",
        TLDBaseKeys.ADMIN_ZIPCODE: r"Admin Postal Code: (.*)",
        TLDBaseKeys.ADMIN_COUNTRY: r"Admin Country: (.+)",
        TLDBaseKeys.ADMIN_PHONE: r"Admin Phone: (.+)",
        TLDBaseKeys.ADMIN_FAX: r"Admin Fax: (.+)",
        TLDBaseKeys.ADMIN_EMAIL: r"Admin Email: (.+)",
        TLDBaseKeys.BILLING_NAME: r"Billing Name: (.+)",
        TLDBaseKeys.BILLING_ID: r"Billing ID: (.+)",
        TLDBaseKeys.BILLING_ORGANIZATION: r"Billing Organization: (.+)",
        TLDBaseKeys.BILLING_CITY: r"Billing City: (.*)",
        TLDBaseKeys.BILLING_ADDRESS: r"Billing Street: (.*)",
        TLDBaseKeys.BILLING_STATE: r"Billing State/Province: (.*)",
        TLDBaseKeys.BILLING_ZIPCODE: r"Billing Postal Code: (.*)",
        TLDBaseKeys.BILLING_COUNTRY: r"Billing Country: (.+)",
        TLDBaseKeys.BILLING_PHONE: r"Billing Phone: (.+)",
        TLDBaseKeys.BILLING_FAX: r"Billing Fax: (.+)",
        TLDBaseKeys.BILLING_EMAIL: r"Billing Email: (.+)",
        TLDBaseKeys.TECH_NAME: r"Tech Name: (.+)",
        TLDBaseKeys.TECH_ID: r"Tech ID: (.+)",
        TLDBaseKeys.TECH_ORGANIZATION: r"Tech Organization: (.+)",
        TLDBaseKeys.TECH_CITY: r"Tech City: (.*)",
        TLDBaseKeys.TECH_ADDRESS: r"Tech Street: (.*)",
        TLDBaseKeys.TECH_STATE: r"Tech State/Province: (.*)",
        TLDBaseKeys.TECH_ZIPCODE: r"Tech Postal Code: (.*)",
        TLDBaseKeys.TECH_COUNTRY: r"Tech Country: (.+)",
        TLDBaseKeys.TECH_PHONE: r"Tech Phone: (.+)",
        TLDBaseKeys.TECH_FAX: r"Tech Fax: (.+)",
        TLDBaseKeys.TECH_EMAIL: r"Tech Email: (.+)",
    }

    multiple_match_keys = (TLDBaseKeys.NAME_SERVERS, TLDBaseKeys.STATUS)
    date_keys = (TLDBaseKeys.CREATED, TLDBaseKeys.UPDATED, TLDBaseKeys.EXPIRES)

    def __init__(self):
        self.reg_expressions = self.base_expressions.copy()


# ==============================
# Custom Query Output Parsers
# ==============================


class RegexRU(TLDParser):
    _ru_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.CREATED: r"created: *(.+)",
        TLDBaseKeys.EXPIRES: r"paid-till: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"org: *(.+)",
        TLDBaseKeys.STATUS: r"state: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
        TLDBaseKeys.ADMIN_EMAIL: r"admin-contact: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ru_expressions)


class RegexCL(TLDParser):
    _cl_expressions = {
        TLDBaseKeys.NAME_SERVERS: r"Name server: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant name: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"Registrant organisation: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar name: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expiration date: (\d{4}-\d{2}-\d{2})",
        TLDBaseKeys.CREATED: r"Creation date: (\d{4}-\d{2}-\d{2})",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._cl_expressions)


class RegexPL(TLDParser):
    _pl_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"DOMAIN NAME: *(.+)\n",
        TLDBaseKeys.REGISTRAR: r"REGISTRAR:\s*(.+)",
        TLDBaseKeys.CREATED: r"created: *(.+)",
        TLDBaseKeys.EXPIRES: r"option expiration date: *(.+)",
        TLDBaseKeys.UPDATED: r"last modified: *(.+)\n",
        TLDBaseKeys.DNSSEC: r"dnssec: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._pl_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        nameservers_match = self.find_match(
            r"nameservers:*(.+)\ncreated:\s", blob, flags=re.DOTALL | re.IGNORECASE
        )
        if nameservers_match:
            parsed_output[TLDBaseKeys.NAME_SERVERS] = [
                self._process(m) for m in nameservers_match.split("\n")
            ]
        return parsed_output


class RegexRO(TLDParser):
    # % The ROTLD WHOIS service on port 43 never discloses any information concerning the registrant.

    _ro_expressions = {
        TLDBaseKeys.CREATED: r"Registered On: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expires On: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Nameserver: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"Referral URL: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ro_expressions)


class RegexPE(TLDParser):
    _pe_expressions = {
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant name: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Sponsoring Registrar: *(.+)",
        TLDBaseKeys.ADMIN_EMAIL: r"Admin Email: *(.+)",
        TLDBaseKeys.DNSSEC: r"DNSSEC: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Name server: *(.+)",
        TLDBaseKeys.STATUS: r"Domain Status: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._pe_expressions)


class RegexEE(TLDParser):
    _ee_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *[\n\r]+\s*name: *([^\n\r]+)",
        TLDBaseKeys.STATUS: r"status: *([^\n\r]+)",
        TLDBaseKeys.CREATED: r"registered: *([^\n\r]+)",
        TLDBaseKeys.UPDATED: r"changed: *([^\n\r]+)",
        TLDBaseKeys.EXPIRES: r"expire: *([^\n\r]+)",
        TLDBaseKeys.REGISTRAR: r"(?<=Registrar)[\s\S]*?name: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"(?<=Registrar)[\s\S]*?url: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_PHONE: r"(?<=Registrar)[\s\S]*?phone: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"country: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ee_expressions)


class RegexFR(TLDParser):
    _fr_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.CREATED: r"created: (\d{4}-\d{2}-\d{2})",
        TLDBaseKeys.UPDATED: r"last-update: (\d{4}-\d{2}-\d{2})",
        TLDBaseKeys.EXPIRES: r"Expiry Date: (\d{4}-\d{2}-\d{2})",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._fr_expressions)


class RegexBR(TLDParser):
    _br_expressions = {
        TLDBaseKeys.CREATED: r"created: ",
        TLDBaseKeys.UPDATED: r"changed: ",
        TLDBaseKeys.STATUS: r"status: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"responsible: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"country: *(.+)",
        TLDBaseKeys.EXPIRES: r"expires: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._br_expressions)


class RegexKR(TLDParser):
    _kr_expressions = {
        TLDBaseKeys.CREATED: r"Registered Date *: (\d{4}\.\s\d{2}\.\s\d{2}\.)",
        TLDBaseKeys.UPDATED: r"Last Updated Date *: (\d{4}\.\s\d{2}\.\s\d{2}\.)",
        TLDBaseKeys.EXPIRES: r"Expiration Date *: (\d{4}\.\s\d{2}\.\s\d{2}\.)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant *: (.+)",
        TLDBaseKeys.ADMIN_EMAIL: r"Administrative Contact(AC) *: *(.+)",
        TLDBaseKeys.ADMIN_NAME: r"AC E-Mail *: *(.+)",
        TLDBaseKeys.DNSSEC: r"DNSSEC *: ([a-zA-Z]+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"Registrant Zip Code: *: (.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Registrant Address *: (.+)",
        TLDBaseKeys.DOMAIN_NAME: r"Domain Name *: (.+)",
        TLDBaseKeys.NAME_SERVERS: r"Host Name *: (.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._kr_expressions)


class RegexEU(TLDParser):
    # .EU whois server disclaimer:
    # % The EURid WHOIS service on port 43 (textual whois) never
    # % discloses any information concerning the registrant.

    _eu_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar:\n.*Name: (.+)",
        TLDBaseKeys.REGISTRAR_URL: r"Registrar:\n.*Name:.+\n.*Website: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._eu_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        # find name servers
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Name servers:", blob
        )
        return parsed_output


class RegexDE(TLDParser):
    # .de disclaimer (very hard to extract information from this provider):
    #
    # % The DENIC whois service on port 43 doesn't disclose any information concerning
    # % the domain holder, general request and abuse contact.
    # % This information can be obtained through use of our web-based whois service
    # % available at the DENIC website:
    # % http://www.denic.de/en/domains/whois-service/web-whois.html

    _de_expressions = {
        TLDBaseKeys.UPDATED: r"Changed: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Nserver: *(.+)",
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._de_expressions)


class RegexUK(TLDParser):
    _uk_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain name:\r\n*(.+)",
        TLDBaseKeys.CREATED: r"Registered on:\s*(\d{2}-\w{3}-\d{4})",
        TLDBaseKeys.UPDATED: r"Last updated:\s*(\d{2}-\w{3}-\d{4})",
        TLDBaseKeys.EXPIRES: r"Expiry date:\s*(\d{2}-\w{3}-\d{4})",
        TLDBaseKeys.REGISTRAR: r"Registrar:\s*(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"(?<=Registrar)[\s\S]*?URL: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant:\n *(.+)",
        TLDBaseKeys.STATUS: r"Registration status:\n *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._uk_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        # handle registrant address
        address_match = re.search(
            r"Registrant's address: *(.+)Data valid", blob, re.DOTALL
        )
        if address_match:
            address_pieces = [
                m.strip() for m in address_match.group(1).split("\n") if m.strip()
            ]
            parsed_output[TLDBaseKeys.REGISTRANT_ADDRESS] = ", ".join(address_pieces)
        # find name servers
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Name servers:", blob
        )
        return parsed_output


class RegexJP(TLDParser):
    _jp_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"\[Domain Name\] *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"\[Registrant\] *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"\[Organization\] *(.+)",
        TLDBaseKeys.CREATED: r"\[登録年月日\] *(.+)",
        TLDBaseKeys.EXPIRES: r"\[(?:有効限|有効期限)\]*(.+)",
        TLDBaseKeys.STATUS: r"\[状態\] *(.+)",
        TLDBaseKeys.UPDATED: r"\[最終更新\] *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"\[Name Server\] *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._jp_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        # check for domain in japanese
        if not parsed_output.get(TLDBaseKeys.DOMAIN_NAME):
            parsed_output[TLDBaseKeys.DOMAIN_NAME] = self.find_match(
                r"\[ドメイン名\] *(.+)", blob
            )
        # check for name servers in japanese
        if not parsed_output.get(TLDBaseKeys.NAME_SERVERS):
            parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_match(
                r"\[ネームサーバ\] *(.+)", blob, many=True
            )
        # check for address
        address_match = re.search(
            r"\[Postal Address\]([^\[|.]+)\[\w+\](.+)", blob, re.DOTALL
        )
        if address_match:
            address_pieces = [
                m.strip() for m in address_match.group(1).split("\n") if m.strip()
            ]
            parsed_output[TLDBaseKeys.REGISTRANT_ADDRESS] = ", ".join(address_pieces)
        return parsed_output


class RegexAU(TLDParser):
    _au_expressions = {
        TLDBaseKeys.UPDATED: r"Last Modified: (\d{2}-\w{3}-\d{4})",
        TLDBaseKeys.REGISTRAR: r"Registrar Name:\s *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._au_expressions)


class RegexAT(TLDParser):
    _at_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
        TLDBaseKeys.UPDATED: r"changed: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"registrant: *(.+)",
        TLDBaseKeys.TECH_NAME: r"tech-c: *(.+)",
    }

    _contact_fields = {
        "name": r"personname: *(.+)",
        "address": r"street address: *(.+)",
        "city": r"city: *(.+)",
        "country": r"country: *(.+)",
        "zipcode": r"postal code: *(.+)",
        "email": "e-mail: *(.+)",
        "phone": "phone: *(.+)",
        "fax": "fax-no: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._at_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parser_output = super().parse(blob)
        contact_field_fills = [
            ["registrant", r"registrant: *(.+)"],
            ["admin", r"admin-c"],
            ["tech", r"tech-c: *(.+)"],
        ]
        # find and save nic-hdls
        for field in contact_field_fills:
            field[1] = self.find_match(field[1], blob) or ""
        # parse contact info using each "nic-hdl"
        for prefix, handle in contact_field_fills:
            pattern = re.compile(
                r"(?:personname):.+\n(?:.+\n){{1,}}nic-hdl: *{nic_hdl}\n(?:.+\n){{1,}}".format(
                    nic_hdl=handle
                ),
                flags=re.I,
            )
            contact_blob = pattern.search(blob)
            if contact_blob:
                for field, field_regex in self._contact_fields.items():
                    key = getattr(TLDBaseKeys, f"{prefix}_{field}".upper())
                    parser_output[key] = self.find_match(
                        field_regex, contact_blob.group()
                    )

        return parser_output


class RegexBE(TLDParser):
    _be_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
        TLDBaseKeys.CREATED: r"Registered: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar:\n.+Name: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"Registrar:\n.+Name:.+\n.+Website:*(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant:\n *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._be_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Name servers:", blob
        )
        return parsed_output


class RegexRF(TLDParser):  # same as RU
    def __init__(self):
        super().__init__()

        self.update_reg_expressions(RegexRU._ru_expressions)


class RegexSU(TLDParser):  # same as RU
    def __init__(self):
        super().__init__()
        self.update_reg_expressions(RegexRU._ru_expressions)


class RegexKG(TLDParser):
    _kg_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain *(.+) ",
        TLDBaseKeys.REGISTRAR: r"Domain support: \s*(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Name: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Address: *(.+)",
        TLDBaseKeys.CREATED: r"Record created: *(.+)",
        TLDBaseKeys.EXPIRES: r"Record expires on \s*(.+)",
        TLDBaseKeys.UPDATED: r"Record last updated on\s*(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._kg_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Name servers in the listed order:", blob
        )
        return parsed_output


class RegexCH(TLDParser):
    _ch_expressions = {
        TLDBaseKeys.REGISTRANT_NAME: r"Holder of domain name:\s*(?:.*\n){1}\s*(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Holder of domain name:\s*(?:.*\n){2}\s*(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar:\n*(.+)",
        TLDBaseKeys.CREATED: r"First registration date:\n*(.+)",
        TLDBaseKeys.DNSSEC: r"DNSSEC:*([\S]+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ch_expressions)


class RegexLI(TLDParser):  # same as CH
    def __init__(self):
        super().__init__()
        self.update_reg_expressions(RegexCH._ch_expressions)


class RegexID(TLDParser):
    _id_expressions = {
        TLDBaseKeys.CREATED: r"Created On:(.+)",
        TLDBaseKeys.EXPIRES: r"Expiration Date:(.+)",
        TLDBaseKeys.UPDATED: r"Last Updated On:(.+)",
        TLDBaseKeys.DNSSEC: r"DNSSEC:(.+)",
        TLDBaseKeys.REGISTRAR: r"Sponsoring Registrar Organization:(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_PHONE: r"Sponsoring Registrar Phone: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"Sponsoring Registrar Email: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"Sponsoring Registrar URL: *(.+)",
        TLDBaseKeys.STATUS: r"Status:(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant Name:(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Registrant Street1:(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._id_expressions)


class RegexSE(TLDParser):
    _se_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"holder\.*: *(.+)",
        TLDBaseKeys.CREATED: r"created\.*: *(.+)",
        TLDBaseKeys.UPDATED: r"modified\.*: *(.+)",
        TLDBaseKeys.EXPIRES: r"expires\.*: *(.+)",
        TLDBaseKeys.DNSSEC: r"dnssec\.*: *(.+)",
        TLDBaseKeys.STATUS: r"status\.*: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._se_expressions)


class RegexIT(TLDParser):
    _it_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
        TLDBaseKeys.CREATED: r"(?<! )Created: *(.+)",
        TLDBaseKeys.UPDATED: r"(?<! )Last Update: *(.+)",
        TLDBaseKeys.EXPIRES: r"(?<! )Expire Date: *(.+)",
        TLDBaseKeys.STATUS: r"Status: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"(?<=Registrant)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=Registrant)[\s\S]*?Address:(.*)",
        TLDBaseKeys.REGISTRAR: r"(?<=Registrar)[\s\S]*?Name: *(.*)",
        TLDBaseKeys.REGISTRAR_URL: r"(?<=Registrar)[\s\S]*?Web: *(.*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._it_expressions)


class RegexSA(TLDParser):
    _sa_expressions = {
        TLDBaseKeys.CREATED: r"Created on: *(.+)",
        TLDBaseKeys.UPDATED: r"Last Updated on: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant:\s*(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=Registrant)[\s\S]*?Address:((?:.+\n)*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._sa_expressions)


class RegexSK(TLDParser):
    _sk_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
        TLDBaseKeys.CREATED: r"(?<=Domain:)[\s\w\W]*?Created: *(.+)",
        TLDBaseKeys.UPDATED: r"(?<=Domain:)[\s\w\W]*?Updated: *(.+)",
        TLDBaseKeys.EXPIRES: r"Valid Until: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Name:\s*(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Street:\s*(.+)",
        TLDBaseKeys.REGISTRAR: r"(?<=Registrar)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"(?<=Registrar)[\s\S]*?Email: *(.*)",
        TLDBaseKeys.REGISTRAR_ABUSE_PHONE: r"(?<=Registrar)[\s\S]*?Phone: *(.*)",
        TLDBaseKeys.REGISTRANT_CITY: r"(?<=^Contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"(?<=^Contact)[\s\S]*?Postal Code:(.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"(?<=^Contact)[\s\S]*?Country Code:(.*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._sk_expressions)


class RegexMX(TLDParser):
    _mx_expressions = {
        TLDBaseKeys.CREATED: r"Created On: *(.+)",
        TLDBaseKeys.UPDATED: r"Last Updated On: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expiration Date: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar:\s*(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"URL: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"(?<=Registrant)[\s\S]*?Name:(.*)",
        TLDBaseKeys.REGISTRANT_CITY: r"(?<=Registrant)[\s\S]*?City:(.*)",
        TLDBaseKeys.REGISTRANT_STATE: r"(?<=Registrant)[\s\S]*?State:(.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"(?<=Registrant)[\s\S]*?Country:(.*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._mx_expressions)


class RegexTW(TLDParser):
    _tw_expressions = {
        TLDBaseKeys.CREATED: r"Record created on (.+) ",
        TLDBaseKeys.EXPIRES: r"Record expires on (.+) ",
        TLDBaseKeys.REGISTRAR: r"Registration Service Provider: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"Registration Service URL: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"(?<=Registrant:)\s+(.*)",
        TLDBaseKeys.REGISTRANT_CITY: r"(?<=Registrant:)\s*(?:.*\n){5}\s+(.*),",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=Registrant:)\s*(?:.*\n){4}\s+(.*)",
        TLDBaseKeys.REGISTRANT_STATE: r"(?<=Registrant:)\s*(?:.*\n){5}.*, (.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"(?<=Registrant:)\s*(?:.*\n){6}\s+(.*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._tw_expressions)


class RegexTR(TLDParser):
    _tr_expressions = {
        TLDBaseKeys.CREATED: r"Created on.*: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expires on.*: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"(?<=[**] Registrant:)[\s\S]((?:\s.+)*)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=[**] Administrative Contact)[\s\S]*?Address\s+: (.*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._tr_expressions)


class RegexIS(TLDParser):
    _is_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.CREATED: r"created\.*: *(.+)",
        TLDBaseKeys.EXPIRES: r"expires\.*: *(.+)",
        TLDBaseKeys.DNSSEC: r"dnssec\.*: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver\.*: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._is_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        # find first instance of person/role (registrant)
        registrant_block = False
        registrant_name = None
        addresses = []
        for line in blob.split("\n"):
            if line.startswith("role") or line.startswith("person"):
                if registrant_block:
                    break
                else:
                    registrant_name = line.split(":")[-1].strip()
                    registrant_block = True
            elif line.startswith("address:"):
                address = line.split(":")[-1].strip()
                addresses.append(address)

        parsed_output[TLDBaseKeys.REGISTRANT_NAME] = registrant_name
        # join the address lines together and save
        parsed_output[TLDBaseKeys.REGISTRANT_ADDRESS] = ", ".join(addresses)
        return parsed_output


class RegexDK(TLDParser):
    _dk_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
        TLDBaseKeys.CREATED: r"Registered: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expires: *(.+)",
        TLDBaseKeys.DNSSEC: r"Dnssec: *(.+)",
        TLDBaseKeys.STATUS: r"Status: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant\s*(?:.*\n){2}\s*Name: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Registrant\s*(?:.*\n){3}\s*Address: *(.+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"Registrant\s*(?:.*\n){4}\s*Postalcode: *(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"Registrant\s*(?:.*\n){5}\s*City: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"Registrant\s*(?:.*\n){6}\s*Country: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._dk_expressions)


class RegexIL(TLDParser):
    _li_expressions = {
        TLDBaseKeys.EXPIRES: r"validity: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"person: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"address *(.+)",
        TLDBaseKeys.DNSSEC: r"DNSSEC: *(.+)",
        TLDBaseKeys.STATUS: r"status: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar name: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._li_expressions)


class RegexFI(TLDParser):
    _fi_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain\.*: *([\S]+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Holder\s*name\.*:\s(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"[Holder\w\W]address\.*: ([\S\ ]+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"[Holder\w\W]address\.*:.+\naddress\.*:\s(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"[Holder\w\W]address\.*:.+\naddress\.*:.+\naddress\.*:\s(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"country\.*:\s(.+)",
        TLDBaseKeys.STATUS: r"status\.*: *([\S]+)",
        TLDBaseKeys.CREATED: r"created\.*: *([\S]+)",
        TLDBaseKeys.UPDATED: r"modified\.*: *([\S]+)",
        TLDBaseKeys.EXPIRES: r"expires\.*: *([\S]+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver\.*: *([\S]+) \[\S+\]",
        TLDBaseKeys.DNSSEC: r"dnssec\.*: *([\S]+)",
        TLDBaseKeys.REGISTRAR: r"registrar\.*:\s(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._fi_expressions)


class RegexNU(TLDParser):
    _nu_expression = {
        TLDBaseKeys.DOMAIN_NAME: r"domain\.*: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"holder\.*: *(.+)",
        TLDBaseKeys.CREATED: r"created\.*: *(.+)",
        TLDBaseKeys.UPDATED: r"modified\.*: *(.+)",
        TLDBaseKeys.EXPIRES: r"expires\.*: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver\.*: *(.+)",
        TLDBaseKeys.DNSSEC: r"dnssec\.*: *(.+)",
        TLDBaseKeys.STATUS: r"status\.*: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._nu_expression)


class RegexPT(TLDParser):
    _pt_expression = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
        TLDBaseKeys.CREATED: r"Creation Date: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expiration Date: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Owner Name: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Owner Address: *(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"Owner Locality: *(.+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"Owner ZipCode: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Name Server: *(.+) \|",
        TLDBaseKeys.STATUS: r"Domain Status: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._pt_expression)


class RegexIE(TLDParser):
    _ie_expressions = {
        TLDBaseKeys.REGISTRANT_NAME: r"Domain Holder: *(.+)",
        TLDBaseKeys.CREATED: r"Registration Date: *(.+)",
        TLDBaseKeys.EXPIRES: r"Renewal Date: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Nserver: *(.+)",
        TLDBaseKeys.STATUS: r"Renewal status: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Account Name: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ie_expressions)


class RegexNZ(TLDParser):
    # These don't seem to be valid anymore:
    # _nz_expressions = {
    #     TLDBaseKeys.DOMAIN_NAME: r"",
    #     TLDBaseKeys.REGISTRAR: r"registrar_name:\s*([^\n\r]+)",
    #     TLDBaseKeys.UPDATED: r"domain_datelastmodified:\s*([^\n\r]+)",
    #     TLDBaseKeys.CREATED: r"domain_dateregistered:\s*([^\n\r]+)",
    #     TLDBaseKeys.EXPIRES: r"domain_datebilleduntil:\s*([^\n\r]+)",
    #     TLDBaseKeys.NAME_SERVERS: r"ns_name_\d*:\s*([^\n\r]+)",
    #     TLDBaseKeys.STATUS: r"status:\s*([^\n\r]+)",
    #     TLDBaseKeys.REGISTRANT_NAME: r"registrant_contact_name:\s*([^\n\r]+)",
    #     TLDBaseKeys.REGISTRANT_ADDRESS: r"registrant_contact_address\d*:\s*([^\n\r]+)",
    #     TLDBaseKeys.REGISTRANT_CITY: r"registrant_contact_city:\s*([^\n\r]+)",
    #     TLDBaseKeys.REGISTRANT_ZIPCODE: r"registrant_contact_postalcode:\s*([^\n\r]+)",
    #     TLDBaseKeys.REGISTRANT_COUNTRY: r"registrant_contact_country:\s*([^\n\r]+)",
    # }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions({})


class RegexLU(TLDParser):
    _lu_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domainname: *(.+)",
        TLDBaseKeys.CREATED: r"registered: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
        TLDBaseKeys.STATUS: r"domaintype: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar-name: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"registrar-email: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"registrar-url: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"org-name: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"org-address: *(.+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"org-zipcode:*(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"org-city: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"org-country: *(.+)",
    }

    def __init__(self):
        super().__init__()

        self.update_reg_expressions(self._lu_expressions)


class RegexCZ(TLDParser):
    _cz_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"name: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"org: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
        TLDBaseKeys.CREATED: r"registered: *(.+)",
        TLDBaseKeys.UPDATED: r"changed: *(.+)",
        TLDBaseKeys.EXPIRES: r"expire: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._cz_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        addresses = []
        seen_contact = False
        # extract address from registrant info block
        for line in blob.split("\n"):
            # check that this is first "contact" block
            if line.startswith("contact:"):
                if not seen_contact:
                    seen_contact = True
                else:
                    # if not; stop
                    break
            # append address
            elif line.startswith("address:"):
                line = line.split(":")[-1].strip()
                addresses.append(line)
        # just combine address lines; don't assume city/zipcode/country happen in any specific order
        address = ", ".join(addresses)
        parsed_output[TLDBaseKeys.REGISTRANT_ADDRESS] = address
        return parsed_output


class RegexHR(TLDParser):
    _hr_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain Name: *(.+)",
        TLDBaseKeys.UPDATED: r"Updated Date: *(.+)",
        TLDBaseKeys.CREATED: r"Creation Date: *(.+)",
        TLDBaseKeys.EXPIRES: r"Registrar Registration Expiration Date: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Name Server: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant Name:\s(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Registrant Street:\s*(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._hr_expressions)


class RegexHK(TLDParser):
    _hk_expressions = {
        TLDBaseKeys.STATUS: r"Domain Status: *(.+)",
        TLDBaseKeys.DNSSEC: r"DNSSEC: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar Name: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"Registrar Contact Information: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_PHONE: r"Registrar Contact Information: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant Contact Information:\s*Company English Name.*:(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=Registrant Contact Information:)[\s\S]*?Address: (.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"[Registrant Contact Information\w\W]+Country: ([\S\ ]+)",
        # 'registrant_email': r'[Registrant Contact Information\w\W]+Email: ([\S\ ]+)',
        TLDBaseKeys.UPDATED: r"Updated Date: *(.+)",
        TLDBaseKeys.CREATED: r"[Registrant Contact Information\w\W]+Domain Name Commencement Date: (.+)",
        TLDBaseKeys.EXPIRES: r"[Registrant Contact Information\w\W]+Expiry Date: (.+)",
        TLDBaseKeys.NAME_SERVERS: r"Name Servers Information:\s+((?:.+\n)*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._hk_expressions)


class RegexUA(TLDParser):
    _ua_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.STATUS: r"status: *(.+)",
        TLDBaseKeys.REGISTRAR: r"(?:Registrar: |(?<=Registrar:)[\s\W\w]*?organization-loc: )(.*)",
        TLDBaseKeys.REGISTRAR_URL: r"(?<=Registrar)[\s\S]*?url: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_PHONE: r"(?<=Registrar)[\s\S]*?abuse-phone: *(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"(?<=Registrar)[\s\S]*?abuse-email: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"(?<=Registrant:)[\s\W\w]*?organization-loc:(.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"(?<=Registrant:)[\s\W\w]*?country-loc:(.*)",
        TLDBaseKeys.REGISTRANT_CITY: r"(?<=Registrant:)[\s\W\w]*?(?:address\-loc:\s+.*\n){2}address-loc:\s+(.*)\n",
        TLDBaseKeys.REGISTRANT_STATE: r"(?<=Registrant:)[\s\W\w]*?(?:address\-loc:\s+.*\n){1}address-loc:\s+(.*)\n",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=Registrant:)[\s\W\w]*?address-loc:\s+(.*)\n",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"(?<=Registrant:)[\s\W\w]*?postal-code-loc:(.*)",
        TLDBaseKeys.UPDATED: "(?:Updated Date: |modified: )(.+)",
        TLDBaseKeys.CREATED: "(?:Creation Date: |created: )(.+)",
        TLDBaseKeys.EXPIRES: "(?:Registry Expiry Date: |expires: )(.+)",
        TLDBaseKeys.NAME_SERVERS: "nserver: *(.+)",
    }

    KNOWN_DATE_FORMATS = [
        "%Y-%m-%d %H:%M:%S%z",
    ]

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ua_expressions)

    @staticmethod
    def _fix_timezone(date_string: str) -> str:
        """
        Fix timezone format for datetime.strptime

        :param date_string: date string
        :return: fixed date string

        >>> RegexUA._fix_timezone("2023-02-17 14:22:06+02")
        '2023-02-17 14:22:06+0200'
        >>>
        >>> RegexUA._fix_timezone("2023-02-17 14:22:06+2")
        '2023-02-17 14:22:06+0200'
        >>>
        >>> RegexUA._fix_timezone("2023-02-17 14:22:06+0200")
        '2023-02-17 14:22:06+0200'
        >>>

        """
        if "+" in date_string:
            date_time, timezone = date_string.split("+")
            if timezone.isdigit() and len(timezone) <= 2:
                date_string = f"{date_time}+{int(timezone):02d}00"

        return date_string

    @staticmethod
    def _parse_date(date_string: str) -> Union[datetime, str]:
        date = TLDParser._parse_date(date_string)
        if isinstance(date, datetime):
            return date

        date_string = RegexUA._fix_timezone(date_string)
        for date_format in RegexUA.KNOWN_DATE_FORMATS:
            try:
                date = datetime.strptime(date_string, date_format)
                return date
            except ValueError:
                pass

        return date_string


class RegexCN(TLDParser):
    _cn_expressions = {
        TLDBaseKeys.REGISTRAR: r"Sponsoring Registrar: *(.+)",
        TLDBaseKeys.CREATED: r"Registration Time: *(.+)",
        TLDBaseKeys.EXPIRES: r"Expiration Time: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant: *(.+)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"Registrant Contact Email: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._cn_expressions)


class RegexAR(TLDParser):
    _ar_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
        TLDBaseKeys.UPDATED: r"changed: *(.+)",
        TLDBaseKeys.CREATED: r"created: *(.+)",
        TLDBaseKeys.EXPIRES: r"expire: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+) \(.*\)",
        TLDBaseKeys.REGISTRANT_NAME: r"name: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ar_expressions)


class RegexBY(TLDParser):
    _by_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain Name: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Person: *(.+)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"Email: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"Org: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"Country: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Address: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._by_expressions)


class RegexCR(TLDParser):
    _cr_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"name: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
        TLDBaseKeys.UPDATED: r"changed: *(.+)",
        TLDBaseKeys.CREATED: r"registered: *(.+)",
        TLDBaseKeys.EXPIRES: r"expire: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"org: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._cr_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        # CR server has the same format as CZ
        return RegexCZ().parse(blob)


class RegexVE(TLDParser):  # double check
    _ve_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
        TLDBaseKeys.CREATED: "registered: *(.+)",
        TLDBaseKeys.EXPIRES: "expire: *(.+)",
        TLDBaseKeys.UPDATED: "changed: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"registrant: *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"address: *(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"address:.+\naddress: *(.+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"(?:address:.+\n){2}address: *(.+)",
        TLDBaseKeys.REGISTRANT_STATE: r"(?:address:.+\n){3}address: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"(?:address:.+\n){4}address: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"org: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ve_expressions)


class RegexAE(TLDParser):
    _ae_expressions = {
        TLDBaseKeys.STATUS: r"Status: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant Contact Name: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"Registrant Contact Organisation: *(.+)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"Registrant Contact Email: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar Name: *(.+)",
        TLDBaseKeys.TECH_NAME: r"Tech Contact Name: *(.+)",
        TLDBaseKeys.TECH_EMAIL: r"Tech Contact Email: *(.+)",
        TLDBaseKeys.TECH_ORGANIZATION: r"Tech Contact Organisation: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ae_expressions)


class RegexSI(TLDParser):
    _si_expressions = {
        TLDBaseKeys.REGISTRAR: r"registrar: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"registrar-url: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nameserver: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"registrant: *(.+)",
        TLDBaseKeys.CREATED: r"created: *(.+)",
        TLDBaseKeys.EXPIRES: r"expire: *(.+)",
        TLDBaseKeys.DOMAIN_NAME: "domain: *(.+)",
        TLDBaseKeys.STATUS: "status: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._si_expressions)


class RegexNO(TLDParser):
    """
    % The whois service at port 43 is intended to contribute to resolving
    % technical problems where individual domains threaten the
    % functionality, security and stability of other domains or the
    % internet as an infrastructure. It does not give any information
    % about who the holder of a domain is. To find information about a
    % domain holder, please visit our website:
    % https://www.norid.no/en/domeneoppslag/
    """

    _no_expressions = {
        TLDBaseKeys.CREATED: r"Created:\s*(.+)",
        TLDBaseKeys.UPDATED: r"Last updated:\s*(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Name Server Handle\.*: *(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar Handle\.*: *(.+)",
        TLDBaseKeys.DOMAIN_NAME: r"Domain Name\.*: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._no_expressions)


class RegexKZ(TLDParser):
    _kz_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain Name.*: (.+)",
        TLDBaseKeys.REGISTRAR: r"Current Registar:\s*(.+)",  # "Registar" typo exists on the whois server
        TLDBaseKeys.CREATED: r"Domain created:\s*(.+)\s\(",
        TLDBaseKeys.UPDATED: r"Last modified\s:\s*(.+)\s\(",
        TLDBaseKeys.NAME_SERVERS: r".+\sserver\.*:\s*(.+)",
        TLDBaseKeys.STATUS: r"Domain status\s:\s(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"Organization Using Domain Name\nName\.*:\s(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"Street Address\.*:\s*(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"City\.*:\s*(.+)",
        TLDBaseKeys.REGISTRANT_ZIPCODE: r"Postal Code\.*:\s*(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"Country\.*:\s*(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Organization Name\.*:\s*(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._kz_expressions)


class RegexIR(TLDParser):
    _ir_expressions = {
        TLDBaseKeys.UPDATED: r"last-updated: *(.+)",
        TLDBaseKeys.EXPIRES: r"expire-date: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"org: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"remarks:\s+\(Domain Holder\) *(.+)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"remarks:\s+\(Domain Holder Address\) *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver: *(.+)",
        TLDBaseKeys.DOMAIN_NAME: r"domain: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ir_expressions)


class RegexTK(TLDParser):
    _tk_expressions = {
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"(?<=Owner contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.REGISTRANT_NAME: r"(?<=Owner contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=Owner contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.REGISTRANT_STATE: r"(?<=Owner contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.REGISTRANT_CITY: r"(?<=Owner contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"(?<=Owner contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"(?<=Owner contact)[\s\S]*?E-mail:(.*)",
        TLDBaseKeys.REGISTRANT_FAX: r"(?<=Owner contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.REGISTRANT_PHONE: r"(?<=Owner contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.ADMIN_ORGANIZATION: r"(?<=Admin contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.ADMIN_NAME: r"(?<=Admin contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.ADMIN_ADDRESS: r"(?<=Admin contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.ADMIN_STATE: r"(?<=Admin contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.ADMIN_CITY: r"(?<=Admin contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.ADMIN_COUNTRY: r"(?<=Admin contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.ADMIN_EMAIL: r"(?<=Admin contact)[\s\S]*?E-mail:(.*)",
        TLDBaseKeys.ADMIN_FAX: r"(?<=Admin contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.ADMIN_PHONE: r"(?<=Admin contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.BILLING_ORGANIZATION: r"(?<=Billing contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.BILLING_NAME: r"(?<=Billing contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.BILLING_ADDRESS: r"(?<=Billing contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.BILLING_STATE: r"(?<=Billing contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.BILLING_CITY: r"(?<=Billing contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.BILLING_COUNTRY: r"(?<=Billing contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.BILLING_EMAIL: r"(?<=Billing contact)[\s\S]*?E-mail:(.*)",
        TLDBaseKeys.BILLING_FAX: r"(?<=Billing contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.BILLING_PHONE: r"(?<=Billing contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.TECH_ORGANIZATION: r"(?<=Tech contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.TECH_NAME: r"(?<=Tech contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.TECH_ADDRESS: r"(?<=Tech contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.TECH_STATE: r"(?<=Tech contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.TECH_CITY: r"(?<=Tech contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.TECH_COUNTRY: r"(?<=Tech contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.TECH_EMAIL: r"(?<=Tech contact)[\s\S]*?E-mail:(.*)",
        TLDBaseKeys.TECH_FAX: r"(?<=Tech contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.TECH_PHONE: r"(?<=Tech contact)[\s\S]*?Phone:(.*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._tk_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        # handle multiline nameservers
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Domain nameservers:", blob
        )
        # a date parser exists for '%d/%m/%Y', but this interferes with the parser needed
        # for this one, which is '%m/%d/%Y', so this date format needs to be parsed separately here
        created_match = re.search(r"Domain registered: *(.+)", blob, re.IGNORECASE)
        if created_match:
            parsed_output[TLDBaseKeys.CREATED] = self._parse_date_mdY(
                created_match.group(1)
            )
        expires_match = re.search(r"Record will expire on: *(.+)", blob, re.IGNORECASE)
        if expires_match:
            parsed_output[TLDBaseKeys.EXPIRES] = self._parse_date_mdY(
                expires_match.group(1)
            )
        # Check if "Status" is inline with Domain Name. For example:
        # Domain Name:
        #   GOOGLE.TK is Active
        #   -- OR --
        #   GOOGLE.TK
        domain_name_match = re.search(r"Domain name:\n*(.+)\n\n", blob, re.IGNORECASE)
        if domain_name_match:
            if " is " in domain_name_match.group(1):
                domain_name, status = domain_name_match.group(1).split(" is ")
                parsed_output[TLDBaseKeys.DOMAIN_NAME] = self._process(
                    domain_name.replace("\n", "")
                )
                parsed_output[TLDBaseKeys.STATUS] = [
                    self._process(status.replace("\n", ""))
                ]
            else:
                parsed_output[TLDBaseKeys.DOMAIN_NAME] = self._process(
                    domain_name_match.group(1).replace("\n", "")
                )
        return parsed_output


class RegexCC(TLDParser):
    _cc_expressions = {TLDBaseKeys.STATUS: r"Domain Status: *(.+)"}

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._cc_expressions)


class RegexEDU(TLDParser):
    _edu_expressions = {
        TLDBaseKeys.CREATED: "Domain record activated: *(.+)",
        TLDBaseKeys.UPDATED: "Domain record last updated: *(.+)",
        TLDBaseKeys.EXPIRES: "Domain expires: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._edu_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        registrant_match = re.search(
            r"Registrant:*(.+)Administrative Contact", blob, re.DOTALL | re.IGNORECASE
        )
        if registrant_match:
            reg_info_raw = registrant_match.group(1).split("\n")
            # remove duplicates and empty strings
            reg_info_clean = []
            for value in reg_info_raw:
                value = value.strip()
                if value and value not in reg_info_clean:
                    reg_info_clean.append(value)
            # country is usually either last or third to last
            country_index = -3
            for i, value in enumerate(reg_info_clean):
                if len(value) == 2:
                    country_index = i
                    break

            org = reg_info_clean[0]
            address = ", ".join(reg_info_clean[1:country_index])
            country = reg_info_clean[country_index]

            parsed_output[TLDBaseKeys.REGISTRANT_NAME] = org
            parsed_output[TLDBaseKeys.REGISTRANT_ORGANIZATION] = org
            parsed_output[TLDBaseKeys.REGISTRANT_COUNTRY] = country
            parsed_output[TLDBaseKeys.REGISTRANT_ADDRESS] = address

        # handle multiline nameservers
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Name Servers:", blob
        )
        return parsed_output


class RegexLV(TLDParser):
    _lv_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain: *(.+)",
        TLDBaseKeys.REGISTRAR: r"\[Registrar\]\n(?:.*)\nName:(.*)+",
        TLDBaseKeys.REGISTRANT_NAME: r"\[Holder\]\n(?:.*)\nName:(.*)+",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"\[Holder\]\n(?:.*)\Address:(.*)+",
        TLDBaseKeys.NAME_SERVERS: r"Nserver: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._lv_expressions)


class RegexGQ(TLDParser):
    _gq_expressions = {}

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._gq_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        # GQ server has the same format as TK
        return RegexTK().parse(blob)


class RegexNL(TLDParser):
    _nl_expressions = {
        TLDBaseKeys.REGISTRAR: r"Registrar:\n(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"Abuse Contact:\n(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._nl_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        # handle multiline nameservers
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Domain nameservers:", blob
        )
        return parsed_output


class RegexMA(TLDParser):
    _ma_expressions = {
        TLDBaseKeys.REGISTRAR: r"Sponsoring Registrar: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ma_expressions)


class RegexGE(TLDParser):
    _ge_expressions = {
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ge_expressions)


class RegexGG(TLDParser):
    _gg_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain:\n*(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant:\n*(.+)",
        TLDBaseKeys.REGISTRAR: r"Registrar:\n*(.+)",
        TLDBaseKeys.CREATED: r"Registered on *(.+) at",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._gg_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        # parse created date
        created_match = parsed_output.get(
            "created"
        )  # looks like 30th April 2003; need to remove day suffix
        if created_match and isinstance(created_match, str):
            date_string = re.sub(r"(\d)(st|nd|rd|th)", r"\1", created_match)
            parsed_output[TLDBaseKeys.CREATED] = datetime.strptime(
                date_string, "%d %B %Y"
            )
        # handle multiline nameservers and statuses
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Name servers:", blob
        )
        parsed_output[TLDBaseKeys.STATUS] = self.find_multiline_match(
            "Domain status:", blob
        )
        return parsed_output


class RegexAW(TLDParser):
    _aw_expressions = {
        TLDBaseKeys.REGISTRAR: r"Registrar:\n*(.+)",
        TLDBaseKeys.REGISTRAR_ABUSE_EMAIL: r"Abuse Contact:\n*(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._aw_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Domain nameservers:", blob
        )
        return parsed_output


class RegexAX(TLDParser):
    _ax_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"domain\.+: *(.+)",
        TLDBaseKeys.REGISTRAR: r"registrar\.+: *(.+)",
        TLDBaseKeys.REGISTRAR_URL: r"www\.+: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"name\.+: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"country\.+: *(.+)",
        TLDBaseKeys.CREATED: r"created\.+: *(.+)",
        TLDBaseKeys.EXPIRES: r"expires\.+: *(.+)",
        TLDBaseKeys.UPDATED: r"modified\.+: *(.+)",
        TLDBaseKeys.STATUS: r"status\.+: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"nserver\.+: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ax_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        addresses = self.find_match(r"address\.+: *(.+)", blob, many=True)
        if addresses:
            parsed_output[TLDBaseKeys.REGISTRANT_ADDRESS] = ", ".join(addresses)
        return parsed_output


class RegexML(TLDParser):
    _ml_expressions = {
        TLDBaseKeys.EXPIRES: r"Record will expire on: *(.+)",
        TLDBaseKeys.CREATED: r"Domain registered: *(.+)",
        TLDBaseKeys.DOMAIN_NAME: r"Domain name:\n*(.+)\sis\s",
        TLDBaseKeys.STATUS: r"Domain name:\n.+\sis\s*(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ml_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        parsed_output = super().parse(blob)
        parsed_output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Domain nameservers:", blob
        )
        for contact in ("Admin", "Billing", "Owner", "Tech"):
            # isolate the appropriate contact block
            contact_blob = re.search(f"{contact} contact:\n(.+)\n\n", blob, re.DOTALL)
            if contact_blob:
                if contact == "Owner":
                    # map "owner" to registrant
                    contact = "Registrant"
                for key in (
                    "Organization",
                    "Name",
                    "Address",
                    "Zipcode",
                    "City",
                    "State",
                    "Country",
                    "Phone",
                    "Fax",
                    "E-mail",
                ):
                    # special case: Email -> E-mail
                    if key == "E-mail":
                        base_key = getattr(TLDBaseKeys, f"{contact}_Email".upper())
                    else:
                        base_key = getattr(TLDBaseKeys, f"{contact}_{key}".upper())
                    if not base_key:
                        continue
                    # updated parser dict
                    parsed_output[base_key] = self.find_match(
                        f"{key}: *(.+)", contact_blob.group(0)
                    )
        date_format = "%m/%d/%Y"  # example: 05/28/2013
        if parsed_output.get(TLDBaseKeys.EXPIRES):
            parsed_output[TLDBaseKeys.EXPIRES] = datetime.strptime(
                parsed_output.get(TLDBaseKeys.EXPIRES), date_format
            )
        if parsed_output.get(TLDBaseKeys.CREATED):
            parsed_output[TLDBaseKeys.CREATED] = datetime.strptime(
                parsed_output.get(TLDBaseKeys.CREATED), date_format
            )
        return parsed_output


class RegexOM(TLDParser):
    _om_expressions = {
        TLDBaseKeys.REGISTRAR: r"Registrar Name: *(.+)",
        TLDBaseKeys.UPDATED: r"Last Modified: *(.+)",
        TLDBaseKeys.REGISTRANT_CITY: r"Registrant Contact City: *(.+)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"Registrant Contact Country: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"Registrant Contact Organisation: *(.+)",
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant Contact Name: *(.+)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"Registrant Contact Email: *(.+)",
        TLDBaseKeys.TECH_CITY: r"Tech Contact City: *(.+)",
        TLDBaseKeys.TECH_COUNTRY: r"Tech Contact Country: *(.+)",
        TLDBaseKeys.TECH_ORGANIZATION: r"Tech Contact Organisation: *(.+)",
        TLDBaseKeys.TECH_NAME: r"Tech Contact Name: *(.+)",
        TLDBaseKeys.TECH_EMAIL: r"Tech Contact Email: *(.+)",
        TLDBaseKeys.NAME_SERVERS: r"Name Server: *(.+)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._om_expressions)


class RegexUZ(TLDParser):
    _uz_expressions = {
        TLDBaseKeys.REGISTRANT_NAME: r"Registrant:\s+([A-Za-z0-9\.\s]+\n)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"Contact with Registrant: *(.+)",
        TLDBaseKeys.ADMIN_NAME: r"Administrative Contact:\s+([A-Za-z0-9\.\s]+\n)",
        TLDBaseKeys.BILLING_NAME: r"Billing Contact:\s+([A-Za-z0-9\.\s]+\n)",
        TLDBaseKeys.TECH_NAME: r"Technical Contact:\s+([A-Za-z0-9\.\s]+\n)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._uz_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        output = super().parse(blob)
        output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Domain servers in listed order:", blob
        )
        return output


class RegexGA(TLDParser):
    _ga_expressions = {
        TLDBaseKeys.DOMAIN_NAME: r"Domain name:\n*(.+) is",
        TLDBaseKeys.STATUS: r"Domain name:\n*.+ is (.+)",
        TLDBaseKeys.CREATED: r"Domain registered: *(.+)",
        TLDBaseKeys.EXPIRES: r"Record will expire on: *(.+)",
        TLDBaseKeys.REGISTRANT_ORGANIZATION: r"(?<=Owner contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.REGISTRANT_NAME: r"(?<=Owner contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.REGISTRANT_ADDRESS: r"(?<=Owner contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.REGISTRANT_STATE: r"(?<=Owner contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.REGISTRANT_CITY: r"(?<=Owner contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.REGISTRANT_COUNTRY: r"(?<=Owner contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.REGISTRANT_EMAIL: r"(?<=Owner contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.REGISTRANT_FAX: r"(?<=Owner contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.REGISTRANT_PHONE: r"(?<=Owner contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.ADMIN_ORGANIZATION: r"(?<=Admin contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.ADMIN_NAME: r"(?<=Admin contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.ADMIN_ADDRESS: r"(?<=Admin contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.ADMIN_STATE: r"(?<=Admin contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.ADMIN_CITY: r"(?<=Admin contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.ADMIN_COUNTRY: r"(?<=Admin contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.ADMIN_EMAIL: r"(?<=Admin contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.ADMIN_FAX: r"(?<=Admin contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.ADMIN_PHONE: r"(?<=Admin contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.BILLING_ORGANIZATION: r"(?<=Billing contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.BILLING_NAME: r"(?<=Billing contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.BILLING_ADDRESS: r"(?<=Billing contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.BILLING_STATE: r"(?<=Billing contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.BILLING_CITY: r"(?<=Billing contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.BILLING_COUNTRY: r"(?<=Billing contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.BILLING_EMAIL: r"(?<=Billing contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.BILLING_FAX: r"(?<=Billing contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.BILLING_PHONE: r"(?<=Billing contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.TECH_ORGANIZATION: r"(?<=Tech contact)[\s\S]*?Organization:(.*)",
        TLDBaseKeys.TECH_NAME: r"(?<=Tech contact)[\s\S]*?Name:(.*)",
        TLDBaseKeys.TECH_ADDRESS: r"(?<=Tech contact)[\s\S]*?Address:(.*)",
        TLDBaseKeys.TECH_STATE: r"(?<=Tech contact)[\s\S]*?State:(.*)",
        TLDBaseKeys.TECH_CITY: r"(?<=Tech contact)[\s\S]*?City:(.*)",
        TLDBaseKeys.TECH_COUNTRY: r"(?<=Tech contact)[\s\S]*?Country:(.*)",
        TLDBaseKeys.TECH_EMAIL: r"(?<=Tech contact)[\s\S]*?Phone:(.*)",
        TLDBaseKeys.TECH_FAX: r"(?<=Tech contact)[\s\S]*?Fax:(.*)",
        TLDBaseKeys.TECH_PHONE: r"(?<=Tech contact)[\s\S]*?Phone:(.*)",
    }

    def __init__(self):
        super().__init__()
        self.update_reg_expressions(self._ga_expressions)

    def parse(self, blob: str) -> Dict[str, Any]:
        output = super().parse(blob)
        output[TLDBaseKeys.NAME_SERVERS] = self.find_multiline_match(
            "Domain Nameservers:", blob
        )
        # date format is m/d/Y
        created = output.get(TLDBaseKeys.CREATED)
        if created:
            output[TLDBaseKeys.CREATED] = self._parse_date_mdY(created)

        expires = output.get(TLDBaseKeys.EXPIRES)
        if expires:
            output[TLDBaseKeys.EXPIRES] = self._parse_date_mdY(expires)

        return output
