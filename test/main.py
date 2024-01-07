
import logging
from pathlib import Path

import sys
sys.path.append(Path(__file__).parent.parent.as_posix()+"/src") # Add src directory to python path so we can access src modules

print(sys.path)

from depdencyInjection.Container import Container
from utils.dependencyInjectionUtils import override


logging.basicConfig()


def main() -> None:
    container = Container()
    override(container)

    container.ui().start()


if __name__ == "__main__":
    main()
