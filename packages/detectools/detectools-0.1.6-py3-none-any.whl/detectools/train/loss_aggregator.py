from typing import Dict

from torch import Tensor


class Aggregator:
    """Aggregator aggregate losses across batchs.
    
    Attributes:
    -----------
    
    Attributes:
        iterations (``int``): Number of iterations.
        losses (``Dict[str, Tensor]``): Dictionnary of epoch losses (over iterations).
    
    Methods:
    ----------
        """

    iterations: int
    losses: dict

    def __init__(self):
        self.iterations = 0
        self.losses: dict = None

    def update(self, batch_losses: Dict[str, Tensor]):
        """Update internal loss dict with new losses.

        Args:
            batch_losses (``Dict[str, Tensor]``): Dict of losses.
        """

        for key, value in self.losses.items():
            self.losses[key] = value + batch_losses[key]

    def __call__(self, batch_losses: Dict[str, Tensor], batch_size: int):
        """Update internal loss dict.

        Args:
            batch_losses (``Dict[str, Tensor]``): Dict of losses.
            batch_size (``int``): Batch size.
        """

        if self.losses:
            self.update(batch_losses)
        else:
            self.losses = batch_losses

        self.iterations += 1 * batch_size

    def compute(self) -> Dict[str, Tensor]:
        """Return loss dict with values divided by iterations (Mean accross samples).

        Returns:
            ``Dict[str, Tensor]``:
                - Losses over iterations.
        """

        out_dict = {
            key: (value / self.iterations) for key, value in self.losses.items()
        }
        return out_dict
