from abc import ABC, abstractmethod

class IMerrymake(ABC):
    @abstractmethod
    def handle(self):
        """
         Used to link actions in the Merrymake.json file to code.

        Parameters
        ----------
        action : string
            The action from the Merrymake.json file
        handler : Action<byte[], JsonObject>
            The code to execute when the action is triggered
        
        Returns
        -------
        The Merrymake builder to define further actions
        """

        pass

    @abstractmethod
    def initialize(self):
        """
         Used to define code to run after deployment but before release. Useful for smoke tests or database consolidation. Similar to an 'init container'

        Parameters
        ----------
        handler : Action<byte[], JsonObject>
            The code to execute
        """
        
        pass
