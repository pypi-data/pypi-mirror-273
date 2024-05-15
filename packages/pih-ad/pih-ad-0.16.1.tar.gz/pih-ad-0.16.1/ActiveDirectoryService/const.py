import ipih

from enum import Enum
from dataclasses import dataclass
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription


NAME: str = "ActiveDirectory"

HOST = Hosts.DC2

VERSION: str = "0.16.1"

PACKAGES: tuple[str, ...] = ("pyad", "pywin32", "wmi")

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Active directory service",
    host=HOST.NAME,
    packages=PACKAGES,
    commands=(
        "authenticate",
        "check_user_exists_by_login",
        "get_user_by_full_name",
        "get_users_by_name",
        "get_user_by_login",
        "get_user_by_telephone_number",
        "get_template_users",
        "get_containers",
        "get_users_by_job_position",
        "get_users_by_group",
        "get_printers",
        "get_computer_description_list",
        "get_computer_list",
        "get_workstation_list_by_user_login",
        "get_user_by_workstation",
        "create_user_by_template",
        "create_user_in_container",
        "set_user_telephone_number",
        "set_user_password",
        "set_user_status",
        "remove_user",
        "drop_user_cache",
        "drop_workstaion_cache",
        "get_user_list_by_property",
    ),
    version=VERSION,
    standalone_name="ad",
    use_standalone=True,
)




class UserExistanceStatus(Enum):
    EXISTS = 1
    INACTIVE = -1
    NOT_EXISTS = 0


@dataclass
class UserExistanceStatusItem:
    login: str | None = None
    status: UserExistanceStatus | None = None
