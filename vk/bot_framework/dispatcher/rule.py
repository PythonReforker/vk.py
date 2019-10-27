import logging
from abc import ABC
from abc import abstractmethod

logger = logging.getLogger(__name__)


class AbstractRule(ABC):
    @abstractmethod
    async def check(self, *args):
        """
        This method will call when rules check.

        :param args:
        :return: True or False. If return 'True' - check next rules or execute handler
        """
        pass


class BaseRule(AbstractRule, ABC):
    meta = None  # information about rule [special for third-party addons]

    async def __call__(self, event, data: dict) -> bool:
        logger.debug(f"Rule {self.__class__.__name__} succesfully called!")
        return await self.check(event, data)


class NamedRule(BaseRule, ABC):
    """
    May be add to list rules with RuleFactory and
    will call in handlers by unique key;

    >>> @dp.message_handler(unique_key = value)

    """

    key = None  # unique value for access to rule in handlers.


class RuleFactory:
    """
    RuleFactory manage your rules.
    """

    def __init__(self, config: dict):
        self.config = config  # dict of all known rules

    def setup(self, rule: NamedRule):
        """
        Register rule in factory.
        :param rule:
        :return:
        """
        if not issubclass(rule, NamedRule):
            raise RuntimeError("Only NamedRules may be added in rule factory!")

        if rule.key is None or not isinstance(rule.key, str):
            raise RuntimeError("Unallowed key for rule")

        self.config.update({rule.key: rule})
        logger.debug(f"Rule {rule.__class__.__name__} succesfully added!")

    def get_rules(self, user_rules: dict):
        """
        Get rules objects by named_rules.
        :param user_rules:
        :return:
        """
        rules = []
        for key, value in user_rules.items():
            if key in self.config:
                rule: BaseRule = self.config[key](value)
                if rule.meta and rule.meta.get("deprecated", False):
                    logger.warning(
                        f"This rule ({rule.__class__.__name__}) deprecated. Not recommended to use."
                    )
                rules.append(rule)
                continue
            else:
                raise RuntimeError(f"Unknown rule passed: {key}")

        return rules
