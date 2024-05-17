"""main entry point for septentrio_gps."""

from rox_septentrio import __version__
import rox_septentrio.gps_node as gps_node


def main() -> None:
    """importable entrypoint"""
    print(f"Septentro gps version: {__version__}")
    gps_node.main()


if __name__ == "__main__":
    main()
